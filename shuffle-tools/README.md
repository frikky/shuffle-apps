# Shuffle tools App documentation
Shuffle tools is a utility app that simplifies your understanding of what happens in a node and also allows you to test on the fly.

## Actions
The Shuffle-tools app comes with a multitude of different actions, here we will check a few out and give a brief description.

1. Repeat back to me - This action does exactly what it says, repeats back to you what you want it to. Why is this important? You need to test as you go whilst creating your workflow, what results does the first node give and are the results okay to use in the subsequent nodes?

2. Router - Reroutes data between different nodes.

3. Check cache contains - Checks Shuffle cache whether a key contains a value in a list

4. Get cache value - Get a value savesd in your Shuffle organization

5. Send SMS Shuffle - Sends an SMS from Shuffle, currently working on getting a few demo trials.

6. Send E-mail Shuffle - Sends an Email from shuffle, currently working on getting a few demo trials.

7. Filter list - Takes a list and filters based on the data

8. Parse IOC - Parses Indicators of Compromise based on https://github.com/fhightower/ioc-finder

9. Translate Value - Takes a list of values and translates it in your input data

10. Map value - Takes a mapping dictionary and translates the input data. This is a search and replace for multiple fields.

11. Regex Capture Group - Returns objects matching the capture group

12. Regex replace - Replace all instances matching the regular expression

13. Parse List - Parses a list and  returns it as a JSON object

14. Execute Bash - Runs bash with the data input

15. Execute Python - Runs python with the data input. Any prints will be returned.

16. Get file value - This function is made for reading files. Prints out their data.

17. Download remote file - Downloads a file from a url

18. Get file meta - Gets file metadata

19. Delete file - Delete's file based on id

20. Extract archive - Extracts compressed files and returns file ids

21. Inflate archive - Compress files in an archive. Return file archive ids

22. XML JSON converter - Converts XML to JSON and vice versa

23. Date to epoch - converts a date field with a given format to an epoch time

24. Compare relative date - Compares an input date and a relative date and returns a True/False response

25. Add list to list - Can append single items to a list, can also add items of a list to another list

26. Merge lists - Merge lists of the same type and length

27. Diff Lists - Differentiates two lists of strings or integers and finds what's missing

28. Set JSON Key - Adds a JSON key to an existing object

29. Delete JSON Keys - Deletes keys in a JSON object

30. Convert JSON tags - Creates Key:Value pairs and converts JSON to tags

31. Run Math Operation - Runs an arithmetic operation

32. Escape HTML - Performs HTML escaping on field

33. Base 64 Conversion - Encodes or Decodes a base64 string

34. Get time stamp - Gets a timestamp for right now. Default returns epoch time

35. Get Hash sum - Returns multiple format of hashes based on the input value

36. Cidr IP match - Check if an IP is contained in a CIDR defined network
