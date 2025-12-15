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
        "InitialCost", "SalePrice", "RentalPrice", "SaleProfit", "TotalRentalRevenue"
    }
    percent_cols = {"RentalROI_Percent"}

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


def print_table(title, rows, columns, max_rows=15):
    print("\n" + title)
    print("-" * len(title))

    if not rows:
        print("No rows returned.")
        return

    # Convert to list of list strings
    data = []
    for r in rows[:max_rows]:
        data.append([fmt_value(r.get(col), col) for col in columns])

    # Compute column widths
    widths = []
    for i, col in enumerate(columns):
        widest = len(col)
        for row in data:
            widest = max(widest, len(row[i]))
        widths.append(widest)

    # Header
    header = " | ".join(columns[i].ljust(widths[i]) for i in range(len(columns)))
    sep = "-+-".join("-" * widths[i] for i in range(len(columns)))
    print(header)
    print(sep)

    # Rows
    for row in data:
        line = " | ".join(row[i].ljust(widths[i]) for i in range(len(columns)))
        print(line)

    if len(rows) > max_rows:
        print(f"\n(Showing first {max_rows} rows out of {len(rows)})")


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
        booking_summary_query = """
            SELECT
                t.TripID,
                t.Destination,
                t.Region,
                t.StartDate,
                t.EndDate,
                b.BookingDate,
                b.Status,
                b.NumberOfParticipants
            FROM Trip t
            JOIN Booking b ON t.TripID = b.TripID
            ORDER BY t.Region, t.StartDate;
        """
        cursor.execute(booking_summary_query)
        booking_rows = cursor.fetchall()

        print_table(
            title="Report Sample: Booking Summary by Trip and Region",
            rows=booking_rows,
            columns=[
                "TripID",
                "Destination",
                "Region",
                "StartDate",
                "EndDate",
                "BookingDate",
                "Status",
                "NumberOfParticipants"
            ],
            max_rows=12
        )

        # ------------------------------------------------------------
        # REPORT SAMPLE 2: Equipment Age and Inventory Status
        # ------------------------------------------------------------
        equipment_age_query = """
            SELECT
                EquipmentID,
                Name,
                Category,
                EquipCondition,
                AvailableQuantity,
                PurchaseDate,
                TIMESTAMPDIFF(YEAR, PurchaseDate, CURDATE()) AS YearsSincePurchase,
                CASE
                    WHEN TIMESTAMPDIFF(YEAR, PurchaseDate, CURDATE()) >= 5 THEN 'Over 5 Years Old'
                    ELSE 'Under 5 Years Old'
                END AS AgeStatus
            FROM Equipment
            ORDER BY YearsSincePurchase DESC, Name;
        """
        cursor.execute(equipment_age_query)
        equipment_age_rows = cursor.fetchall()

        print_table(
            title="Report Sample: Equipment Age and Inventory Status",
            rows=equipment_age_rows,
            columns=[
                "EquipmentID",
                "Name",
                "Category",
                "EquipCondition",
                "AvailableQuantity",
                "PurchaseDate",
                "YearsSincePurchase",
                "AgeStatus"
            ],
            max_rows=12
        )

        # ------------------------------------------------------------
        # REPORT SAMPLE 3: Equipment Rental vs Purchase Totals
        # ------------------------------------------------------------
        rental_vs_purchase_query = """
            SELECT
                e.EquipmentID,
                e.Name,
                e.Category,
                SUM(CASE WHEN t.TransactionType = 'Purchase' THEN t.Quantity ELSE 0 END) AS TotalPurchased,
                SUM(CASE WHEN t.TransactionType = 'Rental' THEN t.Quantity ELSE 0 END) AS TotalRented
            FROM Equipment e
            LEFT JOIN EquipmentTransaction t ON e.EquipmentID = t.EquipmentID
            GROUP BY e.EquipmentID, e.Name, e.Category
            ORDER BY TotalPurchased DESC, TotalRented DESC;
        """
        cursor.execute(rental_vs_purchase_query)
        rvsp_rows = cursor.fetchall()

        print_table(
            title="Report Sample: Equipment Rental vs Purchase Totals",
            rows=rvsp_rows,
            columns=[
                "EquipmentID",
                "Name",
                "Category",
                "TotalPurchased",
                "TotalRented"
            ],
            max_rows=12
        )

        # ------------------------------------------------------------
        # REPORT SAMPLE 4: Equipment Profit and Rental Performance
        # Uses the view EquipmentProfitViewWithRentals
        # ------------------------------------------------------------
        equipment_profit_query = """
            SELECT
                EquipmentID,
                Name,
                Category,
                InitialCost,
                SalePrice,
                SaleProfit,
                RentalPrice,
                RentalROI_Percent,
                TotalRentalRevenue,
                TotalRentalCount
            FROM EquipmentProfitViewWithRentals
            ORDER BY EquipmentID;
        """
        cursor.execute(equipment_profit_query)
        profit_rows = cursor.fetchall()

        print_table(
            title="Report Sample: Equipment Profit and Rental Performance",
            rows=profit_rows,
            columns=[
                "EquipmentID",
                "Name",
                "Category",
                "InitialCost",
                "SalePrice",
                "SaleProfit",
                "RentalPrice",
                "RentalROI_Percent",
                "TotalRentalRevenue",
                "TotalRentalCount"
            ],
            max_rows=12
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
