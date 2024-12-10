import os
import json

def extract_scopus_links_from_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # List to store all "href" values with "@ref" == "scopus"
    scopus_links = []

    # Loop through each object in the JSON
    for record in data:
        link = record.get("link",[])[2].get("@href","")
        scopus_links.append(link)

    return scopus_links

def process_all_json_files(input_folder, output_file):
    all_scopus_links = []

    # Loop through all JSON files in the directory
    for file_name in os.listdir(input_folder):
        if file_name.endswith('.json'):
            file_path = os.path.join(input_folder, file_name)
            try:
                scopus_links = extract_scopus_links_from_json(file_path)
                all_scopus_links.extend(scopus_links)
            except Exception as e:
                print(f"Error processing file {file_name}: {e}")

    # Write all links to an output text file
    with open(output_file, 'w', encoding='utf-8') as f:
        for link in all_scopus_links:
            f.write(link + '\n')

    print(f"All Scopus links have been saved to {output_file}")

# Example usage
input_folder = "Scraping/formScopusAPI"  # Replace with the folder containing your JSON files
output_file = "Scraping/ScopusLinkForScraping/scopus_links.txt"  # Replace with your desired output file name
process_all_json_files(input_folder, output_file)
