import asyncio
import json
import random
import socket
import time

from walkoff_app_sdk.app_base import AppBase

from mysql.connector import connection
from mysql.connector import errorcode

class DbManager(AppBase):
    __version__ = "1.0.0"
    app_name = "DatabaseManager"  # this needs to match "name" in api.yaml

    def __init__(self, redis, logger, console_logger=None):
        """
        Each app should have this __init__ to set up Redis and logging.
        :param redis:
        :param logger:
        :param console_logger:
        """
        super().__init__(redis, logger, console_logger)

    def connection(self, username, password, host, port, database_name):
        cnx = connection.MySQLConnection(user=username, password= password,
                                        host= host,
                                        port=port,
                                        database= database_name)
        print(f"Connection successful, User -->{username} ")
        return cnx

    def query_mysql_database(self, username, password, host, port, database_name, query):

        self.db_connection = self.connection(username, password, host, port, database_name)
        cursor = self.db_connection.cursor(dictionary=True)
        cursor.execute(str(query))
        print("Query executed successfully")
        res = cursor.fetchall()
        cursor.close()
        self.db_connection.close()
        return (json.dumps(res))

if __name__ == "__main__":
    DbManager.run()
