import os
import json

def extract_and_group_json(input_file, output_file):
    try:
        with open(input_file, "r", encoding="utf-8") as file:
            page_data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error reading {input_file}: {e}")
        return

    body_content = page_data.get("body_content", "")
    if not body_content:
        print(f"No body content found in {input_file}")
        return

    # Extract the plain text between the start and end markers
    start_marker = '<div class=\"plp-product-list__products \">'
    end_marker = '<a id=\"products-page-'

    start_index = body_content.find(start_marker)
    end_index = body_content.find(end_marker)

    if start_index == -1:
        print(f"Start marker not found in {input_file}")
        return
    if end_index == -1:
        print(f"End marker not found in {input_file}")
        return

    # Include the start marker and exclude the end marker
    extracted_content = body_content[start_index:end_index]

    try:
        with open(output_file, "w", encoding="utf-8") as file:
            json.dump({"content": extracted_content}, file, indent=4, ensure_ascii=False)
        print(f"Extracted content saved to {output_file}")
    except Exception as e:
        print(f"Error saving to {output_file}: {e}")

def process_all_files(input_folder, output_folder):
    if os.path.exists(output_folder):
        for file in os.listdir(output_folder):
            file_path = os.path.join(output_folder, file)
            if os.path.isfile(file_path):
                os.remove(file_path)
    else:
        os.makedirs(output_folder, exist_ok=True)

    for file_name in os.listdir(input_folder):
        if file_name.endswith(".json"):
            input_file = os.path.join(input_folder, file_name)
            output_file = os.path.join(output_folder, file_name)
            print(f"Processing {file_name}...")
            extract_and_group_json(input_file, output_file)

def process_files_from_furniture_list():
    with open("furniture_list.txt", "r") as file:
        urls = [line.strip() for line in file if line.strip()]

    for url in urls:
        folder_name = url.split("/cat/")[1].split("/")[0]
        input_folder_path = os.path.join(folder_name, "crawl")
        output_folder_path = os.path.join(folder_name, "parse")

        # Ensure directories exist
        os.makedirs(input_folder_path, exist_ok=True)
        os.makedirs(output_folder_path, exist_ok=True)

        process_all_files(input_folder_path, output_folder_path)


if __name__ == "__main__":
    process_files_from_furniture_list()
