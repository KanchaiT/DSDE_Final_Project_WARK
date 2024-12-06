import requests
import pandas as pd

# ตั้งค่า API Key
API_KEY = "1cc942676f0e5ce55217e8df5e45e881"  # ใส่ API Key ที่ได้รับ
HEADERS = {
    "X-ELS-APIKey": API_KEY,
    "Accept": "application/json"
}
BASE_URL = "https://api.elsevier.com/content/search/scopus"

# ตัวอย่าง Query
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
