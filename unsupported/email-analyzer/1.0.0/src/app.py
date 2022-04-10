import asyncio
import datetime
import json
import random
import socket
import time

import eml_parser
import extract_msg
import jsonpickle
import mailparser
from msg_parser import MsOxMessage
from walkoff_app_sdk.app_base import AppBase

def json_serial(obj):
    if isinstance(obj, datetime.datetime):
        serial = obj.isoformat()
        return serial

class EmailAnalyzer(AppBase):
    __version__ = "1.0.0"
    app_name = "Email Analyzer"  # this needs to match "name" in api.yaml


    def __init__(self, redis, logger, console_logger=None):
        """
        Each app should have this __init__ to set up Redis and logging.
        :param redis:
        :param logger:
        :param console_logger:
        """
        super().__init__(redis, logger, console_logger)

    async def parse_email_file(self, file_id, file_extension):

        if file_extension.lower() == 'eml':
            print('working with .eml file')
            file_path = self.get_file(file_id)
            print(file_path['data'])
            ep = eml_parser.EmlParser()
            try:
                parsed_eml = ep.decode_email_bytes(file_path['data'])
                return json.dumps(parsed_eml, default=json_serial)
            except Exception as e:
                return {"Success":"False","Message":f"Exception occured: {e}"}

        if file_extension.lower() == 'msg':
            print('working with .msg file')
            file_path = self.get_file(file_id)
            print(file_path['data'])
            try:
                msg = MsOxMessage(file_path['data'])
                msg_properties_dict = msg.get_properties()
                print(msg_properties_dict)
                frozen = jsonpickle.encode(msg_properties_dict)
                return frozen
            except Exception as e:
                return {"Success":"False","Message":f"Exception occured: {e}"}

    async def parse_email_headers(self, email_headers):
        try:
            email_headers = bytes(email_headers,'utf-8')
            ep = eml_parser.EmlParser()
            parsed_headers = ep.decode_email_bytes(email_headers)
            return json.dumps(parsed_headers, default=json_serial)
        except Exception as e:
            raise Exception(e)

if __name__ == "__main__":
    asyncio.run(EmailAnalyzer.run(), debug=True)
