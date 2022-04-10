import asyncio
import json
import random
import socket
import time
import uuid

import requests
from walkoff_app_sdk.app_base import AppBase

# Antispam
# https://protection.office.com/threatpolicy
# https://protection.office.com/antispam
# https://docs.microsoft.com/en-us/microsoft-365/security/office-365-security/configure-the-connection-filter-policy?view=o365-worldwide

#create_url = "https://compliance.microsoft.com/api/ComplianceSearch"
#Request URL:
# https://docs.microsoft.com/en-us/information-protection/develop/overview
# https://docs.microsoft.com/en-us/graph/api/resources/ediscovery-ediscoveryapioverview?view=graph-rest-beta
# Microsoft Graph Security securityAction entity
# https://docs.microsoft.com/en-us/graph/api/resources/threatassessment-api-overview?view=graph-rest-1.0

# Permissions (Delegated): SecurityEvents, ThreatAssement, ThreatIndicators, Compliance
# !! Have a "report email" internally using office365 !!
# Microsoft Threat Protection
# https://security.microsoft.com/mtp/
# https://protection.office.com/api/AcceptedDomain

class Teams(AppBase):
    __version__ = "1.0.0"
    app_name = "Teams"

    def __init__(self, redis, logger, console_logger=None):
        """
        Each app should have this __init__ to set up Redis and logging.
        :param redis:
        :param logger:
        :param console_logger:
        """
        super().__init__(redis, logger, console_logger)
        self.graph_url = "https://graph.microsoft.com"

    def authenticate(self, tenant_id, client_id, client_secret):
        s = requests.Session()
        auth_url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token"
        auth_data = {
            "grant_type": "client_credentials",
            "client_id": client_id,
            "client_secret": client_secret,
            "scope": f"{self.graph_url}/.default",
        }
        auth_headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "cache-control": "no-cache",
        }

        print(f"Making request to: {auth_url}")
        res = s.post(auth_url, data=auth_data, headers=auth_headers)

        # Auth failed, raise exception with the response
        if res.status_code != 200:
            raise ConnectionError(res.text)

        access_token = res.json().get("access_token")
        s.headers = {"Authorization": f"Bearer {access_token}", "cache-control": "no-cache"}
        print(s)
        return s

        # ENABLE: https://protection.office.com/api/OrganizationCustomization/Enable?source=HostedContentFilterPolicy

    def list_teams(self, tenant_id, client_id, client_secret, user_id):
        session = self.authenticate(tenant_id, client_id, client_secret)
        graph_url = "%s/v1.0/users/%s/joinedTeams" % (self.graph_url, user_id)

        ret = session.get(graph_url)
        print(ret.status_code)
        print(ret.text)
        try:
            data = ret.json()
        except:
            data = ret.text

        if ret.status_code < 300:
            return {"success": True, "value": data}

        return {"success": False, "reason": "Bad status code %d - expecting 200." % ret.status_code, "graph_url": graph_url, "details": data}

    def list_members_in_team(self, tenant_id, client_id, client_secret, team_id):
        session = self.authenticate(tenant_id, client_id, client_secret)
        graph_url = "%s/v1.0/teams/%s/members" % (self.graph_url, team_id)

        ret = session.get(graph_url)
        print(ret.status_code)
        print(ret.text)
        try:
            data = ret.json()
        except:
            data = ret.text

        if ret.status_code < 300:
            return {"success": True, "value": data}

        return {"success": False, "reason": "Bad status code %d - expecting 200." % ret.status_code, "url": graph_url, "details": data}

    def list_channels_in_team(self, tenant_id, client_id, client_secret, team_id):
        session = self.authenticate(tenant_id, client_id, client_secret)
        graph_url = "%s/v1.0/teams/%s/channels" % (self.graph_url, team_id)

        ret = session.get(graph_url)
        print(ret.status_code)
        print(ret.text)
        try:
            data = ret.json()
        except:
            data = ret.text

        if ret.status_code < 300:
            return {"success": True, "value": data}

        return {"success": False, "reason": "Bad status code %d - expecting 200." % ret.status_code, "url": graph_url, "details": data}

    def add_user_to_channel(self, tenant_id, client_id, client_secret, team_id, channel_id, user_id, role):
        session = self.authenticate(tenant_id, client_id, client_secret)
        graph_url = "%s/v1.0/teams/%s/channels/%s/members" % (self.graph_url, team_id, channel_id)

        data = {
            "@odata.type": "#microsoft.graph.aadUserConversationMember",
            "roles": [role],
            "user@odata.bind": "https://graph.microsoft.com/v1.0/users('%s')" % user_id
        }

        ret = session.post(graph_url, json=data)
        try:
            data = ret.json()
        except:
            data = ret.text

        if ret.status_code < 300:
            return {"success": True, "value": data}

        return {"success": False, "reason": "Bad status code %d - expecting 200." % ret.status_code, "url": graph_url, "details": data}

    # Dosnt work: https://docs.microsoft.com/en-us/graph/api/chat-post-messages?view=graph-rest-beta&tabs=http
    def send_message_to_channel(self, tenant_id, client_id, client_secret, team_id, channel_id, user_id, message):
        session = self.authenticate(tenant_id, client_id, client_secret)
        graph_url = "%s/v1.0/teams/%s/channels/%s/messages" % (self.graph_url, team_id, channel_id)

        #"createdDateTime":"2021-02-04T19:58:15.511Z",
        data = {
           "from":{
              "user":{
                 "id":user_id,
                 "displayName":"Fredrik Sveum Ødegårdstuen",
                 "userIdentityType":"aadUser"
              }
           },
           "body":{
              "contentType":"html",
              "content": message,
           }
        }

        ret = session.post(graph_url, json=data)
        try:
            data = ret.json()
        except:
            data = ret.text

        if ret.status_code < 300:
            return {"success": True, "value": data}

        return {"success": False, "reason": "Bad status code %d - expecting 200." % ret.status_code, "url": graph_url, "details": data}

    def create_channel_in_team(self, tenant_id, client_id, client_secret, team_id, name, description):
        session = self.authenticate(tenant_id, client_id, client_secret)
        graph_url = "%s/v1.0/teams/%s/channels" % (self.graph_url, team_id)

        data = {
            "displayName": name,
            "description": description,
            "membershipType": "standard"
        }

        ret = session.post(graph_url, json=data)
        try:
            data = ret.json()
        except:
            data = ret.text

        if ret.status_code < 300:
            return {"success": True, "value": data}

        return {"success": False, "reason": "Bad status code %d - expecting 200." % ret.status_code, "url": graph_url, "details": data}

    def delete_channel(self, tenant_id, client_id, client_secret, team_id, channel_id):
        session = self.authenticate(tenant_id, client_id, client_secret)
        graph_url = "%s/v1.0/teams/%s/channels/%s" % (self.graph_url, team_id, channel_id)
        ret = session.delete(graph_url)
        try:
            data = ret.json()
        except:
            data = ret.text

        if ret.status_code < 300:
            return {"success": True, "value": data}

        return {"success": False, "reason": "Bad status code %d - expecting 200." % ret.status_code, "url": graph_url, "details": data}

    def list_apps_in_team(self, tenant_id, client_id, client_secret, team_id):
        session = self.authenticate(tenant_id, client_id, client_secret)
        graph_url = "%s/v1.0/teams/%s/installedApps" % (self.graph_url, team_id)
        ret = session.get(graph_url)
        try:
            data = ret.json()
        except:
            data = ret.text

        if ret.status_code < 300:
            return {"success": True, "value": data}

        return {"success": False, "reason": "Bad status code %d - expecting 200." % ret.status_code, "url": graph_url, "details": data}

    def get_app_in_team(self, tenant_id, client_id, client_secret, team_id, app_id):
        session = self.authenticate(tenant_id, client_id, client_secret)
        graph_url = "%s/v1.0/teams/%s/installedApps/%s" % (self.graph_url, team_id, app_id)
        ret = session.get(graph_url)
        try:
            data = ret.json()
        except:
            data = ret.text

        if ret.status_code < 300:
            return {"success": True, "value": data}

        return {"success": False, "reason": "Bad status code %d - expecting 200." % ret.status_code, "url": graph_url, "details": data}

    #{
    #    "id": "aa39b2f8-3c8d-4ce1-8b8b-7fe02c59ae3e",
    #    "externalId": null,
    #    "displayName": "Outgoing Webhook",
    #    "distributionMethod": "store"
    #},
    def add_webhook_to_team(self, tenant_id, client_id, client_secret, team_id):
        session = self.authenticate(tenant_id, client_id, client_secret)
        #graph_url = "%s/v1.0/teams/%s/installedApps" % (self.graph_url, team_id)
        graph_url = "%s/v1.0/chats/%s/installedApps" % (self.graph_url, team_id)
	#POST https://graph.microsoft.com/v1.0/chats/19:ea28e88c00e94c7786b065394a61f296@thread.v2/installedApps


        data = {
            "teamsApp@odata.bind": "https://graph.microsoft.com/beta/appCatalogs/teamsApps/aa39b2f8-3c8d-4ce1-8b8b-7fe02c59ae3e"
        }

        ret = session.post(graph_url, json=data)
        try:
            data = ret.json()
        except:
            data = ret.text

        if ret.status_code < 300:
            return {"success": True, "value": data}

        return {"success": False, "reason": "Bad status code %d - expecting 200." % ret.status_code, "url": graph_url, "details": data}

        #POST /teams/87654321-0abc-zqf0-321456789q/installedApps
        #Content-type: application/json

        #{
        #       "teamsApp@odata.bind":"https://graph.microsoft.com/beta/appCatalogs/teamsApps/12345678-9abc-def0-123456789a"
        #}


if __name__ == "__main__":
    Teams.run()
