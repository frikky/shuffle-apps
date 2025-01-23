## Google Workspace
An app for interacting with Google Workspace or GWS.
## Requirements
1) Enable the Admin SDK API from GCP console.
     - Login to Google cloud (Make sure you are using the same administrator acount that you're using for Google Workspace) and In the navigation menu on the left-hand side, click on “APIs & Services” > “Library”.
     - In the API Library, use the search bar to find the "Admin SDK". Click on it to open the API page.
     - Click the “Enable” button to activate the Admin SDK API for your project.
  2) Create a Service account.
	   - Go to the navigation menu, and select “IAM & Admin” > “Service Accounts”.
	   - Click on “Create Service Account” at the top of the page.
       - Enter a service account name and description, then click “Create”. 
       - You can skip the permission part here as we will be adding persmissions from GWS console later on.
       - In the service account details page, click on “Keys”.
		- Click on “Add Key” and select “Create new key”.
		-	Choose “JSON” as the key type and click “Create”. This will download the JSON key file which contains the “client_id”. Note down this client ID.

  3) Subject (Email address associated with the service account)
       - Note down the email address associated with the service account you just created it'll be used in the authentication in Shuffle.
  4) Adding permissions to the service account from GWS console.
	    - Signin to the Google Workspace admin console.
		- In the Admin console, locate the sidebar and navigate to Security > API controls. This area allows you to manage third-party and internal application access to your Google Workspace data.
		- Under the Domain-wide delegation section, click on “Manage Domain Wide Delegation” to view and configure client access.
		- If the service account client ID is not listed, you will add it; if it is already listed but you need to update permissions, click on the service account’s client ID. To add a new client ID:
			- Click on Add new.
			- Enter the Client ID of the service account you noted earlier when creating the service account in GCP.
			- In the OAuth Scopes field, enter the scopes required for your service account to function correctly. OAuth Scopes specify the permissions that your application requests. 
		- Depending on the actions you want to use below are the OAuth scopes required.

| Action              | OAuth Scope                                                                                                                                 |
|---------------------|---------------------------------------------------------------------------------------------------------------------------------------------|
| Reset User Password | `https://www.googleapis.com/auth/admin.directory.user`                                                                                      |
| Suspend User        | `https://www.googleapis.com/auth/admin.directory.user`                                                                                      |
| Get User Devices    |`https://www.googleapis.com/auth/admin.directory.device.mobile` |
| Reactivate User     | `https://www.googleapis.com/auth/admin.directory.user`                                                                                      

## Authentication
1) Upload the Service account JSON file in to the Shuffle files and copy the file id.
2) Now, Inside the GWS app authentication in Shuffle; use the file id you just copied and in subject use the email address asscoitate with your service account.


