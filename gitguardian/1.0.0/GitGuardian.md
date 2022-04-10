## GitGuardian
- An app to interact with GitGuardian's secret detection API.

## Requirements
- You'll need to generate an API token from your GitGuardian workspace.

## Actions
1) Content scan
- Scans text data to discover secrets inside them.
- Use file_id if you have file to scan otherwise use content if you have data coming from another node. Do not use both at once.

## Note
-  Max request payload size is 1 MB.
