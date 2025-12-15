""" import statements """
import mysql.connector # to connect
from mysql.connector import errorcode
from mysql.connector import MySQLConnection

import dotenv # to use .env file
import os
from dotenv import dotenv_values


def display_table(cursor, table_name, show_astable: bool = True) -> None:
    """
    Display all data from a specified table.
    No validation of if the table exists is done here.

    :param cursor: MySQL cursor object
    :param table_name: Name of the table to display data from
    """
    # Fetch and display all data from the table
    print(f"\n--- {table_name} table ---")

    # Execute query to fetch all data
    cursor.execute(f"SELECT * FROM {table_name}")

    # Fetch all rows
    rows = cursor.fetchall()

    if show_astable:
        # Get column names
        columns = [desc[0] for desc in cursor.description]

        # Print column headers
        print(" | ".join(columns))

        print("-" * 50)

        # Print each row
        for row in rows:
            print(" | ".join(str(item) if item is not None else "" for item in row))
    else:
        # Get num of columns
        num_columns = len(cursor.description)

        # Print each row
        for row in rows:
            for i in range(num_columns):
                column_name = cursor.description[i][0]
                print(f"{column_name}: {row[i]}")
            print("-" * 20)

def GetTableData(cursor, table_name) -> list[tuple]:
    """
    Retrieve all data from a specified table.
    No validation of if the table exists is done here.

    :param cursor: MySQL cursor object
    :param table_name: Name of the table to retrieve data from
    :return: List of tuples containing the table data
    :rtype: list[tuple]
    """
    # Execute query to fetch all data
    cursor.execute(f"SELECT * FROM {table_name}")

    # Fetch all rows
    rows = cursor.fetchall()
    return rows

def GetTables(cursor) -> list[str]:
    """
    Retrieve a list of all table names in the 'outland_adventures' database.
    
    :param cursor: MySQL cursor object
    :return: List of table names
    :rtype: list[str]
    """
    cursor.execute("SHOW TABLES FROM outland_adventures;")
    tables = [row[0] for row in cursor.fetchall()]
    return tables

def GetDatabaseConnection() -> MySQLConnection | None :
    """
    Get a connection to the MySQL database.
    
    :return: MySQLConnection object or None if connection fails
    :rtype: MySQLConnection | None
    """

    #Was having issues with relative path settings when running locally.
    # Did this to figure out what was wrong
    current_directory = os.getcwd()
    #using our .env file
    secrets = dotenv_values(current_directory + "\\.env")

    """ database config object """
    config = {
        "user": secrets["USER"],
        "password": secrets["PASSWORD"],
        "host": secrets["HOST"],
        "database": secrets["DATABASE"],
        "raise_on_warnings": True #not in .env file
    }

    try:
        """ try/catch block for handling potential MySQL database errors """ 

        #db = mysql.connector.connect(**config) # connect to the movies database 
        db = MySQLConnection(**config)
        if db is not None:
            return db
    except mysql.connector.Error as err:
        """ on error code """

        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("  The supplied username or password are invalid")

        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("  The specified database does not exist")

        else:
            print(err)
    return None
 

def main():
    # Get a database connection
    conn = GetDatabaseConnection()
    if conn is not None:
        print("Successfully connected to the database.")
    else:
        print("Failed to connect to the database.")
        return
    
    # Create a cursor
    cursor = conn.cursor()

    # Get list of tables
    tables = GetTables(cursor)

    # Display data from each table
    for table in tables:
        display_table(cursor, table)

    # Close the cursor and connection
    cursor.close()
    conn.close()

if __name__ == "__main__":
    main()
