import asyncio
import json
import random
import socket
import time

import boto3
import botocore
from botocore.config import Config
from walkoff_app_sdk.app_base import AppBase

class AWSEC2(AppBase):
    __version__ = "1.0.0"
    app_name = "AWS ec2"

    def __init__(self, redis, logger, console_logger=None):
        """
        Each app should have this __init__ to set up Redis and logging.
        :param redis:
        :param logger:
        :param console_logger:
        """
        super().__init__(redis, logger, console_logger)

    def auth(self, access_key, secret_key, region):
        my_config = Config(
            region_name = region,
            signature_version = 'v4',
            retries = {
                'max_attempts': 10,
                'mode': 'standard'
            },
        )

        return boto3.client(
            'securityhub',
            config=my_config,
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
        )

    # Write your data inside this function
    def enable_security_hub(self, access_key, secret_key, region):
        client = self.auth(access_key, secret_key, region)
        response = client.enable_security_hub(
            Tags={},
            EnableDefaultStandards=True,
        )

        try:
            return json.dumps(response)
        except:
            return response

    # Write your data inside this function
    def get_findings(self, access_key, secret_key, region, filters):
        client = self.auth(access_key, secret_key, region)

        try:
            if not isinstance(filters, list) and not isinstance(filters, object) and not isinstance(filters, dict):
                filters = json.loads(filters)

            response = client.get_findings(Filters=filters)
        except:
            print("Failed to add filters. Couldn't decode JSON")
            response = client.get_findings()

        try:
            return json.dumps(response)
        except:
            pass

        return response

    # Write your data inside this function
    def get_insights(self, access_key, secret_key, region, arn):
        client = self.auth(access_key, secret_key, region)

        response = client.get_insights(
            InsightArns=[insight_arn]
        )

        try:
            return json.dumps(response)
        except:
            pass

        return response

    # Write your data inside this function
    def update_finding(self, access_key, secret_key, region, id, productArn, status):
        client = self.auth(access_key, secret_key, region)
        response = client.batch_update_findings(
            FindingIdentifiers=[
                {
                    "Id": id,
                    "ProductArn": productArn,
                },
            ],
            Workflow={
                'Status': status,
            },
        )

        try:
            return json.dumps(response)
        except:
            pass

        return response

    # Write your data inside this function
    def create_finding(self, access_key, secret_key, region, productArn, id, title, description):
        client = self.auth(access_key, secret_key, region)

        shuffle_id = "SOMETHING_%s" % id
        findings = [{
            'SchemaVersion': '2018-10-08',
            'Id': shuffle_id,
            'ProductArn': productArn,
            'GeneratorId': 'Shuffle',
            'AwsAccountId': 'Shuffle',
            'Types': [],
            'CreatedAt': '2019-08-07T17:05:54.832Z',
            'UpdatedAt': '2019-08-07T17:05:54.832Z',
            'Severity': {},
            'Title': title,
            'Description': description,
            'Resources': [{
                'Type': 'shuffle',
                'Id': shuffle_id,
            }],
        }]

        response = client.batch_import_findings(Findings=findings)

if __name__ == "__main__":
    AWSEC2.run()
