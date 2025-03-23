import pandas as pd
import sqlite3

def excel_to_sqlite(excel_path, db_name="database.db"):
    """
    Reads an Excel file and saves each sheet as a separate table in an SQLite database.

    Args:
        excel_path (str): Path to the Excel file.
        db_name (str): Name of the SQLite database file.
    """
    # Load all sheets into a dictionary of DataFrames
    xls = pd.ExcelFile(excel_path)
    sheets = xls.sheet_names  # Get all sheet names
    
    # Connect to SQLite database (creates file if not exists)
    conn = sqlite3.connect(db_name)

    for sheet in sheets:
        df = pd.read_excel(xls, sheet_name=sheet)  # Read each sheet
        df.to_sql(sheet, conn, if_exists="replace", index=False)  # Save as table

    conn.close()  # Close the connection
    print(f"All sheets from {excel_path} saved to {db_name}")

# Example usage
excel_to_sqlite("my_data.xlsx", "my_database.db")