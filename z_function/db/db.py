import sqlite3
import os
import json

def create_table(cursor):
    """Create the products table if it doesn't exist."""
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS products (
        product_id TEXT PRIMARY KEY,
        product_name TEXT,
        price TEXT,
        image_link TEXT,
        description TEXT,
        href TEXT,
        category TEXT
    )
    """)

def filter_data(data):
    """Filter JSON data to match the database schema."""
    valid_keys = {
        "product-id": "product_id",
        "product_name": "product_name",
        "price": "price",
        "image_link": "image_link",
        "description": "description",
        "href": "href"
    }
    filtered_data = []
    for item in data:
        # Filter and rename keys to match the database schema
        filtered_item = {valid_keys[key]: item[key] for key in item if key in valid_keys}
        filtered_data.append(filtered_item)
    return filtered_data

def insert_data(cursor, data, category):
    """Insert data into the products table."""
    for item in data:
        item["category"] = category  # Add the category to the data
        cursor.execute("""
        INSERT OR REPLACE INTO products (
            product_id, product_name, price, image_link, description, href, category
        ) VALUES (
            :product_id, :product_name, :price, :image_link, :description, :href, :category
        )
        """, item)

def process_json_files_in_folder(folder_path, cursor, category):
    """Process all JSON files in a folder and insert data into SQLite."""
    for file_name in os.listdir(folder_path):
        if file_name.endswith(".json"):
            json_path = os.path.join(folder_path, file_name)
            with open(json_path, "r", encoding="utf-8") as file:
                data = json.load(file)

            # Ensure data is a list of dictionaries
            if isinstance(data, dict):
                data = [data]

            print(f"Processing {file_name} from {folder_path}...")
            filtered_data = filter_data(data)  # Filter and format data
            insert_data(cursor, filtered_data, category)

def main(furniture_list_path, sqlite_db):
    with open(furniture_list_path, "r") as file:
        categories = [line.split("/cat/")[1].split("/")[0].strip() for line in file if line.strip()]

    print(f"Categories found: {categories}")

    conn = sqlite3.connect(sqlite_db)
    cursor = conn.cursor()

    create_table(cursor)

    for category in categories:
        folder_path = os.path.join(category, "result")
        if os.path.exists(folder_path):
            print(f"Processing folder: {folder_path}")
            process_json_files_in_folder(folder_path, cursor, category)
        else:
            print(f"Folder does not exist: {folder_path}")

    conn.commit()
    conn.close()
    print(f"All data has been inserted into {sqlite_db}.")

# Configuration
furniture_list_path = "z_function/db/furniture_list_backup.txt"  # Path to the furniture list file
sqlite_db = "furniture.db"  # SQLite database file

main(furniture_list_path, sqlite_db)
