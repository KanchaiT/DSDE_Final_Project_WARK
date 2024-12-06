import os
import json
import pandas as pd

# Function to extract relevant data from a JSON file
def extract_data_from_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Extract fields based on the provided structure
    citation_title = data.get("abstracts-retrieval-response", {}).get("item", {}).get("bibrecord", {}).get("head", {}).get("citation-title", "")
    abstracts = data.get("abstracts-retrieval-response", {}).get("item", {}).get("bibrecord", {}).get("head", {}).get("abstracts", "")
    classifications = ", ".join([cls.get("classification", "") for cls in data.get("abstracts-retrieval-response", {}).get("item", {}).get("bibrecord", {}).get("head", {}).get("enhancement", {}).get("classificationgroup", {}).get("classifications", [])])
    subject_areas = ", ".join([area.get("$", "") for area in data.get("abstracts-retrieval-response", {}).get("item", {}).get("subject-areas", {}).get("subject-area", [])])
    authors = ", ".join([f"{author.get('preferred-name', {}).get('ce:given-name', '')} {author.get('preferred-name', {}).get('ce:surname', '')}" for author in data.get("abstracts-retrieval-response", {}).get("item", {}).get("bibrecord", {}).get("head", {}).get("author-group", [{}])[0].get("author", [])])

    return {
        "citation_title": citation_title,
        "abstracts": abstracts,
        "classifications": classifications,
        "subject_areas": subject_areas,
        "authors": authors
    }

# Function to process all JSON files in a directory and save as a CSV
def process_json_to_csv(input_folder, output_csv):
    rows = []

    for file_name in os.listdir(input_folder):
        if file_name.endswith(".json"):
            file_path = os.path.join(input_folder, file_name)
            try:
                row = extract_data_from_json(file_path)
                rows.append(row)
            except Exception as e:
                print(f"Error processing file {file_name}: {e}")

    # Create a DataFrame and save to CSV
    df = pd.DataFrame(rows)
    df.to_csv(output_csv, index=False, encoding='utf-8')
    print(f"Data successfully saved to {output_csv}")

# Example usage
input_folder = "Project_RawData/2018"  # Replace with your folder containing JSON files
output_csv = "output_data_2018.csv"  # Replace with your desired output CSV file name
process_json_to_csv(input_folder, output_csv)
