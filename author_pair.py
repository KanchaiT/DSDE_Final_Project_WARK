import pandas as pd

uploaded_file = 'D:/CEDT/2_1_CEDT/Introduction_to_Data_Science_and_Data_Engineering/DSDE_Project/Data_Aj/2/joined_2018-2023.csv'
data = pd.read_csv(uploaded_file)

data['authors'] = data['authors'].fillna('')  # Handle missing values
author_pairs = []
count = 0

for authors in data['authors']:
    author_list = [author.strip() for author in authors.split(';') if author.strip()]
    count = count+1
    k = len(author_list) if len(author_list) < 10 else 10
    for i in range(k):
        for j in range(i + 1, k):
            print(f'author{count} : ({i},{j})')
            author_pairs.append((author_list[i], author_list[j]))
author_pairs_df = pd.DataFrame(author_pairs, columns=["Author 1", "Author 2"])
output_path = "author_pairs.csv"
author_pairs_df.to_csv(output_path, index=False)