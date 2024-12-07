import os
import json
import pandas as pd

# Function to extract relevant data from a JSON file
def extract_data_from_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Extract citation title and abstracts
    citation_title = data.get("abstracts-retrieval-response", {}).get("item", {}).get("bibrecord", {}).get("head", {}).get("citation-title", "")
    abstracts = data.get("abstracts-retrieval-response", {}).get("item", {}).get("bibrecord", {}).get("head", {}).get("abstracts", "")
    # Extract authors
    author_group = data.get("abstracts-retrieval-response", {}).get("authors", {}).get("author",[])
    authors = []
    for a in author_group:
        authors_name = a.get("ce:given-name","")
        authors_surname = a.get("ce:surname","")
        authors.append(f"{authors_surname} {authors_name}".strip())

    # Extract authors with location and department
    authors_with_location_department = []
    authorData_group = data.get("abstracts-retrieval-response", {}).get("item", {}).get("bibrecord", {}).get("head", {}).get("author-group", {})

    if isinstance(authorData_group, list):
        for a in authorData_group:
            authorsData_affi =  a.get("affiliation",{})
            authorsData_city = authorsData_affi.get("city","")
            authorsData_country = authorsData_affi.get("country","")
            authorsData_location = f"author_location:{authorsData_city},{authorsData_country}" 
            
            if isinstance(authorsData_affi.get("organization",{}),list):
                authorsData_department_list = [ i.get("$", "").strip() for i in authorsData_affi.get("organization",{})]
            elif isinstance(authorsData_affi.get("organization",{}),dict):
                authorsData_department_list = [ authorsData_affi.get("organization",{}).get("$", "").strip()]
            authorsData_department = f"author_department:{", ".join(authorsData_department_list)}"
        
            authorsData_fullname_list = []
            if isinstance(a.get("author",{}),list):
                for i in a.get("author",{}):
                    authorsData_name = i.get("ce:given-name","")
                    authorsData_surname = i.get("ce:surname","")
                    authorsData_fullname = f"author_name:{authorsData_surname} {authorsData_name}"
                    authorsData_fullname_list.append(authorsData_fullname)
            elif isinstance(a.get("author",{}),dict):
                authorsData_name = a.get("author",{}).get("ce:given-name","")
                authorsData_surname = a.get("author",{}).get("ce:surname","")
                authorsData_fullname = f"author_name:{authorsData_surname} {authorsData_name}"
                authorsData_fullname_list.append(authorsData_fullname)
            authorsData_fullname_all = f"authors_name:{", ".join(authorsData_fullname_list)}"
            authors_with_location_department.append("/".join([authorsData_location,authorsData_department,authorsData_fullname_all]))
    
    elif isinstance(authorData_group, dict):
        authorsData_affi =  a.get("affiliation",{})
        authorsData_city = authorsData_affi.get("city","")
        authorsData_country = authorsData_affi.get("country","")
        authorsData_location = f"author_location:{authorsData_city},{authorsData_country}" 
        
        if isinstance(authorsData_affi.get("organization",{}),list):
            authorsData_department_list = [ i.get("$", "").strip() for i in authorsData_affi.get("organization",{})]
        elif isinstance(authorsData_affi.get("organization",{}),dict):
            authorsData_department_list = [ authorsData_affi.get("organization",{}).get("$", "").strip()]
        authorsData_department = f"author_department:{", ".join(authorsData_department_list)}"
    
        authorsData_fullname_list = []
        if isinstance(a.get("author",{}),list):
            for i in a.get("author",{}):
                authorsData_name = i.get("ce:given-name","")
                authorsData_surname = i.get("ce:surname","")
                authorsData_fullname = f"author_name:{authorsData_surname} {authorsData_name}"
                authorsData_fullname_list.append(authorsData_fullname)
        elif isinstance(a.get("author",{}),dict):
            authorsData_name = a.get("author",{}).get("ce:given-name","")
            authorsData_surname = a.get("author",{}).get("ce:surname","")
            authorsData_fullname = f"author_name:{authorsData_surname} {authorsData_name}"
            authorsData_fullname_list.append(authorsData_fullname)
                
        authorsData_fullname_all = f"authors_name:{", ".join(authorsData_fullname_list)}"
        authors_with_location_department.append("/".join([authorsData_location,authorsData_department,authorsData_fullname_all]))

    
    # Extract classifications
    classifications = []
    classification_groups = data.get("abstracts-retrieval-response", {}).get("item", {}).get("bibrecord", {}).get("head", {}).get("enhancement", {}).get("classificationgroup",{}).get("classifications",[])
    for group in classification_groups:
        class_type = group.get("@type", "")
        class_set_items = group.get("classification", [])
        class_value = []

        # Handle different structures of 'classification'
        if isinstance(class_set_items, list):
            # If classification is a list, extract "$" or "classification-code" values
            for item in class_set_items:
                if isinstance(item, dict):
                    value = item.get("$", item.get("classification-code", ""))
                    if value:
                        class_value.append(value)
        elif isinstance(class_set_items, dict):
            # If classification is a dict, extract "classification-code"
            value = class_set_items.get("$", class_set_items.get("classification-code", ""))
            if value:
                class_value.append(value)
        elif isinstance(class_set_items, str):
            # If classification is a string, directly append it
            class_value.append(class_set_items)
            
        if class_type and class_value:
            classifications.append({class_type: class_value})
    
    # Extract subject-area names and codes
    subject_areas = data.get("abstracts-retrieval-response", {}).get("subject-areas", {}).get("subject-area", [])
    subject_area_names = [area.get("$", "").strip() for area in subject_areas if "$" in area]
    subject_area_codes = [area.get("@code", "").strip() for area in subject_areas if "@code" in area]

    # Modify the return statement in extract_data_from_json function
    return {
        "citation_title": citation_title if citation_title else "-",
        "abstracts": abstracts if abstracts else "-",
        "authors": "; ".join(authors) if authors else "-",  # Join authors with "; "
        "authors_with_location_department" : "; ".join(authors_with_location_department) if authors_with_location_department else "-",
        "classifications": "; ".join([f"{k}: {', '.join(v)}" for item in classifications for k, v in item.items()]) if classifications else "-",
        "subject_area_name": "; ".join(subject_area_names) if subject_area_names else "-",
        "subject_area_code": "; ".join(subject_area_codes) if subject_area_codes else "-"
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
input_folder = "Project_RawData/0_json_test"  # Replace with your folder containing JSON files
output_csv = "Data_Aj/2/output_data_test.csv"  # Replace with your desired output CSV file name
process_json_to_csv(input_folder, output_csv)