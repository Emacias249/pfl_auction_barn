from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
import time
import sys

def scrape(horse_url):
    # Set up Chrome options to run in headless mode
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")  # Optional: For running on certain environments
    chrome_options.add_argument("--disable-dev-shm-usage")  # Optional: For certain environments

    # Set up the WebDriver with Chrome options
    driver = webdriver.Chrome(options=chrome_options)

    # URL of the webpage to scrape
    driver.get(horse_url)

    # Wait for the page to load completely
    try:
        WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.XPATH, "//div")))
    except TimeoutException:
        print("Page took too long to load")
        driver.quit()
        return

    # Function to find elements with retry mechanism
    def find_elements_with_retry(by, value, retries=5, delay=1):
        for attempt in range(retries):
            try:
                elements = driver.find_elements(by, value)
                return elements
            except StaleElementReferenceException:
                time.sleep(delay)
        raise Exception("Element not found after several retries")

    # Function to safely get attribute with retry mechanism
    def get_attribute_with_retry(element, attribute, retries=5, delay=1):
        for attempt in range(retries):
            try:
                value = element.get_attribute(attribute)
                return value
            except StaleElementReferenceException:
                time.sleep(delay)
        raise Exception("Failed to get attribute after several retries")

    # Find all div elements
    div_elements = find_elements_with_retry(By.XPATH, "//div")

    # Extract the class names and inner HTML
    div_info = []
    for element in div_elements:
        for attempt in range(5):
            try:
                class_name = element.get_attribute("class")
                inner_html = element.get_attribute("innerHTML")
                div_info.append((class_name, inner_html))
                break
            except StaleElementReferenceException:
                time.sleep(1)
        else:
            print("Failed to get attributes after several retries")

    # Write the URL, class names, and inner HTML to a file with UTF-8 encoding
    with open('div_info.txt', 'w', encoding='utf-8') as file:
        file.write(f"Scraping URL: {horse_url}\n\n")
        for class_name, inner_html in div_info:
            file.write(f"Class: {class_name}\nHTML: {inner_html}\n\n")

    # Close the WebDriver
    driver.quit()

    print("Div information has been written to div_info.txt")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        scrape(sys.argv[1])
    else:
        print("No URL provided")
