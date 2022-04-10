## AWS Cloudwatch logs
AWS Cloudwatch app to interact with Amazon CLoudswatch from Shuffle. For more information check out [Cloudwatch logs documentation](https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/WhatIsCloudWatchLogs.html)

## Actions
Parameters written in **Bold** are required. <br />
access_key, secret_key and region are used for authentication.

| No. | Action | Description | Parameters |
|-----|--------|-------------|------------|
|1 | create_log_group | Creates a log group with the specified name |  **log_group_name**, kms_key_id, tags
|2 | delete_log_group | Delete a log group with the specified name |  **log_group_name**
|3 | get_log_events | Lists log events from the specified log stream | **log_group_name**, **log_stream_name**, limit, **start_time**, **end_time**, **start_from_head**,next_token
|4 | start_query | Schedules a query of a log group using CloudWatch Logs Insights. You specify the log group and time range to query and the query string to use. | log_group_name, log_group_list, limit, **start_time**, **end_time**, **query**
|5 | get_query_results | Only the fields requested in the query are returned, along with a @ptr field, which is the identifier for the log record. You can use the value of @ptr in a GetLogRecord operation to get the full log record. | **query_id**
|6 | get_log_record | Retrieves all of the fields and values of a single log event. | **log_record_pointer**
|7 | assign_retention_policy | Sets the retention of the specified log group. A retention policy allows you to configure the number of days for which to retain log events in the specified log group. | **log_group_name**, **retention_days**
|8 | create_export_task | Creates an export task, which allows you to efficiently export data from a log group to an Amazon S3 bucket. | **log_group_name**, log_stream_name_prefix, task_name, **from_time**, **to_time**, **destination**,destination_prefix

## Requirements

1. AWS account.
2. Make sure you have edequate permissions. Refer [this](https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/permissions-reference-cwl.html) for more information on persmissions required.
3. Access key, Secret key and region of the user.

- __How to find access key & secret key ?__
1. Open https://console.aws.amazon.com/
2. From navbar click on user dropwodown &#8594; My Security Credentials.
3. Open the Access keys tab, and then choose Create access key.
4. To see the new access key, choose Show. Your credentials resemble the following:
   - Access key ID: AKIAIOSFODNN7EXAMPLE
   - Secret access key: wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
