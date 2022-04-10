import asyncio
import json
import random
import socket
import time

import requests
from walkoff_app_sdk.app_base import AppBase

class Netcraft(AppBase):
    __version__ = "1.0.0"
    app_name = "netcraft"

    def __init__(self, redis, logger, console_logger=None):
        """
        Each app should have this __init__ to set up Redis and logging.
        :param redis:
        :param logger:
        :param console_logger:
        """
        super().__init__(redis, logger, console_logger)

    def report_attack(self, user, password, attack, comment):
        url = "https://takedown.netcraft.com/apis/authorise.php"
        headers = {
            "Content-Type": "application/json"
        }

        data = {
            "attack": attack,
            "comment": comment,
        }

        auth = (user, password)
        return requests.post(url, auth=auth, headers=headers, data=data).text

    # Can add a lot more to this
    def get_takedowns(self, user, password, id="", group_id="", url="", ip="", attack_url="", domain_attack="", statuses="", phishkit_only=""):
        url = "https://takedown.netcraft.com/apis/get-info.php"
        headers = {
            "Content-Type": "application/json"
        }

        # Set from-date to 2019-01-01 or >6m as its super slow otherwise
        params = {
            "id_after": "6000000"
        }

        if id:
            params["id"] = id
        if group_id:
            params["group_id"] = group_id
        if url:
            params["url"] = url
        if ip:
            params["ip"] = ip
        if attack_url:
            params["attack_url"] = attack_url
        if domain_attack:
            params["domain_attack"] = domain_attack
        if statuses:
            params["statuses"] = statuses
        if phishkit_only:
            params["phishkit_only"] = phishkit_only

        auth = (user, password)
        return requests.get(url, auth=auth, headers=headers, params=params).text

    def get_takedown(self, user, password, id="", group_id=""):
        url = "https://takedown.netcraft.com/apis/get-info.php"
        headers = {
            "Content-Type": "application/json"
        }

        params = {
            "id": id,
            "group_id": group_id,
        }

        auth = (user, password)
        return requests.get(url, auth=auth, headers=headers, params=params).text

    def escalate_takedown(self, user, password, id):
        url = "https://takedown.netcraft.com/apis/escalate.php"
        headers = {
            "Content-Type": "application/json"
        }

        data = {
            "takedown_id": takedown_id,
        }

        auth = (user, password)
        return requests.post(url, auth=auth, headers=headers, data=data).text

    # This is a workaround lmao
    def screenshot(self, user, password, takedownurl, proxies="dk"):
        if not isinstance(proxies, list) or len(proxies) == 0:
            if ", " in proxies:
                proxies = proxies.split(", ")
            else:
                proxies = proxies.split(",")

        if len(takedownurl) == 0:
            print("The url to take down needs to be defined")
            return ""

        homepage = "https://takedown.netcraft.com"
        loginhost = "https://sso.netcraft.com"
        screenshoturl = "https://screenshot.netcraft.com/index.cgi"

        # Imitate firefox
        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0"
        }
        auth = (user, password)

        print("Making new session with CSRF tokens etc, imitating firefox (:")
        client = requests.Session()
        ret = client.get(homepage)
        csrf_token = ""
        for line in ret.text.split("\n"):
            if "csrf_token" in line:
                token_prefix = line.split(" ")[7]
                csrf_token = token_prefix.split("=")[1][1:-1]
                break

        if not csrf_token:
            print("Didn't find any csrf token")
            return ""

        logindata = {
            "csrf_token": csrf_token,
            "destination": "https://takedown.netcraft.com/",
            "credential_0": user,
            "credential_1": password
        }

        print("Logging in with user %s" % user)
        newret = client.post("%s/login" % loginhost, data=logindata, headers=headers, cookies=client.cookies)

        if len(client.cookies) <= 1:
            print("RAW: %s\n\nMissing cookies after login: %s" % (newret.text, newret.status_code))
            return ""

        screenshotparams = {
            "url": takedownurl,
            "type": "interface",
            "level": "customer",
            "proxy_cc": ",".join(proxies),
            "proxy_single": "1"
        }

        print("Taking screenshot of %s" % takedownurl)
        ret = client.post(screenshoturl, data=screenshotparams, headers=headers)
        if ret.status_code != 200:
            print("RAW: %s\n\nBad status code: %d", ret.text, ret.status_code)
            return ""

        with open("/tmp/tmp", "w+") as tmp:
            tmp.write(ret.text)

        print(ret.headers)
        imageurl = ret.headers.get("Screenshot")
        for line in ret.text.split("\n"):
            if "Final URL" in line or "Immediate Redirect URL" in line:
                print(line)

        # Logging out
        print("Logging out of user %s" % user)
        client.post("%s/logout" % loginhost, data=logindata, headers=headers, cookies=client.cookies)

        return imageurl

# Run the actual thing after we've checked params
def run(request):
    action = request.get_json()
    print(action)
    print(type(action))
    authorization_key = action.get("authorization")
    current_execution_id = action.get("execution_id")

    if action and "name" in action and "app_name" in action:
        Netcraft.run(action)
        return f'Attempting to execute function {action["name"]} in app {action["app_name"]}'
    else:
        return f'Invalid action'

if __name__ == "__main__":
    Netcraft.run()
