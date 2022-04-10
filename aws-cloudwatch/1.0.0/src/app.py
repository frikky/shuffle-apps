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

def unix_timestamp(datetime_str):
    """
    input format : 'dd/mm/yyyy hour:minuteAM/PM'
    example : '20/11/2021 11:00AM'

    """
    return int(time.mktime(datetime.datetime.strptime(datetime_str, "%d/%m/%Y %I:%M%p").timetuple()))

class CloudWatch(AppBase):
    __version__ = "1.0.0"
    app_name = "AWS cloudwatch logs"

    def __init__(self, redis, logger, console_logger=None):
        """
        Each app should have this __init__ to set up Redis and logging.
        :param redis:
        :param logger:
        :param console_logger:
        """
        super().__init__(redis, logger, console_logger)

    def auth_cloudwatch(self, access_key, secret_key, region):
        my_config = Config(
            region_name = region,
            signature_version = 'v4',
            retries = {
                'max_attempts': 10,
                'mode': 'standard'
            },
        )

        self.cloudwatch = boto3.client(
            'logs',
            config = my_config,
            aws_access_key_id = access_key,
            aws_secret_access_key = secret_key,
        )
        print(self.cloudwatch)
        return self.cloudwatch

    def create_log_group(self, access_key, secret_key, region, log_group_name, kms_key_id, tags):
        self.cloudwatch = self.auth_cloudwatch(access_key, secret_key, region)

        if not isinstance(tags, list) and not isinstance(tags, object) and not isinstance(tags, dict):
            tags = json.loads(tags)

        kwargs = {
                "logGroupName": log_group_name,
                }

        if kms_key_id:
            kwargs.update({"kmsKeyId":kms_key_id})
        if tags:
            kwargs.update({"tags": tags})

        return self.cloudwatch.create_log_group(**kwargs)

    def delete_log_group(self, access_key, secret_key, region, log_group_name):
        self.cloudwatch = self.auth_cloudwatch(access_key, secret_key, region)
        response = self.cloudwatch.delete_log_group(
            logGroupName=log_group_name
        )
        return response

    def get_log_events(self, access_key, secret_key, region, log_group_name, log_stream_name, start_time, end_time, start_from_head, next_token, limit):

        self.cloudwatch = self.auth_cloudwatch(access_key, secret_key, region)

        kwargs = {
                    "logGroupName":log_group_name,
                    "logStreamName": log_stream_name,
                    "startTime":unix_timestamp(start_time),
                    "endTime":unix_timestamp(end_time),
                    "startFromHead":start_from_head
                }

        if next_token:
            kwargs.update({"nextToken":next_token})
        if limit:
            kwargs.update({"limit":limit})
        return self.cloudwatch.get_log_events(**kwargs)

    def start_query(self, access_key, secret_key, region, log_group_name, log_group_list,
             start_time, end_time,limit,query):
        #needs to tested
        self.cloudwatch = self.auth_cloudwatch(access_key, secret_key, region)
        log_group_list = log_group_name.split(',')

        kwargs = {"startTime":unix_timestamp(start_time),
                  "endTime":unix_timestamp(end_time),
                  "queryString": query
                }

        if log_group_list:
            kwargs.update({"logGroupNames":log_group_list})
        if log_group_name:
            kwargs.update({"logGroupName":log_group_name})
        if limit:
            kwargs.update({"limit":limit})

        return self.cloudwatch.start_query(**kwargs)

    def get_query_results(self, access_key, secret_key, region, query_id):

        self.cloudwatch = self.auth_cloudwatch(access_key, secret_key, region, log_record_pointer)

        response = client.get_query_results(
            queryId=query_id
        )
        return response

    def get_log_record(self, access_key, secret_key, region, log_group_name):

        self.cloudwatch = self.auth_cloudwatch(access_key, secret_key, region, log_record_pointer)

        response = client.get_log_record(
            logRecordPointer=log_record_pointer
        )
        return response

    def assign_retention_policy(self, access_key, secret_key, region, log_group_name, retention_days):

        self.cloudwatch = self.auth_cloudwatch(access_key, secret_key, region, log_record_pointer)

        response = client.put_retention_policy(
            logGroupName=log_group_name,
            retentionInDays=retention_days
        )
        return response

    def create_export_task(self, access_key, secret_key, region, task_name,log_group_name, log_stream_name_prefix, from_time, to_time, destination, destination_prefix):
        self.cloudwatch = self.auth_cloudwatch(access_key, secret_key, region)

        kwargs = {"logGroupName":log_group_name,
                  "fromTime":unix_timestamp(from_time),
                  "to": unix_timestamp(to_time),
                  "destination":destination
                }
        if task_name:
            kwargs.update({"taskName":task_name})
        if log_stream_name_prefix:
            kwargs.update({"logStreamNamePrefix":log_stream_name_prefix})
        if destination_prefix:
            kwargs.update({"destinationPrefix":destination_prefix})

        return self.cloudwatch.start_query(**kwargs)

if __name__ == "__main__":
    CloudWatch.run()
