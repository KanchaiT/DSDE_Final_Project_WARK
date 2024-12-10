import os
import pandas as pd

# Fountion to concat csv colum 
def join_csv_colum(first_file,second_file,output_file):
    
    # Load the first CSV file
    df1 = pd.read_csv(first_file)

    # Load the second CSV file
    df2 = pd.read_csv(second_file)

    # Remove the ".html" extension from the 'file' column in df1
    df1['file'] = df1['file'].str.replace('.html', '', regex=False)

    # Convert the 'file' column in df1 to integer to match 'filename_i' in df2
    df1['file'] = df1['file'].astype(int)

    # Rename the 'filename_i' column in df2 to 'file' for merging
    df2 = df2.rename(columns={'filename_i': 'file'})

    # Merge the two dataframes based on the 'file' column
    merged_df = pd.merge(df1, df2, on='file', how='left')
    
    # Select the desired columns and reorder them
    final_df = merged_df.drop('file',axis=1)
    
    # Save the merged dataframe to a new CSV file
    final_df.to_csv(output_file, index=False)
    print(f"Dataframes merged and saved to {output_file}")
    
def add_missing_columns(input_file, output_file):
    """
    Adds missing columns to a CSV file and fills them with "-" if they don't exist.

    Args:
        input_file: Path to the input CSV file.
        output_file: Path to save the modified CSV file.
    """

    try:
        df = pd.read_csv(input_file)
    except FileNotFoundError:
        print(f"Error: Input file '{input_file}' not found.")
        return

    # Desired columns
    desired_columns = [
        "citation_title",
        "abstracts",
        "authors",
        "authors_with_location_department",
        "affiliations",
        "classifications",
        "subject_area_name",
        "subject_area_code",
        "date",
        "citedby_count",
        "category"
    ]

    # Add missing columns and fill with "-"
    for col in desired_columns:
        if col not in df.columns:
            df[col] = "-"

    # Reorder columns to match the desired order
    df = df[desired_columns]

    # Save the modified DataFrame to a new CSV file
    df.to_csv(output_file, index=False)

    print(f"DataFrame updated and saved to '{output_file}'")
    
# Function to join multiple CSV files into one
def join_csv_files(input_folder, output_file):
    csv_files = [os.path.join(input_folder, f) for f in os.listdir(input_folder) if f.endswith('.csv')]
    dataframes = []

    for file in csv_files:
        try:
            df = pd.read_csv(file)
            dataframes.append(df)
        except Exception as e:
            print(f"Error reading {file}: {e}")

    # Concatenate all dataframes
    if dataframes:
        combined_df = pd.concat(dataframes, ignore_index=True)
        combined_df.to_csv(output_file, index=False, encoding='utf-8')
        print(f"Combined CSV saved to {output_file}")
    else:
        print("No valid CSV files found to join.")

# Example usage
input_folder = "DataFinal"  # Replace with the folder containing your CSV files
output_file = "DataFinal/Final_2017-2023.csv"  # Replace with the desired output file name
join_csv_colum("form_scrap/extracted_html.csv","form_scrap/citedby_counts_summary.csv","DataFinal/final_dataScraping.csv")
add_missing_columns("DataFinal/final_dataScraping.csv", "DataFinal/final_dataScraping.csv")
# join_csv_files(input_folder, output_file)
