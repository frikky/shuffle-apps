import asyncio
import json

import requests
from walkoff_app_sdk.app_base import AppBase


class VulnDB(AppBase):
    __version__ = "1.0.0"
    app_name = "VulnDB"  # this needs to match "name" in api.yaml
    SITE_URL = "https://vulndb.cyberriskanalytics.com"
    TOKEN_URL = SITE_URL + "/oauth/token"
    API_URL = SITE_URL + "/api/v1"

    def __init__(self, redis, logger, console_logger=None):
        """
        Each app should have this __init__ to set up Redis and logging.
        :param redis:
        :param logger:
        :param console_logger:
        """
        super().__init__(redis, logger, console_logger)
        self.headers = ""

    def get_auth_headers(self, ClientID, ClientSecret):
        authentication_data = {
            'grant_type': 'client_credentials',
            'client_id': ClientID,
            'client_secret': ClientSecret
            }

        access_token_response = requests.post(self.TOKEN_URL,
                                              data=authentication_data)

        if access_token_response.status_code != 200:
            raise Exception('VulnDB authentication error: HTTP status code ' +
                            '{}'.format(access_token_response.status_code))
        token = access_token_response.json()['access_token']
        self.headers = {'Content-Type': 'application/json',
                        'Authorization': f'Bearer {token}'}

    def latest_20_vulns(self, ClientID, ClientSecret):
        if self.headers == "":
            self.get_auth_headers(ClientID, ClientSecret)

        url = self.API_URL + "/vulnerabilities"
        response = requests.get(url, headers=self.headers)
        if response.status_code != 200:
            raise Exception('VulnDB latest_20_vulns error: HTTP ' +
                            '{}'.format(response.status_code) +
                            ' {}'.format(response.reason) +
                            ' {} '.format(url))

        vulnerabilities = response.json()['results']

        return vulnerabilities


if __name__ == "__main__":
    VulnDB.run()
