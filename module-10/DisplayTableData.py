""" import statements """
import mysql.connector  # to connect
from mysql.connector import errorcode
from mysql.connector import MySQLConnection

import os
from dotenv import dotenv_values


def display_table(cursor, table_name):
    """
    Display all data from a specified table.
    No validation of if the table exists is done here.

    :param cursor: MySQL cursor object
    :param table_name: Name of the table to display data from
    """
    print(f"\n--- {table_name} table ---")

    cursor.execute(f"SELECT * FROM {table_name}")
    rows = cursor.fetchall()

    columns = [desc[0] for desc in cursor.description]
    print(" | ".join(columns))
    print("-" * 50)

    for row in rows:
        print(" | ".join(str(item) if item is not None else "" for item in row))


def GetTables(cursor) -> list[str]:
    """
    Retrieve a list of all table names in the 'outland_adventures' database.
    """
    cursor.execute("SHOW TABLES FROM outland_adventures;")
    tables = [row[0] for row in cursor.fetchall()]
    return tables


def GetDatabaseConnection() -> MySQLConnection | None:
    """
    Get a connection to the MySQL database.
    """

    # Get folder where this script lives
    current_directory = os.path.dirname(os.path.abspath(__file__))
    # Load .env from that folder
    secrets = dotenv_values(os.path.join(current_directory, ".env"))

    # database config object
    config = {
        "user": secrets["USER"],
        "password": secrets["PASSWORD"],
        "host": secrets["HOST"],
        "database": secrets["DATABASE"],
        "raise_on_warnings": True
    }

    try:
        db = MySQLConnection(**config)
        if db is not None:
            return db
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("The supplied username or password are invalid")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("The specified database does not exist")
        else:
            print(err)
    return None


def main():
    conn = GetDatabaseConnection()
    if conn is not None:
        print("Successfully connected to the database.")
    else:
        print("Failed to connect to the database.")
        return

    cursor = conn.cursor()
    tables = GetTables(cursor)

    for table in tables:
        display_table(cursor, table)

    cursor.close()
    conn.close()


if __name__ == "__main__":
    main()
