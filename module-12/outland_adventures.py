"""
outland_adventures.py
Connects to the outland_adventures MySQL database using .env credentials
and prints clean, presentation friendly report samples.

Expected folder layout:
module-11/
  outland_adventures.py
  .env
"""

import os
import mysql.connector
from mysql.connector import Error
from dotenv import dotenv_values
from prettytable import PrettyTable # Run "pip install PrettyTable" in terminal if you don't have it

def get_connection():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    secrets_path = os.path.join(script_dir, ".env")
    secrets = dotenv_values(secrets_path)

    required_keys = ["HOST", "USER", "PASSWORD", "DATABASE"]
    missing = [k for k in required_keys if k not in secrets or not secrets[k]]
    if missing:
        raise ValueError(
            f"Missing or empty values in .env for: {', '.join(missing)}. "
            f"Make sure .env is in: {script_dir}"
        )

    return mysql.connector.connect(
        host=secrets["HOST"],
        user=secrets["USER"],
        password=secrets["PASSWORD"],
        database=secrets["DATABASE"]
    )


def fmt_value(val, col_name=""):
    if val is None:
        return ""

    # Dates
    if hasattr(val, "strftime"):
        return val.strftime("%Y-%m-%d")

    # Money and percent formatting for report readability
    money_cols = {
        "Initial Cost", "Total Sale Revenue", "Total Rental Revenue", "Total Combined Revenue", "Total Profit"
    }
    percent_cols = {""}

    if col_name in money_cols:
        try:
            return f"${float(val):,.2f}"
        except Exception:
            return str(val)

    if col_name in percent_cols:
        try:
            return f"{float(val):.2f}%"
        except Exception:
            return str(val)

    # Default
    return str(val)


def print_table(cursor, title,query):
    print("\n" + title)
    print("-" * len(title))

    # Execute query to fetch all data
    cursor.execute(query)

    # Fetch all rows
    rows = cursor.fetchall()
    
    if not rows:
        print("No rows returned.")
        return
    # Create PrettyTable object
    table = PrettyTable(field_names=[])
    
    # Get column names
    table.field_names = [desc[0] for desc in cursor.description]

    # Add rows to the table
    # Add formatted rows
    formatted_rows = []
    formatted_row = []
    for row in rows:
        for i in range(len(row)):
            formatted_row.append(fmt_value(row[table.field_names[i]], table.field_names[i]))
        table.add_row(formatted_row)
        formatted_row = []

    
    # Print the table
    print(table)


def connect_and_print_reports():
    connection = None
    cursor = None

    try:
        connection = get_connection()
        print("Successfully connected to MySQL.")
        print("Database:", connection.database)

        cursor = connection.cursor(dictionary=True)

        # ------------------------------------------------------------
        # REPORT SAMPLE 1: Booking Summary by Trip and Region
        # ------------------------------------------------------------
        query = "SELECT * From RegionBookingParticipantsReport"
        print_table(
            cursor=cursor,
            title="Report Sample: Booking Summary by Trip and Region",
            query = query
        )

        # ------------------------------------------------------------
        # REPORT SAMPLE 2: Equipment Age and Inventory Status
        # ------------------------------------------------------------
        query = "SELECT * From EquipmentAgeAndInventoryStatus"

        print_table(
            cursor=cursor,
            title="Report Sample: Equipment Age and Inventory Status",
            query = query
        )

        # ------------------------------------------------------------
        # REPORT SAMPLE 3: Equipment Profit and Rental Performance
        # Uses the view EquipmentProfitViewWithRentals
        # ------------------------------------------------------------
        query = "SELECT * From EquipmentProfitViewWithRentals"

        print_table(
            cursor=cursor,
            title="Report Sample: Equipment Profit and Rental Performance",
            query = query
        )

        print("\nDone. MySQL connection will now close.")

    except Error as e:
        print(f"\nDatabase error: {e}")
    except ValueError as e:
        print(f"\nConfiguration error: {e}")
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()
            print("MySQL connection is closed.")


if __name__ == "__main__":
    connect_and_print_reports()
