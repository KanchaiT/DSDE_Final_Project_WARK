import os
import pandas as pd

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
output_file = "DataFinal/joined_2017-2023.csv"  # Replace with the desired output file name
join_csv_files(input_folder, output_file)
