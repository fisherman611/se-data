from gtts import gTTS
import librosa
import numpy as np
import pandas as pd
from tqdm.auto import tqdm  # Import tqdm
import time  # For sleep


def text_to_speech(text: str, output_filename: str, lang: str = "en") -> None:
    """Convert text to speech and save as an audio file.

    Args:
        text (str): The text to convert to speech.
        output_filename (str): The name of the output audio file.
        lang (str): The language of the text. Default is 'en' (English).
    """
    output = gTTS(text, lang=lang, slow=False)
    output.save(output_filename)


# Read sentences from CSV file
sentences = pd.read_csv("data/sentences.csv")

# Convert English sentences to audio files using tqdm for progress tracking
for i in tqdm(range(len(sentences)), desc="Converting English sentences"):
    text = sentences.iloc[i]["eng"]
    output_filename = f"data/media/english/eng_{i}.mp3"
    try:
        text_to_speech(text, output_filename, lang="en")
    except Exception as e:
        print(f"Error processing English sentence {i}: {e}")
    time.sleep(1.5)  # Pause between requests

# Convert Vietnamese sentences to audio files using tqdm for progress tracking
for i in tqdm(range(len(sentences)), desc="Converting Vietnamese sentences"):
    text = sentences.iloc[i]["viet"]
    output_filename = f"data/media/vietnamese/viet_{i}.mp3"
    try:
        text_to_speech(text, output_filename, lang="vi")
    except Exception as e:
        print(f"Error processing Vietnamese sentence {i}: {e}")
    time.sleep(1.5)  # Pause between requests
