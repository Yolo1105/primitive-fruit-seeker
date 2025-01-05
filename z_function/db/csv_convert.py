import sqlite3
import csv

# Connect to the database
conn = sqlite3.connect("furniture.db")
cursor = conn.cursor()

# Query the data
cursor.execute("SELECT * FROM products")
rows = cursor.fetchall()

# Export to CSV
with open("furniture.csv", "w", newline="", encoding="utf-8") as csvfile:
    csvwriter = csv.writer(csvfile)
    # Write headers
    column_names = [desc[0] for desc in cursor.description]
    csvwriter.writerow(column_names)
    # Write data
    csvwriter.writerows(rows)

print("Data exported to furniture.csv")
conn.close()
