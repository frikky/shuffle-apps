## AWS IAM App
Aws IAM (Identity and Access Management) app for managing IAM operations from the shuffle.

![alt_text](https://github.com/Shuffle/python-apps/blob/master/aws-iam/1.0.0/aws-iam.png?raw=true)

## Actions

| No. | Action | Description | Parameters |
|-----|--------|-------------|------------|
|1 | Get user | Retrieves information about the specified IAM user, including the user's creation date, path, unique ID, and ARN | access_key, secret_key, region, user_name
|2 | Change password | Change password of the specified user | access_key, secret_key, region, username, password
|3 | List users | Lists the IAM users | access_key, secret_key, region, path_prefix, marker, max_items
|4 | List user tags | Lists the tags that are attached to the specified IAM user | access_key, secret_key, region, user_name, marker, max_items
|5 | List attached user policies | Lists all managed policies that are attached to the specified IAM user | access_key, secret_key, region, user_name, marker, max_items
|6 | Attach user policy | Attach policy to the user | access_key, secret_key, region, username, policy_arn
|7 | Get instance profile | Retrieves information about the specified instance profile, including the instance profile's path, GUID, ARN, and role. | access_key, secret_key, region, instance_profile_name
|8 | List access keys | List all access keys | access_key, secret_key, region, username, marker, max_items
|9 | List ssh public keys | List SSH public keys | access_key, secret_key, region, username, marker, max_items

__Note__: access_key, secret_key and region are used for authentication.

## Requirements

1. AWS account
2. Access key, Secret key and region of the user.

- __How to find access key & secret key ?__
1. Open https://console.aws.amazon.com/
2. From navbar click on user dropwodown &#8594; My Security Credentials.
3. Open the Access keys tab, and then choose Create access key.
4. To see the new access key, choose Show. Your credentials resemble the following:
   - Access key ID: AKIAIOSFODNN7EXAMPLE
   - Secret access key: wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY

 ## Note
 Some actions have marker and max_items parameters (Both are used for paginating results).
 - marker : Use this parameter only when paginating results and only after you receive a response indicating that the results are truncated. Set it to the value of the marker element in the response that you received to indicate where the next call should start.
 - max_items : Use this only when paginating results to indicate the maximum number of items you want in the response.
