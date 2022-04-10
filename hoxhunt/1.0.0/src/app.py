import asyncio
import json
import random
import socket
import time

import requests
from walkoff_app_sdk.app_base import AppBase

class Hoxhunt(AppBase):
    __version__ = "1.0.0"
    app_name = "hoxhunt"

    def __init__(self, redis, logger, console_logger=None):
        """
        Each app should have this __init__ to set up Redis and logging.
        :param redis:
        :param logger:
        :param console_logger:
        """
        super().__init__(redis, logger, console_logger)

    def get_incident(self, apikey, organization_id, incident_id):
        url = "https://app.hoxhunt.com/graphql"
        headers = {
            "authorization": apikey,
            "content-type":  "application/json",
        }

        data = {
            "operationName":"IncidentDetailsContainerQuery",
            "variables": {"incidentId": incident_id,"organizationId": organization_id},
            "query": "query IncidentDetailsContainerQuery($incidentId: ID!, $organizationId: ID, $createdBefore: Date) {\n  incidents(filter: {_id_eq: $incidentId, organizationId_eq: $organizationId}) {\n    _id\n    organizationId\n    createdAt\n    policyName\n    state\n    threatCount\n    threats(sort: createdAt_DESC, first: 50, filter: {createdAt_lte: $createdBefore}) {\n      _id\n      createdAt\n      email {\n        subject\n        from {\n          address\n          __typename\n        }\n        __typename\n      }\n      reporterUser {\n        _id\n        emails {\n          address\n          __typename\n        }\n        __typename\n      }\n      userModifiers {\n        userActedOnThreat\n        repliedToEmail\n        downloadedFile\n        openedAttachment\n        visitedLink\n        enteredCredentials\n        other\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n"
        }

        return requests.post(url, headers=headers, json=data)

    def change_incident_status(self, apikey, organization_id, incident_id, state):
        url = "https://app.hoxhunt.com/graphql"
        headers = {
            "authorization": apikey,
            "content-type":  "application/json",
        }

        data = {
            "operationName":"UpdateIncidentState",
            "variables":{"incidentId": incident_id,"organizationId": organization_id,"state": state},
            "query":"mutation UpdateIncidentState($incidentId: ID!, $organizationId: ID!, $state: IncidentState!) {\n  updateIncidentState(incidentId: $incidentId, organizationId: $organizationId, state: $state) {\n    _id\n    state\n    __typename\n  }\n}\n"
        }

        return requests.post(url, headers=headers, json=data)

    def list_incidents(self, apikey, organization_id, state="OPEN", limit=50):
        url = "https://app.hoxhunt.com/graphql"
        headers = {
            "authorization": apikey,
            "content-type":  "application/json",
        }

        data = {
            "operationName":"IncidentListQuery",
            "variables":{"first": limit, "state": state,"organizationId": organization_id, "sort":"lastReportedAt_DESC"},
            "query":"query IncidentListQuery($policyName: IncidentPolicy, $organizationId: ID, $state: IncidentState, $sort: [Incident_sort], $first: Int, $skip: Int) {\n  incidents(first: $first, skip: $skip, filter: {organizationId_eq: $organizationId, policyName_eq: $policyName, state_eq: $state}, sort: $sort) {\n    _id\n    createdAt\n    policyName\n    state\n    threatCount\n    threats(first: 1) {\n      _id\n      userModifiers {\n        repliedToEmail\n        downloadedFile\n        visitedLink\n        openedAttachment\n        enteredCredentials\n        other\n        __typename\n      }\n      email {\n        subject\n        from {\n          address\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n"
        }

        return requests.post(url, headers=headers, json=data)

    def list_threats(self, apikey, organization_id, state="OPEN", limit=50):
        url = "https://app.hoxhunt.com/graphql"
        headers = {
            "authorization": apikey,
            "content-type":  "application/json",
        }

        data = {
            "operationName":"IncidentListQuery",
            "variables":{"first": limit, "state": state,"organizationId": organization_id, "sort":"lastReportedAt_DESC"},
            "query":"query IncidentListQuery($policyName: IncidentPolicy, $organizationId: ID, $state: IncidentState, $sort: [Incident_sort], $first: Int, $skip: Int) {\n  incidents(first: $first, skip: $skip, filter: {organizationId_eq: $organizationId, policyName_eq: $policyName, state_eq: $state}, sort: $sort) {\n    _id\n    createdAt\n    policyName\n    state\n    threatCount\n    threats(first: 1) {\n      _id\n      userModifiers {\n        repliedToEmail\n        downloadedFile\n        visitedLink\n        openedAttachment\n        enteredCredentials\n        other\n        __typename\n      }\n      email {\n        subject\n        from {\n          address\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n"
        }

        return requests.post(url, headers=headers, json=data)

    # This one doesn't work currently.
    def get_threat(self, apikey, organization_id, id):
        url = "https://app.hoxhunt.com/graphql"
        headers = {
            "authorization": apikey,
            "content-type":  "application/json",
        }

        data = {
            "operationName":"ThreatWorkQueueQuery",
            "variables": {"id": id, "organizationId": organization_id},
            "query":"query ThreatWorkQueueQuery($first: Int, $threatId: ID, $searchText: String, $severity: ThreatSeverity, $campaignThreatId: ID, $organizationId: String, $direction: ThreatWorkQueueDirection) {\n  threats: threatsAround(filter: {severity_eq: $severity, organizationId_eq: $organizationId, AND: [{OR: [{email__subject_contains: $searchText}, {email__from__address_contains: $searchText}, {email__to__address_contains: $searchText}]}]}, sort: [createdAt_DESC], first: $first, threatId: $threatId, direction: $direction, campaignThreatId: $campaignThreatId) {\n    createdAt\n    _id\n    severity\n    feedbackSentAt\n    email {\n      subject\n      from {\n        name\n        address\n        __typename\n      }\n      __typename\n    }\n    organization {\n      _id\n      name\n      __typename\n    }\n    escalationEmail {\n      sendDate\n      __typename\n    }\n    reporterUser {\n      _id\n      profile {\n        firstName\n        lastName\n        __typename\n      }\n      emails {\n        address\n        __typename\n      }\n      player {\n        level {\n          current\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n"
        }

        return requests.post(url, headers=headers, json=data)

    def list_threats(self, apikey, incident_id, organization_id, limit=50):
        url = "https://app.hoxhunt.com/graphql"
        headers = {
            "authorization": apikey,
            "content-type":  "application/json",
        }

        data = {
            "operationName":"ThreatWorkQueueQuery",
            "variables": {"first": limit,"organizationId": organization_id},
            "query":"query ThreatWorkQueueQuery($first: Int, $threatId: ID, $searchText: String, $severity: ThreatSeverity, $campaignThreatId: ID, $organizationId: String, $direction: ThreatWorkQueueDirection) {\n  threats: threatsAround(filter: {severity_eq: $severity, organizationId_eq: $organizationId, AND: [{OR: [{email__subject_contains: $searchText}, {email__from__address_contains: $searchText}, {email__to__address_contains: $searchText}]}]}, sort: [createdAt_DESC], first: $first, threatId: $threatId, direction: $direction, campaignThreatId: $campaignThreatId) {\n    createdAt\n    _id\n    severity\n    feedbackSentAt\n    email {\n      subject\n      from {\n        name\n        address\n        __typename\n      }\n      __typename\n    }\n    organization {\n      _id\n      name\n      __typename\n    }\n    escalationEmail {\n      sendDate\n      __typename\n    }\n    reporterUser {\n      _id\n      profile {\n        firstName\n        lastName\n        __typename\n      }\n      emails {\n        address\n        __typename\n      }\n      player {\n        level {\n          current\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n"
        }

        return requests.post(url, headers=headers, json=data)


# Run the actual thing after we've checked params
def run(request):
    action = request.get_json()
    authorization_key = action.get("authorization")
    current_execution_id = action.get("execution_id")

    if action and "name" in action and "app_name" in action:
        Hoxhunt.run(action)
        return f'Attempting to execute function {action["name"]} in app {action["app_name"]}'
    else:
        return f'Invalid action'

if __name__ == "__main__":
    Hoxhunt.run()
