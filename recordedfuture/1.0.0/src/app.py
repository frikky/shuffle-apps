import asyncio
import json
import socket
import time

import requests
from walkoff_app_sdk.app_base import AppBase

class Recordedfuture(AppBase):
    __version__ = "1.0.0"
    app_name = "recordedfuture"

    def __init__(self, redis, logger, console_logger=None):
        """
        Each app should have this __init__ to set up Redis and logging.
        :param redis:
        :param logger:
        :param console_logger:
        """
        super().__init__(redis, logger, console_logger)

    def get_alerts(self, apikey, status="", limit=10):
        url = "https://api.recordedfuture.com/v2/alert/search?limit=%s" % limit
        if status:
            url = "%s&status=%s" % (url, status)

        parsed_headers = {
            'X-RFToken': apikey,
        }

        return requests.get(url, headers=parsed_headers).text

    def get_alert(self, apikey, id):
        url = "https://api.recordedfuture.com/v2/alert/%s" % id
        parsed_headers = {
            'X-RFToken': apikey,
        }

        return requests.get(url, headers=parsed_headers).text


# Run the actual thing after we've checked params
def run(request):
    action = request.get_json()
    print(action)
    print(type(action))
    authorization_key = action.get("authorization")
    current_execution_id = action.get("execution_id")

    if action and "name" in action and "app_name" in action:
        Recordedfuture.run(action)
        return f'Attempting to execute function {action["name"]} in app {action["app_name"]}'
    else:
        return f'Invalid action'

if __name__ == "__main__":
    Recordedfuture.run()
