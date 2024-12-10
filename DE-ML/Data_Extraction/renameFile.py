import os

# Folder containing the files
folder_path = "Project_RawData/2018"

# Loop through all files in the folder
for file_name in os.listdir(folder_path):
    # Construct the full file path
    file_path = os.path.join(folder_path, file_name)
    
    # Check if it's a file and doesn't already have the .json extension
    if os.path.isfile(file_path) and not file_name.endswith('.json'):
        # Rename the file to add the .json extension
        new_file_name = file_name + ".json"
        new_file_path = os.path.join(folder_path, new_file_name)
        os.rename(file_path, new_file_path)
        print(f"Renamed: {file_name} -> {new_file_name}")

print("All files have been renamed with the .json extension.")
