from pyvi import ViTokenizer, ViPosTagger
from underthesea import word_tokenize, ner
import pandas as pd
from transformers import AutoModel, AutoTokenizer   #type: ignore
import torch
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import random
from tqdm.auto import tqdm
from concurrent.futures import ThreadPoolExecutor
import pickle
import os
from deep_translator import GoogleTranslator
import re 
import string

# Configuration
CACHE_FILE = "data/word_embeddings.pkl"
SENTENCES_FILE = "data/selected_sentences.csv"
OUTPUT_FILE = "data/selected_words.csv"
STOPWORDS_FILE = "data/stopwords.txt"

# Sentence cleaning function
def clean_sentence(sentence):
    """Clean a Vietnamese sentence: lowercase, remove punctuation, strip redundant spaces."""
    entities = ner(sentence)
    words = [entity[0] for entity in entities]
    for entity in entities: 
        if entity[3] != 'O':
            words.remove(entity[0])
            
    sentence = ' '.join(words)        #type: ignore
    sentence = sentence.lower()
    sentence = sentence.translate(str.maketrans(string.punctuation, ' ' * len(string.punctuation)))
    sentence = re.sub(r'\s+', ' ', sentence).strip()  # Strip redundant spaces
    
    return sentence

# Load stopwords
# Load stopwords
def load_stopwords(file_path):
    """Load stopwords from a text file."""
    word_set = set()
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f: 
            line = line.replace(' ', '_')
            line = line.strip()
            word_set.add(line)
    return word_set

def load_or_create_embeddings(sentences):
    """Load cached embeddings or create new ones with progress tracking."""
    if os.path.exists(CACHE_FILE):
        print("Loading cached embeddings...")
        with open(CACHE_FILE, "rb") as f:
            return pickle.load(f)
    
    print("Generating new embeddings...")
    vocab = set()
    
    print("Extracting vocabulary...")
    for sentence in tqdm(sentences, desc="Extracting vocabulary"):
        cleaned = clean_sentence(sentence)
        tokenized = ViTokenizer.tokenize(cleaned)
        words, _ = ViPosTagger.postagging(tokenized)
        vocab.update(words)
    
    print("Generating embeddings...")
    vocab = list(vocab)
    embeddings = {}
    
    def process_word(word):
        inputs = tokenizer(word, return_tensors="pt", padding=True, truncation=True)
        with torch.no_grad():
            outputs = model(**inputs)
        return word, outputs.last_hidden_state.mean(dim=1).squeeze().numpy()
    
    with ThreadPoolExecutor(max_workers=4) as executor:
        results = list(tqdm(executor.map(process_word, vocab), total=len(vocab), desc="Generating embeddings"))
        for word, embedding in results:
            embeddings[word] = embedding
    
    with open(CACHE_FILE, "wb") as f:
        pickle.dump(embeddings, f)
    
    return embeddings

# Load PhoBERT
tokenizer = AutoTokenizer.from_pretrained("vinai/phobert-base", use_fast=True)
model = AutoModel.from_pretrained("vinai/phobert-base")

# Load stopwords
stopwords = load_stopwords(STOPWORDS_FILE)

# Initialize translator
translator = GoogleTranslator(source='vi', target='en')

# Load sentences
sentences_df = pd.read_csv(SENTENCES_FILE)
vietnamese_sentences = sentences_df['viet'].tolist()

# Get or create embeddings
word_embeddings = load_or_create_embeddings(vietnamese_sentences)

def find_similar_words(target_word, embeddings_dict, top_n=2):
    """Find similar words using precomputed embeddings."""
    if target_word not in embeddings_dict:
        return []
    
    target_embedding = embeddings_dict[target_word].reshape(1, -1)
    similarities = {}
    
    for word, embedding in embeddings_dict.items():
        if word == target_word:
            continue
        similarity = cosine_similarity(target_embedding, embedding.reshape(1, -1))[0][0]
        similarities[word] = similarity
    
    return sorted(similarities, key=similarities.get, reverse=True)[:top_n]   #type: ignore

# Process sentences
words_data = []
w_id = 1

print("Processing sentences...")
for _, row in tqdm(sentences_df.iterrows(), total=len(sentences_df), desc="Processing sentences"):
    s_id = row['s_id']
    viet_sent = row['viet']
    
    cleaned_sent = clean_sentence(viet_sent)
    tokenized = ViTokenizer.tokenize(cleaned_sent)
    words, pos_tags = ViPosTagger.postagging(tokenized)
    
    candidate_words = [
        (idx + 1, word)
        for idx, (word, tag) in enumerate(zip(words, pos_tags))
        if tag != "Np" and word in word_embeddings
    ]

    print(candidate_words)
    selected_words = random.sample(candidate_words, min(5, len(candidate_words)))
    
    for idx, word in selected_words:
        # Replace underscore with space for display and translation
        word_display = word.replace('_', ' ')
        word_for_translation = word.replace('_', ' ')
        # Find similar words (assuming this function exists)
        similar_words = find_similar_words(word, word_embeddings, top_n=2)
        similar_words_display = [w.replace('_', ' ').lower() for w in similar_words]
        similar_words_for_translation = [w.replace('_', ' ') for w in similar_words]
        
        # Translate the word (assuming a translator object exists)
        try:
            eng = translator.translate(word_for_translation).lower()
        except Exception as e:
            eng = "translation_error"
            print(f"Translation error for word '{word_for_translation}': {e}")
        
        # Translate similar words
        similar_eng = []
        for sim_word in similar_words_for_translation:
            try:
                sim_eng = translator.translate(sim_word).lower()
                similar_eng.append(sim_eng)
            except Exception as e:
                similar_eng.append("translation_error")
                print(f"Translation error for similar word '{sim_word}': {e}")
        
        # Append the row data
        words_data.append({
            "w_id": w_id,
            "s_id": s_id,
            "idx": idx,
            "viet": word_display,
            "viet_similar_words": ", ".join(similar_words_display),
            "eng": eng,
            "eng_similar_words": ", ".join(similar_eng)
        })
        w_id += 1

# Save results with specified columns
columns = ["w_id", "s_id", "idx", "viet", "viet_similar_words", "eng", "eng_similar_words"]
pd.DataFrame(words_data, columns=columns).to_csv(OUTPUT_FILE, index=False)
print("Successfully created the words table!")