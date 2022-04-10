import asyncio
import base64
import datetime
import ipaddress
import json
import os
import re
import subprocess
import tarfile
import tempfile
import zipfile

import markupsafe
import py7zr
import pyminizip
import rarfile
import requests
import xmltodict
from ioc_finder import find_iocs
from json2xml import json2xml
from json2xml.utils import readfromstring
from walkoff_app_sdk.app_base import AppBase




class Tools(AppBase):
    """
    An example of a Walkoff App.
    Inherit from the AppBase class to have Redis, logging, and console
    logging set up behind the scenes.

    """

    __version__ = "1.0.0"
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
            encoded_bytes = base64.b64encode(string.encode("utf-8"))
            encoded_string = str(encoded_bytes, "utf-8")
            return encoded_string

        elif operation == "decode":
            decoded_bytes = base64.b64decode(string.encode("utf-8"))
            decoded_string = str(decoded_bytes, "utf-8")
            return decoded_string

    # This is an SMS function of Shuffle
    def send_sms_shuffle(self, apikey, phone_numbers, body):
        targets = [phone_numbers]
        if ", " in phone_numbers:
            targets = phone_numbers.split(", ")
        elif "," in phone_numbers:
            targets = phone_numbers.split(",")

        data = {"numbers": targets, "body": body}

        url = "https://shuffler.io/api/v1/functions/sendsms"
        headers = {"Authorization": "Bearer %s" % apikey}
        return requests.post(url, headers=headers, json=data).text

    # This is an email function of Shuffle
    def send_email_shuffle(self, apikey, recipients, subject, body):
        targets = [recipients]
        if ", " in recipients:
            targets = recipients.split(", ")
        elif "," in recipients:
            targets = recipients.split(",")

        data = {"targets": targets, "body": body, "subject": subject, "type": "alert"}

        url = "https://shuffler.io/api/v1/functions/sendmail"
        headers = {"Authorization": "Bearer %s" % apikey}
        return requests.post(url, headers=headers, json=data).text

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
                                                "data_type": "%s_%s"
                                                % (key[:-1], subkey),
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

    # https://github.com/fhightower/ioc-finder
    def parse_ioc(self, input_string, input_type="all"):
        if input_type == "":
            input_type = "all"
        else:
            input_type = input_type.split(",")

        iocs = find_iocs(input_string)
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
                    print("Error parsing %s" % ip)
                    pass

        try:
            newarray = json.dumps(newarray)
        except json.decoder.JSONDecodeError as e:
            return "Failed to parse IOC's: %s" % e

        return newarray

    def parse_list(self, items, splitter="\n"):
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
                print("Parse error: %s" % e)
                pass

        return str(len(item))

    def delete_json_keys(self, json_object, keys):
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
                print("Key %s doesn't exist" % key)

        return json_object

    def translate_value(self, input_data, translate_from, translate_to, else_value=""):
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

    def map_value(self, input_data, mapping):

        mapping = json.loads(mapping)
        print(f"Got mapping {json.dumps(mapping, indent=2)}")

        # Get value if input_data in map, otherwise return original input_data
        output_data = mapping.get(input_data, input_data)
        print(f"Mapping {input_data} to {output_data}")

        return output_data

    def regex_replace(
        self, input_data, regex, replace_string="", ignore_case="False"
    ):

        print("=" * 80)
        print(f"Regex: {regex}")
        print(f"replace_string: {replace_string}")
        print("=" * 80)

        if ignore_case.lower().strip() == "true":
            return re.sub(regex, replace_string, input_data, flags=re.IGNORECASE)
        else:
            return re.sub(regex, replace_string, input_data)

    def execute_python(self, code, shuffle_input):
        print("Run with shuffle_data %s" % shuffle_input)
        print("And python code %s" % code)
        # Write the code to a file, then jdjd
        exec(code)  # nosec

        # 1. Take the data into a file
        # 2. Subprocess execute file?

        # May be necessary
        # compile()

        return "Some return: %s" % shuffle_input

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
            print("Succesfully ran bash!")
            item = stdout[0]
        else:
            print("FAILED to run bash!")
            item = stdout[1]

        try:
            ret = item.decode("utf-8")
            return ret
        except Exception:
            return item

        return item

    def filter_list(self, input_list, field, check, value, opposite):
        print(f"\nRunning function with list {input_list}")

        flip = False
        if opposite.lower() == "true":
            flip = True

        try:
            input_list = eval(input_list)  # nosec
        except Exception:
            try:
                input_list = input_list.replace("'", '"', -1)
                input_list = json.loads(input_list)
            except Exception:
                print("Error parsing string to array. Continuing anyway.")

        # Workaround D:
        if not isinstance(input_list, list):
            return {
                "success": False,
                "reason": "Error: input isnt a list. Remove # to use this action."
                % type(input_list),
                "valid": [],
                "invalid": [],
            }

            input_list = [input_list]

        print("\nRunning with check \"%s\" on list of length %d\n" % (check, len(input_list)))
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
                        print("FAILED DECODING: %s" % e)
                        pass

                #print("PRE CHECKS FOR TMP: %")

                # EQUALS JUST FOR STR
                if check == "equals":
                    # Mostly for bools
                    # value = tmp.lower()

                    if str(tmp).lower() == str(value).lower():
                        print("APPENDED BECAUSE %s %s %s" % (field, check, value))
                        if not flip:
                            new_list.append(item)
                        else:
                            failed_list.append(item)
                    else:
                        if flip:
                            new_list.append(item)
                        else:
                            failed_list.append(item)

                # IS EMPTY FOR STR OR LISTS
                elif check == "is empty":
                    if tmp == "[]":
                        tmp = []

                    if type(tmp) == list and len(tmp) == 0 and not flip:
                        new_list.append(item)
                    elif type(tmp) == list and len(tmp) > 0 and flip:
                        new_list.append(item)
                    elif type(tmp) == str and not tmp and not flip:
                        new_list.append(item)
                    elif type(tmp) == str and tmp and flip:
                        new_list.append(item)
                    else:
                        failed_list.append(item)

                # STARTS WITH = FOR STR OR [0] FOR LIST
                elif check == "starts with":
                    if type(tmp) == list and tmp[0] == value and not flip:
                        new_list.append(item)
                    elif type(tmp) == list and tmp[0] != value and flip:
                        new_list.append(item)
                    elif type(tmp) == str and tmp.startswith(value) and not flip:
                        new_list.append(item)
                    elif type(tmp) == str and not tmp.startswith(value) and flip:
                        new_list.append(item)
                    else:
                        failed_list.append(item)

                # ENDS WITH = FOR STR OR [-1] FOR LIST
                elif check == "ends with":
                    if type(tmp) == list and tmp[-1] == value and not flip:
                        new_list.append(item)
                    elif type(tmp) == list and tmp[-1] != value and flip:
                        new_list.append(item)
                    elif type(tmp) == str and tmp.endswith(value) and not flip:
                        new_list.append(item)
                    elif type(tmp) == str and not tmp.endswith(value) and flip:
                        new_list.append(item)
                    else:
                        failed_list.append(item)

                # CONTAINS FIND FOR LIST AND IN FOR STR
                elif check == "contains":
                    if type(tmp) == list and value.lower() in tmp and not flip:
                        new_list.append(item)
                    elif type(tmp) == list and value.lower() not in tmp and flip:
                        new_list.append(item)
                    elif (
                        type(tmp) == str
                        and tmp.lower().find(value.lower()) != -1
                        and not flip
                    ):
                        new_list.append(item)
                    elif (
                        type(tmp) == str
                        and tmp.lower().find(value.lower()) == -1
                        and flip
                    ):
                        new_list.append(item)
                    else:
                        failed_list.append(item)
                elif check == "contains any of":
                    print("Inside contains any of")
                    checklist = value.split(",")
                    print("Checklist and tmp: %s - %s" % (checklist, tmp))
                    found = False
                    for subcheck in checklist:
                        subcheck = subcheck.strip().lower()
                        #ext.lower().strip() == value.lower().strip()
                        if type(tmp) == list and subcheck in tmp and not flip:
                            new_list.append(item)
                            found = True
                            break
                        elif type(tmp) == list and subcheck not in tmp and flip:
                            new_list.append(item)
                            found = True
                            break
                        elif (type(tmp) == str and tmp.lower().find(subcheck) != -1 and not flip):
                            new_list.append(item)
                            found = True
                            break
                        elif (type(tmp) == str and tmp.lower().find(subcheck) == -1 and flip):
                            new_list.append(item)
                            found = True
                            break

                    if not found:
                        failed_list.append(item)

                # CONTAINS FIND FOR LIST AND IN FOR STR
                elif check == "field is unique":
                    #print("FOUND: %s"
                    if tmp.lower() not in found_items and not flip:
                        new_list.append(item)
                        found_items.append(tmp.lower())
                    elif tmp.lower() in found_items and flip:
                        new_list.append(item)
                        found_items.append(tmp.lower())
                    else:
                        failed_list.append(item)

                    #tmp = json.dumps(tmp)

                    #for item in new_list:
                    #if type(tmp) == list and value.lower() in tmp and not flip:
                    #    new_list.append(item)
                    #    found = True
                    #    break
                    #elif type(tmp) == list and value.lower() not in tmp and flip:
                    #    new_list.append(item)
                    #    found = True
                    #    break

                # CONTAINS FIND FOR LIST AND IN FOR STR
                elif check == "contains any of":
                    checklist = value.split(",")
                    tmp = tmp.lower()
                    print("CHECKLIST: %s. Value: %s" % (checklist, tmp))
                    found = False
                    for value in checklist:
                        if value in tmp and not flip:
                            new_list.append(item)
                            found = True
                            break
                        elif value not in tmp and flip:
                            new_list.append(item)
                            found = True
                            break

                    if not found:
                        failed_list.append(item)

                elif check == "larger than":
                    if int(tmp) > int(value) and not flip:
                        new_list.append(item)
                    elif int(tmp) > int(value) and flip:
                        new_list.append(item)
                    else:
                        failed_list.append(item)
                elif check == "less than":
                    if int(tmp) < int(value) and not flip:
                        new_list.append(item)
                    elif int(tmp) < int(value) and flip:
                        new_list.append(item)
                    else:
                        failed_list.append(item)

                # SINGLE ITEM COULD BE A FILE OR A LIST OF FILES
                elif check == "files by extension":
                    if type(tmp) == list:
                        file_list = []

                        for file_id in tmp:
                            filedata = self.get_file(file_id)
                            _, ext = os.path.splitext(filedata["filename"])
                            if (
                                ext.lower().strip() == value.lower().strip()
                                and not flip
                            ):
                                file_list.append(file_id)
                            elif ext.lower().strip() != value.lower().strip() and flip:
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
                        if ext.lower().strip() == value.lower().strip() and not flip:
                            new_list.append(item)
                        elif ext.lower().strip() != value.lower().strip() and flip:
                            new_list.append((item, ext))
                        else:
                            failed_list.append(item)

            except Exception as e:
                # "Error: %s" % e
                print("[WARNING] FAILED WITH EXCEPTION: %s" % e)
                failed_list.append(item)
            # return

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
    #                print(
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
        )
        print(f"RET: {ret}")

        return ret.text

    # Use data from AppBase to talk to backend
    def delete_file(self, file_id):
        headers = {
            "Authorization": "Bearer %s" % self.authorization,
        }
        print("HEADERS: %s" % headers)

        ret = requests.delete(
            "%s/api/v1/files/%s?execution_id=%s"
            % (self.url, file_id, self.current_execution_id),
            headers=headers,
        )
        return ret.text

    def get_file_value(self, filedata):
        if filedata is None:
            return "File is empty?"

        print("INSIDE APP DATA: %s" % filedata)
        return "%s" % filedata["data"].decode()

    def download_remote_file(self, url):
        ret = requests.get(url, verify=False)  # nosec
        filename = url.split("/")[-1]
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

    def extract_archive(self, file_ids, fileformat="zip", password=None):
        try:
            return_data = {"success": False, "files": []}

            try:
                file_ids = eval(file_ids)  # nosec
            except SyntaxError:
                file_ids = file_ids

            print("IDS: %s" % file_ids)
            items = file_ids if type(file_ids) == list else file_ids.split(",")
            for file_id in items:

                item = self.get_file(file_id)
                return_ids = None

                print("Working with fileformat %s" % fileformat)
                with tempfile.TemporaryDirectory() as tmpdirname:

                    # Get archive and save phisically
                    with open(os.path.join(tmpdirname, "archive"), "wb") as f:
                        f.write(item["data"])

                    # Grab files before, upload them later
                    to_be_uploaded = []

                    # Zipfile for zipped archive
                    if fileformat.strip().lower() == "zip":
                        try:
                            with zipfile.ZipFile(
                                os.path.join(tmpdirname, "archive")
                            ) as z_file:
                                if password:
                                    z_file.setpassword(bytes(password.encode()))
                                for member in z_file.namelist():
                                    filename = os.path.basename(member)
                                    if not filename:
                                        continue
                                    source = z_file.open(member)
                                    to_be_uploaded.append(
                                        {"filename": source.name, "data": source.read()}
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

                            continue

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
                                        {"filename": source.name, "data": source.read()}
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
                            continue

                    elif fileformat.strip().lower() == "tar":
                        try:
                            with tarfile.open(
                                os.path.join(tmpdirname, "archive"), mode="r"
                            ) as z_file:
                                for member in z_file.getnames():
                                    member_files = z_file.extractfile(member)
                                    to_be_uploaded.append(
                                        {
                                            "filename": member,
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
                                    "message": e,
                                }
                            )
                            continue
                    elif fileformat.strip().lower() == "tar.gz":
                        try:
                            with tarfile.open(
                                os.path.join(tmpdirname, "archive"), mode="r:gz"
                            ) as z_file:
                                for member in z_file.getnames():
                                    member_files = z_file.extractfile(member)
                                    to_be_uploaded.append(
                                        {
                                            "filename": member,
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
                                    "message": e,
                                }
                            )
                            continue

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
                                            "filename": item["filename"],
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
                            continue
                    else:
                        return "No such format: %s" % fileformat

                    if len(to_be_uploaded) > 0:
                        return_ids = self.set_files(to_be_uploaded)
                        return_data["files"].append(
                            {
                                "success": True,
                                "file_id": file_id,
                                "filename": item["filename"],
                                "file_ids": return_ids,
                            }
                        )
                    else:
                        return_data["files"].append(
                            {
                                "success": False,
                                "file_id": file_id,
                                "filename": item["filename"],
                                "message": "Archive is empty",
                            }
                        )

            return return_data

        except Exception as excp:
            return {"success": False, "message": "%s" % excp}

    def inflate_archive(self, file_ids, fileformat, name, password=None):

        try:
            # TODO: will in future support multiple files instead of string ids?
            file_ids = file_ids.split()
            print("picking {}".format(file_ids))

            # GET all items from shuffle
            items = [self.get_file(file_id) for file_id in file_ids]

            if len(items) == 0:
                return "No file to inflate"

            # Dump files on disk, because libs want path :(
            with tempfile.TemporaryDirectory() as tmpdir:
                paths = []
                print("Number 1")
                for item in items:
                    with open(os.path.join(tmpdir, item["filename"]), "wb") as f:
                        f.write(item["data"])
                        paths.append(os.path.join(tmpdir, item["filename"]))

                # Create archive temporary
                print("{} items to inflate".format(len(items)))
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
                        return {"success": True, "id": return_id[0]}
                    else:
                        return {
                            "success": False,
                            "message": "Upload archive returned {}".format(return_id),
                        }

        except Exception as excp:
            return {"success": False, "message": excp}

    def add_list_to_list(self, list_one, list_two):
        try:
            list_one = json.loads(list_one)
        except json.decoder.JSONDecodeError as e:
            print("Failed to parse list1 as json: %s" % e)
            return "List one is not a valid list: %s" % list_one

        try:
            list_two = json.loads(list_two)
        except json.decoder.JSONDecodeError as e:
            print("Failed to parse list2 as json: %s" % e)
            return "List two is not a valid list: %s" % list_two

        for item in list_two:
            list_one.append(item)

        return list_one

    def diff_lists(self, list_one, list_two):
        try:
            list_one = json.loads(list_one)
        except json.decoder.JSONDecodeError as e:
            print("Failed to parse list1 as json: %s" % e)

        try:
            list_two = json.loads(list_two)
        except json.decoder.JSONDecodeError as e:
            print("Failed to parse list2 as json: %s" % e)

        def diff(li1, li2):
            return list(set(li1) - set(li2)) + list(set(li2) - set(li1))

        return diff(list_one, list_two)

    def merge_lists(self, list_one, list_two, set_field="", sort_key_list_one="", sort_key_list_two=""):
        try:
            list_one = json.loads(list_one)
        except json.decoder.JSONDecodeError as e:
            print("Failed to parse list1 as json: %s" % e)

        try:
            list_two = json.loads(list_two)
        except json.decoder.JSONDecodeError as e:
            print("Failed to parse list2 as json: %s" % e)

        if len(list_one) != len(list_two):
            return {"success": False, "message": "Lists length must be the same. %d vs %d" % (len(list_one), len(list_two))}

        #result = json.loads(input_data)
        print(list_one)
        print(list_two)
        print(set_field)
        print("START: ")

        if len(sort_key_list_one) > 0:
            print("Sort 1 %s by key: %s" % (list_one, sort_key_list_one))
            try:
                list_one = sorted(list_one, key=lambda k: k.get(sort_key_list_one), reverse=True)
            except:
                print("Failed to sort list one")
                pass

        if len(sort_key_list_two) > 0:
            #print("Sort 2 %s by key: %s" % (list_two, sort_key_list_two))
            try:
                list_two = sorted(list_two, key=lambda k: k.get(sort_key_list_two), reverse=True)
            except:
                print("Failed to sort list one")
                pass

        for i in range(len(list_one)):
            #print(list_two[i])
            if isinstance(list_two[i], dict):
                for key, value in list_two[i].items():
                    list_one[i][key] = value
            elif isinstance(list_two[i], str) or isinstance(list_two[i], int) or isinstance(list_two[i], bool):
                print("IN SETTER FOR %s" % list_two[i])
                if len(set_field) == 0:
                    return "Define a JSON key to set for List two (Set Field)"

                list_one[i][set_field] = list_two[i]

        return list_one

    def xml_json_convertor(self, convertto, data):
        try:
            if convertto == "json":
                ans = xmltodict.parse(data)
                json_data = json.dumps(ans)
                return json_data
            else:
                ans = readfromstring(data)
                return json2xml.Json2xml(ans, wrapper="all", pretty=True).to_xml()
        except Exception as e:
            return e

    def date_to_epoch(self, input_data, date_field, date_format):

        print(
            "Executing with {} on {} with format {}".format(
                input_data, date_field, date_format
            )
        )

        result = json.loads(input_data)

        # https://docs.python.org/3/library/datetime.html#strftime-strptime-behavior
        epoch = datetime.datetime.strptime(result[date_field], date_format).strftime(
            "%s"
        )
        result["epoch"] = epoch
        return result

    def compare_relative_date(
        self, input_data, date_format, equality_test, offset, units, direction
    ):

        if input_data == "None":
            return False

        print("Converting input date.")

        if date_format != "%s":
            input_dt = datetime.datetime.strptime(input_data, date_format)
        else:
            input_dt = datetime.datetime.utcfromtimestamp(float(input_data))

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

        if date_format != "%s":
            formatted_dt = datetime.datetime.strptime(
                datetime.datetime.utcnow().strftime(utc_format), date_format
            )
        else:
            formatted_dt = datetime.datetime.utcnow()

        print("Formatted time is: {}".format(formatted_dt))
        if direction == "ago":
            comparison_dt = formatted_dt - delta
        else:
            comparison_dt = formatted_dt + delta
        print("{} {} {} is {}".format(offset, units, direction, comparison_dt))

        diff = (input_dt - comparison_dt).total_seconds()
        print(
            "Difference between {} and {} is {}".format(input_data, comparison_dt, diff)
        )
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
            "At {}, is {} {} than {} {} {}? {}".format(
                formatted_dt,
                input_data,
                equality_test,
                offset,
                units,
                direction,
                result,
            )
        )

        return result

    def run_math_operation(self, operation):
        print("Operation: %s" % operation)
        result = eval(operation)
        return result

    def escape_html(self, input_data, field_name):

        mapping = json.loads(input_data)
        print(f"Got mapping {json.dumps(mapping, indent=2)}")

        result = markupsafe.escape(mapping[field_name])
        print(f"Mapping {input_data} to {result}")

        mapping[field_name] = result
        return mapping

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

        value = requests.post(url, json=data)
        try:
            allvalues = value.json()
            print("VAL1: ", allvalues)
            allvalues["key"] = key
            print("VAL2: ", allvalues)

            try:
                parsedvalue = json.loads(allvalues["value"])
                allvalues["value"] = parsedvalue
            except:
                print("Parsing of value as JSON failed")
                pass

            return json.dumps(allvalues)
        except:
            print("Value couldn't be parsed, or json dump of value failed")
            return value.text

    # FIXME: Add option for org only & sensitive data (not to be listed)
    def set_cache_value(self, key, value):
        org_id = self.full_execution["workflow"]["execution_org"]["id"]
        url = "%s/api/v1/orgs/%s/set_cache" % (self.url, org_id)
        data = {
            "workflow_id": self.full_execution["workflow"]["id"],
            "execution_id": self.current_execution_id,
            "authorization": self.authorization,
            "org_id": org_id,
            "key": key,
            "value": str(value),
        }

        response = requests.post(url, json=data)
        try:
            allvalues = response.json()
            allvalues["key"] = key
            allvalues["value"] = str(value)
            return json.dumps(allvalues)
        except:
            print("Value couldn't be parsed")
            return response.text

    def convert_json_to_tags(self, json_object, split_value=", ", include_key=True, lowercase=True):
        try:
            json_object = json.loads(json_object)
        except json.decoder.JSONDecodeError as e:
            print("Failed to parse list2 as json: %s. Type: %s" % (e, type(json_object)))

        if isinstance(lowercase, str) and lowercase.lower() == "true":
            lowercase = True
        else:
            lowercase = False

        if isinstance(include_key, str) or include_key.lower() == "true":
            include_key = True
        else:
            include_key = False

        parsedstring = []
        for key, value in json_object.items():
            print("KV: %s:%s" % (key, value))
            if isinstance(value, str) or isinstance(value, int) or isinstance(value, bool):
                if include_key == True:
                    parsedstring.append("%s:%s" % (key, value))
                else:
                    parsedstring.append("%s" % (value))
            else:
                print("Can't handle type %s" % type(value))

        fullstring = split_value.join(parsedstring)
        if lowercase == True:
            fullstring = fullstring.lower()

        return fullstring

    def cidr_ip_match(self, ip, networks):
        print("Executing with\nIP: {},\nNetworks: {}".format(ip, networks))

        try:
            networks = json.loads(networks)
        except json.decoder.JSONDecodeError as e:
            print("Failed to parse networks list as json: {}. Type: {}".format(
                e, type(networks)
            ))
            return "Networks is not a valid list: {}".format(networks)

        try:
            ip_networks = list(map(ipaddress.ip_network, networks))
            ip_address = ipaddress.ip_address(ip)
        except ValueError as e:
            return "IP or some networks are not in valid format.\nError: {}".format(e)

        matched_networks = list(filter(lambda net: (ip_address in net), ip_networks))

        result = {}
        result['networks'] = list(map(str, matched_networks))
        result['is_contained'] = True if len(result['networks']) > 0 else False

        return json.dumps(result)

if __name__ == "__main__":
    Tools.run()
