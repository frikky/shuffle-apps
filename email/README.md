## Using curl to test whether you SMPT mails are getting delivered.
```
curl --ssl smtp://1.1.1.1:587 --mail-from example@example.com --mail-rcpt example1@example.com --upload-file email.txt --user 'example:Password123' -k -v
```

## email.txt : Should contain the below
```
From: <example@example.com>
To: <example1@example.com>
Subject: an example.com example email
Date: Thu, 24 Mar 2022 11:29:16

Welcome to this example email. What a lovely day
```
