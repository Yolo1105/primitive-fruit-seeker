import os
import json
from bs4 import BeautifulSoup

def extract_and_group_json(input_file, output_file):
    with open(input_file, "r", encoding="utf-8") as file:
        page_data = json.load(file)

    body_content = page_data.get("body_content", "")
    soup = BeautifulSoup(body_content, "html.parser")
    result = []
    start_divs = soup.find_all("div", attrs={"data-ref-id": True})

    for start_div in start_divs:
        group = {"content": []}
        current_node = start_div
        div_counter = 0

        while current_node:
            if current_node.name == "span" and "aria-label" in current_node.attrs:
                break

            if current_node.name == "div":
                div_counter += 1
                if div_counter == 1:
                    label = "compare"
                elif div_counter == 2:
                    label = "image"
                elif div_counter == 3:
                    label = "price"
                else:
                    label = "div_content"

                subgroup = {label: str(current_node)}
                group["content"].append(subgroup)
            else:
                group["content"].append({"raw_html": str(current_node)})

            current_node = current_node.find_next_sibling()

        result.append(group)

    with open(output_file, "w", encoding="utf-8") as output_file:
        json.dump(result, output_file, indent=4, ensure_ascii=False)

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
            extract_and_group_json(input_file, output_file)

input_folder_path = "sofas-sectionals-fu003/crawl"
output_folder_path = "sofas-sectionals-fu003/parse"

process_all_files(input_folder_path, output_folder_path)
