import asyncio
import json
import random
import socket
import time

import requests
from pygitguardian import GGClient
from walkoff_app_sdk.app_base import AppBase

class GitGuardian(AppBase):
    __version__ = "1.0.0"
    app_name = "GitGuardian"  # this needs to match "name" in api.yaml

    def __init__(self, redis, logger, console_logger=None):
        """
        Each app should have this __init__ to set up Redis and logging.
        :param redis:
        :param logger:
        :param console_logger:
        """
        super().__init__(redis, logger, console_logger)

    def content_scan(self, api_key, content, file_id):
        client = GGClient(api_key=api_key)

        if file_id and content:
            raise Exception("Can not use file_id & content at once, Please use either one of them.")

        if file_id:
            text = file_id['data']
            try:
                scan_result = client.content_scan(document=text)
                return scan_result.to_json()
            except Exception as e:
                return f"Exception occured: {e}"

        if content:
            try:
                scan_result = client.content_scan(document=content)
                return scan_result.to_json()
            except Exception as e:
                return f"Exception occured: {e}"

if __name__ == "__main__":
    GitGuardian.run()
