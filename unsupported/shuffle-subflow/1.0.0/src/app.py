import asyncio
import json
import random
import time

import requests
from walkoff_app_sdk.app_base import AppBase

class Subflow(AppBase):
    """
    An example of a Walkoff App.
    Inherit from the AppBase class to have Redis, logging, and console logging set up behind the scenes.
    """
    __version__ = "1.0.0"
    app_name = "subflow"  # this needs to match "name" in api.yaml

    def __init__(self, redis, logger, console_logger=None):
        """
        Each app should have this __init__ to set up Redis and logging.
        :param redis:
        :param logger:
        :param console_logger:
        """
        super().__init__(redis, logger, console_logger)

    #def run_userinput(self, sms, email, subflow, argument):
    #    url = "%s/api/v1/workflows/%s/execute" % (self.url, workflow)

    #    if len(sms) > 0:

    def run_subflow(self, user_apikey, workflow, argument, source_workflow="", source_execution="", source_node="", source_auth="", startnode=""):
        print("STARTNODE: %s" % startnode)
        url = "%s/api/v1/workflows/%s/execute" % (self.url, workflow)

        params = {}
        if len(source_workflow) > 0:
            params["source_workflow"] = source_workflow
        else:
            print("No source workflow")

        if len(source_auth) > 0:
            params["source_auth"] = source_auth
        else:
            print("No source auth")

        if len(source_node) > 0:
            params["source_node"] = source_node
        else:
            print("No source node")

        if len(source_execution) > 0:
            params["source_execution"] = source_execution
        else:
            print("No source execution")

        if len(startnode) > 0:
            params["start"] = startnode
        else:
            print("No startnode")

        headers = {
            "Authorization": "Bearer %s" % user_apikey,
        }

        if len(argument) == 0:
            ret = requests.post(url, headers=headers, params=params)
        else:
            try:
                ret = requests.post(url, headers=headers, params=params, json=json.loads(argument))
                print(f"Successfully sent argument of length {len(argument)} as JSON")
            except:
                try:
                    ret = requests.post(url, headers=headers, json=argument, params=params)
                    print("Successfully sent as JSON (2)")
                except:
                    ret = requests.post(url, headers=headers, data=argument, params=params)
                    print("Successfully sent as data (3)")

        print("Status: %d" % ret.status_code)
        print("RET: %s" % ret.text)

        return ret.text

        # This logs to the docker logs
        #self.logger.info(message)

        return message

if __name__ == "__main__":
    Subflow.run()
