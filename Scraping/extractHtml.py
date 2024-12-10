import os
import csv
from bs4 import BeautifulSoup

# Directory containing your HTML files
html_directory = "Scraping/OUTPUT_html/real"

# Output CSV file
output_csv = "Scraping/ScrapCsv/extracted_html.csv"

# Error log file
error_log = "Scraping/error_log.txt"

# List to store extracted values
extracted_data = []

# Clear previous error log
with open(error_log, "w") as log_file:
    log_file.write("Error Log:\n")

# Loop through all HTML files in the directory
for filename in os.listdir(html_directory):
    print(f"Processing file: {filename}")
    if filename.endswith(".html"):
        file_path = os.path.join(html_directory, filename)

        try:
            # Open and parse the HTML file
            with open(file_path, "r", encoding="utf-8") as file:
                soup = BeautifulSoup(file, "html.parser")

            # Find all <micro-ui> tags
            micro_ui_tags = soup.find_all("micro-ui")
            
            if len(micro_ui_tags) >= 2:
                micro_ui = micro_ui_tags[1]

                # Locate the citation_title text
                citation_title = "-"
                try:
                    citation_title_tag = micro_ui.find("h2", {"data-testid": "publication-titles"})
                    if citation_title_tag :
                        # แปลง <sub> เป็นข้อความรวมกับข้อความก่อนหน้า
                        for sub in citation_title_tag.find_all("sub"):
                            sub.replace_with(sub.text.strip())  # แทนที่ <sub> ด้วยข้อความภายใน
                        citation_title = citation_title_tag.get_text(separator="",strip=True)
                    else :"-"
                except Exception as e:
                    with open(error_log, "a") as log_file:
                        log_file.write(f"Error extracting citation_title in file {filename}: {e}\n")

                # Locate the abstracts text
                abstract_text = "-"
                try:
                    abstract_heading = micro_ui.find("h3", id="abstract")
                    if abstract_heading:
                        abstract_div = abstract_heading.find_next("div", class_="Abstract-module__pTWiT")
                        if abstract_div :
                            # แปลง <sub> เป็นข้อความรวมกับข้อความก่อนหน้า
                            for sub in abstract_div.find_all("sub"):
                                sub.replace_with(sub.text.strip())  # แทนที่ <sub> ด้วยข้อความภายใน
                            abstract_text = abstract_div.get_text(separator="",strip=True)
                        else :"-"
                except Exception as e:
                    with open(error_log, "a") as log_file:
                        log_file.write(f"Error extracting abstract in file {filename}: {e}\n")

                # Locate the author list
                authors = "-"
                try:
                    author_list_div = micro_ui.find("div", {"data-testid": "author-list"})
                    author_names = []
                    if author_list_div:
                        ul = author_list_div.find("ul")
                        if ul:
                            for button in ul.find_all("button"):
                                span = button.find("span")
                                if span:
                                    author_text = span.text.strip()
                                    if "," in author_text:
                                        surname, name = author_text.split(",", 1)
                                        formatted_name = f"{surname.strip()} {name.strip()}"
                                        author_names.append(formatted_name)
                    authors = "; ".join(author_names) if author_names else "-"
                except Exception as e:
                    with open(error_log, "a") as log_file:
                        log_file.write(f"Error extracting authors in file {filename}: {e}\n")

                # Locate affiliations
                affiliations = "-"
                try:
                    affiliation_section = micro_ui.find("div", {"id": "affiliation-section"})
                    affiliation_list = []
                    if affiliation_section:
                        ul = affiliation_section.find("ul", class_="DocumentHeader-module__p4B_K")
                        if ul:
                            for li in ul.find_all("li"):
                                span = li.find("span")
                                if span:
                                    affiliation_text = span.text.strip()
                                    parts = affiliation_text.split(",")
                                    if len(parts) >= 3:
                                        name = parts[0].strip()
                                        city = parts[1].strip()
                                        country = parts[-1].strip()
                                        formatted_affiliation = f"{name}\\{city}\\{country}"
                                        affiliation_list.append(formatted_affiliation)
                    affiliations = "; ".join(affiliation_list) if affiliation_list else "-"
                except Exception as e:
                    with open(error_log, "a") as log_file:
                        log_file.write(f"Error extracting affiliations in file {filename}: {e}\n")

                # Locate subject area names
                subject_area_name = "-"
                try:
                    author_keywords_heading = micro_ui.find("h3", id="author-keywords")
                    subject_area_names = []
                    if author_keywords_heading:
                        keywords_div = author_keywords_heading.find_next("div")
                        if keywords_div:
                            for keyword_span in keywords_div.find_all("span", class_="Highlight-module__MMPyY"):
                                if keyword_span :
                                    # แปลง <sub> เป็นข้อความรวมกับข้อความก่อนหน้า
                                    for sub in keyword_span.find_all("sub"):
                                        sub.replace_with(sub.text.strip())  # แทนที่ <sub> ด้วยข้อความภายใน
                                    subject_area_names.append(keyword_span.get_text(separator="",strip=True))
                                else :"-"
                    subject_area_name = "; ".join(subject_area_names) if subject_area_names else "-"
                except Exception as e:
                    with open(error_log, "a") as log_file:
                        log_file.write(f"Error extracting subject_area_name in file {filename}: {e}\n")

                # Append the extracted data
                extracted_data.append({
                    "file": filename,
                    "citation_title": citation_title,
                    "abstracts": abstract_text,
                    "authors": authors,
                    "affiliations": affiliations,
                    "classifications": "-",
                    "subject_area_name": subject_area_name
                })
        except Exception as e:
            with open(error_log, "a") as log_file:
                log_file.write(f"Error processing file {filename}: {e}\n")
            continue

# Write extracted data to a CSV file
with open(output_csv, "w", newline="", encoding="utf-8") as csvfile:
    fieldnames = ["file", "citation_title", "abstracts", "authors", "affiliations", "classifications", "subject_area_name"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(extracted_data)

print(f"Extraction complete. Data saved to {output_csv}.")
