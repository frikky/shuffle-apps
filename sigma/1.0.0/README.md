# Sigma
Based on [https://github.com/SigmaHQ/sigma](https://github.com/SigmaHQ/sigma)

Goal of this app is to translate generic sigma rules into the language of your choice.

## Requirements
1. Create a sigma namespace in Shuffle's filesystem:
```
curl https://shuffler.io/api/v1/files/create -H "Authorization: Bearer 09627dcb-7e2a-4843-819b-417d268ff840" -d '{"filename": "tmp.yml", "org_id": "11f67b76-6051-4425-b0d6-be23daac6d12", "workflow_id": "global", "namespace": "sigma"}'
```

2. Go to the Sigma file namespace and upload some rules from Sigma's [Rule repository](https://github.com/SigmaHQ/sigma/tree/master/rules)
![image](https://user-images.githubusercontent.com/5719530/159381443-fccd0f10-69ea-432a-827b-0f7f4c658942.png)

3. Make a new workflow and fill in the variables. The "shuffle_namespace" MUST match the namespace you made for your files and uploaded them into.
4. ![image](https://user-images.githubusercontent.com/5719530/159381597-584b47b7-b6cf-4e85-bbe7-72460e81a46b.png)

4. Run it! As seen in the image above, it returns rules as such:
- Based on Kibana search query
- Uses the sysmon backend
- Uses rules added as files to Shuffle's filesystem


## Continueation
In the case above, we used Kibana. The result can now be used, e.g. on a schedule to search in the siem using the correct API call

Want to use Sigma from Shuffle? [Contact us to help test it](support@shuffler.io)!
