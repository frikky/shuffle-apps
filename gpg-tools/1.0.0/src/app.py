import asyncio
import json
import os
import random
import socket
import subprocess
import tempfile
import time

import gnupg
import requests
from walkoff_app_sdk.app_base import AppBase


class Gpg(AppBase):
    """
    An example of a Walkoff App.
    Inherit from the AppBase class to have Redis, logging, and console logging set up behind the scenes.
    """

    __version__ = "1.0.0"
    app_name = "Gpg Tools"

    def __init__(self, redis, logger, console_logger=None):
        """
        Each app should have this __init__ to set up Redis and logging.
        :param redis:
        :param logger:
        :param console_logger:
        """
        super().__init__(redis, logger, console_logger)

    def decrypt_file(
        self, gpg_home, always_trust, filedata, output_name, passphrase
    ):
        if filedata["success"] == False:
            return "Error managing files."
        always_trust = True if always_trust.lower() == "true" else False

        gpg = gnupg.GPG(gnupghome=os.path.join("/app/local/", gpg_home))
        gpg.decrypt_file(
            filedata["data"],
            passphrase=passphrase,
            output=output_name,
            always_trust=always_trust,
        )

        with open(output_name, "wb") as f:
            data = f.read()

        file_id = self.set_files([{"filename": output_name, "data": data}])
        if len(file_id) == 1:
            file_id = file_id[0]
        return {"success": True, "id": file_id}

    def encrypt_file(
        self,
        gpg_home,
        always_trust,
        filedata,
        output_name,
        recipients,
    ):
        if filedata["success"] == False:
            return "Error managing files."

        if type(recipients) != list:
            try:
                recipients = eval(recipients)
            except SyntaxError:
                return "Recipients must be a list."

        always_trust = True if always_trust.lower() == "true" else False

        print(
            "Using:\n\thome: {}\n\trecipients: {}\n\ttrust: {}".format(
                os.path.join("/app/local/", gpg_home), recipients, always_trust
            )
        )

        gpg = gnupg.GPG(
            gnupghome=os.path.join("/app/local/", gpg_home), gpgbinary="/usr/bin/gpg"
        )

        with tempfile.NamedTemporaryFile(delete=False) as tmpfile:
            with open(tmpfile.name, "wb") as f:
                tmpfile.write(filedata["data"])

        gpg.encrypt_file(
            open(tmpfile.name, "r"),
            recipients=recipients,
            output=output_name,
            always_trust=always_trust,
        )

        os.unlink(tmpfile.name)

        with open(output_name, "r") as f:
            data = f.read()

        file_id = self.set_files([{"filename": output_name, "data": data}])
        if len(file_id) == 1:
            file_id = file_id[0]
        return {"success": True, "id": file_id}


if __name__ == "__main__":
    Gpg.run()
