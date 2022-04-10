# Checkpoint App
Checckpoint app for interacting with various checkpoint firewall functions from shuffle.
### Configure Checkpoint API server
1) Connect with SmartConsole to the Security Management Server.
2) From the left navigation panel, click Manage & Settings.
3) In the upper left section, click Blades.
4) In the Management API section, click Advanced Settings.
5) Configure the Startup Settings and the Access Settings.
- **Configure startup settings.**
 Select Automatic start to automatically start the API server when you start or reboot the Management Server.
- **Configure startup settings.**
Select one of these options to configure which clients can connect to the API Server:

  1) All IP addresses that can be used for GUI clients - You can send API requests from all IP addresses that are defined as Trusted Clients in SmartConsole. This includes requests from SmartConsole, Web services, and the mgmt_cli utility on the Management Server.

  2) All IP addresses - You can send API requests from all IP addresses. This includes requests from SmartConsole, Web services, and the mgmt_cli utility on the Management Server.

6) Publish the SmartConsole session.

7) Restart the API Server on the Management Server with this command:
```
api restart
```
Read more about setting up API server [here](https://sc1.checkpoint.com/documents/R81/WebAdminGuides/EN/CP_R81_SecurityManagement_AdminGuide/Topics-SECMG/Managing-Security-through-API.htm).

### Authentication
- Management server IP, username and password are used for authenticating with the checkpoint app.
- Make sure user have permissions to access the web APIs.

### Note
- Checkpoint API has limit of max 3 session per user per minute. If you're opening more than 3 sessions make sure to add delay among workflow nodes.
