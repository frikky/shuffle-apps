import asyncio
import json
import random
import socket
import time

import requests
from walkoff_app_sdk.app_base import AppBase


class GoogleChat(AppBase):
    __version__ = "1.0.0"
    app_name = "Google Chat"

    def __init__(self, redis, logger, console_logger=None):
        """
        Each app should have this __init__ to set up Redis and logging.
        :param redis:
        :param logger:
        :param console_logger:
        """
        super().__init__(redis, logger, console_logger)

    def send_simple_message(self, webhook_url, message, threadKey=""):
        headers = {'Content-Type': 'application/json'}
        payload = {'text': str(message)}
        # If a thread is specified, add the threakKey query parameter
        if threadKey != "":
            threadKey = "&threadKey=" + threadKey
        r = requests.request("POST", webhook_url+threadKey,
                             headers=headers, json=payload)
        if r.status_code == 200:
            data = r.json()
            return {"success": True, "results": data}
        return {"success": False, "reason": "Bad status code  - expecting 200.", "status_code": r.status_code, "response": r.json()}

    def send_card_message(self, webhook_url, message, app="Shuffle", threadKey=""):
        headers = {'Content-Type': 'application/json'}
        # If a thread is specified, add the threakKey query parameter
        if threadKey != "":
            threadKey = "&threadKey=" + threadKey
        # some custom conditions for different card style
        # Default is Shuffle
        if app == "PrismaCloud":
            title = "Prisma Cloud"
            imageUrl = "https://pan.dev/img/prismalogo.png"
        elif app == "TheHive":
            title = "TheHive"
            imageUrl = "https://docs.thehive-project.org/images/thehive.png"
        elif app == "CVE":
            title = "CVE"
            imageUrl = "https://pbs.twimg.com/profile_images/1334143546656493570/HgSlWtjG_400x400.jpg"
        elif app == "AWSWAF":
            title = "AWS WAF"
            imageUrl = "https://seeklogo.com/images/A/aws-waf-web-application-firewall-logo-03144CA778-seeklogo.com.png"
        elif app == "Splunk":
            title = "Splunk"
            imageUrl = "https://www.cb1security.com/wp-content/uploads/2018/09/Splunk-Logo.png"
        else:
            title = "Shuffle"
            imageUrl = "https://pbs.twimg.com/profile_images/1294997017622536193/xIv5yf0g.jpg"
        # Card-style default payload
        payload = {
            "cards": [
                {
                    "header": {
                        "title": title,
                        "imageUrl": imageUrl,
                        "imageStyle": "IMAGE"
                    },
                    "sections": [
                        {
                            "widgets": [
                                {
                                    "textParagraph": {
                                        "text": str(message)
                                    }
                                }
                            ]
                        }
                    ]
                }
            ]
        }
        r = requests.request("POST", webhook_url+threadKey,
                             headers=headers, json=payload)
        if r.status_code == 200:
            data = r.json()
            return {"success": True, "results": data}
        return {"success": False, "reason": "Bad status code  - expecting 200.", "status_code": r.status_code, "response": r.json()}


if __name__ == "__main__":
    GoogleChat.run()
