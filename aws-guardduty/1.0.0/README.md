# AWS GuardDuty
Amazon Web Services Serverless Compute service (lambda)

## Actions
access_key, secret_key and region are used for authentication.
 **Bold** Parameters are compulsory required.

| No. | Action | Description | Parameters |
|-----|--------|-------------|------------|
|1 | Create Detector | Creates a single Amazon Guardduty detector | access_key, secret_key, region, **enable**
|2 | Delete Detector | Deletes a detector | access_key, secret_key, region, **detectorId**
|3 | Get Detector | Retrieves a detector | access_key, secret_key, region, **detectorId**
|4 | Update Detector | Updates the detector | access_key, secret_key, region, **detectorId**, **enable**
|5 | Create Ip Set | Create a new IPSet, which is called a trusted IP list in the console. | access_key, secret_key, region, **detectorId**, **name**, **fileformat**, **location**, **activate**
|6 | Delete Ip Set | Deletes the IPSet. | access_key, secret_key, region, **detectorId**, **ipSetId**
|7 | List Detectors | List Detector IDs | access_key, secret_key, region
|8 | Update Ip Set | Updates the IPSet. | access_key, secret_key, region, **detectorId**, **ipSetId**, **name**, **location**, **activate**
|9 | Get Ip Set | Retrieves the IPSet. | access_key, secret_key, region, **detectorId**, **ipSetId**
|10 | List Ip Sets | Lists the IpSets. | access_key, secret_key, region, **detectorId**
|11 | Create Threat Intel Set | Create a new ThreatIntelSet. | access_key, secret_key, region, **detectorId**, **name**, **fileformat**, **location**, **activate**
|12 | Delete Threat Intel Set | Deletes the ThreatIntelSet  | access_key, secret_key, region, **detectorId**, **threatIntelSetId**
|13 | Get Threat Intel Set | Retrieves the ThreatIntelSet. | access_key, secret_key, region, **detectorId**, **threatIntelSetId**
|14 | List Threat Intel Sets | Lists the ThreatIntelSets. | access_key, secret_key, region, **detectorId**
|15 | Update Threat Intel Set | Updates the ThreatIntelSet specified by the ThreatIntelSet ID. | access_key, secret_key, region, **detectorId**, **threatIntelSetId**, name, location, activate
|14 | List Findings | Lists the Findings. | access_key, secret_key, region, **detectorId**
|15 | Get Findings | Describes findings specified by finding IDs. | access_key, secret_key, region, **detectorId**, **findingIds**
|16 | Create Sample Findings | Generates example findings of types specified by the list of finding types. | access_key, secret_key, region, **detectorId**, findingIds
|17 | Archive Findings | Archieves findings that are specified by the list of finding IDs. | access_key, secret_key, region, **detectorId**, **findingIds**
|18 | Unarchive Findings | Unarchieves findings that are specified by the list of finding IDs. | access_key, secret_key, region, **detectorId**, **findingIds**
|19 | List Members | Lists details about all member accounts | access_key, secret_key, region, **detectorId**
|20 | Get Members | Retrieves member account | access_key, secret_key, region, **detectorId**,**accountIds**


__Note__:



## Requirements
1. AWS account
2. Access key, Secret key and region of the user.
- __How to find access key & secret key ?__
1. Open https://console.aws.amazon.com/
2. From navbar click on user dropwodown &#8594; My Security Credentials.
3. Open the Access keys tab, and then choose Create access key.
4. To see the new access key, choose Show. Your credentials resemble the following:
- Access key ID: AKIAIOSBODNN7EXAMPLE
- Secret access key: wJalrDTtnFEMI/K7MDENG/bGdRfiCYEXAMPLEKEY
Required AWS IAM Permissions and Roles for Lambda are documented here.
