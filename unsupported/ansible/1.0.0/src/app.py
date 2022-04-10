import asyncio
import json
import random
import socket
import time

import ansible.runner
from walkoff_app_sdk.app_base import AppBase

class Ansible(AppBase):
    __version__ = "1.0.0"
    app_name = "ansible"  # this needs to match "name" in api.yaml

    def __init__(self, redis, logger, console_logger=None):
        """
        Each app should have this __init__ to set up Redis and logging.
        :param redis:
        :param logger:
        :param console_logger:
        """
        super().__init__(redis, logger, console_logger)

    def run_playbook(self, playbook):
        filedata = self.get_file(playbook)
        return filedata

if __name__ == "__main__":
    Ansible.run()
