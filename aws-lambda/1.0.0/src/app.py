import socket
import asyncio
import time
import random
import json
import boto3
import botocore
from botocore.config import Config

from walkoff_app_sdk.app_base import AppBase

class AWSLambda(AppBase):
    __version__ = "1.0.0"
    app_name = "AWS Lambda"  

    def __init__(self, redis, logger, console_logger=None):
        """
        Each app should have this __init__ to set up Redis and logging.
        :param redis:
        :param logger:
        :param console_logger:
        """
        super().__init__(redis, logger, console_logger)

    def auth_lambda(self, access_key, secret_key, region):
        my_config = Config(
            region_name = region,
            signature_version = "v4",
            retries = {
                'max_attempts': 10,
                'mode': 'standard'
            },
        )
        
        if access_key!="":
            return boto3.client(
                'lambda', 
                config=my_config, 
                aws_access_key_id=access_key,
                aws_secret_access_key=secret_key,
            )
        else:
            return boto3.client(
                'lambda', 
                config=my_config, 
            )


    def list_functions(self, access_key, secret_key, region):
        client = self.auth_lambda(access_key, secret_key, region)
        try:
            return client.list_functions()
        except Exception as e:
            return f"Error: {e}"

    def get_function(self, access_key, secret_key, region, function_name, qualifier):
        client = self.auth_lambda(access_key, secret_key, region)
        try:
            kwargs = {'FunctionName':function_name}
            if qualifier:
                kwargs.update({'Qualifier':qualifier})
            return client.get_function(**kwargs)
        except Exception as e:
            return f"Error: {e}"

    def list_aliases(self, access_key, secret_key, region, function_name, function_version):
        client = self.auth_lambda(access_key, secret_key, region)
        try:
            kwargs = {'FunctionName':function_name}
            if function_version:
                kwargs.update({'FunctionVersion':function_version})
            return client.list_aliases(**kwargs)
        except Exception as e:
            return f"Error: {e}"
    
    def invoke(self, access_key, secret_key, region, function_name, invocation_type, logtype):
        client = self.auth_lambda(access_key, secret_key, region)
        kwargs = {
            'FunctionName':function_name,
            'InvocationType': invocation_type,
            'LogType': logtype
            }
        try:
            response = client.invoke(**kwargs)
            response['Payload'] = response['Payload'].read().decode("utf-8")
            return response
        except Exception as e:
            return f"Error: {e}"

    def get_account_settings(self, access_key, secret_key, region):
        client = self.auth_lambda(access_key, secret_key, region)
        try:
            return client.get_account_settings()
        except Exception as e:
            return f"Error: {e}"

    def delete_function(self, access_key, secret_key, region, function_name, qualifier):
        client = self.auth_lambda(access_key, secret_key, region)
        kwargs = {'FunctionName': function_name}
        try:
            if qualifier:
                kwargs.update({'Qualifier':qualifier})
            return client.delete_function(**kwargs)
        except Exception as e:
            return f"Error: {e}"

if __name__ == "__main__":
    AWSLambda.run()
