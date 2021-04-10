import json
import asyncio
import datetime
import eml_parser
import exchangelib

from glom import glom
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from exchangelib import (
    DELEGATE,
    Account,
    Credentials,
    Configuration,
    Version,
    Build,
    Mailbox,
    Message,
    FileAttachment,
)
from exchangelib.protocol import BaseProtocol, NoVerifyHTTPAdapter
from walkoff_app_sdk.app_base import AppBase


def default(o):
    """helpers to store item in json
    arguments:
    - o: field of the object to serialize
    returns:
    - valid serialized value for unserializable fields
    """
    if isinstance(o, (datetime.date, datetime.datetime)):
        return o.isoformat()
    if isinstance(o, set):
        return list(o)
    if isinstance(o, bytes):
        return o.decode("utf-8")


class Owa(AppBase):
    __version__ = "1.0.0"
    app_name = "owa"

    def __init__(self, redis, logger, console_logger=None):
        """
        Each app should have this __init__ to set up Redis and logging.
        :param redis:
        :param logger:
        :param console_logger:
        """
        super().__init__(redis, logger, console_logger)

    async def authenticate(self, username, password, server, build, account, verifyssl):
        """
        Authenticates to Exchange server
        """
        if not verifyssl or verifyssl.lower().strip() == "false":
            BaseProtocol.HTTP_ADAPTER_CLS = NoVerifyHTTPAdapter

        processed_build = None
        if type(build) == str:
            try:
                processed_build = [int(x) for x in build.split(".")]
                if len(build) == 0:
                    build = None
                elif len(build) < 2 or len(build) > 4:
                    return {
                        "account": None,
                        "error": "Build requires at least major and minor version [Eg. 15.1], at most 4 number [Eg. 15.0.1.2345]",
                    }
            except ValueError:
                return {
                    "account": None,
                    "error": "Build needs to be a sequence of numbers dot separated, not %s"
                    % build,
                }

        try:
            credentials = Credentials(username, password)
            if processed_build:
                version = Version(build=Build(*processed_build))
                config = Configuration(
                    server=server, credentials=credentials, version=version
                )
            else:
                config = Configuration(server=server, credentials=credentials)
            account = Account(
                account, config=config, autodiscover=False, access_type=DELEGATE
            )
            account.root.refresh()
        except (exchangelib.errors.TransportError, Exception) as error:
            return {
                "account": None,
                "error": "Can't connect to Exchange server: %s" % (error),
            }

        return {"account": account, "error": False}

    async def parse_folder(self, account, foldername):
        """
        Parses specific folder and returns proper object
        """
        if not foldername:
            print("Defaulting to inbox as foldername")
            foldername = "inbox"

        foldername = foldername.strip().replace("\\", "/")
        folderroot, *foldersubs = foldername.split("/")

        if folderroot.lower() not in ["inbox", "outbox", "sent", "trash", "draft"]:
            return {
                "folder": None,
                "error": "Root folder {} not supported. Valid values are: inbox, outbox, sent, trash, draft".format(
                    folderroot
                ),
            }

        if folderroot == "outbox":
            folder = account.outbox
        elif folderroot == "sent":
            folder = account.sent
        elif folderroot == "trash":
            folder = account.trash
        elif folderroot == "draft":
            folder = account.draft
        else:
            folder = account.inbox

        for sub in foldersubs:
            folder = folder / sub

        return {"folder": folder, "error": False}

    async def send_email(
        self,
        username,
        password,
        server,
        build,
        account,
        verifyssl,
        recipient,
        subject,
        body,
        attachments,
    ):
        # Authenticate
        auth = await self.authenticate(
            username, password, server, build, account, verifyssl
        )
        if auth["error"]:
            return auth["error"]
        account = auth["account"]

        m = Message(
            account=account,
            subject=subject,
            body=body,
            to_recipients=[
                Mailbox(email_address=address) for address in recipient.split(", ")
            ],
        )

        file_uids = attachments.split()
        if len(file_uids) > 0:
            for file_uid in file_uids:
                attachment_data = self.get_file(file_uid)
                file = FileAttachment(
                    name=attachment_data["filename"], content=attachment_data["data"]
                )
                m.attach(file)

        m.send()
        return {"ok": True, "error": False}

    async def mark_email_as_read(
        self, username, password, server, build, account, verifyssl, email_id, foldername="inbox"
    ):
        if not foldername:
            foldername = "inbox"

        # Authenticate
        print(f"Marking {email_id} as read")
        auth = await self.authenticate(
            username, password, server, build, account, verifyssl
        )

        if auth["error"]:
            return auth["error"]

        account = auth["account"]

        folder = await self.parse_folder(account, foldername)
        if folder["error"]:
            return folder["error"]

        folder = folder["folder"]
        email_id = email_id.strip()

        # Authenticates to Exchange server
        try:
            email = folder.get(message_id=email_id)
            email.is_read = True
            email.save()
            account.root.refresh()
            return {"ok": True, "error": False}
        except exchangelib.errors.DoesNotExist as e:
            print("ERROR: %s" % e)
            return {"ok": False, "error": "Email {} does not exists".format(email_id)}

    async def add_category(
        self, username, password, server, build, account, verifyssl, email_id, category, foldername="inbox"
        ):

        if not foldername:
            foldername = "inbox"

        category = [i.strip() for i in category.split(",")]

        # Authenticate
        print(f"Adding category {category} to {email_id}")
        auth = await self.authenticate(
            username, password, server, build, account, verifyssl
        )

        if auth["error"]:
            return auth["error"]

        account = auth["account"]

        folder = await self.parse_folder(account, foldername)
        if folder["error"]:
            return folder["error"]

        folder = folder["folder"]
        email_id = email_id.strip()

        # Authenticates to Exchange server
        try:
            email = folder.get(message_id=email_id)
            email.categories.extend(category)
            email.save()
            account.root.refresh()
            return {"ok": True, "error": False}
        except exchangelib.errors.DoesNotExist as e:
            print("ERROR: %s" % e)
            return {"ok": False, "error": "Email {} does not exists".format(email_id)}

    async def delete_email(
        self, username, password, server, build, account, verifyssl, email_id
    ):
        # Authenticate
        auth = await self.authenticate(
            username, password, server, build, account, verifyssl
        )
        if auth["error"]:
            return auth["error"]
        account = auth["account"]

        # Get email and delete
        try:
            email = account.inbox.get(message_id=email_id)
            email.delete()
            account.root.refresh()
            return {"ok": True, "error": False}
        except exchangelib.errors.DoesNotExist:
            return {"ok": False, "error": "Email {} does not exists".format(email_id)}

    async def move_email(
        self,
        username,
        password,
        server,
        build,
        account,
        verifyssl,
        email_id,
        foldername,
    ):
        # Authenticate
        auth = await self.authenticate(
            username, password, server, build, account, verifyssl
        )
        if auth["error"]:
            return auth["error"]
        account = auth["account"]

        # Parse email destination folder
        folder = await self.parse_folder(account, foldername)
        if folder["error"]:
            return folder["error"]
        folder = folder["folder"]

        # Move email
        try:
            email = account.inbox.get(message_id=email_id)
            email.move(to_folder=folder)
            account.root.refresh()
            return {"ok": True, "error": False}
        except exchangelib.errors.DoesNotExist:
            return {"ok": False, "error": "Email {} does not exists".format(email_id)}

    async def get_emails(
        self,
        username,
        password,
        server,
        build,
        account,
        verifyssl,
        foldername,
        category,
        amount,
        unread,
        fields,
        include_raw_body,
        include_attachment_data,
        upload_email_shuffle,
        upload_attachments_shuffle,
    ):
        def path_to_dict(path, value=None):
            def pack(parts):
                return (
                    {parts[0]: pack(parts[1:]) if len(parts) > 1 else value}
                    if len(parts) > 1
                    else {parts[0]: value}
                )

            return pack(path.split("."))

        def merge(d1, d2):
            for k in d2:
                if k in d1 and isinstance(d1[k], dict) and isinstance(d2[k], dict):
                    merge(d1[k], d2[k])
                else:
                    d1[k] = d2[k]

        # Authenticate
        auth = await self.authenticate(
            username, password, server, build, account, verifyssl
        )
        if auth["error"]:
            return json.dumps({
                "success": False,
                "reason": auth["error"]
            })

        account = auth["account"]

        # Parse email folder
        folder = await self.parse_folder(account, foldername)
        if folder["error"]:
            return json.dumps({
                "success": False,
                "reason": folder["error"]
            })

        folder = folder["folder"]
        if type(amount) == str:
            try:
                amount = int(amount)
            except ValueError:
                return json.dumps({
                    "success": False,
                    "account": None,
                    "error": "Amount needs to be a number, not %s" % amount,
                })

        # Get input from gui
        unread = True if unread.lower().strip() == "true" else False
        category = category.lower().strip()
        include_raw_body = True if include_raw_body.lower().strip() == "true" else False
        include_attachment_data = (
            True if include_attachment_data.lower().strip() == "true" else False
        )
        upload_email_shuffle = (
            True if upload_email_shuffle.lower().strip() == "true" else False
        )
        upload_attachments_shuffle = (
            True if upload_attachments_shuffle.lower().strip() == "true" else False
        )

        # Convert <amount> of mails in json
        emails = []
        ep = eml_parser.EmlParser(
            include_attachment_data=include_attachment_data,
            include_raw_body=include_raw_body,
        )

        try:

            if category:
                folder_filter = folder.filter(is_read=not unread, categories__icontains=category).order_by(
                    "-datetime_received"
                )[:amount]
            else:
                folder_filter = folder.filter(is_read=not unread).order_by(
                    "-datetime_received"
                )[:amount]

            for email in folder_filter:
                output_dict = {}
                parsed_eml = ep.decode_email_bytes(email.mime_content)

                if fields and fields.strip() != "":
                    for field in fields.split(","):
                        field = field.strip()
                        merge(
                            output_dict,
                            path_to_dict(
                                field,
                                glom(parsed_eml, field, default=None),
                            ),
                        )
                else:
                    output_dict = parsed_eml

                # Add message_id as top returned field
                output_dict["message_id"] = parsed_eml["header"]["header"]["message-id"][0]

                if upload_email_shuffle:
                    email_up = [{"filename": "email.msg",
                                 "data": email.mime_content}]
                    email_id = self.set_files(email_up)
                    output_dict["email_fileid"] = email_id[0]

                if upload_attachments_shuffle:
                    atts_up = [
                        {"filename": attachment.name, "data": attachment.content}
                        for attachment in email.attachments
                        if type(attachment) == FileAttachment
                    ]

                    atts_ids = self.set_files(atts_up)
                    output_dict["attachment_uids"] = atts_ids

                try:
                    if len(output_dict["body"]) > 1:
                        output_dict["body"][0]["raw_body"] = output_dict["body"][1]["content"]
                except KeyError as e:
                    print("OK KeyError (1): %s" % e)
                except IndexError as e:
                    print("OK IndexError (1): %s" % e)

                try:
                    if len(output_dict["body"]) > 0:
                        output_dict["body"] = output_dict["body"][0]
                except KeyError as e:
                    print("OK KeyError (2): %s" % e)
                except IndexError as e:
                    print("OK IndexError (2): %s" % e)

                try:
                    del output_dict["attachment"]
                except KeyError as e:
                    print("Ok Error (3): %s" % e)
                except IndexError as e:
                    print("OK IndexError (3): %s" % e)

                print("Appending email")
                emails.append(output_dict)
        except Exception as err:
            return json.dumps({
                "success": False,
                "reason": "Error during email processing: {}".format(err)
            })

        print("FINISHED - RETURNING")
        message = {
            "success": True,
            "messages": emails,
        }

        print(message)

        return json.dumps(message, default=default)
        #json.dumps(message, default=default)


# Run the actual thing after we've checked params
def run(request):
    action = request.get_json()
    authorization_key = action.get("authorization")
    current_execution_id = action.get("execution_id")

    if action and "name" in action and "app_name" in action:
        asyncio.run(Owa.run(action), debug=True)
        return f'Attempting to execute function {action["name"]} in app {action["app_name"]}'
    else:
        return f"Invalid action"


if __name__ == "__main__":
    asyncio.run(Owa.run(), debug=True)
