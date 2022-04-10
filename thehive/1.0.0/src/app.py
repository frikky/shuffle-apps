#!/usr/bin/env python
# -*- coding: utf-8 -*-
import asyncio
import json
import random
import time

import requests
import thehive4py.models
from thehive4py.api import TheHiveApi
from thehive4py.query import *
from walkoff_app_sdk.app_base import AppBase


class TheHive(AppBase):
    """
    An example of a Walkoff App.
    Inherit from the AppBase class to have Redis, logging, and console logging set up behind the scenes.
    """

    __version__ = "1.0.0"
    app_name = "thehive"

    def __init__(self, redis, logger, console_logger=None):
        """
        Each app should have this __init__ to set up Redis and logging.
        :param redis:
        :param logger:
        :param console_logger:
        """
        super().__init__(redis, logger, console_logger)

    # def run_analyzer(self, apikey, url, title_query):
    #    self.thehive = TheHiveApi(url, apikey, cert=False)

    #    response = self.thehive.find_cases(query=String("title:'%s'" % title_query), range='all', sort=[])
    #    return response.text

    def search_cases(self, apikey, url, title_query):
        self.thehive = TheHiveApi(url, apikey, cert=False)

        response = self.thehive.find_cases(
            query=ContainsString("title", title_query), range="all", sort=[]
        )

        return response.text

    def search_query(self, apikey, url, search_for, custom_query):
        self.thehive = TheHiveApi(url, apikey, cert=False)

        try:
            query = json.loads(custom_query)
        except:
            raise IOError("Invalid JSON payload received.")

        if search_for == "alert":
            response = self.thehive.find_alerts(query=query, range="all", sort=[])
        else:
            response = self.thehive.find_cases(query=query, range="all", sort=[])

        if response.status_code == 200:
            return response.text
        else:
            raise IOError(response.text)

    def add_observable(self, apikey, url, case_id, data, datatype, tags):
        self.thehive = TheHiveApi(url, apikey, cert=False)

        if tags:
            if ", " in tags:
                tags = tags.split(", ")
            elif "," in tags:
                tags = tags.split(",")
            else:
                tags = [tags]
        else:
            tags = []

        item = thehive4py.models.CaseObservable(
            dataType=datatype,
            data=data,
            tlp=1,
            ioc=False,
            sighted=False,
            tags=["Shuffle"],
            message="Created by shuffle",
        )

        return self.thehive.create_case_observable(case_id, item).text

    def search_alerts(self, apikey, url, title_query, search_range="0-25"):
        self.thehive = TheHiveApi(url, apikey, cert=False)

        # Could be "all" too
        if search_range == "":
            search_range = "0-25"

        response = self.thehive.find_alerts(
            query=ContainsString("title", title_query), range=search_range, sort=[]
        )
        return response.text

    def create_case(
        self, apikey, url, title, description="", tlp=1, severity=1, tags=""
    ):
        self.thehive = TheHiveApi(url, apikey, cert=False)
        if tags:
            if ", " in tags:
                tags = tags.split(", ")
            elif "," in tags:
                tags = tags.split(",")
            else:
                tags = [tags]
        else:
            tags = []

        # Wutface fix
        if not tlp:
            tlp = 1
        if not severity:
            severity = 1

        if isinstance(tlp, str):
            if not tlp.isdigit():
                return "TLP needs to be a number from 0-2, not %s" % tlp
            tlp = int(tlp)
        if isinstance(severity, str):
            if not severity.isdigit():
                return "Severity needs to be a number from 0-2, not %s" % tlp

            severity = int(severity)

        if tlp > 3 or tlp < 0:
            return "TLP needs to be a number from 0-3, not %d" % tlp
        if severity > 2 or severity < 0:
            return "Severity needs to be a number from 0-2, not %d" % tlp

        case = thehive4py.models.Case(
            title=title,
            tlp=tlp,
            severity=severity,
            tags=tags,
            description=description,
        )

        try:
            ret = self.thehive.create_case(case)
            return ret.text
        except requests.exceptions.ConnectionError as e:
            return "ConnectionError: %s" % e

    def create_alert(
        self,
        apikey,
        url,
        type,
        source,
        sourceref,
        title,
        description="",
        tlp=1,
        severity=1,
        tags="",
    ):
        self.thehive = TheHiveApi(url, apikey, cert=False)
        if tags:
            if ", " in tags:
                tags = tags.split(", ")
            elif "," in tags:
                tags = tags.split(",")
            else:
                tags = [tags]
        else:
            tags = []

        # Wutface fix
        if not tlp:
            tlp = 1
        if not severity:
            severity = 1

        if isinstance(tlp, str):
            if not tlp.isdigit():
                return "TLP needs to be a number from 0-3, not %s" % tlp

            tlp = int(tlp)
        if isinstance(severity, str):
            if not severity.isdigit():
                return "Severity needs to be a number from 1-3, not %s" % severity

            severity = int(severity)

        if tlp > 3 or tlp < 0:
            return "TLP needs to be a number from 0-3, not %d" % tlp
        if severity > 3 or severity < 1:
            return "Severity needs to be a number from 1-3, not %d" % severity

        alert = thehive4py.models.Alert(
            title=title,
            tlp=tlp,
            severity=severity,
            tags=tags,
            description=description,
            type=type,
            source=source,
            sourceRef=sourceref,
        )

        try:
            ret = self.thehive.create_alert(alert)
            return ret.text
        except requests.exceptions.ConnectionError as e:
            return "ConnectionError: %s" % e

    def create_alert_artifact(
        self,
        apikey,
        url,
        alert_id,
        dataType,
        data,
        message=None,
        tlp="2",
        ioc="False",
        sighted="False",
        ignoreSimilarity="False",
        tags=None
    ):
        self.thehive = TheHiveApi(url, apikey, cert=False, version=4)

        if tlp:
            tlp = int(tlp)
        else:
            tlp = 2

        ioc = ioc.lower().strip() == "true"
        sighted = sighted.lower().strip() == "true"
        ignoreSimilarity = ignoreSimilarity.lower().strip() == "true"

        if tags:
            tags = [x.strip() for x in tags.split(",")]
        else:
            tags = []



        alert_artifact = thehive4py.models.AlertArtifact(
            dataType=dataType,
            data=data,
            message=message,
            tlp=tlp,
            ioc=ioc,
            sighted=sighted,
            ignoreSimilarity=ignoreSimilarity,
            tags=tags
        )

        try:
            ret = self.thehive.create_alert_artifact(alert_id, alert_artifact)
        except requests.exceptions.ConnectionError as e:
            return "ConnectionError: %s" % e
        if ret.status_code > 299:
            raise ConnectionError(ret.text)

        return ret.text

    # Gets an item based on input. E.g. field_type = Alert
    def get_item(self, apikey, url, field_type, cur_id):
        self.thehive = TheHiveApi(url, apikey, cert=False)

        newstr = ""
        ret = ""
        if field_type.lower() == "alert":
            ret = self.thehive.get_alert(cur_id + "?similarity=1")
        elif field_type.lower() == "case":
            ret = self.thehive.get_case(cur_id)
        elif field_type.lower() == "case_observables":
            ret = self.thehive.get_case_observables(cur_id)
        elif field_type.lower() == "case_task":
            ret = self.thehive.get_case_task(cur_id)
        elif field_type.lower() == "case_tasks":
            ret = self.thehive.get_case_tasks(cur_id)
        elif field_type.lower() == "case_template":
            ret = self.thehive.get_case_tasks(cur_id)
        elif field_type.lower() == "linked_cases":
            ret = self.thehive.get_linked_cases(cur_id)
        elif field_type.lower() == "task_log":
            ret = self.thehive.get_task_log(cur_id)
        elif field_type.lower() == "task_logs":
            ret = self.thehive.get_task_logs(cur_id)
        else:
            return (
                "%s is not implemented. See https://github.com/frikky/shuffle-apps for more info."
                % field_type
            )

        return ret.text

    def close_alert(self, apikey, url, alert_id):
        self.thehive = TheHiveApi(url, apikey, cert=False)
        return self.thehive.mark_alert_as_read(alert_id).text

    def reopen_alert(self, apikey, url, alert_id):
        self.thehive = TheHiveApi(url, apikey, cert=False)
        return self.thehive.mark_alert_as_unread(alert_id).text

    def create_case_from_alert(self, apikey, url, alert_id, case_template=None):
        self.thehive = TheHiveApi(url, apikey, cert=False)
        response = self.thehive.promote_alert_to_case(
            alert_id=alert_id, case_template=case_template
        )
        return response.text

    def merge_alert_into_case(self, apikey, url, alert_id, case_id):
        self.thehive = TheHiveApi(url, apikey, cert=False)
        req = url + f"/api/alert/{alert_id}/merge/{case_id}"
        ret = requests.post(req, auth=self.thehive.auth)
        return ret.text

    # Not sure what the data should be
    def update_field(self, apikey, url, field_type, cur_id, field, data):
        # This is kinda silly but..
        if field_type.lower() == "alert":
            newdata = {}

            if data.startswith("%s"):
                ticket = self.thehive.get_alert(cur_id)
                if ticket.status_code != 200:
                    pass

                newdata[field] = "%s%s" % (ticket.json()[field], data[2:])
            else:
                newdata[field] = data

            # Bleh
            url = "%s/api/alert/%s" % (url, cur_id)
            if field == "status":
                if data == "New" or data == "Updated":
                    url = "%s/markAsUnread" % url
                elif data == "Ignored":
                    url = "%s/markAsRead" % url

                ret = requests.post(
                    url,
                    headers={
                        "Content-Type": "application/json",
                        "Authorization": "Bearer %s" % apikey,
                    },
                )
            else:
                ret = requests.patch(
                    url,
                    headers={
                        "Content-Type": "application/json",
                        "Authorization": "Bearer %s" % apikey,
                    },
                    json=newdata,
                )

            return str(ret.status_code)
        else:
            return (
                "%s is not implemented. See https://github.com/frikky/walkoff-integrations for more info."
                % field_type
            )

    # https://github.com/TheHive-Project/TheHiveDocs/tree/master/api/connectors/cortex
    def run_analyzer(self, apikey, url, cortex_id, analyzer_id, artifact_id):
        self.thehive = TheHiveApi(url, apikey, cert=False)
        return self.thehive.run_analyzer(cortex_id, artifact_id, analyzer_id).text

    # Creates a task log in TheHive with file
    def create_task_log(self, apikey, url, task_id, message, filedata={}):
        if filedata["success"] == False:
            return "No file to upload. Skipping message."

        headers = {
            "Authorization": "Bearer %s" % apikey,
        }

        files = {}
        if len(filedata["data"]) > 0:
            files = {
                "attachment": (filedata["filename"], filedata["data"]),
            }

        data = {"_json": """{"message": "%s"}""" % message}
        response = requests.post(
            "%s/api/case/task/%s/log" % (url, task_id),
            headers=headers,
            files=files,
            data=data,
        )
        return response.text

    # Creates an observable as a file in a case
    def create_case_file_observable(self, apikey, url, case_id, tags, filedata):
        if filedata["success"] == False:
            return "No file to upload. Skipping message."

        headers = {
            "Authorization": "Bearer %s" % apikey,
        }

        if tags:
            if ", " in tags:
                tags = tags.split(", ")
            elif "," in tags:
                tags = tags.split(",")
            else:
                tags = [tags]

        files = {}
        if len(filedata["data"]) > 0:
            files = {
                "attachment": (filedata["filename"], filedata["data"]),
            }

        outerarray = {"dataType": "file", "tags": tags}
        data = {"_json": """%s""" % json.dumps(outerarray)}
        response = requests.post(
            "%s/api/case/%s/artifact" % (url, case_id),
            headers=headers,
            files=files,
            data=data,
        )
        return response.text


if __name__ == "__main__":
    TheHive.run()
