import asyncio
import json
import random
import socket
import time

import boto3
import botocore
from botocore.config import Config
from walkoff_app_sdk.app_base import AppBase

class AWSSES(AppBase):
    __version__ = "1.0.0"
    app_name = "AWS ses"  # this needs to match "name" in api.yaml

    def __init__(self, redis, logger, console_logger=None):
        """
        Each app should have this __init__ to set up Redis and logging.
        :param redis:
        :param logger:
        :param console_logger:
        """
        super().__init__(redis, logger, console_logger)

    def auth_ses(self, access_key, secret_key, region):
        my_config = Config(
            region_name = region,
            signature_version = 'v4',
            retries = {
                'max_attempts': 10,
                'mode': 'standard'
            },
        )

        self.ses = boto3.client(
            'ses',
            config = my_config,
            aws_access_key_id = access_key,
            aws_secret_access_key = secret_key,
        )

        return self.ses

    def send_email(self, access_key, secret_key, region, source, toAddresses, ccAddresses, bccAddresses, replyToAddresses, subject_data, data_option, content, charset):
        self.ses = self.auth_ses(access_key, secret_key, region)
        client = self.ses
        toAddresses = list(toAddresses.split(','))
        ccAddresses = list(ccAddresses.split(','))
        replyToAddresses = list(replyToAddresses.split(','))
        if '' in ccAddresses:
            ccAddresses.clear()
        bccAddresses = list(bccAddresses.split(','))
        if '' in bccAddresses:
            bccAddresses.clear()
        if '' in replyToAddresses:
            replyToAddresses.clear()

        try:
            if data_option == 'Text':
                response = client.send_email(
                    Source= source,
                    Destination={
                        'ToAddresses': toAddresses,
                        'CcAddresses': ccAddresses,
                        'BccAddresses': bccAddresses
                    },
                    Message={
                        'Subject': {
                            'Data': subject_data,
                            'Charset': charset
                        },
                        'Body': {
                            'Text': {
                                'Data': content,
                                'Charset': charset
                            },
                        }
                    },
                    ReplyToAddresses = replyToAddresses,
                )
                return response
            else:
                response = client.send_email(
                    Source= source,
                    Destination={
                        'ToAddresses': toAddresses,
                        'CcAddresses': ccAddresses,
                        'BccAddresses': bccAddresses
                    },
                    Message={
                        'Subject': {
                            'Data': subject_data,
                            'Charset': charset
                        },
                        'Body': {
                            'Html': {
                                'Data': content,
                                'Charset': charset
                            },
                        }
                    },
                    ReplyToAddresses = replyToAddresses,
                )
                return response
        except Exception as e:
            return e

    def verify_domain_identity(self, access_key, secret_key, region, domain):
        self.ses = self.auth_ses(access_key, secret_key, region)
        client = self.ses
        try:
            return client.verify_domain_identity(
                Domain=domain
                )
        except Exception as e:
            return e

    def verify_email_identity(self, access_key, secret_key, region, emailAddress):
        self.ses = self.auth_ses(access_key, secret_key, region)
        client = self.ses
        try:
            return client.verify_email_identity(
                EmailAddress = emailAddress
                )
        except Exception as e:
            return e

if __name__ == "__main__":
    AWSSES.run()
