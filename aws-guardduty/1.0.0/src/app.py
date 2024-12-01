import socket
import asyncio
import time
import random
import json
import boto3
import botocore
from botocore.config import Config

from walkoff_app_sdk.app_base import AppBase

class AWSGuardduty(AppBase):
    __version__ = "1.0.0"
    app_name = "AWS Guardduty"  

    def __init__(self, redis, logger, console_logger=None):
        """
        Each app should have this __init__ to set up Redis and logging.
        :param redis:
        :param logger:
        :param console_logger:
        """
        super().__init__(redis, logger, console_logger)

    def auth_guardduty(self, access_key, secret_key, region):
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
                'guardduty', 
                config=my_config, 
                aws_access_key_id=access_key,
                aws_secret_access_key=secret_key,
            )
        else:
            return boto3.client(
                'guardduty', 
                config=my_config, 
            )
        
    def create_detector(self, access_key, secret_key, region, enable):
        client = self.auth_guardduty(access_key, secret_key, region)
        try:
            return client.create_detector(bool(enable))
        except Exception as e:
            return f"Error: {e}"

    def delete_detector(self, access_key, secret_key, region, detectorId):
        client = self.auth_guardduty(access_key, secret_key, region)
        try:
            return client.delete_detector(
                DetectorId = detectorId
            )
        except Exception as e:
            return f"Error: {e}"

    def get_detector(self, access_key, secret_key, region, detectorId):
        client = self.auth_guardduty(access_key, secret_key, region)
        try:
            return client.get_detector(
                DetectorId = detectorId
            )
        except Exception as e:
            return f"Error: {e}"
    
    def update_detector(self, access_key, secret_key, region, detectorId, enable):
        client = self.auth_guardduty(access_key, secret_key, region)
        try:
            return client.update_detector(
                DetectorId = detectorId,
                Enable = bool(enable)
            )
        except Exception as e:
            return f"Error: {e}"

    def create_ip_set(self, access_key, secret_key, region, detectorId, name, fileformat, location, activate):
        client = self.auth_guardduty(access_key, secret_key, region)
        try:
            return client.create_ip_set(
                DetectorId = detectorId,
                Name = name,
                Format = fileformat,
                Location = location,
                Activate = bool(activate)
            )
        except Exception as e:
            return f"Error: {e}"

    def delete_ip_set(self, access_key, secret_key, region, detectorId, ipSetId):
        client = self.auth_guardduty(access_key, secret_key, region)
        try:
            return client.delete_ip_set(
                DetectorId = detectorId,
                IpSetId = ipSetId
            )
        except Exception as e:
            return f"Error: {e}"

    def list_detectors(self, access_key, secret_key, region):
        client = self.auth_guardduty(access_key, secret_key, region)
        try:
            return client.list_detectors()
        except Exception as e:
            return f"Error: {e}"

    def update_ip_set(self, access_key, secret_key, region, detectorId, ipSetId, name, location, activate):
        client = self.auth_guardduty(access_key, secret_key, region)
        try:
            return client.update_ip_set(
                DetectorId = detectorId,
                IpSetId = ipSetId,
                Name = name,
                Location = location,
                Activate = bool(activate)
            )
        except Exception as e:
            return f"Error: {e}"

    def get_ip_set(self, access_key, secret_key, region, detectorId, ipSetId):
        client = self.auth_guardduty(access_key, secret_key, region)
        try:
            return client.get_ip_set(
                DetectorId = detectorId,
                IpSetId = ipSetId,
            )
        except Exception as e:
            return f"Error: {e}"

    def list_ip_sets(self, access_key, secret_key, region, detectorId):
        client = self.auth_guardduty(access_key, secret_key, region)
        try:
            return client.list_ip_sets(
                DetectorId = detectorId
            )
        except Exception as e:
            return f"Error: {e}"


    def create_threat_intel_set(self, access_key, secret_key, region, detectorId, name, fileformat, location, activate):
        client = self.auth_guardduty(access_key, secret_key, region)
        try:
            return client.create_threat_intel_set(
                DetectorId = detectorId,
                Name = name,
                Format = fileformat,
                Location = location,
                Activate = bool(activate)
            )
        except Exception as e:
            return f"Error: {e}"

    def delete_threat_intel_set(self, access_key, secret_key, region, detectorId, threatIntelSetId):
        client = self.auth_guardduty(access_key, secret_key, region)
        try:
            return client.delete_threat_intel_set(
                DetectorId = detectorId,
                ThreatIntelSetId = threatIntelSetId
            )
        except Exception as e:
            return f"Error: {e}"

    def get_threat_intel_set(self, access_key, secret_key, region, detectorId, threatIntelSetId):
        client = self.auth_guardduty(access_key, secret_key, region)
        try:
            return client.get_threat_intel_set(
                DetectorId = detectorId,
                ThreatIntelSetId = threatIntelSetId
            )
        except Exception as e:
            return f"Error: {e}"

    def list_threat_intel_sets(self, access_key, secret_key, region, detectorId):
        client = self.auth_guardduty(access_key, secret_key, region)
        try:
            return client.list_threat_intel_sets(
                DetectorId = detectorId
            )
        except Exception as e:
            return f"Error: {e}"

    def update_threat_intel_set(self, access_key, secret_key, region, detectorId, threatIntelSetId, name, location, activate):
        client = self.auth_guardduty(access_key, secret_key, region)
        try:
            return client.update_threat_intel_set(
                DetectorId = detectorId,
                ThreatIntelSetId = threatIntelSetId,
                Name = name,
                Location = location,
                Activate = bool(activate)
            )
        except Exception as e:
            return f"Error: {e}"

    def list_findings(self, access_key, secret_key, region, detectorId):
        client = self.auth_guardduty(access_key, secret_key, region)
        try:
            return client.list_findings(
                DetectorId = detectorId
            )
        except Exception as e:
            return f"Error: {e}"

    def get_findings(self, access_key, secret_key, region, detectorId, findingIds):
        client = self.auth_guardduty(access_key, secret_key, region)
        try:
            findingIds = findingIds.split(',')
            return client.get_findings(
                DetectorId = detectorId,
                FindingIds = findingIds
            )
        except Exception as e:
            return f"Error: {e}"

    def create_sample_findings(self, access_key, secret_key, region, detectorId, findingIds):
        client = self.auth_guardduty(access_key, secret_key, region)
        try:
            findingIds = findingIds.split(',')
            return client.create_sample_findings(
                DetectorId = detectorId,
                FindingIds = findingIds
            )
        except Exception as e:
            return f"Error: {e}"

    def archive_findings(self,access_key, secret_key, region, detectorId, findingIds):
        client = self.auth_guardduty(access_key, secret_key, region)
        try:
            findingIds = findingIds.split(',')
            return client.archive_findings(
                DetectorId = detectorId,
                FindingIds = findingIds
            )
        except Exception as e:
            return f"Error: {e}"

    def unarchive_findings(self,access_key, secret_key, region, detectorId, findingIds):
        client = self.auth_guardduty(access_key, secret_key, region)
        try:
            findingIds = findingIds.split(',')
            return client.unarchive_findings(
                DetectorId = detectorId,
                FindingIds = findingIds
            )
        except Exception as e:
            return f"Error: {e}"

    def list_members(self,access_key, secret_key, region, detectorId):
        client = self.auth_guardduty(access_key, secret_key, region)
        try:
            return client.list_members(
                DetectorId = detectorId,
            )
        except Exception as e:
            return f"Error: {e}"

    def get_members(self,access_key, secret_key, region, detectorId, accountIds):
        client = self.auth_guardduty(access_key, secret_key, region)
        try:
            accountIds = accountIds.split(',')
            return client.get_members(
                DetectorId = detectorId,
                AccountIds = accountIds
            )
        except Exception as e:
            return f"Error: {e}"


if __name__ == "__main__":
    AWSGuardduty.run()
