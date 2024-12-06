import requests
import pandas as pd
from dotenv import load_dotenv
import os

# ตั้งค่า API Key
load_dotenv()
API_KEY = os.getenv("SCOPUS_API_KEY")

HEADERS = {
    "X-ELS-APIKey": API_KEY,
    "Accept": "application/json"
}
BASE_URL = "https://api.elsevier.com/content/search/scopus"

#  Query
query = "TITLE-ABS-KEY(hydration AND health)"
all_results = []

# ดึงข้อมูลแบบแบ่งหน้า
for start in range(0, 1000, 25):
    params = {
        "query": query,
        "start": start,
        "count": 25
    }
    response = requests.get(BASE_URL, headers=HEADERS, params=params)
    if response.status_code == 200:
        data = response.json()
        all_results.extend(data["search-results"]["entry"])
        print(f"Scraped {start}: Retrieved {len(data['search-results']['entry'])} records. Total so far: {len(all_results)}")
    else:
        print(f"Error: {response.status_code} - {response.text}")
        break

# แปลงข้อมูลเป็น DataFrame และบันทึก
papers = []
for paper in all_results:
    papers.append({
        "Title": paper.get("dc:title", "N/A"),
        "DOI": paper.get("prism:doi", "N/A"),
        "Authors": paper.get("dc:creator", "N/A"),
        "Publication Year": paper.get("prism:coverDate", "N/A").split("-")[0]
    })

df = pd.DataFrame(papers)
df.to_csv("scopus_papers.csv", index=False)
print("บันทึกข้อมูลสำเร็จในไฟล์ scopus_papers.csv")
