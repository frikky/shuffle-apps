#!/usr/bin/env python
# -*- coding: utf-8 -*-
import asyncio
import base64
import os
import tempfile

import requests
import urllib3
from walkoff_app_sdk.app_base import AppBase


class Misp(AppBase):
    """
    An example of a Walkoff App.
    Inherit from the AppBase class to have Redis, logging, and console logging set up behind the scenes.
    """

    __version__ = "1.0.0"
    app_name = "misp"

    def __init__(self, redis, logger, console_logger=None):
        """
        Each app should have this __init__ to set up Redis and logging.
        :param redis:
        :param logger:
        :param console_logger:
        """

        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        self.verify = False
        super().__init__(redis, logger, console_logger)

    def simplified_attribute_search(self, apikey, url, data):
        url = "%s/attributes/restSearch" % url
        data = {"value": data}
        headers = {
            "Accept": "application/json",
            "Content-type": "application/json",
            "Authorization": apikey,
        }

        return requests.post(url, headers=headers, json=data, verify=self.verify).text

    def simplified_warninglist_search(self, apikey, url, data):
        url = "%s/warninglists/checkValue" % url
        headers = {
            "Accept": "application/json",
            "Content-type": "application/json",
            "Authorization": apikey,
        }

        return requests.post(url, headers=headers, json=data, verify=self.verify).text

    def simplified_event_search(self, apikey, url, data):
        url = "%s/events/restSearch" % url
        data = {"value": data}
        headers = {
            "Accept": "application/json",
            "Content-type": "application/json",
            "Authorization": apikey,
        }

        return requests.post(url, headers=headers, json=data, verify=self.verify).text

    def attributes_search(self, apikey, url, data):
        url = "%s/attributes/restSearch" % url
        headers = {
            "Accept": "application/json",
            "Content-type": "application/json",
            "Authorization": apikey,
        }

        return requests.post(url, headers=headers, data=data, verify=self.verify).text

    def warninglist_search(self, apikey, url, data):
        url = "%s/warninglists/checkValue" % url
        headers = {
            "Accept": "application/json",
            "Content-type": "application/json",
            "Authorization": apikey,
        }

        return requests.post(url, headers=headers, data=data, verify=self.verify).text

    def events_search(self, apikey, url, data):
        url = "%s/events/restSearch" % url
        headers = {
            "Accept": "application/json",
            "Content-type": "application/json",
            "Authorization": apikey,
        }
        return requests.post(url, headers=headers, data=data, verify=self.verify).text

    def events_index(self, apikey, url, data):
        url = "%s/events/index" % url
        headers = {
            "Accept": "application/json",
            "Content-type": "application/json",
            "Authorization": apikey,
        }
        return requests.post(url, headers=headers, data=data, verify=self.verify).text

    def event_edit(self, apikey, url, event_id, data):
        url = "{}/events/edit/{}".format(url, event_id)
        headers = {
            "Accept": "application/json",
            "Content-type": "application/json",
            "Authorization": apikey,
        }
        return requests.post(url, headers=headers, data=data, verify=self.verify).text

    def attributes_downloadsample(self, apikey, url, md5_list):
        atts_up = []
        items = md5_list if type(md5_list) == list else md5_list.split(",")
        for md5 in items:

            print("Initial md5_list: {}".format(md5_list))

            # value returned from misp is filename|md5
            # the list in converted as string, so items has quote and last closing parenthesis
            md5 = md5.split("|")[-1]
            # .replace("[", "").replace('"', "").replace("]", "")

            print("Downloading with md5: {}".format(md5))

            url = "{}/attributes/downloadSample/{}".format(url, md5)
            misp_headers = {
                "Accept": "application/json",
                "Content-type": "application/json",
                "Authorization": apikey,
            }
            # get sample by md5 (works only if md5 is related to file object)
            ret = requests.get(url, headers=misp_headers, verify=self.verify)

            if ret.status_code == 200:
                sample = ret.json().get("result", None)
                if sample and len(sample) == 1:
                    sample = sample[0]
                elif not sample and ret.json().get("message", None):
                    return "Return message: {}".format(ret.json()["message"])

                atts_up.append(
                    {
                        "filename": "{}.zip".format(sample["filename"]),
                        "data": base64.b64decode(sample["base64"]),
                    }
                )
            else:
                return "Issue downloading {}".format(md5)

        if len(atts_up) > 0:
            uuids = self.set_files(atts_up)
            return uuids


if __name__ == "__main__":
    Misp.run()
