import asyncio
import json
import random
import socket
import time

import requests
from walkoff_app_sdk.app_base import AppBase

class Intune(AppBase):
    __version__ = "1.0.0"
    app_name = "intune"  # this needs to match "name" in api.yaml

    def __init__(self, redis, logger, console_logger=None):
        """
        Each app should have this __init__ to set up Redis and logging.
        :param redis:
        :param logger:
        :param console_logger:
        """
        super().__init__(redis, logger, console_logger)

    def authenticate(self, tenant_id, client_id, client_secret, graph_url):
        s = requests.Session()
        auth_url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token"
        auth_data = {
            "grant_type": "client_credentials",
            "client_id": client_id,
            "client_secret": client_secret,
            "scope": f"{graph_url}/.default",
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
        return s

    def list_devices(self, tenant_id, client_id, client_secret):
        graph_url="https://graph.microsoft.com"
        session = self.authenticate(tenant_id, client_id, client_secret, graph_url)
        graph_url = "https://graph.microsoft.com/v1.0/devices/"
        ret = session.get(graph_url)
        return ret.text

    def list_apps(self, tenant_id, client_id, client_secret):
        graph_url="https://graph.microsoft.com"
        session = self.authenticate(tenant_id, client_id, client_secret, graph_url)
        graph_url = "https://graph.microsoft.com/v1.0/deviceManagement/detectedApps"
        ret = session.get(graph_url)
        return ret.text

    def managed_device_overview(self, tenant_id, client_id, client_secret):
        graph_url="https://graph.microsoft.com"
        session = self.authenticate(tenant_id, client_id, client_secret, graph_url)
        graph_url = "https://graph.microsoft.com/v1.0/deviceManagement/managedDeviceOverview"
        ret = session.get(graph_url)
        return ret.text

    def managed_device(self, tenant_id, client_id, client_secret):
        graph_url="https://graph.microsoft.com"
        session = self.authenticate(tenant_id, client_id, client_secret, graph_url)
        graph_url = "https://graph.microsoft.com/v1.0/deviceManagement/managedDevices"
        ret = session.get(graph_url)
        return ret.text

    def get_managed_device(self, tenant_id, client_id, client_secret, managedDeviceId):
        graph_url="https://graph.microsoft.com"
        session = self.authenticate(tenant_id, client_id, client_secret, graph_url)
        graph_url=f"https://graph.microsoft.com/v1.0/managedDevices/{managedDeviceId}"
        ret = session.get(graph_url)
        return ret.text

    def delete_managed_device(self, tenant_id, client_id, client_secret, managedDeviceId):
        graph_url="https://graph.microsoft.com"
        session = self.authenticate(tenant_id, client_id, client_secret, graph_url)
        graph_url=f"https://graph.microsoft.com/v1.0/managedDevices/{managedDeviceId}"
        ret = session.delete(graph_url)
        return ret.text

    def remotelock(self, tenant_id, client_id, client_secret, managedDeviceId):
        graph_url="https://graph.microsoft.com"
        session = self.authenticate(tenant_id, client_id, client_secret, graph_url)
        graph_url=f"https://graph.microsoft.com/v1.0/managedDevices/{managedDeviceId}/remoteLock"
        ret = session.post(graph_url)
        return ret.text

    def shutdown(self, tenant_id, client_id, client_secret, managedDeviceId):
        graph_url="https://graph.microsoft.com"
        session = self.authenticate(tenant_id, client_id, client_secret, graph_url)
        graph_url=f"https://graph.microsoft.com/v1.0/managedDevices/{managedDeviceId}/shutDown"
        ret = session.post(graph_url)
        return ret.text

    def list_managedAppConfigurations(self, tenant_id, client_id, client_secret):
        graph_url="https://graph.microsoft.com"
        session = self.authenticate(tenant_id, client_id, client_secret, graph_url)
        graph_url=f"https://graph.microsoft.com/v1.0/deviceAppManagement/managedAppPolicies"
        ret = session.post(graph_url)
        return ret.text

if __name__ == "__main__":
    Intune.run()
