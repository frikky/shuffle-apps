import asyncio
import json
import random
import socket
import time

import requests
from walkoff_app_sdk.app_base import AppBase

class BreachSense(AppBase):
    __version__ = "1.0.0"
    app_name = "Breachsense"  # this needs to match "name" in api.yaml

    def __init__(self, redis, logger, console_logger=None):
        """
        Each app should have this __init__ to set up Redis and logging.
        :param redis:
        :param logger:
        :param console_logger:
        """
        super().__init__(redis, logger, console_logger)

    def Basic_search(self, api_key, search_term, date):
        if date:
            url = f"https://breachsense.io/api?lic={api_key}&s={search_term}&date={date}&json"
        else:
            url = f"https://breachsense.io/api?lic={api_key}&s={search_term}&json"
        try:
            response = requests.get(url)
            return response.text
        except Exception as e:
            return "Exception occured: %s" % e

    def Display_Description(self, api_key, search_term, date):
        if date:
            url = f"https://breachsense.io/api?lic={api_key}&s={search_term}&date={date}&attr&json"
        else:
            url = f"https://breachsense.io/api?lic={api_key}&s={search_term}&attr&json"
        try:
            response = requests.get(url)
            return response.text
        except Exception as e:
            return "Exception occured: %s" % e

    def Strict_search(self, api_key, search_term, date):
        if date:
            url = f"https://breachsense.io/api?lic={api_key}&s={search_term}&date={date}&strict&json"
        else:
            url = f"https://breachsense.io/api?lic={api_key}&s={search_term}&strict&json"
        try:
            response = requests.get(url)
            return response.text
        except Exception as e:
            return "Exception occured: %s" % e

    def Check_credits(self, api_key):
        url = f"https://breachsense.io/api?lic={api_key}&r&json"
        try:
            response = requests.get(url)
            return response.text
        except Exception as e:
            return "Exception occured: %s" % e

    def Domain_Monitor(self, api_key, action, domain):
        url = f"https://breachsense.io/api?lic={api_key}&action={action}&dom={domain}&json"
        try:
            response = requests.get(url)
            return response.text
        except Exception as e:
            return "Exception occured: %s" % e

    def Custom_search(self, api_key, search_term, date, extra_Params):
        if date:
            url = f"https://breachsense.io/api?lic={api_key}&s={search_term}&date={date}&{extra_Params}&json"
        else:
            url = f"https://breachsense.io/api?lic={api_key}&s={search_term}&{extra_Params}&json"
        try:
            response = requests.get(url)
            return response.text
        except Exception as e:
            return "Exception occured: %s" % e

if __name__ == "__main__":
    BreachSense.run()
