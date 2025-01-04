import os
import json


def extract_products(content, filename):
    print(f"Processing content from {filename}")

    results = []

    start_index = 0
    while True:
        product = {}

        # Locate <div data-ref-id="
        start_index = content.find('<div data-ref-id="', start_index)
        if start_index == -1:
            break

        # Extract product-id (formerly data-ref-id)
        start_index += len('<div data-ref-id="')
        end_index = content.find('"', start_index)
        product['product-id'] = content[start_index:end_index]

        # Locate class="notranslate plp-price-module__product-name">
        temp_index = content.find('class="notranslate plp-price-module__product-name">', end_index)
        if temp_index != -1:
            temp_index += len('class="notranslate plp-price-module__product-name">')
            temp_end = content.find('</', temp_index)
            product['product_name'] = content[temp_index:temp_end].strip()
        else:
            product['product_name'] = None

        # Locate class="plp-price__sr-text">Price
        temp_index = content.find('class="plp-price__sr-text">Price', end_index)
        if temp_index != -1:
            temp_index += len('class="plp-price__sr-text">Price')
            temp_end = content.find('</span>', temp_index)
            product['data_price'] = content[temp_index:temp_end].strip()
        else:
            product['data_price'] = None

        # Locate class="plp-product__image-link link"><img src="
        temp_index = content.find('class="plp-product__image-link link"><img src="', end_index)
        if temp_index != -1:
            temp_index += len('class="plp-product__image-link link"><img src="')
            temp_end = content.find('"', temp_index)
            product['image_link'] = content[temp_index:temp_end].strip()
        else:
            product['image_link'] = None

        # Locate class="plp-price-module__description">
        temp_index = content.find('class="plp-price-module__description">', end_index)
        if temp_index != -1:
            temp_index += len('class="plp-price-module__description">')
            temp_end = content.find('</', temp_index)
            product['description'] = content[temp_index:temp_end].strip()
        else:
            product['description'] = None

        # Locate <a aria-hidden="true" href="
        temp_index = content.find('<a aria-hidden="true" href="', end_index)
        if temp_index != -1:
            temp_index += len('<a aria-hidden="true" href="')
            temp_end = content.find('"', temp_index)
            product['href'] = content[temp_index:temp_end].strip()
        else:
            product['href'] = None

        # Add the product to results
        results.append(product)
        print(f"Extracted product: {product}")

        # Update start_index to continue parsing after the current product
        start_index = end_index

    print(f"Final extracted data from {filename}: {json.dumps(results, indent=2)}")
    return results


def process_files(input_dir, output_dir):
    os.makedirs(output_dir, exist_ok=True)

    for filename in os.listdir(input_dir):
        if filename.endswith(".json"):
            input_path = os.path.join(input_dir, filename)
            output_path = os.path.join(output_dir, filename)

            print(f"Reading file: {input_path}")
            with open(input_path, "r", encoding="utf-8") as file:
                content = json.load(file).get("content", "")

            if not content:
                print(f"File {filename} has no content. Skipping.")
                continue

            products = extract_products(content, filename)

            print(f"Writing grouped results to: {output_path}")
            with open(output_path, "w", encoding="utf-8") as output_file:
                json.dump(products, output_file, indent=4, ensure_ascii=False)

            print(f"Finished processing {filename}\n{'-' * 40}")


if __name__ == "__main__":
    input_directory = "sofas-sectionals-fu003/parse"
    output_directory = "sofas-sectionals-fu003/result"
    process_files(input_directory, output_directory)
