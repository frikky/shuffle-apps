import asyncio
import json
import socket
import time

import requests
from walkoff_app_sdk.app_base import AppBase

class Passivetotal(AppBase):
    __version__ = "1.0.0"
    app_name = "passivetotal"

    def __init__(self, redis, logger, console_logger=None):
        """
        Each app should have this __init__ to set up Redis and logging.
        :param redis:
        :param logger:
        :param console_logger:
        """
        self.headers = {"Content-Type": "application/json"}
        super().__init__(redis, logger, console_logger)

    def update_project(self, username, apikey, data):
        url = "https://api.passivetotal.org/v2/project"
        auth = (username, apikey)
        print(data)

        return requests.post(url, headers=self.headers, auth=auth, data=data).text

    def parse_tags(self, tags):
        if ", " in tags:
            return tags.split(", ")
        else:
            return tags.split(",")

    def add_artifact(self, username, apikey, project, artifact, tags=""):
        url = "https://api.passivetotal.org/v2/artifact"
        auth = (username, apikey)

        data = {
            "project": project,
            "query": artifact,
            "tags": self.parse_tags(tags),
        }

        return requests.put(url, headers=self.headers, auth=auth, json=data).text

    def checkmonitor(self, verify):
        if verify == True:
            return True
        elif verify == False:
            return False
        elif verify.lower().strip() == "false":
            return False
        else:
            return True

    def update_artifact(self, username, apikey, artifact_id, monitor=False, tags=""):
        url = "https://api.passivetotal.org/v2/artifact"
        auth = (username, apikey)

        data = {
            "artifact": artifact_id,
            "monitor": self.checkmonitor(monitor),
            "tags": self.parse_tags(tags),
        }

        return requests.post(url, headers=self.headers, auth=auth, json=data).text

    def get_artifact(self, username, apikey, query=""):
        url = "https://api.passivetotal.org/v2/artifact"
        auth = (username, apikey)

        params = {
            "query": query,
        }

        return requests.get(url, headers=self.headers, auth=auth, params=params).text

    def get_alerts(self, username, apikey, project_id="", artifact_id="", start="", end=""):
        url = "https://api.passivetotal.org/v2/artifact?"
        auth = (username, apikey)

        params = {
            "project": project_id,
            "artifact": artifact_id,
            "start": start,
            "end": end,
        }

        return requests.get(url, headers=self.headers, auth=auth, params=params).text

# Run the actual thing after we've checked params
def run(request):
    action = request.get_json()
    print(action)
    print(type(action))
    authorization_key = action.get("authorization")
    current_execution_id = action.get("execution_id")

    if action and "name" in action and "app_name" in action:
        Passivetotal.run(action)
        return f'Attempting to execute function {action["name"]} in app {action["app_name"]}'
    else:
        return f'Invalid action'

if __name__ == "__main__":
    Passivetotal.run()
