import os
import csv
from bs4 import BeautifulSoup

# Directory containing your HTML files
html_directory = "Scraping/OUTPUT_html/test"

# Output CSV file
output_csv = "Scraping/Data_Scrap/extracted_html.csv"

# List to store extracted values
extracted_data = []

# Loop through all HTML files in the directory
for filename in os.listdir(html_directory):
    if filename.endswith(".html"):
        file_path = os.path.join(html_directory, filename)
        
        # Open and parse the HTML file
        with open(file_path, "r", encoding="utf-8") as file:
            soup = BeautifulSoup(file, "html.parser")
            
            # Find all <micro-ui> tags
            micro_ui_tags = soup.find_all("micro-ui")
            
            # Extract details from the second <micro-ui> tag if it exists
            if len(micro_ui_tags) >= 2:
                micro_ui = micro_ui_tags[1]
                
                # Locate the citation_title text
                citation_title_tag = micro_ui.find("h2", {"data-testid": "publication-titles"})  # Find the <h2> by its data-testid attribute
                citation_title_span = citation_title_tag.find("span") if citation_title_tag else "-"  # Find the <span> inside the <h2>
                citation_title = citation_title_span.text.strip() if citation_title_span else "-"  # Extract the text
                
                # Locate the abstracts text
                abstract_heading = micro_ui.find("h3", id="abstract")
                if abstract_heading:
                    # Find the next <div> following this <h3>
                    abstract_div = abstract_heading.find_next("div", class_="Abstract-module__pTWiT")
                    if abstract_div:
                        # Find the <p> inside this <div>
                        abstract_paragraph = abstract_div.find("p")
                        if abstract_paragraph:
                            # Find the <span> inside the <p> and extract text
                            abstract_span = abstract_paragraph.find("span")
                            abstract_text = abstract_span.text.strip() if abstract_span else "-"
                
                authors = " " 
                # micro_ui.find("authors").text.strip() if micro_ui.find("authors") else None
                
                affiliations = " "
                # micro_ui.find("affiliations").text.strip() if micro_ui.find("affiliations") else None
                subject_area_name = " "
                # micro_ui.find("subject_area_name").text.strip() if micro_ui.find("subject_area_name") else None
                
                # Append the extracted data
                extracted_data.append({
                    "file": filename,
                    "citation_title": citation_title,
                    "abstracts": abstract_text,
                    "authors": authors,
                    "affiliations": affiliations,
                    "subject_area_name": subject_area_name
                })

# Write extracted data to a CSV file
with open(output_csv, "w", newline="", encoding="utf-8") as csvfile:
    fieldnames = ["file", "citation_title", "abstracts", "authors", "affiliations", "subject_area_name"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    
    # Write header and rows
    writer.writeheader()
    writer.writerows(extracted_data)

print(f"Extraction complete. Data saved to {output_csv}")
