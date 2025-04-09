import pandas as pd
import nltk
from nltk.tokenize import word_tokenize
from underthesea import word_tokenize as viet_word_tokenize
from collections import Counter
from tqdm.auto import tqdm

# Download NLTK's Punkt tokenizer data (if not already downloaded)
nltk.download('punkt')

# Read the sentences.csv file (assumed to contain columns: s_id, eng, viet, topic_name)
sentences = pd.read_csv("data/sentences.csv")

# --------------------
# Step 1: Build Separate Vocabularies (Bag-of-Words) for English and Vietnamese
# --------------------
# Frequency dictionaries for English and Vietnamese
eng_vocab_counter = Counter()
viet_vocab_counter = Counter()

# Iterate over all sentences with a progress bar
for _, row in tqdm(sentences.iterrows(), total=len(sentences), desc="Building vocab frequency"):
    # Tokenize the English sentence using NLTK
    eng_tokens = word_tokenize(row["eng"])
    for token in eng_tokens:
        eng_vocab_counter[token] += 1

    # Tokenize the Vietnamese sentence using Underthesea
    viet_text = row["viet"]
    if isinstance(viet_text, str):  # Ensure valid string
        viet_tokens = viet_word_tokenize(viet_text, format="list")  # returns a list of tokens
        for token in viet_tokens:
            viet_vocab_counter[token] += 1

# Sort the vocabularies by descending frequency and then alphabetically (for ties)
# Most frequent tokens get smaller token IDs (starting with 1)
sorted_eng_vocab = sorted(eng_vocab_counter.items(), key=lambda x: (-x[1], x[0]))
sorted_viet_vocab = sorted(viet_vocab_counter.items(), key=lambda x: (-x[1], x[0]))

# Build the vocabulary mappings: key: (token) -> token_id
eng_vocab_mapping = {token: idx + 1 for idx, (token, _) in enumerate(sorted_eng_vocab)}
viet_vocab_mapping = {token: idx + 1 for idx, (token, _) in enumerate(sorted_viet_vocab)}

# --------------------
# Step 2: Build the Sentence_Token Table
# --------------------
token_rows = []  # list to collect tokens with their details
token_id_counter = 1

# Process each row in the original sentences DataFrame
for _, row in tqdm(sentences.iterrows(), total=len(sentences), desc="Building sentence token table"):
    s_id = row["s_id"]
    
    # Process English sentence and assign token IDs from the English vocabulary
    eng_tokens = word_tokenize(row["eng"])
    for token in eng_tokens:
        tid = eng_vocab_mapping.get(token)
        if tid:
            token_rows.append({
                "token_id": tid,
                "s_id": s_id,
                "language": "en",
                "token": token
            })
    
    # Process Vietnamese sentence and assign token IDs from the Vietnamese vocabulary
    viet_text = row["viet"]
    if isinstance(viet_text, str):  # Ensure valid string
        viet_tokens = viet_word_tokenize(viet_text, format="list")
        for token in viet_tokens:
            tid = viet_vocab_mapping.get(token)
            if tid:
                token_rows.append({
                    "token_id": tid,
                    "s_id": s_id,
                    "language": "vi",
                    "token": token
                })

# Create the sentence_token DataFrame with the desired columns:
sentence_token_df = pd.DataFrame(token_rows, columns=["token_id", "s_id", "language", "token"])

# --------------------
# Step 3: Save Output
# --------------------
sentence_token_df.to_csv("data/sentence_tokens.csv", index=False)
print("sentence_token.csv has been created successfully!")
