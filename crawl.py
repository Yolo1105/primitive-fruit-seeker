import os
import json
import time
from concurrent.futures import ThreadPoolExecutor
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# Path to your downloaded ChromeDriver
CHROME_DRIVER_PATH = r"C:\Users\mohan\Downloads\chromedriver-win64\chromedriver-win64\chromedriver.exe"

# Base URL
BASE_URL = "https://www.ikea.com/us/en/cat/chairs-fu002/?page="

# Setup Chrome options
options = Options()
options.add_argument("--headless")  # Run in headless mode
options.add_argument("--disable-gpu")
options.add_argument("--disable-extensions")

# Function to fetch and save the body content
def fetch_and_save_body(page_number):
    url = f"{BASE_URL}{page_number}"
    print(f"Accessing: {url}")
    
    # Initialize WebDriver
    service = Service(CHROME_DRIVER_PATH)
    driver = webdriver.Chrome(service=service, options=options)
    
    try:
        # Navigate to the page
        driver.get(url)
        time.sleep(2)  # Wait for the page to load

        # Locate the <body> element
        try:
            body_content = driver.find_element("tag name", "body").get_attribute("outerHTML")
        except Exception as e:
            print(f"Failed to find the body content on page {page_number}: {e}")
            body_content = None

        # Ensure the 'chair' folder exists
        output_folder = "chair"
        os.makedirs(output_folder, exist_ok=True)

        # Save the extracted body content to a JSON file
        output_file = os.path.join(output_folder, f"page_{page_number}.json")
        with open(output_file, "w", encoding="utf-8") as file:
            json.dump({"page_number": page_number, "body_content": body_content}, file, indent=4)
        print(f"Page {page_number} body content saved as {output_file}.")
    except Exception as e:
        print(f"Failed to fetch page {page_number}: {e}")
    finally:
        driver.quit()  # Close the WebDriver instance

# Function to run parallel processing
def crawl_pages_concurrently(start_page, end_page, max_workers=4):
    """Crawls pages concurrently using ThreadPoolExecutor."""
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        executor.map(fetch_and_save_body, range(start_page, end_page + 1))

# Main execution
if __name__ == "__main__":
    start_time = time.time()
    crawl_pages_concurrently(start_page=1, end_page=14, max_workers=4)
    print(f"All pages have been processed in {time.time() - start_time:.2f} seconds.")
