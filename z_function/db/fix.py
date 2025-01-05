import os
import json

def process_json_files_in_folder(folder_path):
    """Process all JSON files in a folder to update 'data_price' to 'price'."""
    for file_name in os.listdir(folder_path):
        if file_name.endswith(".json"):
            json_path = os.path.join(folder_path, file_name)

            # Read the JSON data
            with open(json_path, "r", encoding="utf-8") as file:
                data = json.load(file)

            # Ensure data is a list of dictionaries
            if isinstance(data, dict):
                data = [data]

            updated_data = []
            for item in data:
                if "data_price" in item:
                    # Update the price field
                    item["price"] = item["data_price"].replace("$", "").strip()
                    del item["data_price"]  # Remove the old 'data_price' key
                updated_data.append(item)

            # Save the updated data back to the JSON file
            with open(json_path, "w", encoding="utf-8") as file:
                json.dump(updated_data, file, indent=4, ensure_ascii=False)

            print(f"Updated {file_name} in {folder_path}")

def main(furniture_list_path):
    # Extract category names from the furniture list
    with open(furniture_list_path, "r") as file:
        categories = [line.split("/cat/")[1].split("/")[0].strip() for line in file if line.strip()]

    print(f"Categories found: {categories}")

    # Loop over each category folder
    for category in categories:
        folder_path = os.path.join(category, "result")
        if os.path.exists(folder_path):
            print(f"Processing folder: {folder_path}")
            process_json_files_in_folder(folder_path)
        else:
            print(f"Folder does not exist: {folder_path}")

    print("All JSON files have been updated.")

# Configuration
furniture_list_path = "furniture_list_backup.txt"  # Path to the furniture list file

# Run the script
main(furniture_list_path)
