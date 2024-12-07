from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import json

# ตั้งค่า Chrome Driver
chrome_options = Options()
chrome_options.add_argument("--headless")  # รันแบบไม่มี GUI
chrome_options.add_argument("--disable-gpu")
service = Service('/Users/wit/Downloads/chrome-mac-arm64')  # ใส่ path ของ chromedriver

driver = webdriver.Chrome(service=service, options=chrome_options)

# เปิดหน้าเว็บ
driver.get("https://www.scopus.com/inward/record.uri?partnerID=HzOxMe3b&scp=85207964401&origin=inward")

try:
    # ดึง title
    title = driver.title

    # ดึง abstract
    abstract_element = driver.find_element(By.ID, "abstractSection")
    abstract = abstract_element.text if abstract_element else "Abstract not found"

    # บันทึกข้อมูล
    data = {"title": title, "abstract": abstract}
    with open("scopus_results.json", "w", encoding="utf-8") as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)

    print("Data saved successfully.")

finally:
    driver.quit()
