import hmac
import datetime
import json
import time
import markupsafe
import os
import re
import subprocess
import tempfile
import zipfile
import base64
import ipaddress
import hashlib
from io import StringIO
from contextlib import redirect_stdout
import random
import string

import xmltodict
from json2xml import json2xml
from json2xml.utils import readfromstring

from ioc_finder import find_iocs
from dateutil.parser import parse as dateutil_parser
from google.auth import crypt
from google.auth import jwt

import py7zr
import pyminizip
import rarfile
import requests
import tarfile
import binascii
import struct

import paramiko
import concurrent.futures
import multiprocessing

from walkoff_app_sdk.app_base import AppBase

class Tools(AppBase):
    __version__ = "1.2.0"
    app_name = (
        "Shuffle Tools"  # this needs to match "name" in api.yaml for WALKOFF to work
    )

    def __init__(self, redis, logger, console_logger=None):
        """
        Each app should have this __init__ to set up Redis and logging.
        :param redis:
        :param logger:
        :param console_logger:
        """
        super().__init__(redis, logger, console_logger)

    def router(self):
        return "This action should be skipped"

    def base64_conversion(self, string, operation):
        if operation == "encode":
            # Try JSON decoding
            try:
                string = json.dumps(json.loads(string))
            except:
                pass

            encoded_bytes = base64.b64encode(str(string).encode("utf-8"))
            encoded_string = str(encoded_bytes, "utf-8")
            return encoded_string

        elif operation == "to image":
            # Decode the base64 into an image and upload it as a file
            decoded_bytes = base64.b64decode(string)

            # Make the bytes into unicode escaped bytes 
            # UnicodeDecodeError - 'utf-8' codec can't decode byte 0x89 in position 0: invalid start byte
            try:
                decoded_bytes = str(decoded_bytes, "utf-8")
            except:
                pass

            filename = "base64_image.png"
            file = {
                "filename": filename,
                "data": decoded_bytes, 
            }

            fileret = self.set_files([file])
            value = {"success": True, "filename": filename, "file_id": fileret}
            if len(fileret) == 1:
                value = {"success": True, "filename": filename, "file_id": fileret[0]}

            return value

        elif operation == "decode":
            try:
                decoded_bytes = base64.b64decode(string)
                try:
                    decoded_bytes = str(decoded_bytes, "utf-8")
                except:
                    pass

                # Check if json
                try:
                    decoded_bytes = json.loads(decoded_bytes)
                except:
                    pass

                return decoded_bytes
            except Exception as e:
                #return string.decode("utf-16")

                self.logger.info(f"[WARNING] Error in normal decoding: {e}")
                return {
                    "success": False,
                    "reason": f"Error decoding the base64: {e}",
                }
                #newvar = binascii.a2b_base64(string)
                #try:
                #    if str(newvar).startswith("b'") and str(newvar).endswith("'"):
                #        newvar = newvar[2:-1]
                #except Exception as e:
                #    self.logger.info(f"Encoding issue in base64: {e}")
                #return newvar

                #try:
                #    return newvar
                #except:
                #    pass

            return {
                "success": False,
                "reason": "Error decoding the base64",
            }

        return json.dumps({
            "success": False,
            "reason": "No base64 to be converted",
        })

    def parse_list_internal(self, input_list):
        if isinstance(input_list, list):
            input_list = ",".join(input_list)

        try:
            input_list = json.loads(input_list)
            if isinstance(input_list, list):
                input_list = ",".join(input_list)
            else:
                return json.dumps(input_list)
        except:
            pass

        input_list = input_list.replace(", ", ",", -1)
        return input_list

    # This is an SMS function of Shuffle
    def send_sms_shuffle(self, apikey, phone_numbers, body):
        phone_numbers = self.parse_list_internal(phone_numbers)

        targets = [phone_numbers]
        if ", " in phone_numbers:
            targets = phone_numbers.split(", ")
        elif "," in phone_numbers:
            targets = phone_numbers.split(",")

        data = {"numbers": targets, "body": body}

        url = "https://shuffler.io/api/v1/functions/sendsms"
        headers = {"Authorization": "Bearer %s" % apikey}
        return requests.post(url, headers=headers, json=data, verify=False).text

    # This is an email function of Shuffle
    def send_email_shuffle(self, apikey, recipients, subject, body, attachments=""):
        recipients = self.parse_list_internal(recipients)


        targets = [recipients]
        if ", " in recipients:
            targets = recipients.split(", ")
        elif "," in recipients:
            targets = recipients.split(",")

        data = {
            "targets": targets, 
            "subject": subject, 
            "body": body, 
            "type": "alert",
        }

        # Read the attachments
        if attachments != None and len(attachments) > 0:
            try:
                attachments = parse_list(attachments, splitter=",")
                files = []
                for item in attachments:
                    new_file = self.get_file(file_ids)
                    files.append(new_file)
            
                data["attachments"] = files
            except Exception as e:
                self.logger.info(f"Error in attachment parsing for email: {e}")
                

        url = "https://shuffler.io/api/v1/functions/sendmail"
        headers = {"Authorization": "Bearer %s" % apikey}
        return requests.post(url, headers=headers, json=data, verify=False).text

    def repeat_back_to_me(self, call):
        return call

    # https://github.com/fhightower/ioc-finder
    def parse_file_ioc(self, file_ids, input_type="all"):
        def parse(data):
            try:
                iocs = find_iocs(str(data))
                newarray = []
                for key, value in iocs.items():
                    if input_type != "all":
                        if key not in input_type:
                            continue
                    if len(value) > 0:
                        for item in value:
                            if isinstance(value, dict):
                                for subkey, subvalue in value.items():
                                    if len(subvalue) > 0:
                                        for subitem in subvalue:
                                            data = {
                                                "data": subitem,
                                                "data_type": "%s_%s" % (key[:-1], subkey),
                                            }
                                            if data not in newarray:
                                                newarray.append(data)
                            else:
                                data = {"data": item, "data_type": key[:-1]}
                                if data not in newarray:
                                    newarray.append(data)
                for item in newarray:
                    if "ip" in item["data_type"]:
                        item["data_type"] = "ip"
                return {"success": True, "items": newarray}
            except Exception as excp:
                return {"success": False, "message": "{}".format(excp)}

        if input_type == "":
            input_type = "all"
        else:
            input_type = input_type.split(",")

        try:
            file_ids = eval(file_ids)  # nosec
        except SyntaxError:
            file_ids = file_ids
        except NameError:
            file_ids = file_ids

        return_value = None
        if type(file_ids) == str:
            return_value = parse(self.get_file(file_ids)["data"])
        elif type(file_ids) == list and type(file_ids[0]) == str:
            return_value = [
                parse(self.get_file(file_id)["data"]) for file_id in file_ids
            ]
        elif (
            type(file_ids) == list
            and type(file_ids[0]) == list
            and type(file_ids[0][0]) == str
        ):
            return_value = [
                [parse(self.get_file(file_id2)["data"]) for file_id2 in file_id]
                for file_id in file_ids
            ]
        else:
            return "Invalid input"
        return return_value

    def parse_list(self, items, splitter="\n"):
        # Check if it's already a list first
        try:
            newlist = json.loads(items)
            if isinstance(newlist, list):
                return newlist

        except Exception as e:
            self.logger.info("[WARNING] Parse error - fallback: %s" % e)

        if splitter == "":
            splitter = "\n"

        splititems = items.split(splitter)

        return str(splititems)

    def get_length(self, item):
        if item.startswith("[") and item.endswith("]"):
            try:
                item = item.replace("'", '"', -1)
                item = json.loads(item)
            except json.decoder.JSONDecodeError as e:
                self.logger.info("Parse error: %s" % e)

        return str(len(item))

    def set_json_keys(self, json_object, keys_string, values_string):
        self.logger.info(f"OBJ: {json_object}\nKEY: {keys_string}\nVAL: {values_string}")
        if isinstance(json_object, str):
            try:
                json_object = json.loads(json_object)
            except json.decoder.JSONDecodeError as e:
                return {
                    "success": False,
                    "reason": "Item is not valid JSON"
                }

        if isinstance(json_object, list):
            if len(json_object) == 1:
                json_object = json_object[0]
            else:
                return {
                    "success": False,
                    "reason": "Item is valid JSON, but can't handle lists. Use .#"
                }

        keys = keys_string.split(",")
        values = values_string.split(",")

        for key, value in zip(keys, values):
            key = key.strip()
            value = value.strip()

            key_list = key.split(".")
            current = json_object

            for subkey in key_list[:-1]:
                current = current.setdefault(subkey, {})

            last_key = key_list[-1]

            if isinstance(value, str):
                  try:
                    value = json.loads(value)
                  except json.decoder.JSONDecodeError as e:
                      value = str(value)

            current[last_key] = value

        return json_object

    def delete_json_keys(self, json_object, keys):
        keys = self.parse_list_internal(keys)

        splitdata = [keys]
        if ", " in keys:
            splitdata = keys.split(", ")
        elif "," in keys:
            splitdata = keys.split(",")

        for key in splitdata:
            key = key.strip()
            try:
                del json_object[key]
            except:
                self.logger.info(f"[ERROR] Key {key} doesn't exist")

        return json_object

    def replace_value(self, input_data, translate_from, translate_to, else_value=""):
        splitdata = [translate_from]
        if ", " in translate_from:
            splitdata = translate_from.split(", ")
        elif "," in translate_from:
            splitdata = translate_from.split(",")

        if isinstance(input_data, list) or isinstance(input_data, dict):
            input_data = json.dumps(input_data)

        to_return = input_data
        if isinstance(input_data, str):
            found = False
            for item in splitdata:
                item = item.strip()
                if item in input_data:
                    input_data = input_data.replace(item, translate_to)
                    found = True

            if not found and len(else_value) > 0:
                input_data = else_value

        if input_data.lower() == "false":
            return False
        elif input_data.lower() == "true":
            return True

        return input_data

    def replace_value_from_dictionary(self, input_data, mapping, default_value=""):
        if isinstance(mapping, str):
            try:
                mapping = json.loads(mapping)
            except json.decoder.JSONDecodeError as e:
                return {
                    "success": False,
                    "reason": "Mapping is not valid JSON: %s" % e,
                }

        for key, value in mapping.items():
            try:
                input_data = input_data.replace(key, str(value), -1)
            except:
                self.logger.info(f"Failed mapping output data for key {key}")

        return input_data 

    # Changed with 1.1.0 to run with different returns 
    def regex_capture_group(self, input_data, regex):
        try:
            returnvalues = {
                "success": True,
            }

            matches = re.findall(regex, input_data)
            self.logger.info(f"{matches}")
            found = False
            for item in matches:
                if isinstance(item, str):
                    found = True 
                    name = "group_0" 
                    try:
                        returnvalues[name].append(item)
                    except:
                        returnvalues[name] = [item]

                else:
                    for i in range(0, len(item)):
                        found = True 
                        name = "group_%d" % i
                        try:
                            returnvalues[name].append(item[i])
                        except:
                            returnvalues[name] = [item[i]]

            returnvalues["found"] = found

            return returnvalues
        except re.error as e:
            return {
                "success": False,
                "reason": "Bad regex pattern: %s" % e,
            }

    def regex_replace(
        self, input_data, regex, replace_string="", ignore_case="False"
    ):

        #self.logger.info("=" * 80)
        #self.logger.info(f"Regex: {regex}")
        #self.logger.info(f"replace_string: {replace_string}")
        #self.logger.info("=" * 80)

        if ignore_case.lower().strip() == "true":
            return re.sub(regex, replace_string, input_data, flags=re.IGNORECASE)
        else:
            return re.sub(regex, replace_string, input_data)

    def execute_python(self, code):
        self.logger.info(f"Python code {len(code)}. If uuid, we'll try to download and use the file.")

        if len(code) == 36 and "-" in code:
            filedata = self.get_file(code)
            if filedata["success"] == False:
                return {
                    "success": False,
                    "message": f"Failed to get file for ID {code}",
                }

            if ".py" not in filedata["filename"]:
                return {
                    "success": False,
                    "message": f"Filename needs to contain .py",
                }


        # Write the code to a file
        # 1. Take the data into a file
        # 2. Subprocess execute file?
        try:
            f = StringIO()
            def custom_print(*args, **kwargs):
                return print(*args, file=f, **kwargs)
            
            #with redirect_stdout(f): # just in case
            # Add globals in it too
            globals_copy = globals().copy()
            globals_copy["print"] = custom_print

            # Add self to globals_copy
            for key, value in locals().copy().items():
                if key not in globals_copy:
                    globals_copy[key] = value

            globals_copy["self"] = self

            exec(code, globals_copy)

            s = f.getvalue()
            f.close() # why: https://www.youtube.com/watch?v=6SA6S9Ca5-U

            #try:
            #    s = s.encode("utf-8")
            #except Exception as e:
            #    self.logger.info(f"Failed utf-8 encoding response: {e}")

            try:
                return {
                    "success": True,
                    "message": json.loads(s.strip()),
                }
            except Exception as e:
                try:
                    return {
                        "success": True,
                        "message": s.strip(),
                    }
                except Exception as e:
                    return {
                        "success": True,
                        "message": s,
                    }
                
        except Exception as e:
            return {
                "success": False,
                "message": f"exception: {e}",
            }

    def execute_bash(self, code, shuffle_input):
        process = subprocess.Popen(
            code,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            shell=True,  # nosec
        )
        stdout = process.communicate()
        item = ""
        if len(stdout[0]) > 0:
            self.logger.info("[DEBUG] Succesfully ran bash!")
            item = stdout[0]
        else:
            self.logger.info(f"[ERROR] FAILED to run bash command {code}!")
            item = stdout[1]

        try:
            ret = item.decode("utf-8")
            return ret
        except Exception:
            return item

        return item

    # Check if wildcardstring is in all_ips and support * as wildcard
    def check_wildcard(self, wildcardstring, matching_string):
        wildcardstring = str(wildcardstring.lower())
        if wildcardstring in str(matching_string).lower():
            return True
        else:
            wildcardstring = wildcardstring.replace(".", "\.")
            wildcardstring = wildcardstring.replace("*", ".*")

            if re.match(wildcardstring, str(matching_string).lower()):
                return True

        return False

    def filter_list(self, input_list, field, check, value, opposite):
        self.logger.info(f"\nRunning function with list {input_list}")

        # Remove hashtags on the fly
        # E.g. #.fieldname or .#.fieldname

        flip = False
        if str(opposite).lower() == "true":
            flip = True

        try:
            #input_list = eval(input_list)  # nosec
            input_list = json.loads(input_list)
        except Exception:
            try:
                input_list = input_list.replace("'", '"', -1)
                input_list = json.loads(input_list)
            except Exception:
                self.logger.info("[WARNING] Error parsing string to array. Continuing anyway.")

        # Workaround D:
        if not isinstance(input_list, list):
            return {
                "success": False,
                "reason": "Error: input isnt a list. Please use conditions instead if using JSON.", 
                "valid": [],
                "invalid": [],
            }

            input_list = [input_list]

        if str(value).lower() == "null" or str(value).lower() == "none":
            value = "none"

        self.logger.info(f"\nRunning with check \"%s\" on list of length %d\n" % (check, len(input_list)))
        found_items = []
        new_list = []
        failed_list = []
        for item in input_list:
            try:
                try:
                    item = json.loads(item)
                except Exception:
                    pass

                # Support for nested dict key
                tmp = item
                if field and field.strip() != "":
                    for subfield in field.split("."):
                        tmp = tmp[subfield]

                if isinstance(tmp, dict) or isinstance(tmp, list):
                    try:
                        tmp = json.dumps(tmp)
                    except json.decoder.JSONDecodeError as e:
                        self.logger.info("FAILED DECODING: %s" % e)
                        pass

                #self.logger.info("PRE CHECKS FOR TMP: %")

                # EQUALS JUST FOR STR
                if check == "equals":
                    # Mostly for bools
                    # value = tmp.lower()

                    if str(tmp).lower() == str(value).lower():
                        self.logger.info("APPENDED BECAUSE %s %s %s" % (field, check, value))
                        new_list.append(item)
                    else:
                        failed_list.append(item)

                elif check == "equals any of":
                    self.logger.info("Inside equals any of")
                    checklist = value.split(",")
                    self.logger.info("Checklist and tmp: %s - %s" % (checklist, tmp))
                    found = False
                    for subcheck in checklist:
                        subcheck = str(subcheck).strip()

                        #ext.lower().strip() == value.lower().strip()
                        if type(tmp) == list and subcheck in tmp:
                            new_list.append(item)
                            found = True
                            break
                        elif type(tmp) == str and tmp == subcheck:
                            new_list.append(item)
                            found = True
                            break
                        elif type(tmp) == int and str(tmp) == subcheck:
                            new_list.append(item)
                            found = True
                            break
                        else:
                            if str(tmp) == str(subcheck):
                                new_list.append(item)
                                found = True
                                break
                            else:
                                print("Nothing matching")

                    if not found:
                        failed_list.append(item)

                # IS EMPTY FOR STR OR LISTS
                elif check == "is empty":
                    if str(tmp) == "[]":
                        tmp = []

                    if str(tmp) == "{}":
                        tmp = []

                    if type(tmp) == list and len(tmp) == 0:
                        new_list.append(item)
                    elif type(tmp) == str and not tmp:
                        new_list.append(item)
                    else:
                        failed_list.append(item)

                # STARTS WITH = FOR STR OR [0] FOR LIST
                elif check == "starts with":
                    if type(tmp) == list and tmp[0] == value:
                        new_list.append(item)
                    elif type(tmp) == str and tmp.startswith(value):
                        new_list.append(item)
                    else:
                        failed_list.append(item)

                # ENDS WITH = FOR STR OR [-1] FOR LIST
                elif check == "ends with":
                    if type(tmp) == list and tmp[-1] == value:
                        new_list.append(item)
                    elif type(tmp) == str and tmp.endswith(value):
                        new_list.append(item)
                    else:
                        failed_list.append(item)

                # CONTAINS FIND FOR LIST AND IN FOR STR
                elif check == "contains":
                    #if str(value).lower() in str(tmp).lower():
                    if str(value).lower() in str(tmp).lower() or self.check_wildcard(value, tmp): 
                        new_list.append(item)
                    else:
                        failed_list.append(item)

                elif check == "contains any of":
                    value = self.parse_list_internal(value)
                    checklist = value.split(",")
                    self.logger.info("CHECKLIST: %s. Value: %s" % (checklist, tmp))
                    found = False
                    for checker in checklist:
                        if str(checker).lower() in str(tmp).lower() or self.check_wildcard(checker, tmp): 
                            new_list.append(item)
                            found = True
                            break

                    if not found:
                        failed_list.append(item)

                # CONTAINS FIND FOR LIST AND IN FOR STR
                elif check == "field is unique":
                    #self.logger.info("FOUND: %s"
                    if tmp.lower() not in found_items:
                        new_list.append(item)
                        found_items.append(tmp.lower())
                    else:
                        failed_list.append(item)

                # CONTAINS FIND FOR LIST AND IN FOR STR
                elif check == "larger than":
                    list_set = False
                    try:
                        if str(tmp).isdigit() and str(value).isdigit():
                            if int(tmp) > int(value):
                                new_list.append(item)
                                list_set = True
                    except AttributeError as e:
                        self.logger.info("FAILED CHECKING LARGER THAN: %s" % e)
                        pass

                    try:
                        value = len(json.loads(value))
                    except Exception as e:
                        self.logger.info(f"[WARNING] Failed to convert destination to list: {e}")

                    try:
                        # Check if it's a list in autocast and if so, check the length
                        if len(json.loads(tmp)) > int(value):
                            new_list.append(item)
                            list_set = True
                    except Exception as e:
                        self.logger.info(f"[WARNING] Failed to check if larger than as list: {e}")

                    if not list_set:
                        failed_list.append(item)
                elif check == "less than":
                    # Old
                    #if int(tmp) < int(value):
                    #    new_list.append(item)
                    #else:
                    #    failed_list.append(item)

                    list_set = False
                    try:
                        if str(tmp).isdigit() and str(value).isdigit():
                            if int(tmp) < int(value):
                                new_list.append(item)
                                list_set = True
                    except AttributeError as e:
                        self.logger.info("FAILED CHECKING LARGER THAN: %s" % e)
                        pass

                    try:
                        value = len(json.loads(value))
                    except Exception as e:
                        self.logger.info(f"[WARNING] Failed to convert destination to list: {e}")

                    try:
                        # Check if it's a list in autocast and if so, check the length
                        if len(json.loads(tmp)) < int(value):
                            new_list.append(item)
                            list_set = True
                    except Exception as e:
                        self.logger.info(f"[WARNING] Failed to check if larger than as list: {e}")

                    if not list_set:
                        failed_list.append(item)

                elif check == "in cache key":
                    ret = self.check_cache_contains(value, tmp, "true")
                    if ret["success"] == True and ret["found"] == True:
                        new_list.append(item)
                    else:
                        failed_list.append(item)

                    #return {
                    #    "success": True,
                    #    "found": False,
                    #    "key": key,
                    #    "value": new_value,
                    #}

                # SINGLE ITEM COULD BE A FILE OR A LIST OF FILES
                elif check == "files by extension":
                    if type(tmp) == list:
                        file_list = []

                        for file_id in tmp:
                            filedata = self.get_file(file_id)
                            _, ext = os.path.splitext(filedata["filename"])
                            if (ext.lower().strip() == value.lower().strip()):
                                file_list.append(file_id)
                            # else:
                            #    failed_list.append(file_id)

                        tmp = item
                        if field and field.strip() != "":
                            for subfield in field.split(".")[:-1]:
                                tmp = tmp[subfield]
                            tmp[field.split(".")[-1]] = file_list
                            new_list.append(item)
                        else:
                            new_list = file_list
                        # else:
                        #    failed_list = file_list

                    elif type(tmp) == str:
                        filedata = self.get_file(tmp)
                        _, ext = os.path.splitext(filedata["filename"])
                        if ext.lower().strip() == value.lower().strip():
                            new_list.append(item)
                        else:
                            failed_list.append(item)

            except Exception as e:
                self.logger.info("[WARNING] FAILED WITH EXCEPTION: %s" % e)
                failed_list.append(item)
            # return

        if flip:
            tmplist = new_list
            new_list = failed_list
            failed_list = tmplist

        try:
            return json.dumps(
                {
                    "success": True,
                    "valid": new_list,
                    "invalid": failed_list,
                }
            )
            # new_list = json.dumps(new_list)
        except json.decoder.JSONDecodeError as e:
            return json.dumps(
                {
                    "success": False,
                    "reason": "Failed parsing filter list output" + e,
                }
            )

        return new_list

    #def multi_list_filter(self, input_list, field, check, value):
    #    input_list = input_list.replace("'", '"', -1)
    #    input_list = json.loads(input_list)

    #    fieldsplit = field.split(",")
    #    if ", " in field:
    #        fieldsplit = field.split(", ")

    #    valuesplit = value.split(",")
    #    if ", " in value:
    #        valuesplit = value.split(", ")

    #    checksplit = check.split(",")
    #    if ", " in check:
    #        checksplit = check.split(", ")

    #    new_list = []
    #    for list_item in input_list:
    #        list_item = json.loads(list_item)

    #        index = 0
    #        for check in checksplit:
    #            if check == "equals":
    #                self.logger.info(
    #                    "Checking %s vs %s"
    #                    % (list_item[fieldsplit[index]], valuesplit[index])
    #                )
    #                if list_item[fieldsplit[index]] == valuesplit[index]:
    #                    new_list.append(list_item)

    #        index += 1

    #    # "=",
    #    # "equals",
    #    # "!=",
    #    # "does not equal",
    #    # ">",
    #    # "larger than",
    #    # "<",
    #    # "less than",
    #    # ">=",
    #    # "<=",
    #    # "startswith",
    #    # "endswith",
    #    # "contains",
    #    # "re",
    #    # "matches regex",

    #    try:
    #        new_list = json.dumps(new_list)
    #    except json.decoder.JSONDecodeError as e:
    #        return "Failed parsing filter list output" % e

    #    return new_list

    # Gets the file's metadata, e.g. md5
    def get_file_meta(self, file_id):
        headers = {
            "Authorization": "Bearer %s" % self.authorization,
        }

        ret = requests.get(
            "%s/api/v1/files/%s?execution_id=%s"
            % (self.url, file_id, self.current_execution_id),
            headers=headers,
            verify=False,
        )
        self.logger.info(f"RET: {ret}")

        return ret.text

    # Use data from AppBase to talk to backend
    def delete_file(self, file_id):
        headers = {
            "Authorization": "Bearer %s" % self.authorization,
        }
        self.logger.info("HEADERS: %s" % headers)

        ret = requests.delete(
            "%s/api/v1/files/%s?execution_id=%s"
            % (self.url, file_id, self.current_execution_id),
            headers=headers,
            verify=False,
        )
        return ret.text

    def create_file(self, filename, data):
        self.logger.info("Inside function")

        try:
            if str(data).startswith("b'") and str(data).endswith("'"):
                data = data[2:-1]
            if str(data).startswith("\"") and str(data).endswith("\""):
                data = data[2:-1]
        except Exception as e:
            self.logger.info(f"Exception: {e}")

        try:
            #if not isinstance(data, str) and not isinstance(data, int) and not isinstance(float) and not isinstance(data, bool):
            if isinstance(data, dict) or isinstance(data, list):
                data = json.dumps(data)
        except:
            pass

        filedata = {
            "filename": filename,
            "data": data,
        }

        fileret = self.set_files([filedata])
        value = {"success": True, "filename": filename, "file_id": fileret}
        if len(fileret) == 1:
            value = {"success": True, "filename": filename, "file_id": fileret[0]}

        return value 

    # Input is WAS a file, hence it didn't get the files 
    def list_file_category_ids(self, file_category):
        return self.get_file_category_ids(file_category)

    # Input is WAS a file, hence it didn't get the files 
    def get_file_value(self, filedata):
        filedata = self.get_file(filedata)
        if filedata is None:
            return "File is empty?"

        self.logger.info("INSIDE APP DATA: %s" % filedata)
        try:
            return filedata["data"].decode()
        except:
            try:
                return filedata["data"].decode("utf-16")
            except:
                try:
                    return filedata["data"].decode("utf-8")
                except:
                    try:
                        return filedata["data"].decode("latin-1")
                    except:
                        return {
                            "success": False,
                            "reason": "Got the file, but the encoding can't be printed",
                        }

    def download_remote_file(self, url, custom_filename=""):
        ret = requests.get(url, verify=False)  # nosec
        filename = url.split("/")[-1]
        if "?" in filename:
            filename = filename.split("?")[0]

        if custom_filename and len(str(custom_filename)) > 0:
            filename = custom_filename

        fileret = self.set_files(
            [
                {
                    "filename": filename,
                    "data": ret.content,
                }
            ]
        )

        if len(fileret) > 0:
            value = {"success": True, "file_id": fileret[0]}
        else:
            value = {"success": False, "reason": "No files downloaded"}

        return value

    
    def extract_archive(self, file_id, fileformat="zip", password=None):
        try:
            return_data = {"success": False, "files": []}
            to_be_uploaded = []
            item = self.get_file(file_id)
            return_ids = None

            self.logger.info("Working with fileformat %s" % fileformat)
            with tempfile.TemporaryDirectory() as tmpdirname:

                # Get archive and save phisically
                with open(os.path.join(tmpdirname, "archive"), "wb") as f:
                    f.write(item["data"])

                # Grab files before, upload them later

                # Zipfile for zipped archive
                if fileformat.strip().lower() == "zip":
                    try:
                        self.logger.info("Starting zip extraction")
                        with zipfile.ZipFile(os.path.join(tmpdirname, "archive")) as z_file:
                            if password:
                                self.logger.info("In zip extraction with password")
                                z_file.setpassword(bytes(password.encode()))

                            self.logger.info("Past zip extraction")
                            for member in z_file.namelist():
                                filename = os.path.basename(member)
                                if not filename:
                                    continue

                                source = z_file.open(member)
                                to_be_uploaded.append(
                                    {"filename": source.name.split("/")[-1], "data": source.read()}
                                )

                                return_data["success"] = True
                    except (zipfile.BadZipFile, Exception):
                        return_data["files"].append(
                            {
                                "success": False,
                                "file_id": file_id,
                                "filename": item["filename"],
                                "message": "File is not a valid zip archive",
                            }
                        )

                elif fileformat.strip().lower() == "rar":
                    try:
                        with rarfile.RarFile(
                            os.path.join(tmpdirname, "archive")
                        ) as z_file:
                            if password:
                                z_file.setpassword(password)
                            for member in z_file.namelist():
                                filename = os.path.basename(member)
                                if not filename:
                                    continue

                                source = z_file.open(member)
                                to_be_uploaded.append(
                                    {"filename": source.name.split("/")[-1], "data": source.read()}
                                )

                                return_data["success"] = True
                    except Exception:
                        return_data["files"].append(
                            {
                                "success": False,
                                "file_id": file_id,
                                "filename": item["filename"],
                                "message": "File is not a valid rar archive",
                            }
                        )

                elif fileformat.strip().lower() == "tar":
                    try:
                        with tarfile.open(
                            os.path.join(tmpdirname, "archive"), mode="r"
                        ) as z_file:
                            for member in z_file.getnames():
                                member_files = z_file.extractfile(member)

                                if not member_files:
                                    continue

                                to_be_uploaded.append(
                                    {
                                        "filename": member.split("/")[-1],
                                        "data": member_files.read(),
                                    }
                                )
                            return_data["success"] = True
                    except Exception as e:
                        return_data["files"].append(
                            {
                                "success": False,
                                "file_id": file_id,
                                "filename": item["filename"],
                                "message": f"{e}",
                            }
                        )
                elif fileformat.strip().lower() == "tar.gz":
                    try:
                        with tarfile.open(os.path.join(tmpdirname, "archive"), mode="r:gz") as z_file:
                            for member in z_file.getnames():
                                member_files = z_file.extractfile(member)

                                if not member_files:
                                    continue

                                to_be_uploaded.append(
                                    {
                                        "filename": member.split("/")[-1],
                                        "data": member_files.read(),
                                    }
                                )

                            return_data["success"] = True

                    except Exception as e:
                        return_data["files"].append(
                            {
                                "success": False,
                                "file_id": file_id,
                                "filename": item["filename"],
                                "message": f"{e}",
                            }
                        )

                elif fileformat.strip().lower() == "7zip":
                    try:
                        with py7zr.SevenZipFile(
                            os.path.join(tmpdirname, "archive"),
                            mode="r",
                            password=password if password else None,
                        ) as z_file:
                            for filename, source in z_file.readall().items():
                                # Removes paths
                                filename = filename.split("/")[-1]
                                to_be_uploaded.append(
                                    {
                                        "filename": item["filename"].split("/")[-1],
                                        "data": source.read(),
                                    }
                                )
                                return_data["success"] = True
                    except Exception:
                        return_data["files"].append(
                            {
                                "success": False,
                                "file_id": file_id,
                                "filename": item["filename"],
                                "message": "File is not a valid 7zip archive",
                            }
                        )
                else:
                    return "No such format: %s" % fileformat

            self.logger.info("Breaking as this only handles one archive at a time.")
            if len(to_be_uploaded) > 0:
                return_ids = self.set_files(to_be_uploaded)
                self.logger.info(f"Got return ids from files: {return_ids}")

                for i in range(len(return_ids)):
                    return_data["archive_id"] = file_id
                    try:
                        return_data["files"].append(
                            {
                                "success": True,
                                "file_id": return_ids[i],
                                "filename": to_be_uploaded[i]["filename"],
                            }
                        )
                    except:
                        return_data["files"].append(
                            {
                                "success": True,
                                "file_id": return_ids[i],
                            }
                        )
            else:
                self.logger.info(f"No file ids to upload.")
                return_data["success"] = False
                return_data["files"].append(
                    {
                        "success": False,
                        "filename": "No data in archive",
                        "message": "Archive is empty",
                    }
                )

            return return_data

        except Exception as excp:
            return {"success": False, "message": "%s" % excp}

    def create_archive(self, file_ids, fileformat, name, password=None):
        try:
            # TODO: will in future support multiple files instead of string ids?
            if isinstance(file_ids, str):
                file_ids = file_ids.split()
            elif isinstance(file_ids, list):
                file_ids = file_ids
            else:
                return {
                    "success": False,
                    "reason": "Bad file_ids. Example: file_13eea837-c56a-4d52-a067-e673c7186483",
                }

            if len(file_ids) == 0:
                return {
                    "success": False,
                    "reason": "Make sure to send valid file ids. Example: file_13eea837-c56a-4d52-a067-e673c7186483,file_13eea837-c56a-4d52-a067-e673c7186484",
                }

            self.logger.info("picking {}".format(file_ids))
            # GET all items from shuffle
            items = [self.get_file(file_id) for file_id in file_ids]

            if len(items) == 0:
                return "No file to inflate"

            # Dump files on disk, because libs want path :(
            with tempfile.TemporaryDirectory() as tmpdir:
                paths = []
                self.logger.info("Number 1")
                for item in items:
                    with open(os.path.join(tmpdir, item["filename"]), "wb") as f:
                        f.write(item["data"])
                        paths.append(os.path.join(tmpdir, item["filename"]))

                # Create archive temporary
                self.logger.info("{} items to inflate".format(len(items)))
                with tempfile.NamedTemporaryFile() as archive:

                    if fileformat == "zip":
                        archive_name = "archive.zip" if not name else name
                        pyminizip.compress_multiple(
                            paths, [], archive.name, password, 5
                        )

                    elif fileformat == "7zip":
                        archive_name = "archive.7z" if not name else name
                        with py7zr.SevenZipFile(
                            archive.name,
                            "w",
                            password=password if len(password) > 0 else None,
                        ) as sz_archive:
                            for path in paths:
                                sz_archive.write(path)

                    else:
                        return "Format {} not supported".format(fileformat)

                    return_id = self.set_files(
                        [{"filename": archive_name, "data": open(archive.name, "rb")}]
                    )

                    if len(return_id) == 1:
                        # Returns the first file's ID
                        return {"success": True, "file_id": return_id[0]}
                    else:
                        return {
                            "success": False,
                            "message": "Upload archive returned {}".format(return_id),
                        }

        except Exception as excp:
            return {"success": False, "message": excp}

    def add_list_to_list(self, list_one, list_two):
        if not isinstance(list_one, list) and not isinstance(list_one, dict): 
            if not list_one or list_one == " " or list_one == "None" or list_one == "null":
                list_one = "[]"

            try:
                list_one = json.loads(list_one)
            except json.decoder.JSONDecodeError as e:
                self.logger.info("Failed to parse list1 as json: %s" % e)
                if list_one == None:
                    list_one = []
                else:
                    return {
                        "success": False,
                        "reason": f"List one is not a valid list: {list_one}" 
                    }

        if not isinstance(list_two, list) and not isinstance(list_two, dict):
            if not list_two or list_two == " " or list_two == "None" or list_two == "null":
                list_two = "[]"

            try:
                list_two = json.loads(list_two)
            except json.decoder.JSONDecodeError as e:
                self.logger.info("Failed to parse list2 as json: %s" % e)
                if list_one == None:
                    list_one = []
                else:
                    return {
                        "success": False,
                        "reason": f"List two is not a valid list: {list_two}"
                    }

        if isinstance(list_one, dict):
            list_one = [list_one]
        if isinstance(list_two, dict):
            list_two = [list_two]

        for item in list_two:
            list_one.append(item)

        return list_one

    def diff_lists(self, list_one, list_two):
        if isinstance(list_one, str):
            try:
                list_one = json.loads(list_one)
            except json.decoder.JSONDecodeError as e:
                self.logger.info("Failed to parse list1 as json: %s" % e)
                return {
                    "success": False,
                    "reason": "list_one is not a valid list."
                }

        if isinstance(list_two, str):
            try:
                list_two = json.loads(list_two)
            except json.decoder.JSONDecodeError as e:
                self.logger.info("Failed to parse list2 as json: %s" % e)
                return {
                    "success": False,
                    "reason": "list_two is not a valid list."
                }

        def diff(li1, li2):
            try:
                return list(set(li1) - set(li2)) + list(set(li2) - set(li1))
            except TypeError as e:
                # Bad json diffing - at least order doesn't matter :)
                not_found = []
                for item in list_one:
                    #item = sorted(item.items())
                    if item in list_two:
                        pass
                    else:
                        not_found.append(item)

                for item in list_two:
                    if item in list_one:
                        pass
                    else:
                        if item not in not_found:
                            not_found.append(item)

                return not_found

        newdiff = diff(list_one, list_two)
        parsed_diff = []
        for item in newdiff:
            if not item:
                continue

            parsed_diff.append(item)

        return {
            "success": True,
            "diff": newdiff,
        }


    def merge_lists(self, list_one, list_two, set_field="", sort_key_list_one="", sort_key_list_two=""):
        if isinstance(list_one, str):
            try:
                list_one = json.loads(list_one)
            except json.decoder.JSONDecodeError as e:
                self.logger.info("Failed to parse list1 as json: %s" % e)

        if isinstance(list_two, str):
            try:
                list_two = json.loads(list_two)
            except json.decoder.JSONDecodeError as e:
                self.logger.info("Failed to parse list2 as json: %s" % e)

        if not isinstance(list_one, list) or not isinstance(list_two, list):
            if isinstance(list_one, dict) and isinstance(list_two, dict):
                for key, value in list_two.items():
                    list_one[key] = value
            
                return list_one

            return {"success": False, "message": "Both input lists need to be valid JSON lists."}

        if len(list_one) != len(list_two):
            return {"success": False, "message": "Lists length must be the same. %d vs %d" % (len(list_one), len(list_two))}

        if len(sort_key_list_one) > 0:
            self.logger.info("Sort 1 %s by key: %s" % (list_one, sort_key_list_one))
            try:
                list_one = sorted(list_one, key=lambda k: k.get(sort_key_list_one), reverse=True)
            except:
                self.logger.info("Failed to sort list one")
                pass

        if len(sort_key_list_two) > 0:
            #self.logger.info("Sort 2 %s by key: %s" % (list_two, sort_key_list_two))
            try:
                list_two = sorted(list_two, key=lambda k: k.get(sort_key_list_two), reverse=True)
            except:
                self.logger.info("Failed to sort list one")
                pass

        # Loops for each item in sub array and merges items together
        # List one is being overwritten
        base_key = "shuffle_auto_merge"
        try:
            for i in range(len(list_one)):
                #self.logger.info(list_two[i])
                if isinstance(list_two[i], dict):
                    for key, value in list_two[i].items():
                        list_one[i][key] = value
                elif isinstance(list_two[i], str) and list_two[i] == "":
                    continue
                elif isinstance(list_two[i], str) or isinstance(list_two[i], int) or isinstance(list_two[i], bool):
                    self.logger.info("IN SETTER FOR %s" % list_two[i])
                    if len(set_field) == 0:
                        self.logger.info("Define a JSON key to set for List two (Set Field)")
                        list_one[i][base_key] = list_two[i]
                    else:
                        set_field = set_field.replace(" ", "_", -1)
                        list_one[i][set_field] = list_two[i]
        except Exception as e:
            return {
                "success": False,
                "reason": "An error occurred while merging the lists. PS: List one can NOT be a list of integers. If this persists, contact us at support@shuffler.io",
                "exception": f"{e}",
            }

        return list_one

    def merge_json_objects(self, list_one, list_two, set_field="", sort_key_list_one="", sort_key_list_two=""):
        return self.merge_lists(list_one, list_two, set_field=set_field, sort_key_list_one=sort_key_list_one, sort_key_list_two=sort_key_list_two)

    def fix_json(self, json_data):
        try:
            deletekeys = []
            copied_dict = json_data.copy()

            for key, value in copied_dict.items():
                if "@" in key or "." in key or " " in key:
                    deletekeys.append(key)

                    key = key.replace("@", "", -1)
                    key = key.replace(".", "", -1)
                    key = key.replace(" ", "_", -1)
                    json_data[key] = value

                if isinstance(value, dict):
                    json_data[key] = self.fix_json(value)
                else:
                    json_data[key] = value

                #elif isinstance(value, list):
                #    json_data[key] = value
                #else:
                #    json_data[key] = value
                #    #for item in json_data[key]:
                #    #    if isinstance(item, dict):
                #    #        json_data[
                    
            for key in deletekeys:
                del json_data[key]

        except Exception as e:
            print("[DEBUG] Problem in JSON (fix_json): %s" % e)

        return json_data

    def xml_json_convertor(self, convertto, data):
        if isinstance(data, dict) or isinstance(data, list):
            try:
                data = json.dumps(data)
            except:
                pass

        try:
            if convertto == "json":
                data = data.replace(" encoding=\"utf-8\"", " ")
                ans = xmltodict.parse(data)
                ans = self.fix_json(ans)
                json_data = json.dumps(ans)

                return json_data
            else:
                ans = readfromstring(data)
                return json2xml.Json2xml(ans, wrapper="all", pretty=True).to_xml()
        except Exception as e:
            return {
                "success": False,
                "input": data,
                "reason": f"{e}"
            }

    def date_to_epoch(self, input_data, date_field, date_format):

        self.logger.info(
            "Executing with {} on {} with format {}".format(
                input_data, date_field, date_format
            )
        )

        if isinstance(input_data, str):
            result = json.loads(input_data)
        else:
            result = input_data

        # https://docs.python.org/3/library/datetime.html#strftime-strptime-behavior
        epoch = datetime.datetime.strptime(result[date_field], date_format).strftime(
            "%s"
        )
        result["epoch"] = epoch
        return result

    def compare_relative_date(
        self, timestamp, date_format, equality_test, offset, units, direction
    ):
        if timestamp== "None":
            return False

        print("Converting input date.")
   
        if date_format == "autodetect":
            input_dt = dateutil_parser(timestamp).replace(tzinfo=None)
        elif date_format != "%s":
            input_dt = datetime.datetime.strptime(timestamp, date_format)
        else:
            input_dt = datetime.datetime.utcfromtimestamp(float(timestamp))

        offset = int(offset)
        if units == "seconds":
            delta = datetime.timedelta(seconds=offset)
        elif units == "minutes":
            delta = datetime.timedelta(minutes=offset)
        elif units == "hours":
            delta = datetime.timedelta(hours=offset)
        elif units == "days":
            delta = datetime.timedelta(days=offset)

        utc_format = date_format
        if utc_format.endswith("%z"):
            utc_format = utc_format.replace("%z", "Z")

        #if date_format != "%s" and date_format != "autodetect":
        if date_format == "autodetect":
            formatted_dt = datetime.datetime.utcnow() + delta
        elif date_format != "%s":
            formatted_dt = datetime.datetime.strptime(
                datetime.datetime.utcnow().strftime(utc_format), date_format
            )

        else:
            formatted_dt = datetime.datetime.utcnow()

        if date_format == "autodetect":
            comparison_dt = formatted_dt
        elif direction == "ago":
            comparison_dt = formatted_dt - delta
            #formatted_dt - delta
            #comparison_dt = datetime.datetime.utcnow()
        else:
            comparison_dt = formatted_dt + delta
            #comparison_dt = datetime.datetime.utcnow()

        print("{} {} {} is {}. Delta: {}".format(offset, units, direction, comparison_dt, delta))

        diff = int((input_dt - comparison_dt).total_seconds())
        print(
            "\nDifference between {} and {} is {} seconds ({} days)\n".format(timestamp, comparison_dt, diff, int(diff/86400))
        )

        if units == "seconds":
            diff = diff
        elif units == "minutes":
            diff = int(diff/60)
        elif units == "hours":
            diff = int(diff/3600)
        elif units == "days":
            diff = int(diff/86400)
        elif units == "week":
            diff = int(diff/604800)

        result = False
        if equality_test == ">":
            result = 0 > diff
            if direction == "ahead":
                result = not (result)

        elif equality_test == "<":
            result = 0 < diff
            if direction == "ahead":
                result = not (result)

        elif equality_test == "=":
            result = diff == 0 

        elif equality_test == "!=":
            result = diff != 0
        elif equality_test == ">=":
            result = 0 >= diff
            if direction == "ahead" and diff != 0:
                result = not (result)
        elif equality_test == "<=":
            result = 0 <= diff
            if direction == "ahead" and diff != 0:
                result = not (result)

        print(
            "At {}, is {} {} to    {} {} {}? {}. Diff {}".format(
                formatted_dt,
                timestamp,
                equality_test,
                offset,
                units,
                direction,
                result,
                diff,
            )
        )

        parsed_string = "%s %s %s %s" % (equality_test, offset, units, direction)
        newdiff = diff
        if newdiff < 0:
            newdiff = newdiff*-1

        return {
            "success": True,
            "date": timestamp,
            "check": parsed_string,
            "result": result,
            "diff": {
                "days": int(int(newdiff)/86400),
            },
        }


    def run_math_operation(self, operation):
        self.logger.info("Operation: %s" % operation)
        result = eval(operation)
        return result

    # This is kind of stupid
    def escape_html(self, input_data):
        if isinstance(input_data, str):
            mapping = json.loads(input_data)
        else:
            mapping = input_data

        self.logger.info(f"Got mapping {json.dumps(mapping, indent=2)}")

        result = markupsafe.escape(mapping)
        return mapping

    def check_cache_contains(self, key, value, append):
        org_id = self.full_execution["workflow"]["execution_org"]["id"]
        url = "%s/api/v1/orgs/%s/get_cache" % (self.url, org_id)
        data = {
            "workflow_id": self.full_execution["workflow"]["id"],
            "execution_id": self.current_execution_id,
            "authorization": self.authorization,
            "org_id": org_id,
            "search": str(value),
            "key": key,
        }

        if isinstance(value, dict) or isinstance(value, list):
            try:
                value = json.dumps(value)
            except Exception as e:
                self.logger.info(f"[WARNING] Error in JSON dumping (cache contains): {e}")
        
        if not isinstance(value, str):
            value = str(value)

        data["search"] = value

        if str(append).lower() == "true":
            append = True
        else:
            append = False 

        get_response = requests.post(url, json=data, verify=False)
        try:
            allvalues = get_response.json()
            try:
                if allvalues["value"] == None or allvalues["value"] == "null":
                    allvalues["value"] = "[]"
            except:
                pass

            if allvalues["success"] == False:
                if append == True:
                    new_value = [str(value)]
                    data["value"] = json.dumps(new_value)

                    set_url = "%s/api/v1/orgs/%s/set_cache" % (self.url, org_id)
                    set_response = requests.post(set_url, json=data, verify=False)
                    try:
                        allvalues = set_response.json()
                        #allvalues["key"] = key
                        #return allvalues

                        return {
                            "success": True,
                            "found": False,
                            "key": key,
                            "search": value,
                            "value": new_value,
                        }
                    except Exception as e:
                        return {
                            "success": False,
                            "found": False,
                            "key": key,
                            "search": value,
                            "reason": "Failed to find key, and failed to append",
                        }
                else:
                    return {
                        "success": True,
                        "found": False,
                        "key": key,
                        "search": value,
                        "reason": "Not appended, not found",
                    }
            else:
                if allvalues["value"] == None or allvalues["value"] == "null":
                    allvalues["value"] = "[]"

                allvalues["value"] = str(allvalues["value"])

                try:
                    parsedvalue = json.loads(allvalues["value"])
                except json.decoder.JSONDecodeError as e:
                    parsedvalue = [str(allvalues["value"])]
                except Exception as e:
                    print("Error parsing JSON - overriding: %s" % e)
                    parsedvalue = [str(allvalues["value"])]

                print("In ELSE2: '%s'" % parsedvalue)
                    
                try:
                    for item in parsedvalue:
                        #return "%s %s" % (item, value)
                        if item == value:
                            if not append:
                                return {
                                    "success": True,
                                    "found": True,
                                    "reason": "Found and not appending!",
                                    "key": key,
                                    "search": value,
                                    "value": json.loads(allvalues["value"]),
                                }
                            else:
                                return {
                                    "success": True,
                                    "found": True,
                                    "reason": "Found, was appending, but item already exists",
                                    "key": key,
                                    "search": value,
                                    "value": json.loads(allvalues["value"]),
                                }
                                
                            # Lol    
                            break
                except Exception as e:
                    print("Error in check_cache_contains: %s" % e)
                    parsedvalue = [str(parsedvalue)]
                    append = True

                if not append:
                    return {
                        "success": True,
                        "found": False,
                        "reason": "Not found, not appending (2)!",
                        "key": key,
                        "search": value,
                        "value": json.loads(allvalues["value"]),
                    }

                new_value = parsedvalue
                if new_value == None:
                    new_value = [value]

                new_value.append(value)
                data["value"] = json.dumps(new_value)

                set_url = "%s/api/v1/orgs/%s/set_cache" % (self.url, org_id)
                response = requests.post(set_url, json=data, verify=False)
                exception = ""
                try:
                    allvalues = response.json()
                    #return allvalues

                    return {
                        "success": True,
                        "found": False,
                        "reason": "Appended as it didn't exist",
                        "key": key,
                        "search": value,
                        "value": new_value,
                    }
                except Exception as e:
                    exception = e
                    pass

                return {
                    "success": False,
                    "found": True,
                    "reason": f"Failed to set append the value: {exception}. This should never happen",
                    "search": value,
                    "key": key
                }
                            
                self.logger.info("Handle all values!") 

            #return allvalues

        except Exception as e:
            print("[ERROR] Failed to handle cache contains: %s" % e)
            return {
                "success": False,
                "key": key,
                "reason": f"Failed to handle cache contains. Is the original value a list?: {e}",
                "search": value,
                "found": False,
            }

        return value.text 

    
    ## Adds value to a subkey of the cache
    ## subkey = "hi", value = "test", overwrite=False
    ## {"subkey": "hi", "value": "test"}
    ## subkey = "hi", value = "test2", overwrite=True
    ## {"subkey": "hi", "value": "test2"}
    ## subkey = "hi", value = "test3", overwrite=False
    ## {"subkey": "hi", "value": ["test2", "test3"]}

    #def set_cache_value(self, key, value):
    def change_cache_subkey(self, key, subkey, value, overwrite):
        org_id = self.full_execution["workflow"]["execution_org"]["id"]
        url = "%s/api/v1/orgs/%s/set_cache" % (self.url, org_id)

        if isinstance(value, dict) or isinstance(value, list):
            try:
                value = json.dumps(value)
            except Exception as e:
                self.logger.info(f"[WARNING] Error in JSON dumping (set cache): {e}")
        elif not isinstance(value, str):
            value = str(value)

        data = {
            "workflow_id": self.full_execution["workflow"]["id"],
            "execution_id": self.current_execution_id,
            "authorization": self.authorization,
            "org_id": org_id,
            "key": key,
            "value": value,
        }

        response = requests.post(url, json=data, verify=False)
        try:
            allvalues = response.json()
            allvalues["key"] = key
            #allvalues["value"] = json.loads(json.dumps(value))

            if (value.startswith("{") and value.endswith("}")) or (value.startswith("[") and value.endswith("]")):
                try:
                    allvalues["value"] = json.loads(value)
                except json.decoder.JSONDecodeError as e:
                    self.logger.info("[WARNING] Failed inner value cache parsing: %s" % e)
                    allvalues["value"] = str(value)
            else:
                allvalues["value"] = str(value)

            return json.dumps(allvalues)
        except:
            self.logger.info("Value couldn't be parsed")
            return response.text

    def delete_cache_value(self, key):
        return self.delete_cache(key)

    def get_cache_value(self, key):
        org_id = self.full_execution["workflow"]["execution_org"]["id"]
        url = "%s/api/v1/orgs/%s/get_cache" % (self.url, org_id)
        data = {
            "workflow_id": self.full_execution["workflow"]["id"],
            "execution_id": self.current_execution_id,
            "authorization": self.authorization,
            "org_id": org_id,
            "key": key,
        }

        value = requests.post(url, json=data, verify=False)
        try:
            allvalues = value.json()
            #self.logger.info("VAL1: ", allvalues)
            allvalues["key"] = key
            #self.logger.info("VAL2: ", allvalues)

            if allvalues["success"] == True and len(allvalues["value"]) > 0:
                allvalues["found"] = True
            else:
                allvalues["success"] = True 
                allvalues["found"] = False 

            try:
                parsedvalue = json.loads(allvalues["value"])
                allvalues["value"] = parsedvalue

            except:
                self.logger.info("Parsing of value as JSON failed")
                pass

            return json.dumps(allvalues)
        except:
            self.logger.info("Value couldn't be parsed, or json dump of value failed")
            return value.text

    # FIXME: Add option for org only & sensitive data (not to be listed)
    def set_cache_value(self, key, value):
        org_id = self.full_execution["workflow"]["execution_org"]["id"]
        url = "%s/api/v1/orgs/%s/set_cache" % (self.url, org_id)

        if isinstance(value, dict) or isinstance(value, list):
            try:
                value = json.dumps(value)
            except Exception as e:
                self.logger.info(f"[WARNING] Error in JSON dumping (set cache): {e}")
        
        if not isinstance(value, str):
            value = str(value)

        data = {
            "workflow_id": self.full_execution["workflow"]["id"],
            "execution_id": self.current_execution_id,
            "authorization": self.authorization,
            "org_id": org_id,
            "key": key,
            "value": value,
        }

        response = requests.post(url, json=data, verify=False)
        try:
            allvalues = response.json()
            allvalues["key"] = key
            #allvalues["value"] = json.loads(json.dumps(value))

            if (value.startswith("{") and value.endswith("}")) or (value.startswith("[") and value.endswith("]")):
                try:
                    allvalues["value"] = json.loads(value)
                except json.decoder.JSONDecodeError as e:
                    self.logger.info("[WARNING] Failed inner value cache parsing: %s" % e)
                    allvalues["value"] = str(value)
            else:
                allvalues["value"] = str(value)

            return json.dumps(allvalues)
        except:
            self.logger.info("Value couldn't be parsed")
            return response.text

    def convert_json_to_tags(self, json_object, split_value=", ", include_key=True, lowercase=True):
        if isinstance(json_object, str):
            try:
                json_object = json.loads(json_object)
            except json.decoder.JSONDecodeError as e:
                self.logger.info("Failed to parse list2 as json: %s. Type: %s" % (e, type(json_object)))

        if isinstance(lowercase, str) and lowercase.lower() == "true":
            lowercase = True
        else:
            lowercase = False

        if isinstance(include_key, str) or include_key.lower() == "true":
            include_key = True
        else:
            include_key = False

        parsedstring = []
        try:
            for key, value in json_object.items():
                self.logger.info("KV: %s:%s" % (key, value))
                if isinstance(value, str) or isinstance(value, int) or isinstance(value, bool):
                    if include_key == True:
                        parsedstring.append("%s:%s" % (key, value))
                    else:
                        parsedstring.append("%s" % (value))
                else:
                    self.logger.info("Can't handle type %s" % type(value))
        except AttributeError as e:
            return {
                "success": False,
                "reason": "Json Object is not a dictionary",
            }

        fullstring = split_value.join(parsedstring)
        if lowercase == True:
            fullstring = fullstring.lower()

        return fullstring

    def cidr_ip_match(self, ip, networks):
        self.logger.info("Executing with\nIP: {},\nNetworks: {}".format(ip, networks))

        if isinstance(networks, str):
            try:
                networks = json.loads(networks)
            except json.decoder.JSONDecodeError as e:
                self.logger.info("Failed to parse networks list as json: {}. Type: {}".format(
                    e, type(networks)
                ))
                return {
                    "success": False,
                    "reason": "Networks is not a valid list: {}".format(networks),
                }

        try:
            ip_networks = list(map(ipaddress.ip_network, networks))
            ip_address = ipaddress.ip_address(ip)
        except ValueError as e:
            return "IP or some networks are not in valid format.\nError: {}".format(e)

        matched_networks = list(filter(lambda net: (ip_address in net), ip_networks))

        result = {}
        result["ip"] = ip
        result['networks'] = list(map(str, matched_networks))
        result['is_contained'] = True if len(result['networks']) > 0 else False

        return json.dumps(result)

    def get_timestamp(self, time_format):
        timestamp = int(time.time())
        if time_format == "unix" or time_format == "epoch":
            self.logger.info("Running default timestamp %s" % timestamp)

        return timestamp

    def get_hash_sum(self, value):
        md5_value = ""
        sha256_value = ""

        try:
            md5_value = hashlib.md5(str(value).encode('utf-8')).hexdigest()
        except Exception as e:
            self.logger.info(f"Error in md5sum: {e}")

        try:
            sha256_value = hashlib.sha256(str(value).encode('utf-8')).hexdigest()
        except Exception as e:
            self.logger.info(f"Error in sha256: {e}")

        parsedvalue = {
            "success": True,
            "original_value": value,
            "md5": md5_value,
            "sha256": sha256_value,
        }

        return parsedvalue 

    def run_oauth_request(self, url, jwt):
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
        }

        data = "grant_type=urn%3Aietf%3Aparams%3Aoauth%3Agrant-type%3Ajwt-bearer&assertion=%s" % jwt

        return requests.post(url, data=data, headers=headers, verify=False).text

    # Based on https://google-auth.readthedocs.io/en/master/reference/google.auth.crypt.html
    def get_jwt_from_file(self, file_id, jwt_audience, scopes, complete_request=True):
        allscopes = scopes


        if "," in scopes:
            allscopes = " ".join(scopes.split(","))
     
        # Service account key path
        filedata = self.get_file(file_id)
        if filedata["success"] == False:
            return {
                "success": False,
                "message": f"Failed to get file for ID {file_id}",
            }
    
        data = json.loads(filedata["data"], strict=False)
        #sa_keyfile = ""
        sa_keyfile = data["private_key"]
        sa_email = data["client_email"]
    
        # The audience to target
        audience = jwt_audience
    
        """Generates a signed JSON Web Token using a Google API Service Account or similar."""
        def get_jwt(sa_keyfile,
                     sa_email,
                     audience,
                     allscopes,
                     expiry_length=3600):
        
            now = int(time.time())
            
            # build payload
            payload = {
                # expires after 'expiry_length' seconds.
                # iss must match 'issuer' in the security configuration in your
                # swagger spec (e.g. service account email). It can be any string.
                'iss': sa_email,
                # aud must be either your Endpoints service name, or match the value
                # specified as the 'x-google-audience' in the OpenAPI document.
                'scope': allscopes,
                'aud':  audience,
                "exp": now + expiry_length,
                'iat': now,

                # sub and email should match the service account's email address
                'sub': sa_email,
                'email': sa_email,
            }
            
            # sign with keyfile
            #signer = crypt.RSASigner.from_service_account_file(sa_keyfile)
            signer = crypt.RSASigner.from_string(sa_keyfile)
            jwt_token = jwt.encode(signer, payload)
            # print(jwt_token.decode('utf-8'))
            return jwt_token
    
    
        signed_jwt = get_jwt(sa_keyfile, sa_email, audience, allscopes)

        if str(complete_request).lower() == "true":
            return self.run_oauth_request(audience, signed_jwt.decode())
        else:
            return {
                "success": True,
                "jwt": signed_jwt.decode(),
            }

    def get_synonyms(self, input_type):
        if input_type == "cases":
            return {
                "id": [
                    "id",
                    "ref",
                    "sourceref",
                    "reference",
                    "sourcereference",
                    "alertid",
                    "caseid",
                    "incidentid",
                    "serviceid",
                    "sid",
                    "uid",
                    "uuid",
                    "teamid",
                    "messageid",
                  ],
                  "title": ["title", "message", "subject", "name"],
                  "description": ["description", "status", "explanation", "story", "details", "snippet"],
                  "email": ["mail", "email", "sender", "receiver", "recipient"],
                  "data": [
                    "data",
                    "ip",
                    "domain",
                    "url",
                    "hash",
                    "md5",
                    "sha2",
                    "sha256",
                    "value",
                    "item",
                    "rules",
                  ],
                  "tags": ["tags", "taxonomies", "labels", "labelids"],
                  "assignment": [
                    "assignment",
                    "user",
                    "assigned_to",
                    "users",
                    "closed_by",
                    "closing_user",
                    "opened_by",
                  ],
                  "severity": [
                    "severity",
                    "sev",
                    "magnitude",
                    "relevance",
                  ]
            }
        
        return []
    
    def find_key(self, inputkey, synonyms):
        inputkey = inputkey.lower().replace(" ", "").replace(".", "")
        for key, value in synonyms.items():
            if inputkey in value:
                return key
    
        return inputkey
    
    def run_key_recursion(self, json_input, synonyms):
        if isinstance(json_input, str) or isinstance(json_input, int) or isinstance(json_input, float):
            return json_input, {}
    
        if isinstance(json_input, list):
            if len(json_input) != 1:
                return json_input, {}
            else:
                json_input = json_input[0]
    
            #new_list = []
            #for item in json_input:
            #run_key_recursion(item, synonyms)
            #new_dict[new_key], found_important = run_key_recursion(value, synonyms)
    
        # Looks for exact key:value stuff in other format
        if len(json_input.keys()) == 2:
            newkey = ""
            newvalue = ""
            for key, value in json_input.items():
                if key == "key" or key == "name":
                    newkey = value
                elif key == "value":
                    newvalue = value
    
            if len(newkey) > 0 and len(newvalue) > 0:
                json_input[newkey] = newvalue
                try:
                    del json_input["name"]
                except:
                    pass
    
                try:
                    del json_input["value"]
                except:
                    pass
    
                try:
                    del json_input["key"]
                except:
                    pass
    
        important_fields = {}
        new_dict = {}
        for key, value in json_input.items():
            new_key = self.find_key(key, synonyms)
    
            if isinstance(value, list):
                new_list = []
                for subitem in value:
                    returndata, found_important = self.run_key_recursion(subitem, synonyms)
    
                    new_list.append(returndata)
                    for subkey, subvalue in found_important.items():
                        important_fields[subkey] = subvalue 
    
                new_dict[new_key] = new_list
    
            elif isinstance(value, dict):
                # FIXMe: Try to understand Key:Values as well by translating them
                # name/key: subject
                # value: This is a subject
                # will become:
                # subject: This is a subject
                    
                new_dict[new_key], found_important = self.run_key_recursion(value, synonyms)
    
                for subkey, subvalue in found_important.items():
                    important_fields[subkey] = subvalue
            else:
                new_dict[new_key] = value
    
            # Translated fields are added as important
            if key.lower().replace(" ", "").replace(".", "") != new_key:
                try:
                    if len(new_dict[new_key]) < str(important_fields[new_key]):
                        important_fields[new_key] = new_dict[new_key]
                except KeyError as e:
                    important_fields[new_key] = new_dict[new_key]
                except:
                    important_fields[new_key] = new_dict[new_key]
    
            #break
    
        return new_dict, important_fields
    
    # Should translate the data to something more useful
    def get_standardized_data(self, json_input, input_type):
        if isinstance(json_input, str):
            json_input = json.loads(json_input, strict=False)
    
        input_synonyms = self.get_synonyms(input_type)
        parsed_data, important_fields = self.run_key_recursion(json_input, input_synonyms)
    
        # Try base64 decoding and such too?
        for key, value in important_fields.items():
            try:
                important_fields[key] = important_fields[key][key]
            except:
                pass
    
            try:
                important_fields[key] = base64.b64decode(important_fields[key])
            except:
                pass
    
        return {
            "success": True,
            "original": json_input,
            "parsed": parsed_data,
            "changed_fields": important_fields,
        }

    def generate_random_string(length=16, special_characters=True):
        try:
            length = int(length)
        except:
            return {
                "success": False,
                "error": "Length needs to be a whole number",
            }

        # get random password pf length 8 with letters, digits, and symbols
        characters = string.ascii_letters + string.digits + string.punctuation
        if str(special_characters).lower() == "false":
            characters = string.ascii_letters + string.digits + string.punctuation

        password = ''.join(random.choice(characters) for i in range(length))

        return {
            "success": True,
            "password": password,
        }
    
    def run_ssh_command(self, host, port, user_name, private_key_file_id, password, command):
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        if port:
            port = int(port)
        else:
            port = 22

        if private_key_file_id:
            new_file = self.get_file(private_key_file_id)

            try:
                key_data = new_file["data"].decode()
            except Exception as e:
                return {"success":"false","message":str(e)}

            private_key_file = StringIO()
            private_key_file.write(key_data)
            private_key_file.seek(0)
            private_key = paramiko.RSAKey.from_private_key(private_key_file)
            
            try:
                ssh_client.connect(hostname=host,username=user_name,port=port, pkey= private_key)
            except Exception as e:
                return {"success":"false","message":str(e)}
        else:
            #print("AUTH WITH PASSWORD")
            try:
                ssh_client.connect(hostname=host,username=user_name,port=port, password=str(password))
            except Exception as e:
                return {"success":"false","message":str(e)}

        try:
            stdin, stdout, stderr = ssh_client.exec_command(str(command))
        except Exception as e:
            return {"success":"false","message":str(e)}

        return {"success":"true","output": stdout.read().decode(errors='ignore')}

    def parse_ioc(self, input_string, input_type="all"):
        ioc_types = ["domains", "urls", "email_addresses", "ipv4s", "ipv4_cidrs", "md5s", "sha256s", "sha1s", "cves"]

        # Remember overriding ioc types we care about
        if input_type == "" or input_type == "all":
            input_type = "all"
        else:
            input_type = input_type.split(",")
            for item in input_type:
                item = item.strip()

            ioc_types = input_type

        iocs = find_iocs(str(input_string), included_ioc_types=ioc_types)
        newarray = []
        for key, value in iocs.items():
            if input_type != "all":
                if key not in input_type:
                    continue

            if len(value) > 0:
                for item in value:
                    # If in here: attack techniques. Shouldn't be 3 levels so no
                    # recursion necessary
                    if isinstance(value, dict):
                        for subkey, subvalue in value.items():
                            if len(subvalue) > 0:
                                for subitem in subvalue:
                                    data = {
                                        "data": subitem,
                                        "data_type": "%s_%s" % (key[:-1], subkey),
                                    }
                                    if data not in newarray:
                                        newarray.append(data)
                    else:
                        data = {"data": item, "data_type": key[:-1]}
                        if data not in newarray:
                            newarray.append(data)

        # Reformatting IP
        for item in newarray:
            if "ip" in item["data_type"]:
                item["data_type"] = "ip"
                try:
                    item["is_private_ip"] = ipaddress.ip_address(item["data"]).is_private
                except:
                    self.logger.info("Error parsing %s" % item["data"])

        try:
            newarray = json.dumps(newarray)
        except json.decoder.JSONDecodeError as e:
            return "Failed to parse IOC's: %s" % e

        return newarray
    

    def split_text(self, text):
        # Split text into chunks of 10kb. Add each 10k to array
        # In case e.g. 1.2.3.4 lands exactly on 20k boundary, it may be useful to overlap here.
        # (just shitty code to reduce chance of issues) while still going fast
        arr_one = []
        max_len = 5000 
        current_string = ""
        overlaps = 100 

        for i in range(0, len(text)):
            current_string += text[i]
            if len(current_string) > max_len:
                # Appending just in case even with overlaps
                if len(text) > i+overlaps:
                    current_string += text[i+1:i+overlaps]
                else:
                    current_string += text[i+1:]

                arr_one.append(current_string)
                current_string = ""

        if len(current_string) > 0:
            arr_one.append(current_string)

        return arr_one 

    def _format_result(self, result):
        final_result = {}
        
        for res in result:
            for key,val in res.items():
                if key in final_result:
                    if isinstance(val, list) and len(val) > 0:
                        for i in val:
                            final_result[key].append(i)
                    elif isinstance(val, dict):
                        #print(key,":::",val)
                        if key in final_result:
                            if isinstance(val, dict):
                                for k,v in val.items():
                                    #print("k:",k,"v:",v)
                                    val[k].append(v)
                        #print(val)
                    #final_result[key].append([i for i in val if len(val) > 0])
                else:
                    final_result[key] = val

        return final_result

    # See function for how it works~: parse_ioc_new(..)
    def _with_concurency(self, array_of_strings, ioc_types):
        results = []
        #start = time.perf_counter()

        # Workers dont matter..?
        # What can we use instead? 
        print("Strings:", len(array_of_strings))

        workers = 4
        with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor:
            # Submit the find_iocs function for each string in the array
            futures = [executor.submit(
                find_iocs, 
                text=string, 
                included_ioc_types=ioc_types,
            ) for string in array_of_strings]

            # Wait for all tasks to complete
            concurrent.futures.wait(futures)

            # Retrieve the results if needed
            results = [future.result() for future in futures]
        
        #print("Total time taken:", time.perf_counter()-start)
        return self._format_result(results)

    # FIXME: Make this good and actually faster than normal
    # For now: Concurrency doesn't make it faster due to GIL in python.
    # May need to offload this to an executable or something 
    def parse_ioc_new(self, input_string, input_type="all"):
        if input_type == "":
            input_type = "all"

        ioc_types = ["domains", "urls", "email_addresses", "ipv4s", "ipv4_cidrs", "md5s", "sha256s", "sha1s", "cves"]

        if input_type == "" or input_type == "all":
            ioc_types = ioc_types
        else:
            input_type = input_type.split(",")
            for item in input_type:
                item = item.strip()

            ioc_types = input_type

        input_string = str(input_string)

        if len(input_string) > 10000:
            iocs = self._with_concurency(self.split_text(input_string), ioc_types=ioc_types)
        else:
            iocs = find_iocs(input_string, included_ioc_types=ioc_types)

        newarray = []
        for key, value in iocs.items():
            if input_type != "all":
                if key not in input_type:
                    continue
    
            if len(value) == 0:
                continue

            for item in value:
                # If in here: attack techniques. Shouldn't be 3 levels so no
                # recursion necessary
                if isinstance(value, dict):
                    for subkey, subvalue in value.items():
                        if len(subvalue) == 0:
                            continue

                        for subitem in subvalue:
                            data = {
                                "data": subitem,
                                "data_type": "%s_%s" % (key[:-1], subkey),
                            }

                            if data not in newarray:
                                newarray.append(data)
                else:
                    data = {"data": item, "data_type": key[:-1]}
                    if data not in newarray:
                        newarray.append(data)

        # Reformatting IP
        i = -1
        for item in newarray:
            i += 1
            if "ip" not in item["data_type"]:
                continue

            newarray[i]["data_type"] = "ip"
            try:
                newarray[i]["is_private_ip"] = ipaddress.ip_address(item["data"]).is_private
            except Exception as e:
                print("Error parsing %s: %s" % (item["data"], e))

        try:
            newarray = json.dumps(newarray)
        except json.decoder.JSONDecodeError as e:
            return "Failed to parse IOC's: %s" % e

        return newarray
    

if __name__ == "__main__":
    Tools.run()
