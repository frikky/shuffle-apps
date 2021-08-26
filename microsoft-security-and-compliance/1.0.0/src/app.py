import socket
import asyncio
import time
import random
import json
import uuid
import time
import requests

from walkoff_app_sdk.app_base import AppBase

# Antispam
# https://protection.office.com/threatpolicy
# https://protection.office.com/antispam
# https://docs.microsoft.com/en-us/microsoft-365/security/office-365-security/configure-the-connection-filter-policy?view=o365-worldwide

#create_url = "https://compliance.microsoft.com/api/ComplianceSearch"
#Request URL: 
# https://docs.microsoft.com/en-us/information-protection/develop/overview
# https://docs.microsoft.com/en-us/graph/api/resources/ediscovery-ediscoveryapioverview?view=graph-rest-beta
# Microsoft Graph Security securityAction entity
# https://docs.microsoft.com/en-us/graph/api/resources/threatassessment-api-overview?view=graph-rest-1.0

# Permissions (Delegated): SecurityEvents, ThreatAssement, ThreatIndicators, Compliance
# !! Have a "report email" internally using office365 !! 
# Microsoft Threat Protection
# https://security.microsoft.com/mtp/
# https://protection.office.com/api/AcceptedDomain

class MSComplianceCenter(AppBase):
    __version__ = "1.0.0"
    app_name = "Microsoft Security and Compliance"

    def __init__(self, redis, logger, console_logger=None):
        """
        Each app should have this __init__ to set up Redis and logging.
        :param redis:
        :param logger:
        :param console_logger:
        """
        super().__init__(redis, logger, console_logger)

    async def authenticate(self, tenant_id, client_id, client_secret, graph_url):
        s = requests.Session()
        auth_url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token"
        auth_data = {
            "grant_type": "client_credentials",
            "client_id": client_id,
            "client_secret": client_secret,
            "scope": f"{graph_url}/.default",
        }
        auth_headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "cache-control": "no-cache",
        }

        print(f"Making request to: {auth_url}")
        res = s.post(auth_url, data=auth_data, headers=auth_headers)

        # Auth failed, raise exception with the response
        if res.status_code != 200:
            raise ConnectionError(res.text)

        access_token = res.json().get("access_token")
        s.headers = {"Authorization": f"Bearer {access_token}", "cache-control": "no-cache"}
        print(s)
        return s

        #graph_url = "https://graph.microsoft.com"
        #session = await self.authenticate(tenant_id, client_id, client_secret, graph_url)
        #create_url = "https://protection.office.com/api/ComplianceSearch"
        #create_url = "https://compliance.microsoft.com/api/ComplianceSearch"
        ##https://protection.office.com/api/HostedContentFilterRule
        #ret = session.post(graph_url)
        #print(ret.status_code)
        #print(ret.text)
        #if ret.status_code < 300:
        #    data = ret.json()
        #    #return {"success": True, "alerts": data["value"]}

        #return {"success": False, "reason": "Bad status code %d - expecting 200." % ret.status_code}

        # ENABLE: https://protection.office.com/api/OrganizationCustomization/Enable?source=HostedContentFilterPolicy


        # GET:https://graph.microsoft.com/v1.0/me/messages?$filter=from/emailAddress/address+eq+'xx@xxxx.onmicrosoft.com'+and+isRead+eq+False

    async def get_alerts(self, tenant_id, client_id, client_secret, top):
        graph_url = "https://graph.microsoft.com"
        session = await self.authenticate(tenant_id, client_id, client_secret, graph_url)
        if top:
            graph_url = f"https://graph.microsoft.com/v1.0/security/alerts?$top={top}"
        else:
            graph_url = f"https://graph.microsoft.com/v1.0/security/alerts?$top=10"
        ret = session.get(graph_url)
        print(ret.status_code)
        print(ret.text)
        if ret.status_code < 300:
            data = ret.json()
            return {"success": True, "alerts": data["value"]}

        return {"success": False, "reason": "Bad status code %d - expecting 200." % ret.status_code}

    async def get_alerts_by_severity(self, tenant_id, client_id, client_secret, top, severity):
        graph_url = "https://graph.microsoft.com"
        session = await self.authenticate(tenant_id, client_id, client_secret, graph_url)
        if top:
            graph_url = f"https://graph.microsoft.com/v1.0/security/alerts?$filter=Severity eq '{severity}'&$top={top}"
        else:
            graph_url = f"https://graph.microsoft.com/v1.0/security/alerts?$filter=Severity eq '{severity}'&$top=5"
        ret = session.get(graph_url)
        print(ret.status_code)
        print(ret.text)
        if ret.status_code < 300:
            data = ret.json()
            return {"success": True, "alerts": data["value"]}

        return {"success": False, "reason": "Bad status code %d - expecting 200." % ret.status_code}   

    async def get_alerts_by_vendors(self, tenant_id, client_id, client_secret, vendor, top):
        vendor_code = {
            "Azure Advanced Threat Protection":"Azure Advanced Threat Protection",
            "Azure Security Center":"ASC",
            "Microsoft Cloud App Security":"MCAS",
            "Azure Active Directory Identity Protection":"IPC",
            "Azure Sentinel":"Azure Sentinel",
            "Microsoft Defender Advanced Threat Protection":"Microsoft Defender ATP"
        }
        graph_url = "https://graph.microsoft.com"
        session = await self.authenticate(tenant_id, client_id, client_secret, graph_url)
        if top:
            graph_url = f"https://graph.microsoft.com/v1.0/security/alerts?$filter=vendorInformation/provider eq '{vendor_code[vendor]}'&$top={top}"
        else:
            graph_url = f"https://graph.microsoft.com/v1.0/security/alerts?$filter=vendorInformation/provider eq '{vendor_code[vendor]}'&$top=5" 
        ret = session.get(graph_url)
        print(ret.status_code)
        print(ret.text)
        if ret.status_code < 300:
            data = ret.json()
            return {"success": True, "alerts": data["value"]}

        return {"success": False, "reason": "Bad status code %d - expecting 200." % ret.status_code}     
    
    async def get_alert_by_id(self, tenant_id, client_id, client_secret,alert_id):
        graph_url = "https://graph.microsoft.com"
        session = await self.authenticate(tenant_id, client_id, client_secret, graph_url)

        graph_url = f"https://graph.microsoft.com/v1.0/security/alerts/{alert_id}"
        ret = session.get(graph_url)
        print(ret.status_code)
        print(ret.text)
        if ret.status_code < 300:
            data = ret.json()
            return {"success": True, "alerts": data["value"]}

        return {"success": False, "reason": "Bad status code %d - expecting 200." % ret.status_code, "error_response":ret.text}

    async def update_alert(self, tenant_id, client_id, client_secret, alert_id, assigned_to, comments, tags, feedback, status, vendor, provider, sub_provider,provider_version):
        """This function needs to be tested."""
        
        graph_url = "https://graph.microsoft.com"
        session = await self.authenticate(tenant_id, client_id, client_secret, graph_url)

        graph_url = f"https://graph.microsoft.com/v1.0/security/alerts/{alert_id}"

        tags_list = []
        if tags:
            for tag in tags.split(","):
                 tags_list.append(tag)         

        request_body = {
            "assignedTo": assigned_to,
            "comments":[comments],
            "tags":tags_list,
            "feedback": feedback,
            "status": status,
            "vendorInformation": {
                "provider": provider,
                "providerVersion": provider_version,
                "subProvider": sub_provider,
                "vendor": vendor
            }
        }
        filtered_request_body = {k:v for k,v in request_body.items() if len(v) > 0}
        print(filtered_request_body)
        ret = session.patch(graph_url, json=filtered_request_body)
        print(ret.status_code)
        print(ret.text)
        if ret.status_code < 300:
            data = ret.json()
            return data

        return {"success": False, "reason": "Bad status code %d - expecting 200." % ret.status_code, "error_response":ret.text}

    async def list_threat_assesment_requests(self, tenant_id, client_id, client_secret):
        graph_url = "https://graph.microsoft.com"
        session = await self.authenticate(tenant_id, client_id, client_secret, graph_url)

        graph_url = "https://graph.microsoft.com/v1.0/informationProtection/threatAssessmentRequests"
        ret = session.get(graph_url)
        print(ret.status_code)
        print(ret.text)
        if ret.status_code < 300:
            data = ret.json()
            return data

        return {"success": False, "reason": "Bad status code %d - expecting 200." % ret.status_code,"error_response":ret.text}

    async def get_threat_assesment_request(self, tenant_id, client_id, client_secret, request_id):
        graph_url = "https://graph.microsoft.com"
        session = await self.authenticate(tenant_id, client_id, client_secret, graph_url)

        graph_url = f"https://graph.microsoft.com/v1.0/informationProtection/threatAssessmentRequests/{request_id}"        
        ret = session.get(graph_url)
        print(ret.status_code)
        print(ret.text)
        if ret.status_code < 300:
            data = ret.json()
            return data

        return {"success": False, "reason": "Bad status code %d - expecting 200." % ret.status_code,"error_response":ret.text}    

    async def create_mail_threat_assessment(self, tenant_id, client_id, client_secret, reciepient_email, expected_assessment, category, message_uri, status):
        graph_url = "https://graph.microsoft.com"
        session = await self.authenticate(tenant_id, client_id, client_secret, graph_url)
        graph_url = f"https://graph.microsoft.com/v1.0/informationProtection/threatAssessmentRequests"
        
        headers = {
            "Content-type": "application/json"
        }

        request_body = {
            "@odata.type": "#microsoft.graph.mailAssessmentRequest",
            "recipientEmail": reciepient_email,
            "expectedAssessment": expected_assessment,
            "category": category,
            "messageUri": message_uri,
            "status": status
        }

        ret = session.post(graph_url, headers=headers, json =request_body )
        print(ret.status_code)
        print(ret.text)
        if ret.status_code < 300:
            data = ret.json()
            return data

        return {"success": False, "reason": "Bad status code %d - expecting 200." % ret.status_code,"error_response":ret.text} 


    async def create_url_threat_assessment(self, tenant_id, client_id, client_secret, url, expected_assessment, category, status):
        graph_url = "https://graph.microsoft.com"
        session = await self.authenticate(tenant_id, client_id, client_secret, graph_url)
        graph_url = "https://graph.microsoft.com/v1.0/informationProtection/threatAssessmentRequests"


        request_body ={
            "@odata.type": "#microsoft.graph.urlAssessmentRequest",
            "url": url,
            "expectedAssessment": expected_assessment,
            "category": category,
            "status": status
            }

        ret = session.post(graph_url,json =request_body )
        print(ret.status_code)
        print(ret.text)
        if ret.status_code < 300:
            data = ret.json()
            return data

        return {"success": False, "reason": "Bad status code %d - expecting 200." % ret.status_code,"error_response":ret.text}

    async def create_file_threat_assessment(self, tenant_id, client_id, client_secret, filename, content_data, expected_assessment, category, status):
        graph_url = "https://graph.microsoft.com"
        session = await self.authenticate(tenant_id, client_id, client_secret, graph_url)
        graph_url = "https://graph.microsoft.com/v1.0/informationProtection/threatAssessmentRequests"

        headers = {
            "Content-type": "application/json"
        }

        request_body ={
            "@odata.type": "#microsoft.graph.fileAssessmentRequest",
            "expectedAssessment": expected_assessment,
            "category": category,
            "fileName": filename,
            "contentData": content_data
            }

        ret = session.post(graph_url, headers= headers ,json =request_body )
        print(ret.status_code)
        print(ret.text)
        if ret.status_code < 300:
            data = ret.json()
            return data

        return {"success": False, "reason": "Bad status code %d - expecting 200." % ret.status_code,"error_response":ret.text}    

    async def list_secure_score(self, tenant_id, client_id, client_secret, top):
        graph_url = "https://graph.microsoft.com"
        session = await self.authenticate(tenant_id, client_id, client_secret, graph_url)
        if top:
            graph_url = f"https://graph.microsoft.com/v1.0/security/secureScores?$top={top}"
        else:
            graph_url = "https://graph.microsoft.com/v1.0/security/secureScores?$top=1"

        ret = session.get(graph_url)
        print(ret.status_code)
        print(ret.text)
        if ret.status_code < 300:
            data = ret.json()
            return data

        return {"success": False, "reason": "Bad status code %d - expecting 200." % ret.status_code,"error_response":ret.text}
    
    async def list_cases(self, tenant_id, client_id, client_secret):
        graph_url = "https://graph.microsoft.com"
        session = await self.authenticate(tenant_id, client_id, client_secret, graph_url)
        graph_url = "https://graph.microsoft.com/beta/compliance/ediscovery/cases"

        ret = session.get(graph_url)
        print(ret.status_code)
        print(ret.text)
        if ret.status_code < 300:
            data = ret.json()
            return data

        return {"success": False, "reason": "Bad status code %d - expecting 200." % ret.status_code,"error_response":ret.text}
    
    async def get_case(self, tenant_id, client_id, client_secret,case_id):
        graph_url = "https://graph.microsoft.com"
        session = await self.authenticate(tenant_id, client_id, client_secret, graph_url)
        graph_url = f"https://graph.microsoft.com/beta/compliance/ediscovery/cases/{case_id}"

        ret = session.get(graph_url)
        print(ret.status_code)
        print(ret.text)
        if ret.status_code < 300:
            data = ret.json()
            return data

        return {"success": False, "reason": "Bad status code %d - expecting 200." % ret.status_code,"error_response":ret.text}

    async def create_case(self, tenant_id, client_id, client_secret, display_name):
        graph_url = "https://graph.microsoft.com"
        session = await self.authenticate(tenant_id, client_id, client_secret, graph_url)
        graph_url = "https://graph.microsoft.com/beta/compliance/ediscovery/cases"

        headers = {
            "Content-type": "application/json"
        }

        request_body = {
            "displayName": display_name
        }
        ret = session.post(graph_url, headers = headers ,json = request_body)
        print(ret.status_code)
        print(ret.text)
        if ret.status_code < 300:
            data = ret.json()
            return data

        return {"success": False, "reason": "Bad status code %d - expecting 200." % ret.status_code,"error_response":ret.text}    
    
    async def update_case(self, tenant_id, client_id, client_secret,case_id, display_name, description, external_id):
        graph_url = "https://graph.microsoft.com"
        session = await self.authenticate(tenant_id, client_id, client_secret, graph_url)
        graph_url = f"https://graph.microsoft.com/beta/compliance/ediscovery/cases/{case_id}"

        headers = {
            "Content-type": "application/json"
        }

        request_body = {
            "displayName": "My Case 1 - Renamed",
            "description": "Updated description",
            "externalId": "Updated externalId"
        }
        ret = session.patch(graph_url, headers = headers ,json = request_body)
        print(ret.status_code)
        print(ret.text)
        if ret.status_code < 300:
            data = ret.json()
            return data

        return {"success": False, "reason": "Bad status code %d - expecting 200." % ret.status_code,"error_response":ret.text}
    
    async def close_case(self, tenant_id, client_id, client_secret, case_id):
        graph_url = "https://graph.microsoft.com"
        session = await self.authenticate(tenant_id, client_id, client_secret, graph_url)
        graph_url = "https://graph.microsoft.com/beta/compliance/ediscovery/cases/{case_id}/close"

        ret = session.post(graph_url)
        print(ret.status_code)
        print(ret.text)
        if ret.status_code < 300:
            data = ret.json()
            return data

        return {"success": False, "reason": "Bad status code %d - expecting 200." % ret.status_code,"error_response":ret.text}

    async def reopen_case(self, tenant_id, client_id, client_secret, case_id):
        graph_url = "https://graph.microsoft.com"
        session = await self.authenticate(tenant_id, client_id, client_secret, graph_url)
        graph_url = "https://graph.microsoft.com/beta/compliance/ediscovery/cases/{case_id}/reopen"

        ret = session.post(graph_url)
        print(ret.status_code)
        print(ret.text)
        if ret.status_code < 300:
            data = ret.json()
            return data

        return {"success": False, "reason": "Bad status code %d - expecting 200." % ret.status_code,"error_response":ret.text}

    async def list_custodians(self, tenant_id, client_id, client_secret,case_id):
        graph_url = "https://graph.microsoft.com"
        session = await self.authenticate(tenant_id, client_id, client_secret, graph_url)
        graph_url = f"https://graph.microsoft.com/beta/compliance/ediscovery/cases/{case_id}/custodians"

        ret = session.get(graph_url)
        print(ret.status_code)
        print(ret.text)
        if ret.status_code < 300:
            data = ret.json()
            return data

        return {"success": False, "reason": "Bad status code %d - expecting 200." % ret.status_code,"error_response":ret.text}

    async def get_custodian(self, tenant_id, client_id, client_secret, case_id, custodian_id):
        graph_url = "https://graph.microsoft.com"
        session = await self.authenticate(tenant_id, client_id, client_secret, graph_url)
        graph_url = f"https://graph.microsoft.com/beta/compliance/ediscovery/cases/{case_id}/custodians/{custodian_id}"

        ret = session.get(graph_url)
        print(ret.status_code)
        print(ret.text)
        if ret.status_code < 300:
            data = ret.json()
            return data

        return {"success": False, "reason": "Bad status code %d - expecting 200." % ret.status_code,"error_response":ret.text}


    async def create_custodian(self, tenant_id, client_id, client_secret, case_id, email, apply_hold_to_sources):
        graph_url = "https://graph.microsoft.com"
        session = await self.authenticate(tenant_id, client_id, client_secret, graph_url)
        graph_url = f"https://graph.microsoft.com/beta/compliance/ediscovery/cases/{case_id}/custodians/"

        headers = {
            "Content-Type": "application/json",
            "Content-length": "279"
        }
        request_body = {
            "email": email,
            "applyHoldToSources":apply_hold_to_sources
        }

        ret = session.post(graph_url, headers=headers ,json= request_body)
        print(ret.status_code)
        print(ret.text)
        if ret.status_code < 300:
            data = ret.json()
            return data

        return {"success": False, "reason": "Bad status code %d - expecting 200." % ret.status_code,"error_response":ret.text}    

    async def update_custodian(self, tenant_id, client_id, client_secret,case_id, custodian_id, apply_hold_to_sources):
        graph_url = "https://graph.microsoft.com"
        session = await self.authenticate(tenant_id, client_id, client_secret, graph_url)
        graph_url = f"https://graph.microsoft.com/beta/compliance/ediscovery/cases/{case_id}/custodians/{custodian_id}"

        request_body = {
            "applyHoldToSources": apply_hold_to_sources
        }

        ret = session.patch(graph_url, headers = headers ,json = request_body)
        print(ret.status_code)
        print(ret.text)
        if ret.status_code < 300:
            data = ret.json()
            return data

        return {"success": False, "reason": "Bad status code %d - expecting 200." % ret.status_code,"error_response":ret.text}

    async def activate_custodian(self, tenant_id, client_id, client_secret,case_id, custodian_id):
        graph_url = "https://graph.microsoft.com"
        session = await self.authenticate(tenant_id, client_id, client_secret, graph_url)
        graph_url = f"https://graph.microsoft.com/beta/compliance/ediscovery/cases/{case_id}/custodians/{custodian_id}/activate"

        headers = {
            "Content-Type": "application/json"
        }

        ret = session.post(graph_url)
        print(ret.status_code)
        print(ret.text)
        if ret.status_code < 300:
            data = ret.json()
            return data

        return {"success": False, "reason": "Bad status code %d - expecting 200." % ret.status_code,"error_response":ret.text}

    async def release_custodian(self, tenant_id, client_id, client_secret,case_id, custodian_id):
        graph_url = "https://graph.microsoft.com"
        session = await self.authenticate(tenant_id, client_id, client_secret, graph_url)
        graph_url = f"https://graph.microsoft.com/beta/compliance/ediscovery/cases/{case_id}/custodians/{custodian_id}/release"

        headers = {
            "Content-Type": "application/json"
        }

        ret = session.post(graph_url,headers= headers)
        print(ret.status_code)
        print(ret.text)
        if ret.status_code < 300:
            data = ret.json()
            return data

        return {"success": False, "reason": "Bad status code %d - expecting 200." % ret.status_code,"error_response":ret.text}        

    async def list_legalholds(self, tenant_id, client_id, client_secret,case_id):
        graph_url = "https://graph.microsoft.com"
        session = await self.authenticate(tenant_id, client_id, client_secret, graph_url)
        graph_url = f"https://graph.microsoft.com/beta/compliance/ediscovery/cases/{case_id}/legalholds"

        ret = session.get(graph_url)
        print(ret.status_code)
        print(ret.text)
        if ret.status_code < 300:
            data = ret.json()
            return data

        return {"success": False, "reason": "Bad status code %d - expecting 200." % ret.status_code,"error_response":ret.text}
    
    async def get_legalhold(self, tenant_id, client_id, client_secret, case_id, legalhold_id):
        graph_url = "https://graph.microsoft.com"
        session = await self.authenticate(tenant_id, client_id, client_secret, graph_url)
        graph_url = f"https://graph.microsoft.com/beta/compliance/ediscovery/cases/{case_id}/custodians/{legalhold_id}"

        ret = session.get(graph_url)
        print(ret.status_code)
        print(ret.text)
        if ret.status_code < 300:
            data = ret.json()
            return data

        return {"success": False, "reason": "Bad status code %d - expecting 200." % ret.status_code,"error_response":ret.text}

    async def create_legalhold(self, tenant_id, client_id, client_secret, case_id, display_name, description, is_enabled, status, content_query,errors):
        graph_url = "https://graph.microsoft.com"
        session = await self.authenticate(tenant_id, client_id, client_secret, graph_url)
        graph_url = f"https://graph.microsoft.com/beta/compliance/ediscovery/cases/{case_id}/legalHolds"
        
        error_list = [str(i) for i in errors.split(',')]
        headers = {
            "Content-Type": "application/json"
        }
        request_body = {
            "@odata.type": "#microsoft.graph.ediscovery.legalHold",
            "description": str(description),
            "isEnabled": is_enabled,
            "status": status,
            "contentQuery": "String",
            "errors": error_list,
            "displayName": display_name
        }
        filtered_request_body = {k:v for k,v in request_body.items() if v is not None}

        ret = session.post(graph_url ,headers=headers ,json= filtered_request_body)
        print(ret.status_code)
        print(ret.text)
        if ret.status_code < 300:
            data = ret.json()
            return data

        return {"success": False, "reason": "Bad status code %d - expecting 200." % ret.status_code,"error_response":ret.text}    
    
    async def list_source_collections(self, tenant_id, client_id, client_secret,case_id):
        graph_url = "https://graph.microsoft.com"
        session = await self.authenticate(tenant_id, client_id, client_secret, graph_url)
        graph_url = f"https://graph.microsoft.com/beta/compliance/ediscovery/cases/{case_id}/sourceCollections"

        ret = session.get(graph_url)
        print(ret.status_code)
        print(ret.text)
        if ret.status_code < 300:
            data = ret.json()
            return data

        return {"success": False, "reason": "Bad status code %d - expecting 200." % ret.status_code,"error_response":ret.text}

    async def list_people(self, tenant_id, client_id, client_secret, user_principal_name):
        graph_url = "https://graph.microsoft.com"
        session = await self.authenticate(tenant_id, client_id, client_secret, graph_url)
        graph_url = f"https://graph.microsoft.com/v1.0/users/{user_principal_name}/people"

        ret = session.get(graph_url)
        print(ret.status_code)
        print(ret.text)
        if ret.status_code < 300:
            data = ret.json()
            return data

        return {"success": False, "reason": "Bad status code %d - expecting 200." % ret.status_code,"error_response":ret.text}    
    
    #https://protection.office.com/api/ComplianceSearch/StartSearch?id=Another+search&retry=False

if __name__ == "__main__":
    asyncio.run(MSComplianceCenter.run(), debug=True)
