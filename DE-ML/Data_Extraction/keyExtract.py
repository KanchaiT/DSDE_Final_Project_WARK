import json

# Load the JSON file
file_path = "Project_RawData/2018/201800000.json"
with open(file_path, "r", encoding="utf-8") as f:
    data = json.load(f)

# Function to recursively extract keys from the JSON

def extract_keys(data, parent_key=""):
    keys = []
    if isinstance(data, dict):
        for key, value in data.items():
            full_key = f"{parent_key}.{key}" if parent_key else key
            keys.append(full_key)
            keys.extend(extract_keys(value, full_key))
    elif isinstance(data, list):
        for idx, item in enumerate(data):
            full_key = f"{parent_key}[{idx}]" if parent_key else str(idx)
            keys.extend(extract_keys(item, full_key))
    return keys

# Extract all keys from the JSON
dictionary_keys = extract_keys(data)

# Print the extracted keys
for key in dictionary_keys:
    print(key)

# Save keys to a file (optional)
output_file = "json_keys.txt"
with open(output_file, "w", encoding="utf-8") as f:
    for key in dictionary_keys:
        f.write(f"{key}\n")

print(f"Extracted keys saved to {output_file}")
