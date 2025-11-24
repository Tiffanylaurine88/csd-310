"""
mysql_test.py
Module 6.2 – Movies: Setup
"""

import mysql.connector
from mysql.connector import errorcode

from dotenv import dotenv_values


# load secrets from .env file
secrets = dotenv_values(".env")

config = {
    "user": secrets["USER"],
    "password": secrets["PASSWORD"],
    "host": secrets["HOST"],
    "database": secrets["DATABASE"],
    "raise_on_warnings": True
}


def main():
    try:
        # connect to the database
        db = mysql.connector.connect(**config)

        print(
            f"\n  Database user {config['user']} connected to MySQL "
            f"on host {config['host']} with database {config['database']}"
        )

        input("\n\n  Press any key to continue...")

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("  The supplied username or password are invalid")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("  The specified database does not exist")
        else:
            print(err)
    finally:
        try:
            db.close()
        except NameError:
            # db was never created
            pass


if __name__ == "__main__":
    main()
