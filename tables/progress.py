import pandas as pd 
import random 
from datetime import datetime, timedelta

users = pd.read_csv('data/users.csv')
lessons = pd.read_csv('data/lessons.csv')
topics = pd.read_csv('data/topics.csv')

progress_data = []

for user_id in users['u_id']:
    for i in range(len(lessons)):
        score = round(random.uniform(0, 10000))
        if score < 1000:
            score = 0
        elif score > 9000:
            score = 10000
        
        if score == 0:
            status = 'Not Started'
        elif score < 10000:
            status = 'In Progress'
        else:
            status = 'Completed'
        
        last_updated = datetime.now() - timedelta(days=random.randint(0, 365))
        
        progress_data.append({
            'u_id': user_id,
            'topic_id': lessons['topic_id'][i],
            'lesson_id': lessons['lesson_id'][i],
            'score': score,
            'status': status,
            'last_updated': last_updated.strftime('%Y-%m-%d %H:%M:%S')
        })

# Create the progress DataFrame
progress_df = pd.DataFrame(progress_data)   

# Save to CSV
progress_df.to_csv('data/progress.csv', index=False)

print("Progress data generated and saved to data/progress.csv")
