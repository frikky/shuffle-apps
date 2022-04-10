import asyncio
import datetime
import json
import random
import socket
import time

import boto3
import botocore
from botocore.config import Config
from walkoff_app_sdk.app_base import AppBase

def datetime_handler(x):
    """ This function is used make datetime object json serilizable,
    removing this function can cause error in some actions """

    if isinstance(x, datetime.datetime):
        return x.isoformat()
    raise TypeError("Unknown type")

class AWSIAM(AppBase):
    __version__ = "1.0.0"
    app_name = "AWS IAM"

    def __init__(self, redis, logger, console_logger=None):
        """
        Each app should have this __init__ to set up Redis and logging.
        :param redis:
        :param logger:
        :param console_logger:
        """
        super().__init__(redis, logger, console_logger)

    def auth_iam(self, access_key, secret_key, region):
        my_config = Config(
            region_name = region,
            signature_version = 'v4',
            retries = {
                'max_attempts': 10,
                'mode': 'standard'
            },
        )

        self.iam = boto3.resource(
            'iam',
            config=my_config,
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
        )

        return self.iam

    def change_password(self, access_key, secret_key, region, username, password):
        self.iam = self.auth_iam(access_key, secret_key, region)
        client = self.iam.meta.client

        try:
            return client.update_login_profile(UserName=username, Password=password, PasswordResetRequired=True)
        except botocore.exceptions.ClientError as e:
            print("Error: %s" % e)
            return "%s" % e

    def attach_user_policy(self, access_key, secret_key, region, username, policy_arn):
        self.iam = self.auth_iam(access_key, secret_key, region)
        client = self.iam.meta.client

        try:
            response = client.attach_user_policy(
                PolicyArn=str(policy_arn),
                UserName= str(username),
            )
            return json.dumps(response)
        except botocore.exceptions.ClientError as e:
            print(f"Error: {e}")
            return f'{e}'

    def list_access_keys(self, access_key, secret_key, region, username, marker, max_items):
        self.iam = self.auth_iam(access_key, secret_key, region)
        client = self.iam.meta.client

        try:
            response = client.list_access_keys(
                UserName= str(username)
                )
            if marker:
                response = client.list_access_keys(
                UserName= str(username),
                Marker = str(marker)
                )
            if max_items:
                response = client.list_access_keys(
                UserName= str(username),
                MaxItems = int(max_items)
                )
            if marker and max_items:
                response = client.list_access_keys(
                UserName= str(username),
                MaxItems = int(max_items),
                Marker = str(marker)
                )
            return json.dumps(response, default=datetime_handler)
        except botocore.exceptions.ClientError as e:
            return f'{e}'

    def list_ssh_public_keys(self, access_key, secret_key, region, username, marker, max_items):
        self.iam = self.auth_iam(access_key, secret_key, region)
        client = self.iam.meta.client

        try:
            response = client.list_ssh_public_keys(
                UserName= str(username)
                )
            if marker:
                response = client.list_ssh_public_keys(
                UserName= str(username),
                Marker = str(marker)
                )
            if max_items:
                response = client.list_ssh_public_keys(
                UserName= str(username),
                MaxItems = int(max_items)
                )
            if marker and max_items:
                response = client.list_ssh_public_keys(
                UserName= str(username),
                MaxItems = int(max_items),
                Marker = str(marker)
                )

            return json.dumps(response, default=datetime_handler)
        except botocore.exceptions.ClientError as e:
            return f'{e}'

    def get_instance_profile(self, access_key, secret_key, region, instance_profile_name):
        self.iam = self.auth_iam(access_key, secret_key, region)
        client = self.iam.meta.client

        try:
            response = client.get_instance_profile(
                InstanceProfileName= str(instance_profile_name)
            )
            return json.dumps(response, default=datetime_handler)
        except botocore.exceptions.ClientError as e:
            print(f"Error: {e}")
            return f'{e}'

    def get_user(self, access_key, secret_key, region, user_name):
        self.iam = self.auth_iam(access_key, secret_key, region)
        client = self.iam.meta.client

        try:
            response = client.get_user(
                UserName= str(user_name)
            )
            return json.dumps(response, default= datetime_handler)
        except botocore.exceptions.ClientError as e:
            print(f"Error: {e}")
            return f'{e}'

    def list_attached_user_policies(self, access_key, secret_key, region, user_name, marker, max_items):
        self.iam = self.auth_iam(access_key, secret_key, region)
        client = self.iam.meta.client

        try:
            response = client.list_attached_user_policies(
                UserName= str(user_name)
                )
            if marker:
                response = client.list_attached_user_policies(
                UserName= str(user_name),
                Marker = str(marker)
                )
            if max_items:
                response = client.list_attached_user_policies(
                UserName= str(user_name),
                MaxItems = int(max_items)
                )
            if marker and max_items:
                response = client.list_attached_user_policies(
                userName= str(user_name),
                MaxItems = int(max_items),
                Marker = str(marker)
                )

            return json.dumps(response, default=datetime_handler)
        except botocore.exceptions.ClientError as e:
            return f'{e}'

    def list_users(self, access_key, secret_key, region, path_prefix, marker, max_items):
        self.iam = self.auth_iam(access_key, secret_key, region)
        client = self.iam.meta.client

        try:
            response = client.list_users(
                PathPrefix = path_prefix
                )
            if marker:
                response = client.list_users(
                PathPrefix = path_prefix,
                Marker = str(marker)
                )
            if max_items:
                response = client.list_users(
                PathPrefix = path_prefix,
                MaxItems = int(max_items)
                )
            if marker and max_items:
                response = client.list_users(
                PathPrefix = path_prefix,
                MaxItems = int(max_items),
                Marker = str(marker)
                )

            return json.dumps(response, default=datetime_handler)
        except botocore.exceptions.ClientError as e:
            return f'{e}'

    def list_user_tags(self, access_key, secret_key, region, user_name, marker, max_items):
        self.iam = self.auth_iam(access_key, secret_key, region)
        client = self.iam.meta.client

        try:
            response = client.list_user_tags(
                UserName = str(user_name)
                )
            if marker:
                response = client.list_user_tags(
                UserName = str(user_name),
                Marker = str(marker)
                )
            if max_items:
                response = client.list_user_tags(
                UserName = str(user_name),
                MaxItems = int(max_items)
                )
            if marker and max_items:
                response = client.list_user_tags(
                UserName = str(user_name),
                MaxItems = int(max_items),
                Marker = str(marker)
                )

            return json.dumps(response, default=datetime_handler)
        except botocore.exceptions.ClientError as e:
            return f'{e}'

if __name__ == "__main__":
    AWSIAM.run()
