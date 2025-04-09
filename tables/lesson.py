import pandas as pd 

topics = pd.read_csv('data/topics.csv')

lesson_data = []
for i in range(len(topics)):
    lesson_data.append({
        'lesson_id': topics['topic_id'][i],
        'topic_id': topics['topic_id'][i],
        'title': topics['topic_name'][i]
    })

# Create a DataFrame from the lesson data
lesson_df = pd.DataFrame(lesson_data)

# Save the DataFrame to a CSV file
lesson_df.to_csv('data/lessons.csv', index=False)

print("Lesson table has been created successfully!")