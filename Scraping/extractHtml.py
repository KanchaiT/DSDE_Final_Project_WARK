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
                # Locate the author_list
                author_list_div = micro_ui.find("div", {"data-testid": "author-list"})
                author_names = []

                if author_list_div:
                    # Find all <ul> elements within this div
                    ul = author_list_div.find("ul")
                    if ul:
                        # Iterate through all <li> or <button> elements
                        for button in ul.find_all("button"):
                            # Find the <span> inside each button
                            span = button.find("span")
                            if span:
                                # Extract the text and format it
                                author_text = span.text.strip()
                                if "," in author_text:
                                    surname, name = author_text.split(",", 1)
                                    formatted_name = f"{surname.strip()} {name.strip()}"
                                    author_names.append(formatted_name)
                # Format the author list
                authors = "; ".join([name for name in author_names]) if author_names else "-"
                
                # Location affiliations
                affiliation_section = micro_ui.find("div", {"id": "affiliation-section"})
                affiliations = []
                
                if affiliation_section:
                    # Locate the <ul> within this section
                    ul = affiliation_section.find("ul", class_="DocumentHeader-module__p4B_K")
                    if ul:
                        # Iterate through all <li> elements
                        for li in ul.find_all("li"):
                            # Extract the <span> inside the <li>
                            span = li.find("span")
                            if span:
                                # Parse the affiliation details
                                affiliation_text = span.text.strip()
                                # Split into parts by commas (name, city, postcode, country)
                                parts = affiliation_text.split(",")
                                if len(parts) >= 3:
                                    name = parts[0].strip()
                                    city = parts[1].strip()
                                    country = parts[-1].strip()
                                    formatted_affiliation = f"{name}\\{city}\\{country}"
                                    affiliations.append(formatted_affiliation)
                
                # Format the affiliations as requested
                affiliations_formatted = ";".join(affiliations) if affiliations else "-"

                # Location subject_area_name
                author_keywords_heading = micro_ui.find("h3", id="author-keywords")
                subject_area_names = []
                
                if author_keywords_heading:
                    # Find the <div> following this <h3>
                    keywords_div = author_keywords_heading.find_next("div")
                    if keywords_div:
                        # Iterate through all <span> elements with the desired class
                        for keyword_span in keywords_div.find_all("span", class_="Highlight-module__MMPyY"):
                            # Extract the text from each <span>
                            keyword_text = keyword_span.text.strip()
                            subject_area_names.append(keyword_text)
                
                # Format the keywords as a semicolon-separated string
                subject_area_name = "; ".join(subject_area_names) if subject_area_names else "-"
            
                
                
                # Append the extracted data
                extracted_data.append({
                    "file": filename,
                    "citation_title": citation_title,
                    "abstracts": abstract_text,
                    "authors": authors,
                    "affiliations": affiliations_formatted,
                    "classifications" : "-",
                    "subject_area_name": subject_area_name
                })

# Write extracted data to a CSV file
with open(output_csv, "w", newline="", encoding="utf-8") as csvfile:
    fieldnames = ["file", "citation_title", "abstracts", "authors", "affiliations","classifications", "subject_area_name"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    
    # Write header and rows
    writer.writeheader()
    writer.writerows(extracted_data)

print(f"Extraction complete. Data saved to {output_csv}")
