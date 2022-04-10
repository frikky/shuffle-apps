import asyncio
import json
import random
import socket
import time

import requests
from walkoff_app_sdk.app_base import AppBase

class Siemonster(AppBase):
    __version__ = "1.0.0"
    app_name = "siemonster"  # this needs to match "name" in api.yaml

    def __init__(self, redis, logger, console_logger=None):
        """
        Each app should have this __init__ to set up Redis and logging.
        :param redis:
        :param logger:
        :param console_logger:
        """
        super().__init__(redis, logger, console_logger)

    def ping(self, username, password, url):
        message = f"SIEMonster welcomes from {socket.gethostname()} in workflow {self.current_execution_id}!"

        # This logs to the docker logs
        self.logger.info(message)

        return message

    def es_get_cluster_health(self, username, password, url):
        return requests.get(url + "/_cluster/health", auth=(username, password), verify=False).text

    def es_query(self, method, username, password, url, path, body):
        headers = {
            "Accept": "application/json",
            "Content-type": "application/json",
        }
        return requests.request(method, url + path, auth=(username, password), data=body, headers=headers, verify=False).text

if __name__ == "__main__":
    Siemonster.run()
