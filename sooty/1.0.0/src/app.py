import asyncio
import hashlib
import json
import random
import re
import socket
import time
import urllib

import requests
from ipwhois import IPWhois
from walkoff_app_sdk.app_base import AppBase

class Sooty(AppBase):
    __version__ = "1.0.0"
    app_name = "Sooty"  # this needs to match "name" in api.yaml

    # Write your data inside this function
    def Urlsanitise(self, url):
        # It comes in as a string, so needs to be set to JSON
        try:
            x = re.sub(r"\.", "[.]", url)
            x = re.sub("http://", "hxxp://", x)
            x = re.sub("https://", "hxxps://", x)
            return {"Success":"True",'Result':x}
        except Exception as e:
            raise Exception(e)

    def UrlDecoder(self, url):
        url = url.strip()
        decodedUrl = urllib.parse.unquote(url)
        return {"Success":"True",'DecodedUrl':decodedUrl}


    def SafelinksDecoder(self, url):
        url = url.strip()
        dcUrl = urllib.parse.unquote(url)
        dcUrl = dcUrl.replace('https://nam02.safelinks.protection.outlook.com/?url=', '')
        return {"Success":"True",'DcUrl':dcUrl}

    def UnshortenUrl(self, url):
        link = url.strip()
        req = requests.get(str('https://unshorten.me/s/' + link))
        return {"Success":"True",'UnshortenUrl':req.text}

    def Cisco7Decoder(self, password):
        pw = password.strip()

        key = [0x64, 0x73, 0x66, 0x64, 0x3b, 0x6b, 0x66, 0x6f, 0x41,
            0x2c, 0x2e, 0x69, 0x79, 0x65, 0x77, 0x72, 0x6b, 0x6c,
            0x64, 0x4a, 0x4b, 0x44, 0x48, 0x53, 0x55, 0x42]

        try:
            # the first 2 characters of the password are the starting index in the key array
            index = int(pw[:2],16)
            # the remaining values are the characters in the password, as hex bytes
            pw_text = pw[2:]
            pw_hex_values = [pw_text[start:start+2] for start in range(0,len(pw_text),2)]
            # XOR those values against the key values, starting at the index, and convert to ASCII
            pw_chars = [chr(key[index+i] ^ int(pw_hex_values[i],16)) for i in range(0,len(pw_hex_values))]
            pw_plaintext = ''.join(pw_chars)
            return {"Success":"True",'Result':pw_plaintext}
        except Exception as e:
            raise Exception(e)

    # def ReverseDnsLookup(self, ip):
    #     ip=ip.strip()
    #     try:
    #         s = socket.gethostbyaddr(ip)
    #         return str(s)
    #     except:
    #         return("Hostname not found")

    def DnsLookup(self, domainname):
        d = domainname.strip()
        d = re.sub("http://", "", d)
        d = re.sub("https://", "", d)
        try:
            s = socket.gethostbyname(d)
            return {"Success":"True",'Ip':s}
        except:
            return("Website not found")

    def HashText(self, text):
        return hashlib.md(text.encode("utf-8")).hexdigest()

    def WhoIs(self, ip):
        try:
            w = IPWhois(ip)
            w = w.lookup_whois()
            return w
        except Exception as e:
            raise Exception(e)


if __name__ == "__main__":
    Sooty.run()
