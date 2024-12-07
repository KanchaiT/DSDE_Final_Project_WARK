from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException, WebDriverException
import os
from bs4 import BeautifulSoup
import time

# Your login credentials
email = "wark.cedt@gmail.com"
password = "wark_404_cedt"

# ChromeDriver setup
chrome_options = Options()
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

webdriver_path = "/usr/local/bin/chromedriver"

def create_driver():
    """Creates and returns a new WebDriver instance."""
    service = Service(webdriver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

def wait_and_click(driver, by, value, timeout=10):
    """Waits for an element to be clickable and clicks it."""
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((by, value))
        )
        element.click()
        print("Element clicked successfully!")
    except TimeoutException:
        print(f"Element with {by}='{value}' not found within {timeout} seconds.")
    except StaleElementReferenceException:
        print("StaleElementReferenceException occurred. Retrying...")
        element = driver.find_element(by, value)
        element.click()
    except Exception as e:
        print(f"Error clicking element: {e}")

def scraping(driver, url, i, output_folder):
    """Scrapes the content of a webpage and saves it to a file."""
    try:
        print(f"Opening page: {url}")
        driver.get(url)
        WebDriverWait(driver, 10).until(lambda d: d.execute_script('return document.readyState') == 'complete')

        # Handle redirection to SSO login page
        if "id.elsevier.com" in driver.current_url:
            print("Redirected to Elsevier login page.")
            try:
                email_field = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.ID, "bdd-email"))
                )
                email_field.send_keys(email)
                email_field.send_keys(Keys.RETURN)

                password_field = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.ID, "bdd-password"))
                )
                password_field.send_keys(password)
                password_field.send_keys(Keys.RETURN)

                print("SSO login completed.")
            except Exception as e:
                print(f"Error during SSO login: {e}")
                return  # Skip further processing if login fails

        if driver.find_elements(By.ID, "signin_link_move"):
            wait_and_click(driver, By.ID, "signin_link_move")

        # Check and click primary button
        if driver.find_elements(By.ID, "bdd-elsPrimaryBtn"):
            wait_and_click(driver, By.ID, "bdd-elsPrimaryBtn", timeout=20)
        else:
            print("Primary button not found in the current DOM. Skipping...")

        # Save the full HTML content to a file
        full_html = BeautifulSoup(driver.page_source, "lxml")
        os.makedirs(output_folder, exist_ok=True)
        output_file = os.path.join(output_folder, f"{i}.html")
        with open(output_file, "w", encoding="utf-8") as html_file:
            html_file.write(full_html.prettify())
        print(f"Full HTML content saved to {output_file}")

    except WebDriverException as e:
        print(f"Error during scraping: {e}")
        print(f"Current URL: {driver.current_url}")
        print(f"Page Source:/n{driver.page_source[:500]}")
    except Exception as e:
        print(f"Unexpected error: {e}")


def process_all_json_files(input_file, output_folder):
    """Processes all URLs in the input file."""
    i = 0
    try:
        with open(input_file, 'r') as file:
            links = [line.strip() for line in file.readlines() if line.strip()]

        for link in links:
            i += 1
            try:
                driver = create_driver()  # Create a new driver for each link
                scraping(driver, link, i, output_folder)
            except Exception as e:
                print(f"Error processing URL {link}: {e}")
            finally:
                driver.quit()
                time.sleep(1)  # Add delay between requests to avoid overloading server

    except Exception as e:
        print(f"Error processing input file: {e}")

# Input and output paths
input_file = "Scraping/INPUT_link/link_test.txt"
output_folder = "Scraping/OUTPUT_html/test/"
process_all_json_files(input_file, output_folder)
