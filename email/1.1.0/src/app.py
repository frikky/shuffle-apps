import asyncio
import base64
import datetime
import imaplib
import json
import random
import smtplib
import socket
import time
import uuid
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import eml_parser
import extract_msg
import jsonpickle
import mailparser
import requests
from glom import glom
from msg_parser import MsOxMessage
from walkoff_app_sdk.app_base import AppBase

def json_serial(obj):
    if isinstance(obj, datetime.datetime):
        serial = obj.isoformat()
        return serial

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


class Email(AppBase):
    __version__ = "1.1.0"
    app_name = "email"

    def __init__(self, redis, logger, console_logger=None):
        """
        Each app should have this __init__ to set up Redis and logging.
        :param redis:
        :param logger:
        :param console_logger:
        """
        super().__init__(redis, logger, console_logger)

    # This is an email function of Shuffle
    def send_email_shuffle(self, apikey, recipients, subject, body):
        targets = [recipients]
        if ", " in recipients:
            targets = recipients.split(", ")
        elif "," in recipients:
            targets = recipients.split(",")

        data = {"targets": targets, "body": body, "subject": subject, "type": "alert"}

        url = "https://shuffler.io/functions/sendmail"
        headers = {"Authorization": "Bearer %s" % apikey}
        return requests.post(url, headers=headers, json=data).text

    def send_email_smtp(
        self, username, password, smtp_host, recipient, subject, body, smtp_port, attachments="", ssl_verify="True"
    ):
        if type(smtp_port) == str:
            try:
                smtp_port = int(smtp_port)
            except ValueError:
                return "SMTP port needs to be a number (Current: %s)" % smtp_port

        try:
            s = smtplib.SMTP(host=smtp_host, port=smtp_port)
        except socket.gaierror as e:
            return f"Bad SMTP host or port: {e}"

        if ssl_verify == "false" or ssl_verify == "False":
            pass
        else:
            s.starttls()

        if len(username) > 0 or len(password) > 0:
            try:
                s.login(username, password)
            except smtplib.SMTPAuthenticationError as e:
                return f"Bad username or password: {e}"

        # setup the parameters of the message
        msg = MIMEMultipart()
        msg["From"] = username
        msg["To"] = recipient
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "html"))

        # Read the attachments
        attachment_count = 0
        try:
            if attachments != None and len(attachments) > 0:
                print("Got attachments: %s" % attachments)
                attachmentsplit = attachments.split(",")

                #attachments = parse_list(attachments, splitter=",")
                #print("Got attachments2: %s" % attachmentsplit)
                print("Before loop")
                files = []
                for file_id in attachmentsplit:
                    print(f"Looping {file_id}")
                    file_id = file_id.strip()
                    new_file = self.get_file(file_id)
                    print(f"New file: {new_file}")
                    try:
                        part = MIMEApplication(
                            new_file["data"],
                            Name=new_file["filename"],
                        )
                        part["Content-Disposition"] = f"attachment; filename=\"{new_file['filename']}\""
                        msg.attach(part)
                        attachment_count += 1
                    except Exception as e:
                        print(f"[WARNING] Failed to attach {file_id}: {e}")


                    #files.append(new_file)

                #return files
                #data["attachments"] = files
        except Exception as e:
            print(f"Error in attachment parsing for email: {e}")


        try:
            s.send_message(msg)
        except smtplib.SMTPDataError as e:
            return {
                "success": False,
                "reason": f"Failed to send mail: {e}"
            }

        print("Successfully sent email with subject %s to %s" % (subject, recipient))
        return {
            "success": True,
            "reason": "Email sent to %s!" % recipient,
            "attachments": attachment_count
        }

    def get_emails_imap(
        self,
        username,
        password,
        imap_server,
        foldername,
        amount,
        unread,
        fields,
        include_raw_body,
        include_attachment_data,
        upload_email_shuffle,
        upload_attachments_shuffle,
        ssl_verify="True"
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

        if type(amount) == str:
            try:
                amount = int(amount)
            except ValueError:
                return "Amount needs to be a number, not %s" % amount

        try:
            email = imaplib.IMAP4_SSL(imap_server)
        except ConnectionRefusedError as error:
            try:
                email = imaplib.IMAP4(imap_server)

                if ssl_verify == "false" or ssl_verify == "False":
                    pass
                else:
                    email.starttls()
            except socket.gaierror as error:
                return "Can't connect to IMAP server %s: %s" % (imap_server, error)
        except socket.gaierror as error:
            return "Can't connect to IMAP server %s: %s" % (imap_server, error)

        try:
            email.login(username, password)
        except imaplib.IMAP4.error as error:
            return "Failed to log into %s: %s" % (username, error)

        email.select(foldername)
        unread = True if unread.lower().strip() == "true" else False
        try:
            # IMAP search queries, e.g. "seen" or "read"
            # https://www.rebex.net/secure-mail.net/features/imap-search.aspx
            mode = "(UNSEEN)" if unread else "ALL"
            thistype, data = email.search(None, mode)
        except imaplib.IMAP4.error as error:
            return "Couldn't find folder %s." % (foldername)

        email_ids = data[0]
        id_list = email_ids.split()
        if id_list == None:
            return "Couldn't retrieve email. Data: %s" % data

        try:
            print("LIST: ", len(id_list))
        except TypeError:
            return "Error getting email. Data: %s" % data

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
            include_attachment_data=include_attachment_data
            or upload_attachments_shuffle,
            include_raw_body=include_raw_body,
        )
        try:
            for i in range(len(id_list) - 1, len(id_list) - amount - 1, -1):
                resp, data = email.fetch(id_list[i], "(RFC822)")
                error = None

                if resp != "OK":
                    print("Failed getting %s" % id_list[i])
                    continue

                if data == None:
                    continue

                output_dict = {}
                parsed_eml = ep.decode_email_bytes(data[0][1])

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

                # Add message-id as top returned field
                output_dict["message-id"] = parsed_eml["header"]["header"][
                    "message-id"
                ][0]

                if upload_email_shuffle:
                    email_up = [{"filename": "email.msg", "data": data[0][1]}]
                    email_id = self.set_files(email_up)
                    output_dict["email_uid"] = email_id[0]

                if upload_attachments_shuffle:
                    atts_up = [
                        {
                            "filename": x["filename"],
                            "data": base64.b64decode(x["raw"]),
                        }
                        for x in parsed_eml["attachment"]
                    ]
                    atts_ids = self.set_files(atts_up)
                    output_dict["attachments_uids"] = atts_ids

                emails.append(output_dict)
        except Exception as err:
            return "Error during email processing: {}".format(err)
        return json.dumps(emails, default=default)

    def parse_email_file(self, file_id, file_extension):
        file_path = self.get_file(file_id)
        if file_path["success"] == False:
            return {
                "success": False,
                "reason": "Couldn't get file with ID %s" % file_id
            }

        print("File: %s" % file_path)
        if file_extension.lower() == 'eml':
            print('working with .eml file')
            ep = eml_parser.EmlParser()
            try:
                parsed_eml = ep.decode_email_bytes(file_path['data'])
                return json.dumps(parsed_eml, default=json_serial)
            except Exception as e:
                return {"Success":"False","Message":f"Exception occured: {e}"}
        elif file_extension.lower() == 'msg':
            print('working with .msg file')
            try:
                msg = MsOxMessage(file_path['data'])
                msg_properties_dict = msg.get_properties()
                print(msg_properties_dict)
                frozen = jsonpickle.encode(msg_properties_dict)
                return frozen
            except Exception as e:
                return {"Success":"False","Message":f"Exception occured: {e}"}
        else:
            return {"Success":"False","Message":f"No file handler for file extension {file_extension}"}

    def parse_email_headers(self, email_headers):
        try:
            email_headers = bytes(email_headers,'utf-8')
            ep = eml_parser.EmlParser()
            parsed_headers = ep.decode_email_bytes(email_headers)
            return json.dumps(parsed_headers, default=json_serial)
        except Exception as e:
            raise Exception(e)


# Run the actual thing after we've checked params
def run(request):
    action = request.get_json()
    authorization_key = action.get("authorization")
    current_execution_id = action.get("execution_id")

    if action and "name" in action and "app_name" in action:
        Email.run(action)
        return f'Attempting to execute function {action["name"]} in app {action["app_name"]}'
    else:
        return f"Invalid action"


if __name__ == "__main__":
    Email.run()
