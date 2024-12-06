import json
import os
import pandas as pd

# Folder containing JSON files
json_folder = "Project_RawData/2018"

# List to hold data
data_list = []

# Loop through all JSON files
for file in os.listdir(json_folder):
    if file.startswith('2018'):
        file_path = os.path.join(json_folder, file)
        with open(file_path, 'r', encoding='utf-8') as f:
            # Parse JSON and append to list
            data = json.load(f)
            data_list.append(data)

# Flatten the nested JSON data into a DataFrame
df = pd.json_normalize(data_list)

# Save the DataFrame to a CSV file
output_csv_path = "Project_RawData/2018_data.csv"
df.to_csv(output_csv_path, index=False)

# Confirm saved path
print(f"CSV file saved to: {output_csv_path}")
print(df.head())
