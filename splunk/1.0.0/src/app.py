#!/usr/bin/env python
# -*- coding: utf-8 -*-
import asyncio
import json
import random
import time

import requests
import urllib3
from walkoff_app_sdk.app_base import AppBase

class Splunk(AppBase):
    """
    Splunk integration for WALKOFF with some basic features
    """
    __version__ = "1.0.0"
    app_name = "splunk"

    def __init__(self, redis, logger, console_logger=None):
        """
        Each app should have this __init__ to set up Redis and logging.
        :param redis:
        :param logger:
        :param console_logger:
        """
        self.verify = False
        self.timeout = 10
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        super().__init__(redis, logger, console_logger)

    def echo(self, input_data):
        return input_data

    def run_search(self, auth, url, query):
        url = '%s/services/search/jobs?output_mode=json' % (url)
        ret = requests.post(url, auth=auth, data=query, timeout=self.timeout, verify=False)
        return ret

    def get_search(self, auth, url, search_sid):
        # Wait for search to be done?
        firsturl = '%s/services/search/jobs/%s?output_mode=json' % (url, search_sid)
        print("STARTED FUNCTION WITH URL %s" % firsturl)
        time.sleep(0.2)
        maxrunduration = 30
        ret = "No results yet"
        while(True):
            try:
                ret = requests.get(firsturl, auth=auth, timeout=self.timeout, verify=False)
            except requests.exceptions.ConnectionError:
                print("Sleeping for 1 second")
                time.sleep(1)
                continue

            try:
                content = ret.json()["entry"][0]["content"]
            except KeyError as e:
                print("\nKEYERROR: %s\n" % content)
                time.sleep(1)
                continue

            try:
                if content["resultCount"] > 0 or content["isDone"] or content["isFinalized"] or content["runDuration"] > maxrunduration:
                    print("CONTENT PRE EVENTS: ", content)
                    eventsurl = '%s/services/search/jobs/%s/events' % (url, search_sid)
                    print("Running events check towards %s" % eventsurl)
                    try:
                        newret = requests.get(eventsurl, auth=auth, timeout=self.timeout, verify=False)
                        if ret.status_code < 300 and ret.status_code >= 200:
                            return newret.text
                        else:
                            return "Bad status code for events: %sd", ret.status_code
                    except requests.exceptions.ConnectionError:
                        return "Events requesterror: %s" % e
            except KeyError:
                try:
                    return ret.json()["messages"]
                except KeyError as e:
                    return "KeyError: %s" % e

            time.sleep(1)

        return ret

    def SplunkQuery(self, url, username, password, query, result_limit=100, earliest_time="-24h", latest_time="now"):
        auth = (username, password)

        # "latest_time": "now"
        query = {
            "search": "| search %s" % query,
            "exec_mode": "normal",
            "count": result_limit,
            "earliest_time": earliest_time,
            "latest_time": latest_time
        }

        print("Current search: %s" % query["search"])

        try:
            ret = self.run_search(auth, url, query)
        except requests.exceptions.ConnectTimeout as e:
            print("Timeout: %s" % e)
            return "Timeout: %s" % e

        if ret.status_code != 201:
            print("Bad status code: %d" % ret.status_code)
            return "Bad status code: %d" % ret.status_code

        search_id = ret.json()["sid"]

        print("Search ID: %s" % search_id)

        ret = self.get_search(auth, url, search_id)
        return ret
        #if len(ret.json()["entry"]) == 1:
        #    count = ret.json()["entry"][0]["content"]["resultCount"]
        #    print("Result: %d" % count)
        #    return str(count)

        #print("No results (or wrong?): %d" % (len(ret.json()["entry"])))
        #return "No results"

if __name__ == "__main__":
    Splunk.run()
