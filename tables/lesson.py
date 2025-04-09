import pandas as pd 

topics = pd.read_csv('data/topics.csv')

lesson_types = ['Vocab', 'Fill_in_the_blank', 'Re_order_words', 'Re_order_chars', 'Listen_and_fill']
lesson_data = []
for i in range(len(topics)):
    for j in range(5):
        lesson_data.append({
            'topic_id': topics['topic_id'][i],
            'lesson_id': j + 1,
            'lesson_type': lesson_types[j],
            'title': lesson_types[j].replace('_', ' ').title()
        })

# Create a DataFrame from the lesson data
lesson_df = pd.DataFrame(lesson_data)

# Save the DataFrame to a CSV file
lesson_df.to_csv('data/lessons.csv', index=False)

print("Lesson table has been created successfully!")