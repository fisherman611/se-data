import pandas as pd 
import random 

topics = pd.read_csv('final_data/topics.csv')
sentences = pd.read_csv('data/selected_sentences.csv')

lesson_types = ['Vocab', 'Fill_in_the_blank', 'Re_order_words', 'Re_order_chars', 'Listen_and_fill']
lesson_data = []
for i in range(len(topics)):
    selected_sentences = sentences[sentences['topic'] == topics['topic_name'][i]]['s_id'].to_list()
    for j in range(5):
        for s_id in selected_sentences[:10]:
            lesson_data.append({
                'topic_id': topics['topic_id'][i],
                'lesson_id': j + 1,
                's_id': s_id
            })

# Create a DataFrame from the lesson data
lesson_df = pd.DataFrame(lesson_data)

# Save the DataFrame to a CSV file
lesson_df.to_csv('final_data/lessons_sentences.csv', index=False)

print("Lesson table has been created successfully!")