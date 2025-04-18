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

K = 2000
# Convert English sentences to audio files using tqdm for progress tracking
# for i in tqdm(range(len(sentences)), desc="Converting English sentences"):
for i in tqdm(range(0, K), desc="Converting English sentences"):
# for i in tqdm(range(K, 2*K), desc="Converting English sentences"):
# for i in tqdm(range(2*K, 3*K), desc="Converting English sentences"):
# for i in tqdm(range(3*K, 4*K), desc="Converting English sentences"):
# for i in tqdm(range(4*K, 5*K), desc="Converting English sentences"):
# for i in tqdm(range(5*K, len(sentences)), desc="Converting English sentences"):
    text = sentences.iloc[i]["eng"]
    output_filename = f"data/media/english/eng_{i + 1}.mp3"
    try:
        text_to_speech(text, output_filename, lang="en")
    except Exception as e:
        print(f"Error processing English sentence {i + 1}: {e}")
    time.sleep(1.5)

# # Convert Vietnamese sentences to audio files using tqdm for progress tracking
# # for i in tqdm(range(len(sentences)), desc="Converting Vietnamese sentences"):
# for i in tqdm(range(0, K), desc="Converting Vietnamese sentences"):
# # for i in tqdm(range(K, 2*K), desc="Converting Vietnamese sentences"):
# # for i in tqdm(range(2*K, 3*K), desc="Converting Vietnamese sentences"):
# # for i in tqdm(range(3*K, 4*K), desc="Converting Vietnamese sentences"):
# # for i in tqdm(range(4*K, 5*K), desc="Converting Vietnamese sentences"):
# # for i in tqdm(range(5*K, len(sentences)), desc="Converting Vietnamese sentences"):
#     text = sentences.iloc[i]["viet"]
#     output_filename = f"data/media/vietnamese/viet_{i + 1}.mp3"
#     try:
#         text_to_speech(text, output_filename, lang="vi")
#     except Exception as e:
#         print(f"Error processing Vietnamese sentence {i + 1}: {e}")
#     time.sleep(1.5)