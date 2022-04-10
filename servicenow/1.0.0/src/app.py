import asyncio
import json
import random
import socket
import time

import requests
from walkoff_app_sdk.app_base import AppBase

class Servicenow(AppBase):
    __version__ = "1.0.0"
    app_name = "servicenow"

    def __init__(self, redis, logger, console_logger=None):
        """
        Each app should have this __init__ to set up Redis and logging.
        :param redis:
        :param logger:
        :param console_logger:
        """
        super().__init__(redis, logger, console_logger)

    def send_request(self, url, username, password, path, method='get', body=None, params=None, headers=None, json=None, files=None):
        body = body if body is not None else {}
        params = params if params is not None else {}

        url = '{}{}'.format(url, path)
        print("HEADERS: %s" % headers)
        if not headers and files == None:
            headers = {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            }

        if files:
            # Not supported in v2
            url = url.replace('v2', 'v1')
            #{'file': ('report.csv', 'some,data,to,send\nanother,row,to,send\n')}
            #file_entry = file['id']
            #file_name = file['name']
            try:
                #shutil.copy(demisto.getFilePath(file_entry)['path'], file_name)
                #with open(file_name, 'rb') as f:
                #files = {'file': f}

                try:
                    res = requests.request(method, url, headers=headers, params=params, data=body, files=files, json=json, auth=(username, password))
                except requests.exceptions.ReadTimeout as e:
                    return "Readtimeout: %s" % e
                except requests.exceptions.ConnectionError as e:
                    return "ConnectionError: %s" % e

                #shutil.rmtree(demisto.getFilePath(file_entry)['name'], ignore_errors=True)
            except Exception as e:
                return 'Failed to upload file - ' + str(e)
        else:
            try:
                res = requests.request(method, url, headers=headers, data=json.dumps(body) if body else {}, json=json, params=params, auth=(username, password))
            except requests.exceptions.ReadTimeout as e:
                return "Readtimeout: %s" % e
            except requests.exceptions.ConnectionError as e:
                return "ConnectionError: %s" % e

        try:
            obj = res.json()
        except Exception as e:
            if not res.content:
                return ''
            return 'Error parsing reply - {} - {}'.format(res.content, str(e))

        if 'error' in obj:
            message = obj.get('error', {}).get('message')
            details = obj.get('error', {}).get('detail')
            if message == 'No Record found':
                return {
                    # Return an empty results array
                    'result': []
                }
            return 'ServiceNow Error: {}, details: {}'.format(message, details)

        if res.status_code < 200 or res.status_code >= 300:
            return 'Got status code {} with url {} with body {} with headers {}'.format(str(res.status_code), url, str(res.content), str(res.headers))

        #print("RES: %s" % res)
        #print("TEXT: %s" % res.text)
        return res.text

    def get_ticket(self, url, username, password, table_name, sys_id, number=None):
        path = None
        query_params = {}  # type: Dict
        if sys_id:
            path = "/api/now/v1/table/%s/%s" % (table_name, sys_id)
        elif number:
            path = '/api/now/v1/table/%s' % table_name
            query_params = {
                'number': number
            }
        else:
            # Only in cases where the table is of type ticket
            return 'servicenow-get-ticket requires either ticket ID or ticket number'

        print("PATH: %s" % path)
        return self.send_request(url, username, password, path, 'get', params=query_params)

    def list_table(self, url, username, password, table_name, limit=1):
        query_params = {
            "sysparm_limit": limit,
        }

        #path = '/table/%s' % table_name
        path = "/api/now/v1/table/%s" % table_name

        return self.send_request(url, username, password, path, 'get', params=query_params)

    def create_ticket(self, url, username, password, table_name, body, file_id=""):
        if not isinstance(body, list) and not isinstance(body, object) and not isinstance(body, dict):
            try:
                data = json.loads(body)
            except json.decoder.JSONDecodeError as e:
                return {"success": False, "reason": e}
        else:
            data = body


        path = "/api/now/v1/table/%s" % table_name
        query_params = {}
        base_request = self.send_request(url, username, password, path, 'post', params=query_params, json=data)

        if file_id:
            tmp_file = self.get_file(file_id)
            files = {'file': (tmp_file["filename"], tmp_file["data"])}

            try:
                parsed_return = json.loads(base_request)
            except:
                print("[INFO] Failed parsed_return loading")
                return base_request

            ticket_id = parsed_return["result"]["sys_id"]
            params = {
                "file_name": tmp_file["filename"],
                "table_name": table_name,
                "table_sys_id": ticket_id,
            }

            filepath = "/api/now/v1/attachment/file"
            file_request = self.send_request(url, username, password, filepath, 'post', params=params, files=files, headers={})
            print(file_request)

        return base_request

    def update_ticket(self, url, username, password, table_name, sys_id, body, file_id=""):
        if not isinstance(body, list) and not isinstance(body, object) and not isinstance(body, dict):
            try:
                data = json.loads(body)
            except json.decoder.JSONDecodeError as e:
                return {"success": False, "reason": e}
        else:
            data = body


        path = "/api/now/v1/table/%s/%s" % (table_name, sys_id)
        query_params = {}
        base_request = self.send_request(url, username, password, path, 'patch', params=query_params, json=data)

        if file_id:
            tmp_file = self.get_file(file_id)
            files = {'file': (tmp_file["filename"], tmp_file["data"])}

            try:
                parsed_return = json.loads(base_request)
            except:
                print("[INFO] Failed parsed_return loading")
                return base_request

            ticket_id = parsed_return["result"]["sys_id"]
            params = {
                "file_name": tmp_file["filename"],
                "table_name": table_name,
                "table_sys_id": ticket_id,
            }

            filepath = "/api/now/v1/attachment/file"
            file_request = self.send_request(url, username, password, filepath, '', params=params, files=files, headers={})
            print(file_request)

        return base_request

# Run the actual thing after we've checked params
def run(request):
    action = request.get_json()
    print(action)
    print(type(action))
    authorization_key = action.get("authorization")
    current_execution_id = action.get("execution_id")

    if action and "name" in action and "app_name" in action:
        Servicenow.run(action)
        return f'Attempting to execute function {action["name"]} in app {action["app_name"]}'
    else:
        return f'Invalid action'

if __name__ == "__main__":
    Servicenow.run()
