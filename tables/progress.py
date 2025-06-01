import pandas as pd 
import random 
from datetime import datetime, timedelta

users = pd.read_csv('data/users.csv')
lessons = pd.read_csv('data/lessons.csv')
topics = pd.read_csv('data/topics.csv')
lessons = lessons.drop_duplicates(subset=['topic_id', 'lesson_id'])
lessons = lessons[['topic_id', 'lesson_id']]
lessons = lessons.reset_index(drop=True)

progress_data = []
in_progress_scores = [1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000]

for user_id in users['u_id']:
    for i in range(len(lessons)):
        # Generate random score trigger
        score_trigger = random.uniform(0, 10000)
        
        # Assign score and status based on trigger
        if score_trigger < 1000:
            score = 0
            status = 'Not Started'
        elif score_trigger > 9000:
            score = 10000
            status = 'Completed'
        else:
            score = random.choice(in_progress_scores)
            status = 'In Progress'
        
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