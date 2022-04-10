# Thehive App

## Configuration

![conf](conf.png)

### Thehive3
- Leave **Organisation** empty

### Thehive4

**For unique api user by organisation:**
- Each action for a different organisation, you need to set the **Apikey** for that user/organisation
- Leave **Organisation** empty

**For same api user across the organisations:**
- Setup the user **Apikey**
- Each action for a different organisation, you need to specify the **Organisation**

**Note:** You may want one api key from thehive to be used by Shuffle or one per org, so the configuration of the Thehive App depends on your choice.

Of course on each use case, you can setup an **Authentication**, and every time you add a new node
you just need to select from the list which authentication to use. The only different will be
between having multiple api users or a single one. -- recommended way
