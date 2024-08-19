from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException, WebDriverException
import time
import sys

def scrape(horse_url):
    # Set up Chrome options to run in headless mode
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    driver = None
    try:
        # Set up the WebDriver with Chrome options
        driver = webdriver.Chrome(options=chrome_options)

        # URL of the webpage to scrape
        driver.get(horse_url)

        # Wait for the page to load completely
        try:
            WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//div")))
        except TimeoutException:
            print("Page took too long to load")
            return

        # Function to safely get attribute with retry mechanism
        def get_attribute_with_retry(element, attribute, retries=5, delay=1):
            for attempt in range(retries):
                try:
                    value = element.get_attribute(attribute)
                    return value
                except StaleElementReferenceException:
                    time.sleep(delay)
            raise Exception("Failed to get attribute after several retries")

        # Find the first div element
        div_element = None
        for attempt in range(5):
            try:
                div_element = driver.find_element(By.XPATH, "//div")
                break
            except StaleElementReferenceException:
                time.sleep(1)
        else:
            print("Failed to find the first div element after several retries")
            return

        # Extract the class name and inner HTML of the first div element
        if div_element:
            class_name = get_attribute_with_retry(div_element, "class")
            inner_html = get_attribute_with_retry(div_element, "innerHTML")

            # Write the URL, class name, and inner HTML to a file with UTF-8 encoding
            with open('div_info.txt', 'w', encoding='utf-8') as file:
                file.write(f"Scraping URL: {horse_url}\n\n")
                file.write(f"Class: {class_name}\nHTML: {inner_html}\n\n")

            print("Div information has been written to div_info.txt")

    except WebDriverException as e:
        print(f"WebDriverException occurred: {str(e)}")

    finally:
        # Always ensure the WebDriver is closed to free up resources
        if driver:
            driver.quit()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        scrape(sys.argv[1])
    else:
        print("No URL provided")
