import pandas as pd
from datasets import load_dataset
from transformers import AutoModelForSequenceClassification, AutoTokenizer
import numpy as np
from scipy.special import expit
from tqdm.auto import tqdm

# Load the sentences and convert splits to DataFrames
ds = load_dataset("HoangVuSnape/vi_en_translation_small")
train = ds["train"].to_pandas()
valid = ds["valid"].to_pandas()
test = ds["test"].to_pandas()

# Concatenate splits and reset index
sentences = pd.concat([train, valid, test])
sentences.reset_index(drop=True, inplace=True)
sentences.rename(columns={"English:": "eng", "Vietnamese": 'viet'}, inplace=True)

# Load the model and tokenizer
MODEL = "cardiffnlp/tweet-topic-21-multi"
tokenizer = AutoTokenizer.from_pretrained(MODEL)
model = AutoModelForSequenceClassification.from_pretrained(MODEL)
class_mapping = model.config.id2label

# Set a batch size for faster inference
BATCH_SIZE = 32
topics = []

# Process the 'English' column in batches with tqdm progress bar.
for i in tqdm(range(0, len(sentences), BATCH_SIZE), desc="Classifying topics"):
    batch_texts = sentences['English'].iloc[i:i + BATCH_SIZE].tolist()
    # Tokenize the batch with padding and truncation
    tokens = tokenizer(batch_texts, return_tensors='pt', padding=True, truncation=True)
    output = model(**tokens)
    # Get model logits and apply the sigmoid function for scores
    logits = output.logits.detach().numpy()
    scores = expit(logits)
    # Process predictions for each sentence in the batch
    for row_scores in scores:
        prediction_id = int(np.argmax(row_scores))
        prediction_score = float(np.max(row_scores))
        if prediction_score < 0.5:
            topics.append(None)
        else:
            topics.append(class_mapping[prediction_id].replace("_", " ").title())

# Add the predicted topics as a new column in the sentences
sentences['topic_name'] = topics

# Drop rows where topic is None
sentences = sentences.dropna(subset=['topic_name'])

# Insert a new column 's_id' at the beginning with sequential IDs
sentences.insert(0, "s_id", range(1, len(sentences) + 1))

# Save the resulting DataFrame to a CSV file without the default index
sentences.to_csv("data/sentences.csv", index=False)

# Save the topic to a CSV file 
topics = pd.DataFrame(class_mapping.items(), columns=['topic_id', 'topic_name'])
topics['topic_name'] = topics['topic_name'].apply(lambda x: x.replace("_", " ").title())

descriptions = [
    "Discover the language of creativity and expression through topics on literature, visual arts, music, and cultural traditions. Deepen your understanding while learning vocabulary that brings art and culture to life.",
    "Learn the key terms and phrases used in the professional world—from meetings and negotiations to startup lingo. Perfect for aspiring professionals and entrepreneurs eager to navigate international business communications.",
    "Dive into the vibrant world of entertainment, celebrity news, and current trends. Expand your vocabulary with topics that keep you updated on pop culture and the lifestyles of famous personalities.",
    "Practice everyday language through real-life narratives and personal stories. Topics include daily routines, personal reflections, and informal conversations that make learning practical and relatable.",
    "Explore vocabulary and expressions centered on family relationships, from bonding with relatives to describing family dynamics. Ideal for understanding both formal terms and everyday language at home.",
    "Learn the words and phrases that describe modern trends and timeless styles. This topic covers clothing, accessories, and expressions that help you discuss fashion confidently.",
    "Discover the language used in movies, television shows, and online videos. Improve your listening and conversational skills by engaging with content about entertainment, reviews, and film discussions.",
    "Build your vocabulary around well-being, exercise, and lifestyle health. From gym routines to healthy eating, learn useful terms that help you communicate about fitness and personal wellness.",
    "Delve into the world of culinary delights with terms related to food, cooking, and dining out. Learn how to order, discuss recipes, and explore the rich vocabulary surrounding Vietnam’s food culture.",
    "Immerse yourself in the language of digital play with vocabulary and expressions related to video games, online communities, and esports. Great for those who love interactive and modern gaming culture.",
    "Focus on language skills within academic and educational contexts. Topics include studying strategies, classroom discussions, and learning resources to support your language journey.",
    "Explore vocabulary and topics around music genres, lyrics, and the art of sound. Understand how music influences language and culture while enhancing your listening skills.",
    "Stay informed with vocabulary and expressions used in current affairs and social issues. This topic helps you discuss politics, local news, and global events in a clear, conversational style.",
    "Broaden your language skills by exploring various leisure activities and personal interests. From crafts to outdoor activities, learn expressions that describe your favorite pastimes.",
    "Enhance your understanding of interpersonal communication with topics focused on friendships, romantic relationships, and social dynamics. Perfect for learning how to express emotions and connect with others.",
    "Build a strong technical vocabulary with lessons on scientific discoveries and technological innovations. Ideal for discussing modern trends and academic subjects in everyday conversations.",
    "Learn the vocabulary of athletic competitions, team sports, and physical activities. From game-day commentary to fitness talk, this topic helps you engage in lively sports discussions.",
    "Equip yourself with essential travel phrases and vocabulary for booking trips, exploring new places, and describing local experiences. Perfect for adventurers planning their next journey.",
    "Connect with language that reflects the energy and experiences of young learners and students. Topics include campus life, student culture, and the challenges and joys of youth."
]
topics['description'] = descriptions

topics.to_csv("data/topics.csv", index=False)