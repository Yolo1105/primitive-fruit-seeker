import re
import json
from bs4 import BeautifulSoup

# The input HTML data
data = """<div class=\"plp-mastercard\" data-cs-capture=\"\" data-currency=\"USD\" data-price=\"99.99\" data-product-compact=\"\" data-product-name=\"HEMNES\" data-product-number=\"70245872\" data-ref-id=\"70245872\" data-testid=\"plp-product-card\"><div class=\"plp-mastercard__item plp-mastercard__compare\"><div class=\"plp-listing-compare-wrapper\"><span class=\"plp-checkbox--subtle plp-checkbox plp-listing-compare-checkbox\"><input aria-label='Select for product comparison, Bench with shoe storage, 33 1/2x12 5/8x25 5/8 \"' id=\"plp-compact-compare-checkbox-70245872\" name=\"checkboxname\" type=\"checkbox\" value=\"compare-70245872\"/><span class=\"plp-checkbox__symbol\"></span><span class=\"plp-checkbox__label\"><label for=\"plp-compact-compare-checkbox-70245872\">Compare</label></span></span></div></div><div class=\"plp-mastercard__item plp-mastercard__image\"><a aria-disabled=\"false\" aria-hidden=\"true\" class=\"plp-product__image-link link\" href=\"https://www.ikea.com/us/en/p/hemnes-bench-with-shoe-storage-black-brown-70245872/\"><img class=\"plp-image plp-product__image\" loading=\"lazy\" src=\"https://www.ikea.com/us/en/images/products/hemnes-bench-with-shoe-storage-black-brown__0710743_pe727761_s5.jpg?f=xxs\"/><img class=\"image plp-product__image plp-product__image--alt\" loading=\"lazy\" src=\"https://www.ikea.com/us/en/images/products/hemnes-bench-with-shoe-storage-black-brown__1151277_pe886187_s5.jpg?f=xxs\"/></a></div><div class=\"plp-mastercard__item plp-mastercard__price\"><a aria-disabled=\"false\" class=\"plp-price-link-wrapper link\" href=\"https://www.ikea.com/us/en/p/hemnes-bench-with-shoe-storage-black-brown-70245872/\"><div class=\"plp-price-module plp-price-module--small plp-price-module--commercial-message-placeholder plp-price-module--none\"><div class=\"plp-price-module__information\"><h3 class=\"plp-price-module__name notranslate\"><span class=\"plp-price-module__name-decorator\"><span class=\"notranslate plp-price-module__product-name\">HEMNES</span></span> <span class=\"plp-price-module__description\">Bench with shoe storage, 33 1/2x12 5/8x25 5/8 \"</span></h3></div><div class=\"plp-price-module__price\"><div class=\"plp-price-module__primary-currency-price\"><span class=\"plp-price plp-price--leading plp-price--leading plp-price--medium plp-price--currency-super-aligned plp-price--decimal-super-aligned plp-price-module__current-price notranslate\"><span aria-hidden=\"true\" class=\"notranslate\"><span class=\"plp-price__nowrap\"><span class=\"plp-price__currency\">$</span><span class=\"plp-price__integer\">99</span></span><span class=\"plp-price__decimal\"><span class=\"plp-price__separator\">.</span>99</span></span><span class=\"plp-price__sr-text\">Price $ 99.99</span></span></div></div></div></a><button class=\"plp-ratings-button--product-card\"><span aria-label=\"Review: 4.8 out of 5 stars. Total reviews: 197\" class=\"plp-ratings plp-ratings--small plp-ratings--product-card notranslate\" role=\"img\"><svg class=\"plp-ratings-icon\"><use href=\"#plp-filled_star\"></use></svg><svg class=\"plp-ratings-icon\"><use href=\"#plp-filled_star\"></use></svg><svg class=\"plp-ratings-icon\"><use href=\"#plp-filled_star\"></use></svg><svg class=\"plp-ratings-icon\"><use href=\"#plp-filled_star\"></use></svg><svg class=\"plp-ratings-icon\"><use href=\"#plp-filled_star\"></use></svg><span class=\"plp-ratings-label\">(197)</span></span></button></div><div class=\"plp-mastercard__item plp-mastercard__button-container\"><div class=\"plp-button-container\"><button aria-label='Add \"HEMNES Bench with shoe storage\" to cart' class=\"plp-btn plp-btn--small plp-btn--icon-emphasised\" type=\"button\"><span class=\"plp-btn__inner\"><svg aria-hidden=\"true\" class=\"plp-svg-icon plp-btn__icon\" focusable=\"false\" height=\"24\" viewbox=\"0 0 24 24\" width=\"24\"><use href=\"#plp-add_to_cart\"></use></svg></span></button><button aria-label='Save \"HEMNES Bench with shoe storage\" to shopping list' class=\"plp-btn plp-btn--small plp-btn--icon-tertiary btn--wishlist\" type=\"button\"><span class=\"plp-btn__inner\"><svg aria-hidden=\"true\" class=\"plp-svg-icon plp-btn__icon\" focusable=\"false\" height=\"24\" viewbox=\"0 0 24 24\" width=\"24\"><use href=\"#plp-add_to_favourites\"></use></svg></span></button></div></div><div class=\"plp-mastercard__item plp-mastercard__availability\"><div class=\"plp-availability-information\"><span class=\"plp-status plp-status--green plp-status--labelled plp-status--leading\" data-skapa-n=\"@ingka/status\" data-skapa-v=\"10.1.11\"><span class=\"plp-status__label\">Available for delivery</span><span class=\"plp-status__dot\"></span></span></div><div class=\"plp-availability-information\"><span class=\"plp-status plp-status--green plp-status--labelled plp-status--leading\" data-skapa-n=\"@ingka/status\" data-skapa-v=\"10.1.11\"><span class=\"plp-status__label\">In stock at Brooklyn, NY</span><span class=\"plp-status__dot\"></span></span></div></div><div class=\"plp-mastercard__item plp-mastercard__thumbnails\"></div></div>"""

# Parse the HTML using BeautifulSoup
soup = BeautifulSoup(data, "html.parser")

def extract_data(soup):
    result = {}
    # Locate the main div with the relevant attributes
    main_div = soup.find("div", class_="plp-mastercard")
    if main_div:
        result["brand_name"] = main_div.get("data-product-name")
        result["data-ref-id"] = main_div.get("data-ref-id")
        result["data-price"] = main_div.get("data-price")
    else:
        result["brand_name"] = None
        result["data-ref-id"] = None
        result["data-price"] = None

    # Extract description
    description_tag = soup.find("span", class_="plp-price-module__description")
    if description_tag:
        # Remove escaped double quotes
        result["description"] = description_tag.text.replace("\"", "").strip()
    
    # Extract href and real_name
    href_tag = soup.find("a", href=True)
    if href_tag:
        result["href"] = href_tag["href"]  # Ensure href is extracted
        match = re.search(r"/p/(.*)-\d+/", href_tag["href"])
        if match:
            result["product_name"] = match.group(1)
    
    # Reorder keys
    reordered_result = {
        "product_name": result.pop("product_name", None),
        "brand_name": result.pop("brand_name", None),
        "data-ref-id": result.pop("data-ref-id", None),
        "data-price": result.pop("data-price", None),
        "description": result.pop("description", None),
        "href": result.pop("href", None)  # Ensure href is included
    }
    return reordered_result

# Apply the extraction
output = extract_data(soup)

# Convert to JSON
json_output = json.dumps(output, indent=4)

print(json_output)