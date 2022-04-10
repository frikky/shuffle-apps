import asyncio
import json
import os
import random
import socket
import time

import requests
import yara  # noreorder
from walkoff_app_sdk.app_base import AppBase

class Yara(AppBase):
    __version__ = "1.0.0"
    app_name = "yara"

    def __init__(self, redis, logger, console_logger=None):
        """
        Each app should have this __init__ to set up Redis and logging.
        :param redis:
        :param logger:
        :param console_logger:
        """
        super().__init__(redis, logger, console_logger)

    # Write your data inside this function
    #https://yara.readthedocs.io/en/latest/yarapython.html
    def download_rules(self, namespace):
        zipfiles = self.get_file_namespace(namespace)
        if zipfiles == None:
            return {
                "success": False,
                "reason": "Failed loading files from namespace %s" % namespace,
            }

        all_files = ""
        for name in zipfiles.namelist():
            for line in zipfiles.open(name).readlines():
                linedata = line.decode('utf-8')
                all_files += linedata

        return all_files

    # Write your data inside this function
    #https://yara.readthedocs.io/en/latest/yarapython.html
    def analyze_by_rule(self, file_id, rule, timeout=15):
        if timeout == 0 or not timeout:
            timeout = 15
        else:
            timeout = int(timeout)

        file_ret = self.get_file(file_id)
        #print("Getting file: %s" % file_id)
        #print("FINISHED GETTING FILE: %s" % file_ret)
        #rules.match(file)

        all_matches = []

        rule='rule dummy { condition: true }'
        rules = yara.compile(sources={
            'rule': rule,
        })

        matches = rules.match(data=file_ret["data"], timeout=timeout)
        if len(matches) > 0:
            for item in matches:
                submatch = {
                    "tags": item.tags,
                    "file": filepath,
                }

                try:
                    submatch["rule"] = item.rule.decode("utf-8")
                except:
                    print(f"Failed RULE decoding for {item.rule}")

                try:
                    submatch["match"] = item.strings.decode("utf-8")
                except:
                    print(f"Failed MATCH decoding for {item.strings}")

                all_matches.append(submatch)

        print("Matches: %d" % len(all_matches))
        print(all_matches)

        return_data = {
            "success": True,
            "matches": all_matches
        }

        try:
            return json.dumps(return_data)
        except (json.JSONDecodeError, TypeError):
            return return_data

    def find_files(self, get_dir):
        all_files = []
        data = os.listdir(get_dir)
        for filename in data:
            parsedpath = "%s/%s" % (get_dir, filename)
            if not filename.startswith(".") and os.path.isdir(parsedpath):
                #print("FOLDER: %s" % parsedpath)
                folderpaths = self.find_files(parsedpath)
                all_files.extend(folderpaths)
                #print("FOLDERPATHS: %s" % folderpaths)
                pass
            else:
                if filename.endswith(".yar"):
                    all_files.append(parsedpath)

        return all_files


    # Write your data inside this function
    #https://yara.readthedocs.io/en/latest/yarapython.html
    def analyze_file(self, file_id, timeout=15):
        if timeout == 0 or not timeout:
            timeout = 15
        else:
            timeout = int(timeout)

        print(f"Getting file {file_id} to be analyzed")
        file_ret = self.get_file(file_id)
        #print("FINISHED GETTING FILE: %s" % file_ret)
        #rules.match(file)

        all_matches = []
        failed_rules = []

        basefolder = "/rules"
        #filepaths = os.listdir(basefolder)
        filepaths = self.find_files(basefolder)
        #print(f"FILES: {filepaths}")
        print(f"LENGTH: {len(filepaths)}")
        total_string_matches = 0

        for filepath in filepaths:
            try:
                rules = yara.compile(filepath)
            except:
                print(f"[INFO] Rule {filepath} failed")
                failed_rules.append(filepath)
                continue

            matches = rules.match(data=file_ret["data"], timeout=timeout)
            if len(matches) > 0:
                for item in matches:
                    submatch = {
                        "rule": item.rule,
                        "tags": item.tags,
                        "file": filepath,
                        "matches": []
                    }

                    for string in item.strings:
                        try:
                            submatch["matches"].append({
                                "number": string[0],
                                "name": string[1],
                                "string": string[2].decode("utf-8"),
                            })
                        except:
                            print(f"Failed MATCH decoding for {string}")

                    submatch["total_matches"] = len(item.strings)
                    total_string_matches += len(item.strings)
                    all_matches.append(submatch)

        #print("Matches: %d" % len(all_matches))
        #print(all_matches)

        if len(all_matches) >= 10:
            all_matches = all_matches[0:9]

        return_data = {
            "success": True,
            "matches": all_matches,
            "failed_rules": len(failed_rules),
            "total_rule_files": len(filepaths),
            "total_string_matches": total_string_matches,
        }

        #print(f"RETURN: {return_data}")

        try:
            return json.dumps(return_data)
        except (json.JSONDecodeError, TypeError):
            return return_data

if __name__ == "__main__":
    Yara.run()
