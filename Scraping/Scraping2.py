from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import json

# Set up Selenium WebDriver
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in headless mode
chrome_options.add_argument("--disable-gpu")
chrome_service = Service('/Users/wit/Downloads/chromedriver_mac_arm64/chromedriver')  # Replace with your ChromeDriver path

driver = webdriver.Chrome(service=chrome_service, options=chrome_options)

# URL of the Scopus record
url = "https://www.scopus.com/record/display.uri?eid=2-s2.0-85179929360&origin=inward"

try:
    # Open the webpage
    driver.get(url)
    
    # Wait for the content to load (adjust time as necessary)
    driver.implicitly_wait(10)
    
    # Extract the title
    title = driver.title.strip()

    # Extract the abstract section
    try:
        abstract_section = driver.find_element(By.ID, "abstractSection")
        abstract = abstract_section.find_element(By.TAG_NAME, "p").text.strip()
    except Exception:
        abstract = "Abstract not found"

    # Extract the author keywords (adjust the selector if necessary)
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
