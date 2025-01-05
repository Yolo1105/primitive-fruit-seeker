import os
import json

def convert_to_json(input_file, output_file):
    try:
        with open(input_file, "r", encoding="utf-8") as file:
            content = file.read()
    except FileNotFoundError as e:
        print(f"Error reading {input_file}: {e}")
        return

    # Predefined keys for dimensions
    predefined_keys = [
        "Height including back cushions",
        "Backrest height",
        "Depth chaise",
        "Width",
        "Depth",
        "Seat depth, chaise lounge",
        "Height under furniture",
        "Armrest width",
        "Armrest height",
        "Seat width",
        "Seat depth",
        "Seat height"
    ]

    dimensions = {}
    for line in content.splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            key = key.strip()
            if key in predefined_keys:
                dimensions[key] = value.strip()

    # Save as JSON
    try:
        with open(output_file, "w", encoding="utf-8") as file:
            json.dump(dimensions, file, indent=4, ensure_ascii=False)
        print(f"Converted content saved to {output_file}")
    except Exception as e:
        print(f"Error saving to {output_file}: {e}")

def process_all_text_files(input_folder, output_folder):
    if os.path.exists(output_folder):
        for file in os.listdir(output_folder):
            file_path = os.path.join(output_folder, file)
            if os.path.isfile(file_path):
                os.remove(file_path)
    else:
        os.makedirs(output_folder, exist_ok=True)

    for file_name in os.listdir(input_folder):
        if file_name.endswith(".txt"):
            input_file = os.path.join(input_folder, file_name)
            output_file = os.path.join(output_folder, file_name.replace(".txt", ".json"))
            print(f"Processing {file_name}...")
            convert_to_json(input_file, output_file)

if __name__ == "__main__":
    input_folder = "input_text_files"  # Replace with your actual input folder
    output_folder = "output_json_files"  # Replace with your actual output folder
    process_all_text_files(input_folder, output_folder)
