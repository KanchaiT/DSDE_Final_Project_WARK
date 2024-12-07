from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
import json
import time

# Your login credentials
email = "wark.cedt@gmail.com"
password = "wark_404_cedt"

# URL of the Scopus login page and target record
login_url = "https://www.scopus.com/home.uri"
record_url = "https://www.scopus.com/record/display.uri?eid=2-s2.0-85179929360&origin=inward"

print(f"Opening page: {record_url}")  # Print progress as soon as the page starts loading
chrome_options = Options()
chrome_options.add_argument("--disable-gpu")  # Disable GPU acceleration (useful for some environments)
webdriver_path = r"C:/Users/Public/Documents/My/DataSci/chromedriver-win64/chromedriver.exe"

# Create a Service object
service = Service(webdriver_path)

# Optional: Add Chrome options if needed
chrome_options = webdriver.ChromeOptions()

# Initialize the WebDriver using the Service object
driver = webdriver.Chrome(service=service, options=chrome_options)

try:
    # Step 1: Open the login page
    driver.get(login_url)
    time.sleep(3)  # Wait for the page to load

    # Step 2: Find and fill the email input field
    email_field = driver.find_element(By.ID, "bdd-email")  # Update this selector if necessary
    email_field.send_keys(email)

    # Step 3: Submit email and move to password step
    email_field.send_keys(Keys.RETURN)
    time.sleep(2)  # Adjust time as necessary for the next step to load

    # Step 4: Find and fill the password input field
    password_field = driver.find_element(By.ID, "bdd-password")  # Update this selector if necessary
    password_field.send_keys(password)

    # Step 5: Submit the login form
    password_field.send_keys(Keys.RETURN)
    time.sleep(5)  # Wait for the login to complete

    # Step 6: Navigate to the specific Scopus record after login
    driver.get(record_url)
    driver.implicitly_wait(10)  # Wait for the content to load

    # Extract the title
    title = driver.title.strip()

    # Extract the abstract section
    try:
        abstract_section = driver.find_element(By.ID, "abstractSection")
        abstract = abstract_section.find_element(By.TAG_NAME, "p").text.strip()
    except Exception:
        abstract = "Abstract not found"

    # Extract the author keywords
    try:
        keyword_elements = driver.find_elements(By.CSS_SELECTOR, "#authorKeywords .badges")
        keywords = [keyword.text for keyword in keyword_elements]
    except Exception:
        keywords = []

    # Prepare data for saving
    data = {
        "title": title,
        "abstract": abstract,
        "author_keywords": keywords
    }

    # Save data to a JSON file
    with open("scopus_results.json", "w", encoding="utf-8") as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)
    print("Data saved to scopus_results.json")

    # Save the full HTML content to a file
    full_html = driver.page_source
    with open("scopus_full_html.html", "w", encoding="utf-8") as html_file:
        html_file.write(full_html)
    print("Full HTML content saved to scopus_full_html.html")

finally:
    # Close the WebDriver
    driver.quit()