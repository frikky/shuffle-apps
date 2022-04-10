import asyncio
import json

from walkoff_app_sdk.app_base import AppBase

import mysql.connector
from mysql.connector import errorcode


class MySQL(AppBase):
    __version__ = "1.0.0"
    app_name = "MySQL"  # this needs to match "name" in api.yaml

    def __init__(self, redis, logger, console_logger=None):
        """
        Each app should have this __init__ to set up Redis and logging.
        :param redis:
        :param logger:
        :param console_logger:
        """
        super().__init__(redis, logger, console_logger)

    # Write your data inside this function

    def create_database(self, server, user, password, database, name, tables=None):
        try:
            conn = mysql.connector.connect(host=server, user=user, passwd=password)
            cursor = conn.cursor()
        except Exception as err:
            error = {"Error": "Couldn't import the data!"}
            return error

        # try to create the database
        try:
            cursor.execute(
                f"CREATE DATABASE {name} CHARACTER SET = 'utf8' COLLATE = 'utf8_general_ci'"
            )
        except mysql.connector.Error as err:
            error = {"Error": f"Failed creating database: {err}"}
            return error

        # Try to use the database, if it does not exist it creates
        try:
            cursor.execute(f"USE {name}")
        except mysql.connector.Error as err:
            print(f"Database {name} does not exists.")
            if err.errno == errorcode.ER_BAD_DB_ERROR:
                self.create_database(cursor)
                print(f"Database {name} created successfully.")
                conn.database = name
            else:
                error = {"Error": f"Couldn't use the database {name}: {err}"}
                return err
        else:
            if tables:
                if not isinstance(tables, list) and not isinstance(tables, dict):
                    tables = json.loads(tables)

                t_count = 0
                for table_name in tables:
                    table_description = tables[table_name]
                    try:
                        print(f"Creating table {table_name}: ", end="")
                        cursor.execute(table_description)
                        print(f"Table {table_name} created with success!")
                        t_count += 1
                    except mysql.connector.Error as err:
                        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                            print(f"Table {table_name} already exists.")
                            error = {"Error": f"Table {table_name} already exists."}
                            return error
                        else:
                            print(err.msg)
                            error = {
                                "Error": f"Couldn't create table {table_name}: {err.msg}"
                            }
                            return error

                response = {
                    "message": f"Database {name} and tables created with success!",
                    "tables": tables,
                }

                return json.dumps(response, indent=4)
            else:
                return f"Database {name} created with success!"

    # Create Tables
    def create_tables(self, server, user, password, database, tables):
        if not isinstance(tables, list) and not isinstance(tables, dict):
            tables = json.loads(tables)

        try:
            conn = mysql.connector.connect(
                host=server, user=user, passwd=password, db=database
            )
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
                error = {"Error": "Something is wrong with your user name or password"}
                return error
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
                error = {"Error": "Database does not exist"}
                return error
            else:
                print(err)
                error = {"Error": f"{err}"}
                return error
        else:
            cursor = conn.cursor()
            t_count = 0
            for table_name in tables:
                table_description = tables[table_name]
                try:
                    print(f"Creating table {table_name}: ", end="")
                    cursor.execute(table_description)
                    print("created with success!")
                    t_count += 1
                except mysql.connector.Error as err:
                    if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                        print("already exists.")
                        error = {"Error": f"Table {table_name} already exists."}
                        return error
                    else:
                        print(err.msg)
                        error = {"Error": f"{err.msg}"}
                        return error
            result = (
                "Table(s) created with success!"
                if t_count > 1
                else "Table created with success!"
            )

            cursor.close()
            conn.close()

            return result

    # Insert data into table
    def insert_data(self, server, user, password, database, table, data):
        if not isinstance(data, list) and not isinstance(data, dict):
            data = json.loads(data)

        try:
            conn = mysql.connector.connect(
                host=server, user=user, passwd=password, db=database
            )
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
                error = {"Error": "Something is wrong with your user name or password"}
                return error
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
                error = {"Error": "Database does not exist"}
                return error
            else:
                print(err)
                error = {"Error": f"{err}"}
                return error
        else:
            cursor = conn.cursor()
            if isinstance(data, list):
                for row in data:
                    fields = ""
                    value_fields = ""

                    if len([*row]) > 1:
                        fields = ", ".join(row.keys())
                        for i, key in enumerate(row.keys()):
                            value_fields += (
                                f"%({key})s, "
                                if i != len(row.keys()) - 1
                                else f"%({key})s"
                            )
                    else:
                        fields = next(iter(row.keys()))

                    sql = (
                        "INSERT INTO `"
                        + table
                        + "` ("
                        + fields
                        + ") VALUES ("
                        + value_fields
                        + ")"
                    )

                    try:
                        print(f"Inserting data into {table}: ", end="")
                        cursor.execute(sql, row)
                        print("inserted with success!")
                        conn.commit()
                    except mysql.connector.Error as err:
                        print(err)
                        error = {"Error": f"{err}"}
                        return error
            else:
                fields = ""
                value_fields = ""

                if len([*data]) > 1:
                    fields = ", ".join(data.keys())
                    for i, key in enumerate(data.keys()):
                        value_fields += (
                            f"%({key})s, "
                            if i != len(data.keys()) - 1
                            else f"%({key})s"
                        )
                else:
                    fields = next(iter(data.keys()))

                sql = (
                    "INSERT INTO `"
                    + table
                    + "` ("
                    + fields
                    + ") VALUES ("
                    + value_fields
                    + ")"
                )

                try:
                    print(f"Inserting data into {table}: ", end="")
                    cursor.execute(sql, data)
                    print("inserted with success!")
                    conn.commit()
                except mysql.connector.Error as err:
                    print(err)
                    error = {"Error": f"{err}"}
                    return error

            cursor.close()
            conn.close()
            response = {
                "message": f"Data inserted with success into table {table}!",
                "data": data,
            }

            return json.dumps(response, indent=4)

    # Query Data
    def query_data(
        self, server, user, password, database, table, fields=None, condition=None
    ):
        query = f"SELECT {fields} FROM {table}" if fields else f"SELECT * FROM {table}"
        if condition:
            query += f" WHERE {condition}"

        try:
            conn = mysql.connector.connect(
                host=server, user=user, passwd=password, db=database
            )
            cursor = conn.cursor()
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
                return "Something is wrong with your user name or password"
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
                return "Database does not exist"
            else:
                print(err)
                return err

        cursor.execute(query)
        row_headers = [x[0] for x in cursor.description]
        json_data = []
        for result in cursor.fetchall():
            json_data.append(dict(zip(row_headers, result)))
        result = cursor
        cursor.close()
        conn.close()
        return json.dumps(json_data, indent=4)


if __name__ == "__main__":
    MySQL.run()
