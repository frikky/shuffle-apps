#!/usr/bin/env python
# -*- coding: utf-8 -*-
import asyncio
import json
import random
import time

import requests
import thehive4py.models
from thehive4py.api import TheHiveApi
from thehive4py.models import *
from thehive4py.query import *
from walkoff_app_sdk.app_base import AppBase


class TheHive(AppBase):
    """
    An example of a Walkoff App.
    Inherit from the AppBase class to have Redis, logging, and console logging set up behind the scenes.
    """

    __version__ = "1.1.0"
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

    def __connect_thehive(self, url, apikey, organisation):
        if organisation:
            self.thehive = TheHiveApi(
                url, apikey, cert=False, organisation=organisation
            )
        else:
            self.thehive = TheHiveApi(url, apikey, cert=False)

    def search_case_title(self, apikey, url, organisation, title_query):
        self.__connect_thehive(url, apikey, organisation)

        response = self.thehive.find_cases(
            query=ContainsString("title", title_query), range="all", sort=[]
        )

        return response.text

    def custom_search(
        self, apikey, url, organisation, search_for, custom_query, range="all"
    ):
        self.__connect_thehive(url, apikey, organisation)

        try:
            custom_query = json.loads(custom_query)
        except:
            # raise IOError("Invalid JSON payload received.")
            pass

        if search_for == "alert":
            response = self.thehive.find_alerts(
                query=custom_query, range="all", sort=[]
            )
        else:
            response = self.thehive.find_cases(query=custom_query, range="all", sort=[])

        if (
            response.status_code == 200
            or response.status_code == 201
            or response.status_code == 202
        ):
            return response.text
        else:
            raise IOError(response.text)

    def add_case_artifact(
        self, apikey, url, organisation, case_id, data, datatype, tags
    ):
        self.__connect_thehive(url, apikey, organisation)

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
            tags=tags,
            message="Created by shuffle",
        )

        return self.thehive.create_case_observable(id, item).text

    def search_alert_title(
        self, apikey, url, organisation, title_query, search_range="0-25"
    ):
        self.__connect_thehive(url, apikey, organisation)

        # Could be "all" too
        if search_range == "":
            search_range = "0-25"

        response = self.thehive.find_alerts(
            query=ContainsString("title", title_query), range=search_range, sort=[]
        )

        return response.text

    def create_case(
        self,
        apikey,
        url,
        organisation,
        template,
        title,
        description="",
        tlp=1,
        severity=1,
        tags="",
    ):
        self.__connect_thehive(url, apikey, organisation)
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

        Casetemplate = template if template else None

        case = thehive4py.models.Case(
            title=title,
            tlp=tlp,
            severity=severity,
            tags=tags,
            description=description,
            template=Casetemplate,
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
        organisation,
        type,
        source,
        sourceref,
        title,
        description="",
        tlp=1,
        severity=1,
        tags="",
        artifacts="",
    ):
        self.__connect_thehive(url, apikey, organisation)
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

        all_artifacts = []
        if artifacts != "":
            # print("ARTIFACTS: %s" % artifacts)
            if isinstance(artifacts, str):
                # print("ITS A STRING!")
                try:
                    artifacts = json.loads(artifacts)
                except:
                    print("[ERROR] Error in parsing artifacts!")

            # print("ART HERE: %s" % artifacts)
            # print("ART: %s" % type(artifacts))
            if isinstance(artifacts, list):
                print("ITS A LIST!")
                for item in artifacts:
                    print("ITEM: %s" % item)
                    try:
                        artifact = thehive4py.models.AlertArtifact(
                            dataType=item["data_type"],
                            data=item["data"],
                        )

                        try:
                            artifact["message"] = item["message"]
                        except:
                            pass

                        if item["data_type"] == "ip":
                            try:
                                if item["is_private_ip"]:
                                    message += " IP is private."
                            except:
                                pass

                        all_artifacts.append(artifact)
                    except KeyError as e:
                        print("Error in artifacts: %s" % e)

        alert = thehive4py.models.Alert(
            title=title,
            tlp=tlp,
            severity=severity,
            tags=tags,
            description=description,
            type=type,
            source=source,
            sourceRef=sourceref,
            artifacts=all_artifacts,
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
        organisation,
        alert_id,
        dataType,
        data,
        message=None,
        tlp="2",
        ioc="False",
        sighted="False",
        ignoreSimilarity="False",
        tags=None,
    ):
        self.__connect_thehive(url, apikey, organisation, version=4)

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
            tags=tags,
        )

        try:
            ret = self.thehive.create_alert_artifact(alert_id, alert_artifact)
        except requests.exceptions.ConnectionError as e:
            return "ConnectionError: %s" % e
        if ret.status_code > 299:
            raise ConnectionError(ret.text)

        return ret.text

    # Gets an item based on input. E.g. field_type = Alert
    def get_item(self, apikey, url, organisation, field_type, cur_id):
        self.__connect_thehive(url, apikey, organisation)

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

    def close_alert(self, apikey, url, organisation, alert_id):
        self.__connect_thehive(url, apikey, organisation)
        return self.thehive.mark_alert_as_read(alert_id).text

    def reopen_alert(self, apikey, url, organisation, alert_id):
        self.__connect_thehive(url, apikey, organisation)
        return self.thehive.mark_alert_as_unread(alert_id).text

    def create_case_from_alert(
        self, apikey, url, organisation, alert_id, case_template=None
    ):
        self.__connect_thehive(url, apikey, organisation)
        response = self.thehive.promote_alert_to_case(
            alert_id=alert_id, case_template=case_template
        )
        return response.text

    def merge_alert_into_case(self, apikey, url, organisation, alert_id, case_id):
        self.__connect_thehive(url, apikey, organisation)
        req = url + f"/api/alert/{alert_id}/merge/{case_id}"
        ret = requests.post(req, auth=self.thehive.auth)
        return ret.text

    # Not sure what the data should be
    def update_field(
        self, apikey, url, organisation, field_type, cur_id, field, data
    ):
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
    def delete_alert_artifact(self, apikey, url, organisation, artifact_id):
        self.__connect_thehive(url, apikey, organisation, version=4)
        return self.thehive.delete_alert_artifact(artifact_id).text

    # https://github.com/TheHive-Project/TheHiveDocs/tree/master/api/connectors/cortex
    def run_analyzer(
        self, apikey, url, organisation, cortex_id, analyzer_id, artifact_id
    ):
        self.__connect_thehive(url, apikey, organisation)
        return self.thehive.run_analyzer(cortex_id, artifact_id, analyzer_id).text

    # Creates a task log in TheHive with file
    def create_task_log(
        self, apikey, url, organisation, task_id, message, filedata={}
    ):
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
    def create_case_file_observable(
        self, apikey, url, organisation, case_id, tags, filedata
    ):
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
            verify=False,
        )
        return response.text

    # Get all artifacts of a given case
    def get_case_artifacts(
        self,
        apikey,
        url,
        organisation,
        case_id,
        dataType,
    ):
        self.__connect_thehive(url, apikey, organisation)

        query = And(Eq("dataType", dataType)) if dataType else {}

        # Call the API
        response = self.thehive.get_case_observables(
            case_id, query=query, sort=["-startDate", "+ioc"], range="all"
        )

        # Display the result
        if response.status_code == 200:
            # Get response data
            list = response.json()

            # Display response data
            return (
                json.dumps(list, indent=4, sort_keys=True)
                if list
                else json.dumps(
                    {"status": 200, "message": "No observable results"},
                    indent=4,
                    sort_keys=True,
                )
            )
        else:
            return f"Failure: {response.status_code}/{response.text}"

    # Update TheHive Case
    def update_case(
        self,
        apikey,
        url,
        organisation,
        cur_id,
        title="",
        description="",
        severity=None,
        owner="",
        flag=None,
        tlp=None,
        pap=None,
        tags="",
        status="",
        resolution_status="",
        impact_status="",
        summary="",
        custom_fields=None,
        custom_json=None,
    ):
        self.__connect_thehive(url, apikey, organisation)

        # Get current case data and update fields if new data exists
        case = self.thehive.get_case(cur_id).json()
        case_title = title if title else case["title"]
        case_description = description if description else case["description"]
        case_severity = int(severity) if severity else case["severity"]
        case_owner = owner if owner else case["owner"]
        case_flag = (
            (False if flag.lower() == "false" else True) if flag else case["flag"]
        )
        case_tlp = int(tlp) if tlp else case["tlp"]
        case_pap = int(pap) if pap else case["pap"]
        case_tags = tags.split(",") if tags else case["tags"]
        case_status = status if status else case["status"]
        case_resolutionStatus = (
            resolution_status if resolution_status else case["resolutionStatus"]
        )
        case_impactStatus = impact_status if impact_status else case["impactStatus"]
        case_summary = summary if summary else case["summary"]
        case_customFields = case["customFields"]

        # Prepare the customfields
        customfields = CustomFieldHelper()
        if case_customFields:
            for key, value in case_customFields.items():
                if list(value)[0] == "integer":
                    customfields.add_integer(key, list(value.items())[0][1])
                elif list(value)[0] == "string":
                    customfields.add_string(key, list(value.items())[0][1])
                elif list(value)[0] == "boolean":
                    customfields.add_boolean(key, list(value.items())[0][1])
                elif list(value)[0] == "float":
                    customfields.add_float(key, list(value.items())[0][1])
                else:
                    print(
                        f'The value type "{value}" of the field {key} is not suported by the function.'
                    )

        custom_fields = json.loads(custom_fields) if custom_fields else {}
        for key, value in custom_fields.items():
            if type(value) == int:
                customfields.add_integer(key, value)
            elif type(value) == str:
                customfields.add_string(key, value)
            elif type(value) == bool:
                customfields.add_boolean(key, value)
            elif type(value) == float:
                customfields.add_float(key, value)
            else:
                print(
                    f'The value type "{value}" of the field {key} is not suported by the function.'
                )

        customfields = customfields.build()

        custom_json = json.loads(custom_json) if custom_json else {}

        # Prepare the fields to be updated
        case = Case(
            id=cur_id,
            title=case_title,
            description=case_description,
            severity=case_severity,
            owner=case_owner,
            flag=case_flag,
            tlp=case_tlp,
            pap=case_pap,
            tags=case_tags,
            status=case_status,
            resolutionStatus=case_resolutionStatus,
            impactStatus=case_impactStatus,
            summary=case_summary,
            customFields=customfields,
            json=custom_json,
        )

        result = self.thehive.update_case(
            case,
            fields=[
                "title",
                "description",
                "severity",
                "owner",
                "flag",
                "tlp",
                "pap",
                "tags",
                "status",
                "resolutionStatus",
                "impactStatus",
                "summary",
                "customFields",
            ],
        )

        return json.dumps(result.json(), indent=4, sort_keys=True)

    # Get TheHive Organisations
    def get_organisations(
        self,
        apikey,
        url,
        organisation,
    ):
        headers = {
            "Authorization": f"Bearer {apikey}",
            "Content-Type": "application/json",
        }

        response = requests.get(
            f"{url}/api/organisation",
            headers=headers,
            verify=False,
        )

        return response.text

    # Create TheHive Organisation
    def create_organisation(
        self,
        apikey,
        url,
        organisation,
        name,
        description,
    ):
        headers = {
            "Authorization": f"Bearer {apikey}",
            "Content-Type": "application/json",
        }

        data = {"name": f"{name}", "description": f"{description}"}

        response = requests.post(
            f"{url}/api/organisation",
            headers=headers,
            json=data,
            verify=False,
        )

        return response.text

    # Create User in TheHive
    def create_user(
        self,
        apikey,
        url,
        organisation,
        login,
        name,
        profile,
    ):
        headers = {
            "Authorization": f"Bearer {apikey}",
            "Content-Type": "application/json",
        }

        data = {
            "login": f"{login}",
            "name": f"{name}",
            "profile": f"{profile}",
            "organisation": f"{organisation}",
        }

        response = requests.post(
            f"{url}/api/v1/user",
            headers=headers,
            json=data,
            verify=False,
        )

        return response.text


if __name__ == "__main__":
    TheHive.run()
