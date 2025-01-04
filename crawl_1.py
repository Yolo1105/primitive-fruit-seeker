import os
import json
import time
from concurrent.futures import ThreadPoolExecutor
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

CHROME_DRIVER_PATH = r"C:\Users\mohan\Downloads\chromedriver-win64\chromedriver-win64\chromedriver.exe"

def get_folder_name(base_url):
    start = base_url.find("/cat/") + len("/cat/")
    end = base_url.find("/", start)
    return base_url[start:end]

def fetch_and_save_body(base_url, page_number, crawl_folder):
    url = f"{base_url}?page={page_number}"
    service = Service(CHROME_DRIVER_PATH)
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-extensions")
    driver = webdriver.Chrome(service=service, options=options)
    
    try:
        driver.get(url)
        time.sleep(2)
        body_content = driver.find_element("tag name", "body").get_attribute("outerHTML")
        if "no results" in body_content.lower() or "no items found" in body_content.lower():
            return False
        os.makedirs(crawl_folder, exist_ok=True)
        output_file = os.path.join(crawl_folder, f"page_{page_number}.json")
        with open(output_file, "w", encoding="utf-8") as file:
            json.dump({"page_number": page_number, "body_content": body_content}, file, indent=4)
        return True
    finally:
        driver.quit()

def crawl_category(base_url):
    folder_name = get_folder_name(base_url)
    crawl_folder = os.path.join(folder_name, "crawl")
    os.makedirs(crawl_folder, exist_ok=True)
    for page_number in range(1, 10):
        success = fetch_and_save_body(base_url, page_number, crawl_folder)
        if not success:
            break

def crawl_multiple_categories(urls, max_workers=4):
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        executor.map(crawl_category, urls)

if __name__ == "__main__":
    start_time = time.time()
    with open("furniture_list.txt", "r") as file:
        urls = [line.strip() for line in file if line.strip()]
    crawl_multiple_categories(urls, max_workers=4)
    print(f"All pages have been processed in {time.time() - start_time:.2f} seconds.")
