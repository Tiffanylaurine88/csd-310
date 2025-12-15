import DisplayTableData as TableData

def main():
    # Get a database connection
    conn = TableData.GetDatabaseConnection()
    if conn is not None:
        print("Successfully connected to the database.")
    else:
        print("Failed to connect to the database.")
        return
    
    # Create a cursor
    cursor = conn.cursor()

    # Get Report from view
    TableData.display_table(cursor, "EquipmentAgeAndInventoryStatus", False)

    # Close the cursor and connection
    cursor.close()
    conn.close()

if __name__ == "__main__":
    main()