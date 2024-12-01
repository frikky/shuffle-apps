import socket
import asyncio
import time
import random
import json
import boto3
import botocore
from botocore.config import Config

from walkoff_app_sdk.app_base import AppBase

class AWSDynamoDB(AppBase):
    __version__ = "1.0.0"
    app_name = "AWS DynamoDB"  

    def __init__(self, redis, logger, console_logger=None):
        """
        Each app should have this __init__ to set up Redis and logging.
        :param redis:
        :param logger:
        :param console_logger:
        """
        super().__init__(redis, logger, console_logger)

    def auth_dynamodb(self, access_key, secret_key, region):
        my_config = Config(
            region_name = region,
            signature_version = "dynamodbv4",
            retries = {
                'max_attempts': 10,
                'mode': 'standard',
            },
        )

        if access_key!="":
            self.dynamodb = boto3.resource(
                'dynamodb', 
                config=my_config, 
                aws_access_key_id=access_key,
                aws_secret_access_key=secret_key,
            )
        else:
            self.dynamodb = boto3.resource(
                'dynamodb', 
                config=my_config,
            )

        return self.dynamodb

    def list_tables(self, access_key, secret_key, region):
        self.dynamodb = self.auth_dynamodb(access_key, secret_key, region)
        client = self.dynamodb.meta.client
        try:
            return client.list_tables()
        except botocore.exceptions.ClientError as e:
            return "Error: %s" % e

    def list_global_tables(self, access_key, secret_key, region):
        self.dynamodb = self.auth_dynamodb(access_key, secret_key, region)
        client = self.dynamodb.meta.client
        try:
            return client.list_global_tables()
        except botocore.exceptions.ClientError as e:
            return "Error: %s" % e

    def get_global_table_setttings(self, access_key, secret_key, region, table_name):
        self.dynamodb = self.auth_dynamodb(access_key, secret_key, region)
        client = self.dynamodb.meta.client

        try:
            return client.describe_global_table_settings(GlobalTableName=table_name)
        except botocore.exceptions.ClientError as e:
            return "Error: %s" % e

    def get_backups(self, access_key, secret_key, region, table_name):
        self.dynamodb = self.auth_dynamodb(access_key, secret_key, region)
        client = self.dynamodb.meta.client

        try:
            return client.list_backups(TableName=table_name)
        except botocore.exceptions.ClientError as e:
            return "Error: %s" % e

if __name__ == "__main__":
    AWSDynamoDB.run()
