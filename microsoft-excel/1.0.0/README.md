# Microsoft Excel
- An app to interact with an excel file from Shuffle using Microsoft Graph Api.
- This app will help to insert, update and clear data of an excel workbook.

![App_image](https://github.com/Shuffle/python-apps/blob/master/microsoft-excel/1.0.0/Microsoft_excel.png?raw=true)

## Actions
- #### Get_user_id
    - Retrieve a list of user objects.
- #### Get_files
    - Gives information about files present in onedrive. Return a collection of DriveItems in the children relationship of a DriveItem.
- #### list_worksheets
    - Retrieve the properties and relationships of worksheet object.
- #### add_worksheets
    - Adds a new worksheet to the workbook. The worksheet will be added at the end of existing worksheets.
- #### delete_worksheet
    - Deletes the worksheet from the workbook.
- #### insert_or_update_data
    - Insert or Update the cell values associated with the range.
    - Parameter **address** will take input as follows:
        - StartCell Address : LastCell Address
        -  Example: A1:A3 (3 cells row wise)
        -  Example: A1:B2 (4 cells A1,B1,A2 and B2)
        -  Example: A1:C1 (3 cells column wise)
    - Parameter **value** will take input as follows:
        - Columns: Comma seperated
        - Rows: Semicolon seperated
        - Example: Row1Column1 ,Row1Column2 ; Row2Column1,Row2Column2
        - Example Input: 10,20;30,40
        - Example Output:
        - | Index | Column 1 | Column 2 |
            |-----|--------|-------------|
            |Row 1| 10 | 20 |
            |Row 2| 30 | 40 |
- #### clear_data
    - Deletes the cells associated with the range.

## Setup

- #### Register an App
#### Step 1: Go to the Azure Portal

 - You'll need to go to the [Azure Portal](https://portal.azure.com/) and login.

#### Step 2: Go to the Azure Active Directory Service

- Once you are logged into Azure, Register a new application so you can access
the Microsoft Graph API. To register a new application go to your **Azure Active Directory**
and once there go down to **App Registrations** a new window will pop up.

#### Step 3: Register a New App
- Set name of your choice.
- Select supported account type
- You don't have to set redirect URL.

#### Step 4: Generate client secret
- Go to your application &#8594; Certificates & Secrets &#8594; New client Secret
### Note
- You'll need Tenant ID, Client ID & client Secret Value for authentication (Tenant ID & Client ID are available under application overview and for Client Secret  go to Certificate & Secrets section).
- Make sure your application has adequate permissions.
- To add permission, Go to your application &#8594; API permission &#8594; Add permission (some of the permissions will require admin consent)
- For Excel app we need Files.ReadWrite.All, Sites.ReadWrite.All, User.ReadWrite.All permissions.
- After adding permission , Grant consent.
