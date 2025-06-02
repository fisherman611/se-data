import pandas as pd 
import random 

topics = pd.read_csv('data/topics.csv')
sentences = pd.read_csv('data/sentences.csv')

lesson_types = ['Vocab', 'Fill_in_the_blank', 'Re_order_words', 'Re_order_chars', 'Listen_and_fill']
lesson_data = []
sents = []

for i in range(len(topics)):
    selected_sentences = sentences[sentences['topic_name'] == topics['topic_name'][i]]['s_id'].to_list()
    # with open(f"selected_sentences_{i}.txt", "w") as f:
    #     for s_id in selected_sentences:
    #         f.write(f"{s_id}\n")
    # for j in range(5):
    #     for s_id in selected_sentences[:10]:
    #         lesson_data.append({
    #             'topic_id': topics['topic_id'][i],
    #             'lesson_id': j + 1,
    #             's_id': s_id
    #         })'
    for s_id in selected_sentences[:10]:
        sents.append({
            's_id': s_id,
            'viet': sentences[sentences['s_id'] == s_id]['viet'].values[0],
            'eng': sentences[sentences['s_id'] == s_id]['eng'].values[0],
            'topic': sentences[sentences['s_id'] == s_id]['topic_name'].values[0]
        })
        

# Create a DataFrame from the lesson data
# lesson_df = pd.DataFrame(lesson_data)
sentences_df = pd.DataFrame(sents)

# Save the DataFrame to a CSV file
# lesson_df.to_csv('data/lessons_sentences.csv', index=False)
sentences_df.to_csv('data/selected_sentences.csv', index=False)

print("Lesson table has been created successfully!")