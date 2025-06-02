import pandas as pd

# Load the CSV file
df = pd.read_csv('data/selected_words.csv')
df2 = pd.read_csv('data/selected_sentences.csv')
df3 = pd.read_csv('final_data/lessons_sentences.csv')

# Show basic info
print(df.info())
print(df.head())

# Get the list of unique s_id
s_id_list = df['s_id'].unique().tolist()
s_id_list2 = df2['s_id'].unique().tolist()
s_id_list3 = df3['s_id'].unique().tolist()
print("List of unique s_id:", sorted(s_id_list))
print("List of unique s_id in sentences:", sorted(s_id_list2))
print(sorted(s_id_list) == sorted(s_id_list3))