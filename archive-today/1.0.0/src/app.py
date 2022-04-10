import asyncio
import json
import socket
import time

import archiveis
import requests
from walkoff_app_sdk.app_base import AppBase

class ArchiveToday(AppBase):
    __version__ = "1.0.0"
    app_name = "Archive.today"    # this needs to match "name" in api.yaml

    def __init__(self, redis, logger, console_logger=None):
        """
        Each app should have this __init__ to set up Redis and logging.
        :param redis:
        :param logger:
        :param console_logger:
        """
        self.headers = {"Content-Type": "application/json"}
        super().__init__(redis, logger, console_logger)


    def archive_target(self, target):
        archive_url = archiveis.capture(target)
        """
        Returns log of what was archived
        """
        message = f"target {target} has been archived"

        # This logs to the docker logs
        self.logger.info(message)
        return archive_url

#        return target

if __name__ == "__main__":
    ArchiveToday.run()
