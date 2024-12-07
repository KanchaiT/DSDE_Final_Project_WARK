from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import json
import time
from bs4 import BeautifulSoup

# Your login credentials
email = "wark.cedt@gmail.com"
password = "wark_404_cedt"

chrome_options = Options()
chrome_options.add_argument("--disable-gpu")  # Disable GPU acceleration (useful for some environments)
webdriver_path = r"C:/Users/Public/Documents/My/DataSci/chromedriver-win64/chromedriver.exe"

# Create a Service object
service = Service(webdriver_path)

# Optional: Add Chrome options if needed
chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument("--headless")  # Run in headless mode

# Initialize the WebDriver using the Service object
driver = webdriver.Chrome(service=service, options=chrome_options)


def scraping(url,i,output_folder):
    try:
        print(f"Opening page: {url}") 
        driver.get(url)
        WebDriverWait(driver,10).until(lambda d: d.execute_script('return document.readyState') == 'complete')

        if driver.find_element(By.ID,"signin_link_move"):
            btn = driver.find_element(By.ID,"signin_link_move")
            btn.submit()
            WebDriverWait(driver,5).until(lambda d: d.execute_script('return document.readyState') == 'complete')

            email_field = driver.find_element(By.ID, "bdd-email")  # Update this selector if necessary
            email_field.send_keys(email)
            WebDriverWait(driver,5).until(lambda d: d.execute_script('return document.readyState') == 'complete')

            email_field.send_keys(Keys.RETURN)
            WebDriverWait(driver,5).until(lambda d: d.execute_script('return document.readyState') == 'complete')

            btn.click()
            WebDriverWait(driver,5).until(lambda d: d.execute_script('return document.readyState') == 'complete')

            password_field = driver.find_element(By.ID, "bdd-password")  # Update this selector if necessary
            password_field.send_keys(password)
            WebDriverWait(driver,5).until(lambda d: d.execute_script('return document.readyState') == 'complete')

            password_field.send_keys(Keys.RETURN)
            WebDriverWait(driver,5).until(lambda d: d.execute_script('return document.readyState') == 'complete')

            btn = driver.find_element(By.ID,"bdd-elsPrimaryBtn")
            btn.click()
            WebDriverWait(driver,5).until(lambda d: d.execute_script('return document.readyState') == 'complete')
        

        # Save the full HTML content to a file
        full_html = BeautifulSoup(driver.page_source,"lxml")
        os.makedirs(output_folder, exist_ok=True)  # สร้างโฟลเดอร์ถ้ายังไม่มี
        output_file = os.path.join(output_folder, f"{i}.html")
        with open(output_file, "w", encoding="utf-8") as html_file:
            html_file.write(str(full_html))
        print(f"Full HTML content saved to {output_file}")

    finally:
        # Close the WebDriver
        driver.quit()                       

def process_all_json_files(input_file, output_folder):
    i = 0
    # Loop through all link in file
    with open(input_file, 'r') as file:
        for link in [line.strip() for line in file.readlines() if line.strip()]:
            i=i+1
            scraping(link,i,output_folder)


input_file = "Scraping/INPUT_link/link_test.txt"
output_folder = "Scraping/OUTPUT_html/test/"
process_all_json_files(input_file, output_folder)