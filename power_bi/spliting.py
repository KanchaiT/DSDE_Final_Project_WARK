from itertools import combinations
import pandas as pd

# อ่านข้อมูล (สมมติว่าข้อมูลของคุณอยู่ในไฟล์ CSV)
try:
    df = pd.read_csv('joined_2018-2023.csv')
except FileNotFoundError:
    print("Error: File not found. Please check the file path.")
    exit()
except pd.errors.EmptyDataError:
    print("Error: The CSV file is empty.")
    exit()
except Exception as e:
    print(f"An unexpected error occurred while reading the CSV file: {e}")
    exit()

# ตรวจสอบคอลัมน์ที่จำเป็น
required_columns = ['citation_title', 'authors']
if not all(col in df.columns for col in required_columns):
    print(f"Error: Missing required columns. The CSV file must contain: {', '.join(required_columns)}")
    exit()

# ฟังก์ชัน generator ที่จำกัดจำนวน pairings
def generate_pairings(data, max_pairings=3000):
    pairings_count = 0
    for index, row in data.iterrows():
        try:
            authors_list = row['authors'].split('; ')
            if len(authors_list) > 1:
                for pair in combinations(authors_list, 2):
                    if pairings_count >= max_pairings:
                        return  # หยุดเมื่อครบ 4000
                    yield {'citation_title': row['citation_title'], 'author1': pair[0], 'author2': pair[1]}
                    pairings_count += 1
            elif len(authors_list) == 1:
                author = authors_list[0]
                if pairings_count >= max_pairings:
                    return  # หยุดเมื่อครบ 4000
                yield {'citation_title': row['citation_title'], 'author1': author, 'author2': author}
                pairings_count += 1
        except Exception as e:
            print(f"An error occurred while processing row {index}: {e}")
            continue

# ประมวลผลข้อมูลทีละคู่ โดยจำกัดจำนวน pairings ที่ 4000
limited_pairings = []
for pairing in generate_pairings(df, max_pairings=3000):
    limited_pairings.append(pairing)
    # print(pairing)  # ถ้าต้องการ print แต่ละ pairing ให้เอาคอมเมนต์ออก

print(f"Generated {len(limited_pairings)} pairings.")
print("Data processing complete.")

# ส่วนของการบันทึกหรือประมวลผล limited_pairings ต่อไป
# ... เช่น บันทึกลงไฟล์ CSV หรือนำไปวิเคราะห์ต่อ
try:
    df_limited_pairings = pd.DataFrame(limited_pairings)
    df_limited_pairings.to_csv('limited_pairings.csv', index=False)
    print("Limited pairings saved to 'limited_pairings.csv'")
except Exception as e:
    print(f"An error occurred while saving limited pairings to CSV: {e}")