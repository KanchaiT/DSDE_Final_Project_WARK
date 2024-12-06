import requests
import json
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
query = "PUBYEAR = 2017"
all_results = []

# ดึงข้อมูลแบบแบ่งหน้า
for start in range(0, 1500, 25):
    params = {
        "query": query,
        "start": start,
        "count": 25
    }
    response = requests.get(BASE_URL, headers=HEADERS, params=params)
    if response.status_code == 200:
      data = response.json()
      all_results.extend(data["search-results"]["entry"])
    
      # เขียนข้อมูลลงไฟล์ JSON
      with open(f"results_{start}.json", "w", encoding="utf-8") as file:
        json.dump(data["search-results"]["entry"], file, ensure_ascii=False, indent=4)
    
      print(f"Scraped {start}: Retrieved {len(data['search-results']['entry'])} records. Saved to results_{start}.json")
    else:
      print(f"Error: {response.status_code} - {response.text}")
      break


# แปลงข้อมูลเป็น DataFrame และบันทึก
# papers = []
# for paper in all_results:
#     papers.append({
#         "Title": paper.get("dc:title", "N/A"),  # ชื่อของบทความ (Title)
#         "Abstract": paper.get("dc:description", "N/A"),  # บทคัดย่อ (Abstract)
#         "Keywords": paper.get("authkeywords", "N/A"),  # คำสำคัญ (Keywords)
#         "Subject Area": paper.get("subject-areas", {}).get("subject-area", "N/A")  # หัวข้อวิจัย
#     })

# df = pd.DataFrame(papers)
# df.to_csv("scopus_papers.csv", index=False)
# print("บันทึกข้อมูลสำเร็จในไฟล์ scopus_papers.csv")
