import os
import json
import pandas as pd

# Function to extract relevant data from a JSON file
def extract_data_from_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)  

    # Extract citation title and abstracts
    citation_title = data.get("abstracts-retrieval-response", {}).get("item", {}).get("bibrecord", {}).get("head", {}).get("citation-title","-")
    abstracts = data.get("abstracts-retrieval-response", {}).get("item", {}).get("bibrecord", {}).get("head", {}).get("abstracts","-")

    # Extract authors
    author_group = data.get("abstracts-retrieval-response", {}).get("authors", {}).get("author", [])
    authors = []
    for a in author_group:
        authors_name = a.get("preferred-name", {}).get("ce:given-name","-")
        authors_surname = a.get("preferred-name", {}).get("ce:surname","-")
        authors.append(f"{authors_surname} {authors_name}".strip())

    # Extract authors with location and department
    authors_with_location_department = []
    authorData_group = data.get("abstracts-retrieval-response", {}).get("item", {}).get("bibrecord", {}).get("head", {}).get("author-group", {})

    if isinstance(authorData_group, list):
        for a in authorData_group:
            authorsData_affi =  a.get("affiliation",{})
            authorsData_country = authorsData_affi.get("country","-")
            authorsData_city = authorsData_affi.get("city","-")
            authorsData_location = f"author_location:{authorsData_city}\\{authorsData_country}" 
            
            if isinstance(authorsData_affi.get("organization",{}),list):
                authorsData_department_list = []  
                for i in authorsData_affi.get("organization",[]):
                    authorsData_department_list.append(i.get("$","-").strip())
            if isinstance(authorsData_affi.get("organization",{}),dict):
                authorsData_department_list = [authorsData_affi.get("organization",{}).get("$","-").strip()]
            authorsData_department = f"author_department:{'\\'.join(authorsData_department_list)}"
        
            authorsData_fullname_list = []
            if isinstance(a.get("author",{}),list):
                for i in a.get("author",{}):
                    authorsData_name = i.get("preferred-name",{}).get("ce:given-name","-")
                    authorsData_surname = i.get("preferred-name",{}).get("ce:surname","-")
                    authorsData_fullname = f"{authorsData_surname} {authorsData_name}"
                    authorsData_fullname_list.append(authorsData_fullname)
            elif isinstance(a.get("author",{}),dict):
                authorsData_name = a.get("author",{}).get("preferred-name",{}).get("ce:given-name","-")
                authorsData_surname = a.get("author",{}).get("preferred-name",{}).get("ce:surname","-")
                authorsData_fullname = f"{authorsData_surname} {authorsData_name}"
                authorsData_fullname_list.append(authorsData_fullname)
            authorsData_fullname_all = f"authors_name:{", ".join(authorsData_fullname_list)}"
            authors_with_location_department.append('||'.join([authorsData_location,authorsData_department,authorsData_fullname_all]))
    
    elif isinstance(authorData_group, dict):
        a = authorData_group
        authorsData_affi =  a.get("affiliation",{})
        authorsData_city = authorsData_affi.get("city","-")
        authorsData_country = authorsData_affi.get("country","-")
        authorsData_location = f"author_location:{authorsData_city}\\{authorsData_country}" 
        
        if isinstance(authorsData_affi.get("organization",{}),list):
            authorsData_department_list = [ i.get("$","-").strip() for i in authorsData_affi.get("organization",{})]
        elif isinstance(authorsData_affi.get("organization",{}),dict):
            authorsData_department_list = [ authorsData_affi.get("organization",{}).get("$","-").strip()]
        authorsData_department = f"author_department:{'\\'.join(authorsData_department_list)}"
    
        authorsData_fullname_list = []
        if isinstance(a.get("author",{}),list):
            for i in a.get("author",{}):
                authorsData_name = i.get("preferred-name",{}).get("ce:given-name","-")
                authorsData_surname = i.get("preferred-name",{}).get("ce:surname","-")
                authorsData_fullname = f"{authorsData_surname} {authorsData_name}"
                authorsData_fullname_list.append(authorsData_fullname)
        elif isinstance(a.get("author",{}),dict):
            authorsData_name = a.get("author",{}).get("preferred-name",{}).get("ce:given-name","-")
            authorsData_surname = a.get("author",{}).get("preferred-name",{}).get("ce:surname","-")
            authorsData_fullname = f"{authorsData_surname} {authorsData_name}"
            authorsData_fullname_list.append(authorsData_fullname)

        authorsData_fullname_all = f"authors_name:{", ".join(authorsData_fullname_list)}"
        authors_with_location_department.append('||'.join([authorsData_location,authorsData_department,authorsData_fullname_all]))

    # Extract affiliations
    affiliations = []
    affiliation_list = data.get("abstracts-retrieval-response", {}).get("affiliation",{})
    if isinstance(affiliation_list,list):
        for af in affiliation_list:
            affiliation_name = af.get("affilname","-")
            affiliation_city = af.get("affilname-city","-")
            affiliation_country = af.get("affiliation-country","-")
            affiliations.append(f"{affiliation_name}\\{affiliation_city}\\{affiliation_country}")

    elif isinstance(affiliation_list,dict):
        affiliation_name = affiliation_list.get("affilname","-")
        affiliation_city = affiliation_list.get("affilname-city","-")
        affiliation_country = affiliation_list.get("affiliation-country","-")
        affiliations.append(f"{affiliation_name}\\{affiliation_city}\\{affiliation_country}")   

    # Extract classifications
    classifications = []
    classification_groups = data.get("abstracts-retrieval-response", {}).get("item", {}).get("bibrecord", {}).get("head", {}).get("enhancement", {}).get("classificationgroup", {}).get("classifications", [])
    for group in classification_groups:
        class_type = group.get("@type","-")
        class_set_items = group.get("classification", [])
        class_value = []

        if isinstance(class_set_items, list):
            for item in class_set_items:
                if isinstance(item, dict):
                    value = item.get("$", item.get("classification-code","-"))
                    if value:
                        class_value.append(value)
        elif isinstance(class_set_items, dict):
            value = class_set_items.get("$", class_set_items.get("classification-code","-"))
            if value:
                class_value.append(value)
        elif isinstance(class_set_items, str):
            class_value.append(class_set_items)

        if class_type and class_value:
            classifications.append({class_type: class_value})

    # Extract subject-area names and codes
    subject_areas = data.get("abstracts-retrieval-response", {}).get("subject-areas", {}).get("subject-area", [])
    subject_area_names = [area.get("$","-").strip() for area in subject_areas if "$" in area]
    subject_area_codes = [area.get("@code","-").strip() for area in subject_areas if "@code" in area]
    
    date = data.get("abstracts-retrieval-response", {}).get("coredata", {}).get("prism:coverDate","-")


    citedby_count = data.get("abstracts-retrieval-response", {}).get("coredata", {}).get("citedby-count","0")

    return {
        "citation_title": citation_title if citation_title else "-",
        "abstracts": abstracts if abstracts else "-",
        "authors": "; ".join(authors) if authors else "-",
        "authors_with_location_department": "; ".join(authors_with_location_department) if authors_with_location_department else "-",
        "affiliations" : "; ".join(affiliations),
        "classifications": "; ".join([f"{k}: {'\\'.join(v)}" for item in classifications for k, v in item.items()]) if classifications else "-",
        "subject_area_name": "; ".join(subject_area_names) if subject_area_names else "-",
        "subject_area_code": "; ".join(subject_area_codes) if subject_area_codes else "-",
        "date" : date if date else "-",
        "citedby_count": citedby_count if citedby_count else "0"
    }

# Function to process all JSON files in a directory and save as a CSV
def process_json_to_csv(input_folder, output_csv):
    rows = []

    for root, _, files in os.walk(input_folder):
        for file_name in files:
            if file_name.endswith(".json"):
                file_path = os.path.join(root, file_name)
    
            try:
                row = extract_data_from_json(file_path)
                rows.append(row)
            except Exception as e:
                print(f"Error processing file {file_path}: {e}")

    # Create a DataFrame and save to CSV
    df = pd.DataFrame(rows)
    df.to_csv(output_csv, index=False, encoding='utf-8')
    print(f"Data successfully saved to {output_csv}")

# Example usage
input_folder = "Project_RawData"  # Replace with your folder containing JSON files
output_csv = "Data_Aj/2/joined_2018-2023.csv"  # Replace with your desired output CSV file name
process_json_to_csv(input_folder, output_csv)
