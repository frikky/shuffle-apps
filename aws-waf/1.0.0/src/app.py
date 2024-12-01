import sys
import socket
import asyncio
import time
import random
import json
import boto3
import botocore
from botocore.config import Config

from walkoff_app_sdk.app_base import AppBase

class AWSEC2(AppBase):
    __version__ = "1.0.0"
    app_name = "AWS WAF"  

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
        if access_key!="":
           return boto3.client('wafv2', config=my_config, aws_access_key_id=access_key, aws_secret_access_key=secret_key)
        else:
            return boto3.client('wafv2', config=my_config)


    # Write your data inside this function
    def block_ip_waf(self, access_key, secret_key, region, ipset_name, ip):
        #ret = block_ip_waf (access_key, secret_key, region, ipset_name, ip)

        client = self.auth(access_key, secret_key, region)
        scope = "REGIONAL"
        if "/" not in ip:
            ip = "%s/32" % ip

        # 1. Handle IP setting
        arn = ""
        try:
            response = client.create_ip_set(
                Name=ipset_name,
                Scope=scope,
                IPAddressVersion='IPV4',
                Addresses=[
                    ip,
                ],
            )

            arn = response["Summary"]["ARN"]
            print("AFTER ARN GRAB FROM IPSET CREATION - pre sleep")
            time.sleep(1)
        except:
            #print("IN EXCEPT")
            #print(sys.exc_info()[0])
            #print(sys.exc_info()[1])
            info = str(sys.exc_info()[0])
            #print("INFO: %s" % info)
            if info == "<class 'botocore.errorfactory.WAFUnavailableEntityException'>":
                #print("IT EQUALS!")
                return "Failed to create ip set: %s" % info

            print("IP rule set %s already exists" % ipset_name)
            response = client.list_ip_sets(
                Scope='REGIONAL',
                Limit=100
            )

            selected = {}
            for item in response["IPSets"]:
                if item["Name"] == ipset_name:
                    selected = item
                    break

            try:
                item_id = selected["Id"]
            except KeyError:
                return "Couldn't find ipset for name %s" % ipset_name

            new_resp = client.get_ip_set(
                Name=ipset_name,
                Id=item_id,
                Scope=scope,
            )

            arn = new_resp["IPSet"]["ARN"]
            found = False 
            for address in  new_resp["IPSet"]["Addresses"]:
                if address == ip:
                    found = True
                    break
                    #return "%s is already in this WAF rule" % ip

            if not found:
                new_resp["IPSet"]["Addresses"].append(ip)
                update_resp = client.update_ip_set(
                    Name = new_resp["IPSet"]["Name"],
                    Scope = scope,
                    Id = new_resp["IPSet"]["Id"],
                    LockToken = new_resp["LockToken"],
                    Addresses = new_resp["IPSet"]["Addresses"],
                )

        # 2: Handle rule group creation 
        #arn = "arn:aws:wafv2:ap-northeast-1:202262580068:regional/ipset/shuffle-test/f2a8df33-82cf-4a9e-8601-880023c617a6"
        updateRule = {
                'Name': ipset_name,
                'Priority': 1,
                'Statement': {
                    'IPSetReferenceStatement': {
                        "ARN": arn,
                        'IPSetForwardedIPConfig': {
                            'HeaderName': "ANY",
                            'FallbackBehavior': 'MATCH',
                            'Position': 'ANY'
                        },
                    },
                },
                "Action": {
                    "Block": {},    
                },
                "VisibilityConfig": {
                    'SampledRequestsEnabled': False,
                    'CloudWatchMetricsEnabled': True,
                    'MetricName': 'string'
                },
            }
        try:
            outerresponse = client.create_rule_group(
                Name=ipset_name,
                Scope=scope,
                Capacity=99,
                Rules=[updateRule],
                VisibilityConfig={
                    'SampledRequestsEnabled': False,
                    'CloudWatchMetricsEnabled': True,
                    'MetricName': 'string'
                },
            )

            print("Rule group creation: %s" % outerresponse)
        except:
            print("Rule group %s already exists" % ipset_name)
            # Get the rule
            get_groups = client.list_rule_groups(
                Scope=scope,
                Limit=100,
            )

            cur_rule = {}
            for rule in get_groups["RuleGroups"]:
                #print("Rule: %s" % rule)
                if rule["Name"] == ipset_name:
                    cur_rule = rule 
                    break

            try:
                if cur_rule["Name"] == ipset_name:
                    pass
            except KeyError:
                return "Couldn't find rule group %s" % ipset_name

            get_group = client.get_rule_group(
                Scope=scope,
                Id=cur_rule["Id"],
                Name=cur_rule["Name"],
            )

            found = False
            for rule in get_group["RuleGroup"]["Rules"]:
                try:
                    if rule["Name"] == ipset_name:
                        # ["Statement"]["IPSetReferenceStatement"]["ARN"] == arn:
                        return "Successfully blocked %s in WAF (2)" % ip
                except KeyError as e:
                    print("Keyerror: %s" % e)

            rules = get_group["RuleGroup"]["Rules"]
            rules.append(updateRule)

            # If here, add it to the group
            update_group = client.update_rule_group(
                Name=get_group["RuleGroup"]["Name"],
                Scope=scope,
                Id=get_group["RuleGroup"]["Id"],
                LockToken=get_group["LockToken"],
                Rules=rules,
                VisibilityConfig={
                    'SampledRequestsEnabled': False,
                    'CloudWatchMetricsEnabled': True,
                    'MetricName': 'string'
                },
            )

        return "Successfully blocked %s in WAF (4)" % ip


if __name__ == "__main__":
    AWSEC2.run()
