## AWS EC2 App
AWS EC2 (Elastic Compute Cloud) app to interact with Amazon EC2 from Shuffle.

![alt_text](https://github.com/frikky/Shuffle-apps/blob/master/aws-ec2/1.0.0/ec2.png?raw=true)

## Actions

| No. | Action | Description | Parameters |
|-----|--------|-------------|------------|
|1 | Create Image | Creates an Amazon EBS-backed AMI from an Amazon EBS-backed instance that is either running or stopped. | access_key, secret_key, region, **InstanceId**, Description, **Name**, NoReboot, **DryRun**
|2 | Deregister Image | Deregisters the specified AMI (Amazon Machine Image). | access_key, secret_key, region, **ImageId**, **DryRun**
|3 | Create snapshot | Creates a snapshot of an EBS volume and stores it in Amazon S3. | access_key, secret_key, region, Description, **VolumeId**, **DryRun**
|4 | Delete snapshot | Deletes the specified snapshot. | access_key, secret_key, region, user_name, **SnapshotId**, **DryRun**
|5 | Create network interface | Creates a network interface in the specified subnet. | access_key, secret_key, region, Description, **Subnetid**, **DryRun**
|6 | Delete network interface | Deletes the specified network interface. | access_key, secret_key, region, user_name, **NetworkInterfaceId**, **DryRun**
|7 | Describe address | Describes the specified Elastic IP addresses or all of your Elastic IP addresses. | access_key, secret_key, region, *PublicIps*, **DryRun**
|8 | Describe keypair | Describes the specified key pairs or all of your key pairs. | access_key, secret_key, region, *KeyNames*, *KeyPairIds*, **DryRun**
|9 | Describe networkacls | Describes one or more of your network ACLs. | access_key, secret_key, region, ***NetworkAclIds***, **DryRun**
|10 | Describe securitygroups | Describes the specified security groups or all of your security groups. | access_key, secret_key, region, *GroupIds*, **DryRun**
|11 | Describe_vpc | Describes one or more of your VPCs | access_key, secret_key, region, *VpcIds*, **DryRun**
|12 | Get rules | Gets the rules for an ACL ID, A resource representing an EC2 NetworkAcl | access_key, secret_key, region, **NetworkAclId**, **DryRun**
|13 | Block ip | Creates a new firewall entry to block an IP | access_key, secret_key, region, **NetworkAclId**, **ip**, **direction**, **DryRun**
|14 | instance state change | Termiante/Start/Stop an EC2 Instance | access_key, secret_key, region, **instance_id**, **action**, **DryRun**
|15 | Create acl_entry| Creates an ACL entry |access_key, secret_key, region, **NetworkAclId** , **cidr_block**, **direction**, **portrange_from**, **portrange_to**, **protocol**, **rule_action**, **rule_number**, **DryRun**

__Note__:
- access_key, secret_key and region are used for authentication.
- **Bold** Parameters are compulsory required.
- *Italic* Parameters can take single value as well as multiple values in comma separated manner (E.g. value1,value2,value3 )
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
 
