import asyncio
import json
import random
import socket
import time
import uuid

import requests
from openpyxl import load_workbook
from openpyxl import Workbook
from walkoff_app_sdk.app_base import AppBase

class MSExcel(AppBase):
    __version__ = "1.0.0"
    app_name = "Microsoft Excel"

    def __init__(self, redis, logger, console_logger=None):
        """
        Each app should have this __init__ to set up Redis and logging.
        :param redis:
        :param logger:
        :param console_logger:
        """
        super().__init__(redis, logger, console_logger)

    def authenticate(self, tenant_id, client_id, client_secret, graph_url):
        s = requests.Session()
        auth_url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token"
        auth_data = {
            "grant_type": "client_credentials",
            "client_id": client_id,
            "client_secret": client_secret,
            "scope": f"{graph_url}/.default",
        }
        auth_headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "cache-control": "no-cache",
        }

        print(f"Making request to: {auth_url}")
        res = s.post(auth_url, data=auth_data, headers=auth_headers)

        # Auth failed, raise exception with the response
        if res.status_code != 200:
            raise ConnectionError(res.text)

        access_token = res.json().get("access_token")
        s.headers = {"Authorization": f"Bearer {access_token}", "cache-control": "no-cache"}
        return s

    def get_user_id(self, tenant_id, client_id, client_secret):
        graph_url = "https://graph.microsoft.com"
        session = self.authenticate(tenant_id, client_id, client_secret, graph_url)
        graph_url = "https://graph.microsoft.com/v1.0/users"
        ret = session.get(graph_url)
        return ret.text

    def get_files(self, tenant_id, client_id, client_secret, user_id):
        graph_url = "https://graph.microsoft.com"
        session = self.authenticate(tenant_id, client_id, client_secret, graph_url)
        graph_url = f"https://graph.microsoft.com/v1.0/users/{user_id}/drive/root/children"
        ret = session.get(graph_url)
        return ret.text

    def list_worksheets(self, tenant_id, client_id, client_secret, user_id, file_id):
        graph_url = "https://graph.microsoft.com"
        session = self.authenticate(tenant_id, client_id, client_secret, graph_url)
        graph_url = f"https://graph.microsoft.com/v1.0/users/{user_id}/drive/items/{file_id}/workbook/worksheets"
        ret = session.get(graph_url)
        return ret.text

    def add_worksheet(self, tenant_id, client_id, client_secret, user_id, file_id, name):
        graph_url = "https://graph.microsoft.com"
        session = self.authenticate(tenant_id, client_id, client_secret, graph_url)
        graph_url = f"https://graph.microsoft.com/v1.0/users/{user_id}/drive/items/{file_id}/workbook/worksheets"
        if len(name)!=0:
            body = {
                "name": name
                }
        else:
            body = {}
        ret = session.post(graph_url, json = body)
        return ret.text

    def delete_worksheet(self, tenant_id, client_id, client_secret, user_id, file_id, name):
        graph_url = "https://graph.microsoft.com"
        session = self.authenticate(tenant_id, client_id, client_secret, graph_url)
        graph_url = f"https://graph.microsoft.com/v1.0/users/{user_id}/drive/items/{file_id}/workbook/worksheets/{name}"
        ret = session.delete(graph_url)
        if ret.status_code != 200:
            return "Action failed"
        else:
            return "Action successfully completed"

    def insert_or_update_data(self, tenant_id, client_id, client_secret, user_id, file_id, sheet_name, address, value):
        graph_url = "https://graph.microsoft.com"
        session = self.authenticate(tenant_id, client_id, client_secret, graph_url)
        graph_url = f"https://graph.microsoft.com/v1.0/users/{user_id}/drive/items/{file_id}/workbook/worksheets/{sheet_name}/range(address='{address}')"
        lt = []
        for i in value.split(';'):
            temp_var = []
            for j in i.split(','):
                temp_var.append(j)
            lt.append(temp_var)
        body = {
            "values":lt
        }
        ret = session.patch(graph_url, json=body)
        return ret.text

    def clear_data(self, tenant_id, client_id, client_secret, user_id, file_id, sheet_name, address):
        graph_url = "https://graph.microsoft.com"
        session = self.authenticate(tenant_id, client_id, client_secret, graph_url)
        graph_url = f"https://graph.microsoft.com/v1.0/users/{user_id}/drive/items/{file_id}/workbook/worksheets/{sheet_name}/range(address='{address}')/clear"
        ret = session.post(graph_url)
        if ret.status_code != 200:
            return "Action failed"
        else:
            return "Action successfully completed"

    def convert_to_csv(self, tenant_id, client_id, client_secret, file_id, sheet="Sheet1"):
        filedata = self.get_file(file_id)
        if filedata["success"] != True:
            return filedata

        basename = "file.xlsx"
        with open(basename, "wb") as tmp:
            tmp.write(filedata["data"])

        if sheet == "":
            sheet = "Sheet1"

        #wb = Workbook(basename)
        wb = load_workbook(basename)
        print("Sheets: %s" % wb.sheetnames)

        # grab the active worksheet
        ws = wb.active
        for item in ws.iter_rows():
            print(item)

        csvdata = ""
        for row in ws.values:
            for value in row:
                #print(value)
                if value == None:
                    csvdata += ","
                elif isinstance(value, str):
                    csvdata += value+","
                else:
                    csvdata += str(value)+","

            csvdata = csvdata[:-1]+"\n"
        csvdata = csvdata[:-1]

        print()
        print("Data:\n%s\n" % csvdata)

        return csvdata

    def get_excel_file_data(self, file_id):
        filedata = self.get_file(file_id)
        if filedata["success"] != True:
            print(f"Bad info from file: {filedata}")
            return filedata
        #filedata = file_id

        basename = "file.xlsx"
        with open(basename, "wb") as tmp:
            tmp.write(filedata["data"])

        #wb = Workbook(basename)
        try:
            wb = load_workbook(basename)
        except Exception as e:
            return {
                "success": False,
                "reason": "The file is invalid. Are you sure it's a valid excel file?",
                "exception": "Error: %s" % e,
            }

        print("Sheets: %s" % wb.sheetnames)

        output_data = []
        for ws in wb.worksheets:
            print(f"Title: {ws.title}")

            # grab the active worksheet
            csvdata = ""
            for row in ws.values:
                for value in row:
                    #print(value)
                    if value == None:
                        csvdata += ","
                    elif isinstance(value, str):
                        csvdata += value+","
                    else:
                        csvdata += str(value)+","

                csvdata = csvdata[:-1]+"\n"
            csvdata = csvdata[:-1]

            print()
            print("Data:\n%s\n" % csvdata)
            output_data.append({
                "sheet": ws.title,
                "data": csvdata,
            })

        return output_data

if __name__ == "__main__":
    MSExcel.run()
