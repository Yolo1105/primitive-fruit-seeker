import json
from bs4 import BeautifulSoup

def extract_and_group_json(input_file, output_file):
    # Load the JSON content
    with open(input_file, "r", encoding="utf-8") as file:
        page_data = json.load(file)

    # Extract the body content
    body_content = page_data.get("body_content", "")

    # Parse the HTML content
    soup = BeautifulSoup(body_content, "html.parser")

    # Initialize the result list
    result = []

    # Find all <div data-ref-id> and iterate over them
    start_divs = soup.find_all("div", attrs={"data-ref-id": True})

    for start_div in start_divs:
        # Create a new group for each <div data-ref-id>
        group = {"content": []}
        current_node = start_div

        div_counter = 0  # Counter to track <div> positions in the group

        while current_node:
            # Stop copying if <span aria-label> is found
            if current_node.name == "span" and "aria-label" in current_node.attrs:
                break

            # Check if the current node is a <div> and assign a subgroup label
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
                # Otherwise, just add the raw HTML of the current node
                group["content"].append({"raw_html": str(current_node)})

            # Move to the next sibling
            current_node = current_node.find_next_sibling()

        # Add the group to the result list
        result.append(group)

    # Save the result as JSON
    with open(output_file, "w", encoding="utf-8") as output_file:
        json.dump(result, output_file, indent=4, ensure_ascii=False)

    print(f"Extracted content saved to {output_file.name}")

# Input and output file paths
input_file_path = "chair/page_14.json"  # Replace with the path to your input JSON file
output_file_path = "grouped_extracted_content.json"  # Replace with the desired output path

# Run the function
extract_and_group_json(input_file_path, output_file_path)
