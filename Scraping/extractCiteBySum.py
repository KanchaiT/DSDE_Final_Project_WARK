import os
import json
import csv
# Directory containing your JSON files
json_directory = "Scraping/formScopusAPI"
# Output CSV file
output_csv = "Scraping/ScrapCsv/citedby_counts_summary.csv"
# List to store extracted data
summary_data = []
# Counter for continuous item numbering
item_counter = 1
# Loop through all JSON files in the directory
for filename in os.listdir(json_directory):
    if filename.endswith(".json"):
        file_path = os.path.join(json_directory, filename)
        
        # Open and read the JSON file
        with open(file_path, "r", encoding="utf-8") as file:
            try:
                data = json.load(file)  # Assuming each JSON file contains a list of dicts
                for entry in data:
                    date = entry.get("prism:coverDate","-")
                    citedby_count = entry.get("citedby-count", "0")  # Extract "citedby-count"
                    
                    summary_data.append({
                        "filename_i": f"{item_counter}",
                        "date" : date,
                        "citedby_count": citedby_count
                    })
                    item_counter += 1  # Increment the counter for each entry
            except json.JSONDecodeError:
                print(f"Error decoding JSON in file: {filename}")
# Write extracted data to a CSV file
with open(output_csv, "w", newline="", encoding="utf-8") as csvfile:
    fieldnames = ["filename_i","date","citedby_count"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    
    # Write header and rows
    writer.writeheader()
    writer.writerows(summary_data)
print(f"Summarization complete. Data saved to {output_csv}")