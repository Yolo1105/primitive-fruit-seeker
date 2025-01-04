import os
import re
import json
from bs4 import BeautifulSoup

input_dir = "sofas-sectionals-fu003/parse"
output_dir = "sofas-sectionals-fu003/result"
os.makedirs(output_dir, exist_ok=True)

def extract_data(file_content):
    soup = BeautifulSoup(file_content, "html.parser")
    result = {}

    main_div = soup.find("div", class_="plp-mastercard")
    if main_div:
        result["brand_name"] = main_div.get("data-product-name") or None
        result["data-ref-id"] = main_div.get("data-ref-id") or None
        result["data-price"] = main_div.get("data-price") or None
    else:
        result["brand_name"] = None
        result["data-ref-id"] = None
        result["data-price"] = None

    description_tag = soup.find("span", class_="plp-price-module__description")
    if description_tag and description_tag.text:
        result["description"] = description_tag.text.replace("\"", "").strip()
    else:
        result["description"] = None

    href_tag = soup.find("a", href=True)
    if href_tag and href_tag.get("href"):
        href = href_tag["href"].strip()
        result["href"] = href
        match = re.search(r"/p/(.*)-\d+/", href)
        if match:
            result["product_name"] = match.group(1)
        else:
            result["product_name"] = None
    else:
        result["href"] = None
        result["product_name"] = None

    reordered_result = {
        "product_name": result.get("product_name"),
        "brand_name": result.get("brand_name"),
        "data-ref-id": result.get("data-ref-id"),
        "data-price": result.get("data-price"),
        "description": result.get("description"),
        "href": result.get("href")
    }
    return reordered_result

for filename in os.listdir(input_dir):
    input_path = os.path.join(input_dir, filename)
    if os.path.isfile(input_path):
        with open(input_path, "r", encoding="utf-8") as file:
            content = file.read()
        data = extract_data(content)
        output_path = os.path.join(output_dir, f"{os.path.splitext(filename)[0]}.json")
        with open(output_path, "w", encoding="utf-8") as outfile:
            json.dump(data, outfile, indent=4)
