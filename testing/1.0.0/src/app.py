import asyncio
import json
import random
import socket
import time

import requests
from walkoff_app_sdk.app_base import AppBase

class HelloWorld(AppBase):
    """
    An example of a Walkoff App.
    Inherit from the AppBase class to have Redis, logging, and console logging set up behind the scenes.
    """
    __version__ = "1.0.0"
    app_name = "hello_world"  # this needs to match "name" in api.yaml

    def __init__(self, redis, logger, console_logger=None):
        """
        Each app should have this __init__ to set up Redis and logging.
        :param redis:
        :param logger:
        :param console_logger:
        """
        super().__init__(redis, logger, console_logger)

    def hello_world(self):
        """
        Returns Hello World from the hostname the action is run on
        :return: Hello World from your hostname
        """
        message = f"Hello World from {socket.gethostname()} in workflow {self.current_execution_id}!"

        # This logs to the docker logs
        self.logger.info(message)

        return message

    def repeat_back_to_me(self, call):
        return call

    def repeat_back_to_me_multi(self, call, call2, call3):
        return {"call1": call, "call2": call2, "call3": call3}

    def return_plus_one(self, number):
        return int(number) + 1

    def pause(self, seconds):
        time.sleep(seconds)
        return "Waited %d seconds" % seconds

    def get_type(self, value):
        return "Type: %s" % type(value)

    def input_options_test(self, call):
        return "Value: %s" % call

    def get_file_value(self, filedata):
        if filedata == None:
            return "File is empty?"

        print("INSIDE APP DATA: %s" % filedata)
        return "%s" % filedata["data"].decode()

    def create_file(self, filename, data):
        print("Inside function")
        filedata = {
            "filename": filename,
            "data": data,
        }

        fileret = self.set_files([filedata])
        value = {"success": True, "file_ids": fileret}
        return value
        #print("Done with upload function")

        #return ("Successfully put your data in a file", filedata)

    def download_file(self, url):
        ret = requests.get(url, verify=False)
        fileret = self.set_files([{
            "filename": "downloaded",
            "data": ret.content,
        }])

        value = {"success": True, "file_ids": fileret}
        return value

        #return ("Successfully put your data in a file", filedata)

    def delete_file(self, file_id):
        headers = {
            "Authorization": "Bearer %s" % self.authorization,
        }
        print("HEADERS: %s" % headers)

        ret = requests.delete("%s/api/v1/files/%s?execution_id=%s" % (self.base_url, file_id, self.current_execution_id), headers=headers)
        return ret.text

if __name__ == "__main__":
    HelloWorld.run()
