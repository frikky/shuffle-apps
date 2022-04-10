## Microsoft Intune
- An app to interact with Microsoft Intune.

### Authentication
To authenticate this app, you'll need an app registered in the Azure Portal. This app should use what's called **"application permissions"**, NOT "delegated permissions". More about this farther down. **Make sure to have admin consent**.

**Required**:
- tenant_id
- client_id
- client_secret

### Permissions
Permissions are meant to be granular according to your needs. Make sure to not give too many permissions. To make the whole app work, add the following permissions to your app. How to register an app farther down.

**Application Permissions:**
- Device.Read.All
- Device.ReadWrite.All
- Directory.Read.All
- Directory.ReadWrite.All
- DeviceManagementManagedDevices.Read.All
- DeviceManagementManagedDevices.ReadWrite.All
- DeviceManagementApps.Read.All
- DeviceManagementApps.ReadWrite.All

## How to register app in Active Directory on Azure portal ?

### Step 1: Go to the Azure portal

 - You'll need to go to the [Azure Portal](https://portal.azure.com/#blade/Microsoft_AAD_RegisteredApps/ApplicationsListBlade) and login.

### Step 2: Go to the Azure Active Directory Service

- Once you are logged into Azure, Register a new application so you can access
the Microsoft Graph API. To register a new application go to your **Azure Active Directory**
and once there go down to **App Registrations** a new window will pop up.

### Step 3: Register a New App
- Set name of your choice.
- Select supported account type.
- You don't have to set redirect URL.

### Step 4: Generate client secret
- Go to your application &#8594; Certificates & Secrets &#8594; New client Secret.

## Note
- You'll need Tenant ID, Client ID & client Secret for authentication (Tenant ID & Client ID are available under application overview and for Client Secret  go to Certificate & Secrets section).
- Make sure your application has adequate permissions.
- Each action may require different permission to run. To add permissions, Go to your application in azure portal &#8594; API permission &#8594; Add permission (some of the permissions will require admin consent).
- After adding permission , Grant consent.
- Be sure to use work / business account. Most of the actions are not supported on personal account.
