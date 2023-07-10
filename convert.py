import sqlite3
import csv


def convert_db_to_csv(db_file, table_name, csv_file):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # Retrieve all rows from the table
    cursor.execute(f"SELECT * FROM {table_name}")
    rows = cursor.fetchall()

    # Retrieve column names from the table
    cursor.execute(f"PRAGMA table_info({table_name})")
    columns = [column[1] for column in cursor.fetchall()]

    # Write rows to the CSV file
    with open(csv_file, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(columns)  # Write column names as the first row
        writer.writerows(rows)  # Write data rows

    conn.close()
    print(f"Successfully converted '{table_name}' table to '{csv_file}'")


# Example usage
db_file = "store.db"  # Replace with the actual name of your SQLite database file
table_name = "items"  # Replace with the name of the table you want to convert
csv_file = "items.csv"  # Specify the desired name for the CSV file

convert_db_to_csv(db_file, table_name, csv_file)
