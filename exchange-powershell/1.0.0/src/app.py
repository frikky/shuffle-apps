import asyncio
import base64
import json
import random
import socket
import subprocess
import time

from walkoff_app_sdk.app_base import AppBase

# 1. Generate the api.yaml based on downloaded files
# 2. Add a way to choose the rule and the target platform for it
# 3. Add the possibility of translating rules back and forth

# 4. Make it so you can start with Mitre Att&ck techniques
# and automatically get the right rules set up with your tools :O
class exchange_powershell(AppBase):
    __version__ = "1.0.0"
    app_name = "exchange-powershell"

    def __init__(self, redis, logger, console_logger=None):
        """
        Each app should have this __init__ to set up Redis and logging.
        :param redis:
        :param logger:
        :param console_logger:
        """
        self.filename = "replacementfile.ps1"
        super().__init__(redis, logger, console_logger)

    def cleanup(self, item):
        newlines = []
        record = False
        skipped = 0
        for line in item.split("\n"):
            if line.startswith("{") or line.startswith("["):
                record = True

            if not record and not line.startswith("{") and not line.startswith("["):
                skipped += 1

            if record:
                newlines.append(line)


        print(f"SKIPPED {skipped} lines")
        if len(newlines) == 0:
            return item

        item = "\n".join(newlines)

        return item

    def replace_and_run(self, username, password, parsed_command):
        data = ""
        with open(self.filename, "r") as tmp:
            data = tmp.read()

        if len(data) == 0:
            return ""

        data = data.replace("{USERNAME}", username)
        data = data.replace("{PASSWORD}", password)
        data = data.replace("{COMMAND}", parsed_command)

        with open(self.filename, "w+") as tmp:
            tmp.write(data)

        command = f"pwsh -file {self.filename}"
        print(f"PRE POPEN: {command}")
        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            shell=True,  # nosec
        )
        print("POST STDOUT")
        stdout = process.communicate()
        print(f"STDOUT: {stdout}")
        item = ""
        if len(stdout[0]) > 0:
            item = stdout[0]
            print("Succesfully ran bash. Stdout: %s" % item)
        else:
            item = stdout[1]
            print("FAILED to run bash. Stdout: %s!" % item)
            #return item

        try:
            new_cleanup = self.cleanup(item)
            if len(new_cleanup) > 0:
                item = new_cleanup
        except Exception as e:
            pass

        try:
            return item.decode("utf-8")
        except Exception as e:
            return item

        return item

    # Write your data inside this function
    def release_quarantine_message(self, username, password, message_id):
        parsed_command = f"Release-QuarantineMessage -Identity {message_id} | ConvertTo-Json"

        ret = self.replace_and_run(username, password, parsed_command)
        return ret

    # Write your data inside this function
    def preview_quarantine_message(self, username, password, message_id):
        parsed_command = f"Preview-QuarantineMessage -Identity {message_id} | ConvertTo-Json"

        ret = self.replace_and_run(username, password, parsed_command)
        return ret

    # Write your data inside this function
    def export_quarantine_message(self, username, password, message_id, skip_upload="false"):
        parsed_command = f"Export-QuarantineMessage -Identity {message_id} | ConvertTo-Json"

        ret = self.replace_and_run(username, password, parsed_command)
        print("RET: %s" % ret)
        try:
            if not isinstance(ret, list) and not isinstance(ret, object) and not isinstance(ret, dict):
                ret = json.loads(ret)
        except json.decoder.JSONDecodeError:
            return ret

        file_eml = ret["Eml"]
        if skip_upload == "true":
            return file_eml

        message_bytes = base64.b64decode(file_eml)

        fileinfo = self.set_files({
            "filename": f"{message_id}.eml",
            "data": message_bytes
        })

        if len(fileinfo) == 1:
            return {
                "success": True,
                "file_id": fileinfo[0]
            }

        return fileinfo

    # Write your data inside this function
    def delete_quarantine_message(self, username, password, message_id):
        parsed_command = f"Delete-QuarantineMessage -Identity {message_id} | ConvertTo-Json"

        ret = self.replace_and_run(username, password, parsed_command)
        return ret

    # Write your data inside this function
    def get_quarantine_message(self, username, password, message_id):
        parsed_command = f"Get-QuarantineMessage {message_id} | ConvertTo-Json"

        ret = self.replace_and_run(username, password, parsed_command)
        return ret

    # Write your data inside this function
    def get_quarantine_messages(self, username, password, time_from, time_to):
        parsed_command = f"Get-QuarantineMessage -StartReceivedDate {time_from} -EndReceivedDate {time_to} | ConvertTo-Json"

        ret = self.replace_and_run(username, password, parsed_command)
        return ret

    # Write your data inside this function
    def get_quarantine_messageheaders(self, username, password, message_id):
        parsed_command = f"Get-QuarantineMessageHeader {message_id} | ConvertTo-Json"

        ret = self.replace_and_run(username, password, parsed_command)
        return ret

if __name__ == "__main__":
    exchange_powershell.run()
