#Office 365 Management API Event Poller

__author__ = "Robert Evans"
__version__ = "1.0.0"
__maintainer__ = "Robert Evans"
__email__ = "rob.evans512@gmail.com"
__status__ = "Production"

import sys
import os
import re
import json
import datetime as DT
import requests
import logging
import logging.handlers

def pollOffice(planType,tenantID,clientID,clientSecret,pollInterval):
    #Office365Plan type
    #Enterprise - Enterprise Plan
    #GCC - GCC Government Plan
    #GCCHigh - GCC High Government Plan
    #DoD - DoD Government Plan
    loginURL = ""
    mgmtEndpoint = ""

    if "" in [planType,tenantID,clientID,clientSecret]:
        print("Issue with credentials, exiting")
        return "Credentials or variables missing"

    if planType == "Enterprise":
        #Login and Base urls are unique per plan type
        loginURL = "https://login.windows.net"
        mgmtEndpoint = "https://manage.office.com"
    elif planType == "GCC":
        #GCC Plan
        loginURL = "https://login.microsoftonline.com"
        mgmtEndpoint = "https://manage-gcc.office.com"
    elif planType == "GCCHigh":
        #Login URL for GCC High
        loginURL = "https://login.microsoftonline.us"
        #Management Endpoint for GCC High
        mgmtEndpoint = "https://manage.office365.us"
    elif planType == "DoD":
        #DoD plan - untested loginURL may be different
        loginURL = "https://login.microsoftonline.us"
        mgmtEndpoint = "https://manage.protection.apps.mil"
    else:
        print("Please specify plan type in config file, exiting.")
        exit(1)

    scope = mgmtEndpoint + '/.default'

    #url-form-encoded data for auth
    payload = {'client_id': clientID,
                     'scope': scope,
                      'client_secret': clientSecret,
                      'grant_type': 'client_credentials'}

    authURL = loginURL + '/' + tenantID + '/oauth2/v2.0/token'

    #make request for token
    resp = requests.post(authURL, data=payload)
    if resp.status_code != 200:
        print("Authentication error has occurred: ", resp.json())
        return "Auth error occurred" + str(resp.json())
    json_resp = resp.json()
    access_token = json_resp['access_token']

    #build api request now that we are authenticated
    base_url = mgmtEndpoint + '/api/v1.0/' + tenantID + '/activity/feed'
    auth_header = 'Bearer ' + access_token
    headers = {
        'User-Agent' : "Stratozen",
        'Accept' : 'application/json',
        'Content-Type' : 'application/json',
        'Authorization' : auth_header
    }

    #Start a subscription (or list an existing for polling later)
    #Start one for each content type - note DLP requires special permissions
    #Content Types:
    #Audit.AzureActiveDirectory
    #Audit.Exchange
    #Audit.SharePoint
    #Audit.General
    #DLP.All
    content_types = ["Audit.AzureActiveDirectory", "Audit.Exchange","Audit.SharePoint","Audit.General","DLP.All"]

    existingSubscriptions = subscriptionList(base_url,headers,tenantID)
    if existingSubscriptions is None:
        for content_type in content_types:
            #Start every subscription possible
            subscriptionStart(base_url,headers,content_type,tenantID)
            #If this content type was started, try to poll data
            #Note: It can take up to 12 hours from subscription start for data to be consumable
            #Microsoft limitation
    else:
        #Iterate existingSubscriptions and try to start any missing
        print("Existing subscriptions: ",existingSubscriptions)
        for content_type in content_types:
            subExists = False
            for sub in existingSubscriptions:
                existingSubType = sub['contentType']
                if content_type == existingSubType:
                    subExists = True
            #If content_type is not already in list, start the subscription
            if subExists == False:
                #Try to start the subscription
                subscriptionStart(base_url,headers,content_type,tenantID)

    #Continue with existing subscriptions for now, next iteration we will get the new ones
    #Start and End polling times in UTC format
    #Future state mechanism should store last poll time and pick up from there
    #Start and end times cannot be greater than 24 hours apart
    now = DT.datetime.now(DT.timezone.utc) #aware UTC object

    #start_time = now - DT.timedelta(minutes=10)
    start_time = now - DT.timedelta(minutes=int(pollInterval))
    end_time = now


    #String format for dates that api expects
    start_time_str = start_time.strftime('%Y-%m-%dT%H:%M:%S')
    end_time_str = end_time.strftime('%Y-%m-%dT%H:%M:%S')

    print("Start Time: ",start_time_str)
    print("End Time: ",end_time_str)

    #init json data var to return to Shuffle calling function
    json_data = {}
    #For each available subscription check for available content
    for sub in existingSubscriptions:
        content_type = sub['contentType']
        #Call list available content function and process any data
        sub_data = processContent(content_type,base_url, headers,tenantID,start_time_str,end_time_str)
        if sub_data is not None:
            json_data.update(sub_data) #assumes json dict is returned

    #Finally, return all the data
    #Return data
    return json.dumps(json_data)


def subscriptionList(base_url,headers,tenantID):
    #Lists available O365 subscriptions, returns list of available subscriptions
    listURL = base_url + "/subscriptions/list"
    payload = {'PublisherIdentifier': tenantID}

    resp = requests.get(listURL, headers=headers,params=payload)

    if resp.status_code == 200:
        #return json data
        return resp.json()
    else:
        print("Error occured while listing subscription: ",resp.json())
        return None

def subscriptionStart(base_url,headers,content_type,tenantID):
    #Starts a subscription - return true on success
    start_sub_payload = {'contentType': content_type,
                                      'PublisherIdentifier': tenantID}
    #Call URL
    start_sub_url = base_url + '/subscriptions/start'

    resp = requests.post(start_sub_url, headers=headers,params=start_sub_payload)

    resp_json = resp.json()
    if resp.status_code == 200:
        #Process any object uris in returned data
        print("Subscription: ", content_type, " started successfully")
    else:
        error_code = resp_json['error']['code']
        message = resp_json['error']['message']
        if error_code == "AF20024":
            print("Subscription already enabled, continue like normal.")
        else:
            print("Error Occurred: ", resp_json)
            print("Error Code: ",error_code)

def processContent(content_type,base_url,headers,tenantID,start_time,end_time):

        json_data = {} #empty dict
        #List content from given subscription
        print("Listing Content for content type: ",content_type,"\n\n\n")
        list_avail_content_url = base_url + '/subscriptions/content'
        list_content_payload = {'contentType' : content_type,
                                              'PublisherIdentifier': tenantID,
                                              'startTime' : start_time,
                                              'endTime' : end_time}
        #List if available content exists for given contentType
        resp = requests.get(list_avail_content_url, headers=headers,params=list_content_payload)
        resp_json = resp.json()
        if resp.status_code == 200:
            #Iterate content objects
            #print("Data: ", resp_json)
            print("List URL: ", str(resp.url))
            #Call content and process it
            for content_object in resp_json:
                content_uri = content_object['contentUri']
                cont_resp = requests.get(content_uri, headers=headers)
                cont_resp_json = cont_resp.json()
                for event in cont_resp_json:
                    json_data.update(processEvent(event))
            #Check for next page of data and call it
            while 'NextPageUri' in resp.headers:
                #As long as pagination returns more data process it
                print("Next URL is: ",resp.headers['NextPageUri'])
                resp = requests.get(resp.headers['NextPageUri'], headers=headers)
                if resp.status_code == 200:
                    #Iterate content objects
                    #Call content and process it
                    for content_object in resp.json():
                        content_uri = content_object['contentUri']
                        cont_resp = requests.get(content_uri, headers=headers)
                        cont_resp_json = cont_resp.json()
                        #print("Header info test: ",cont_resp.headers)
                        for event in cont_resp_json:
                            print("Processing Event: ")
                            json_data.update(processEvent(event))
                else:
                    print("Some error occurred: ", resp.json())

        else:
            print("Some error occurred: ",resp_json)

        #Return json data
        return json_data

def processEvent(event):
    #Takes single json event as argument
    #Take some action on the data
    #Send to syslog
    #Email it
    #Parse and do deeper inspection with it
    """
        {
        "CreationTime": "2015-06-29T20:03:19",
        "Id": "80c76bd2-9d81-4c57-a97a-accfc3443dca",
        "Operation": "PasswordLogonInitialAuthUsingPassword",
        "OrganizationId": "41463f53-8812-40f4-890f-865bf6e35190",
        "RecordType": 9,
        "ResultStatus": "failed",
        "UserKey": "1153977025279851686@contoso.onmicrosoft.com",
        "UserType": 0,
        "Workload": "AzureActiveDirectory",
        "ClientIP": "134.170.188.221",
        "ObjectId": "admin@contoso.onmicrosoft.com",
        "UserId": "admin@contoso.onmicrosoft.com",
        "AzureActiveDirectoryEventType": 0,
        "ExtendedProperties": [
            {
                "Name": "LoginError",
                "Value": "-2147217390;PP_E_BAD_PASSWORD;The entered and stored passwords do not match."
            }
        ],
        "Client": "Exchange",
        "LoginStatus": -2147217390,
        "UserDomain": "contoso.onmicrosoft.com"
    },
    """
    #Return json dict
    return  event
    #print("Event: ", event)
