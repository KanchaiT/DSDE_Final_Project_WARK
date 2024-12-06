import pandas as pd

# Load the CSV file
csv_file = "Project_RawData/2018_data.csv"
df = pd.read_csv(csv_file)

df.describe