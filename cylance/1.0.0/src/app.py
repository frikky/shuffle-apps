import asyncio
import json
import random
import socket
import time
import uuid
from datetime import datetime
from datetime import timedelta

import jwt
import requests
from walkoff_app_sdk.app_base import AppBase

class Cylance(AppBase):
    __version__ = "1.0.0"
    app_name = "Cylance"


    def __init__(self, redis, logger, console_logger=None):
        """
        Each app should have this __init__ to set up Redis and logging.
        :param redis:
        :param logger:
        :param console_logger:
        """
        super().__init__(redis, logger, console_logger)

    # This system is fucking stupid - every developer ever :)
    def auth(self, app_id, app_secret, tid_val):
        timeout = 1800
        now = datetime.utcnow()
        timeout_datetime = now + timedelta(seconds=timeout)
        epoch_time = int((now - datetime(1970, 1, 1)).total_seconds())
        epoch_timeout = int((timeout_datetime - datetime(1970, 1, 1)).total_seconds())
        jti_val = str(uuid.uuid4())
        AUTH_URL = "https://protectapi.cylance.com/auth/v2/token"
        claims = {
            "exp": epoch_timeout,
            "iat": epoch_time,
            "iss": "http://cylance.com",
            "sub": app_id,
            "tid": tid_val,
            "jti": jti_val,
            #"scp": ["policy:create","policy:list","policy:read","policy:update"]
        }

        encoded = jwt.encode(claims, app_secret, algorithm='HS256').decode('utf-8')
        payload = {"auth_token": encoded}
        headers = {"Content-Type": "application/json; charset=utf-8"}
        resp = requests.post(AUTH_URL, headers=headers, data=json.dumps(payload))
        auth_token = resp.json()["access_token"]
        return auth_token

    def get_threat(self, app_id, app_secret, tenant_id, threat_id):
        auth_token = self.auth(app_id, app_secret, tenant_id)
        url = f"https://protectapi.cylance.com/threats/v2/{threat_id}"
        params = {}

        headers = {
            "Authorization": f"Bearer {auth_token}"
        }

        resp = requests.get(url, headers=headers, params=params)
        return resp.text

    def get_detection(self, app_id, app_secret, tenant_id, detection_id):
        auth_token = self.auth(app_id, app_secret, tenant_id)
        url = f"https://protectapi.cylance.com/detections/v2/{detection_id}"
        params = {}

        headers = {
            "Authorization": f"Bearer {auth_token}"
        }

        resp = requests.get(url, headers=headers, params=params)
        return resp.text

    def list_threats(self, app_id, app_secret, tenant_id, page=1, page_size=20):
        auth_token = self.auth(app_id, app_secret, tenant_id)

        if page == 0 or page == "":
            page = 1
        if page_size == 0 or page_size == "":
            page_size = 20

        url = "https://protectapi.cylance.com/threats/v2"
        params = {
            "page": page,
            "page_size": page_size,
        }
        params = {}

        headers = {
            "Authorization": f"Bearer {auth_token}"
        }

        resp = requests.get(url, headers=headers, params=params)
        return resp.text

    def list_detections(self, app_id, app_secret, tenant_id, page=1, page_size=20):
        auth_token = self.auth(app_id, app_secret, tenant_id)

        if page == 0 or page == "":
            page = 1
        if page_size == 0 or page_size == "":
            page_size = 20

        url = "https://protectapi.cylance.com/detections/v2"
        params = {
            "page": page,
            "page_size": page_size,
        }
        params = {}

        headers = {
            "Authorization": f"Bearer {auth_token}"
        }

        resp = requests.get(url, headers=headers, params=params)
        return resp.text
        print(resp.text)
        print(resp.status_code)

    def get_global_list(self, app_id, app_secret, tenant_id, list_type="GlobalSafe", page=1):
        auth_token = self.auth(app_id, app_secret, tenant_id)


        if list_type == "GlobalQuarantine":
            list_type = 0
        else:
            list_type = 1

        page_size = 50

        url = "https://protectapi.cylance.com/globallists/v2"
        params = {
            "listTypeId": list_type,
            "page-m": page,
            "page_size": page_size,
        }

        headers = {
            "Authorization": f"Bearer {auth_token}"
        }

        resp = requests.get(url, headers=headers, params=params)
        return resp.text

    def add_to_global_list(self, app_id, app_secret, tenant_id, list_type, sha256):
        auth_token = self.auth(app_id, app_secret, tenant_id)

        data = {
            "sha256": sha256,
            "list_type": list_type,
            "category": "CommercialSoftware",
            "reason": "test",
        }

        #?listTypeId={0|1}&page-m&page_size=n"
        url = "https://protectapi.cylance.com/globallists/v2"
        headers = {
            "Authorization": f"Bearer {auth_token}"
        }

        resp = requests.post(url, headers=headers, json=data)
        return resp.text

    def delete_from_global_list(self, app_id, app_secret, tenant_id, list_type, sha256):
        auth_token = self.auth(app_id, app_secret, tenant_id)

        data = {
            "sha256": sha256,
            "list_type": list_type,
        }

        url = "https://protectapi.cylance.com/globallists/v2"
        headers = {
            "Authorization": f"Bearer {auth_token}"
        }

        resp = requests.delete(url, headers=headers, json=data)
        return resp.text

    def get_searches(self, app_id, app_secret, tenant_id, page=1):
        auth_token = self.auth(app_id, app_secret, tenant_id)

        page_size = 50

        params = {
            "page-m": page,
            "page_size": page_size,
        }

        url = "https://protectapi.cylance.com/instaqueries/v2"
        headers = {
            "Authorization": f"Bearer {auth_token}"
        }

        resp = requests.get(url, headers=headers, params=params)
        return resp.text

    def create_search(self, app_id, app_secret, tenant_id, search):
        auth_token = self.auth(app_id, app_secret, tenant_id)

        data = search
        url = "https://protectapi.cylance.com/instaqueries/v2"
        headers = {
            "Authorization": f"Bearer {auth_token}"
        }

        resp = requests.post(url, headers=headers, json=data)
        return resp.text

    def get_search_results(self, app_id, app_secret, tenant_id, search_id):
        auth_token = self.auth(app_id, app_secret, tenant_id)

        page_size = 50

        params = {
            "page-m": page,
            "page_size": page_size,
        }

        url = "https://protectapi.cylance.com/instaqueries/v2/%s/results" % search_id
        headers = {
            "Authorization": f"Bearer {auth_token}"
        }

        resp = requests.get(url, headers=headers, params=params)
        return resp.text


if __name__ == "__main__":
    Cylance.run()
