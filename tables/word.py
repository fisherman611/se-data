from pyvi import ViTokenizer, ViPosTagger
import pandas as pd
from transformers import AutoModel, AutoTokenizer
import torch
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import random
from tqdm.auto import tqdm
from concurrent.futures import ThreadPoolExecutor
import pickle
import os

# Configuration
CACHE_FILE = "data/word_embeddings.pkl"
SENTENCES_FILE = "data/sentences.csv"
OUTPUT_FILE = "data/words.csv"

def load_or_create_embeddings(sentences):
    """Load cached embeddings or create new ones with progress tracking"""
    if os.path.exists(CACHE_FILE):
        print("Loading cached embeddings...")
        with open(CACHE_FILE, "rb") as f:
            return pickle.load(f)
    
    print("Generating new embeddings...")
    vocab = set()
    
    # First pass: Extract vocabulary
    print("Extracting vocabulary...")
    for sentence in tqdm(sentences, desc="Extracting vocabulary"):
        tokenized = ViTokenizer.tokenize(sentence)
        words, pos_tags = ViPosTagger.postagging(tokenized)
        vocab.update(words)  # Keep all words initially
    
    # Second pass: Generate embeddings in parallel
    print("Generating embeddings...")
    vocab = list(vocab)
    embeddings = {}
    
    # Use threading for embedding generation (I/O bound)
    def process_word(word):
        inputs = tokenizer(word, return_tensors="pt", padding=True, truncation=True)
        with torch.no_grad():
            outputs = model(**inputs)
        return word, outputs.last_hidden_state.mean(dim=1).squeeze().numpy()
    
    with ThreadPoolExecutor(max_workers=4) as executor:
        results = list(tqdm(executor.map(process_word, vocab), total=len(vocab), desc="Generating embeddings"))
        for word, embedding in results:
            embeddings[word] = embedding
    
    # Cache the embeddings
    with open(CACHE_FILE, "wb") as f:
        pickle.dump(embeddings, f)
    
    return embeddings

# Load PhoBERT (only once)
tokenizer = AutoTokenizer.from_pretrained("vinai/phobert-base")
model = AutoModel.from_pretrained("vinai/phobert-base")

# Load sentences
sentences_df = pd.read_csv(SENTENCES_FILE)
vietnamese_sentences = sentences_df['viet'].tolist()

# Get or create embeddings
word_embeddings = load_or_create_embeddings(vietnamese_sentences)

def find_similar_words(target_word, embeddings_dict, top_n=3):
    """Find similar words using precomputed embeddings"""
    if target_word not in embeddings_dict:
        return []
    
    target_embedding = embeddings_dict[target_word].reshape(1, -1)
    similarities = {}
    
    for word, embedding in embeddings_dict.items():
        if word == target_word:
            continue
        similarity = cosine_similarity(target_embedding, embedding.reshape(1, -1))[0][0]
        similarities[word] = similarity
    
    return sorted(similarities, key=similarities.get, reverse=True)[:top_n]

# Process sentences
words_data = []
w_id = 1

print("Processing sentences...")
for _, row in tqdm(sentences_df.iterrows(), total=len(sentences_df), desc="Processing sentences"):
    s_id = row['s_id']
    viet_sent = row['viet']
    
    tokenized = ViTokenizer.tokenize(viet_sent)
    words, pos_tags = ViPosTagger.postagging(tokenized)
    
    # Filter non-proper nouns and select random words
    candidate_words = [
        (idx+1, word) 
        for idx, (word, tag) in enumerate(zip(words, pos_tags)) 
        if tag != "Np" and word in word_embeddings
    ]
    
    selected_words = random.sample(candidate_words, min(2, len(candidate_words)))
    
    for idx, word in selected_words:
        similar_words = find_similar_words(word, word_embeddings)
        words_data.append({
            "w_id": w_id,
            "s_id": s_id,
            "idx": idx,
            "word": word,
            "similar_words": ", ".join(similar_words)
        })
        w_id += 1

# Save results
pd.DataFrame(words_data).to_csv(OUTPUT_FILE, index=False)
print("Successfully created the words table!")