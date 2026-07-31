# ==========================================================
# preprocessing.py
# Fake News Detection – Data Cleaning & Text Preprocessing
# ==========================================================

import os
import re
import string

import nltk
import pandas as pd

from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

# ---------------------------------------------------------------------------
# Paths (resolved relative to this file so the script can be run from
# anywhere inside the project)
# ---------------------------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATASET_DIR = os.path.join(BASE_DIR, "dataset")
FAKE_CSV    = os.path.join(DATASET_DIR, "Fake.csv")
TRUE_CSV    = os.path.join(DATASET_DIR, "True.csv")
OUTPUT_CSV  = os.path.join(DATASET_DIR, "processed_fake_news.csv")


# ---------------------------------------------------------------------------
# Text-cleaning helpers
# ---------------------------------------------------------------------------
nltk.download("stopwords", quiet=True)
_stop_words = set(stopwords.words("english"))
_stemmer    = PorterStemmer()


def clean_text(text: str) -> str:
    """Lowercase, strip URLs/HTML/digits/punctuation, remove stop-words, stem."""
    text = str(text).lower()
    text = re.sub(r"http\S+", "", text)          # remove URLs
    text = re.sub(r"www\S+",  "", text)          # remove www-links
    text = re.sub(r"<.*?>",   "", text)          # remove HTML tags
    text = re.sub(r"\d+",     "", text)          # remove digits
    text = text.translate(str.maketrans("", "", string.punctuation))
    words = [
        _stemmer.stem(w)
        for w in text.split()
        if w not in _stop_words
    ]
    return " ".join(words)


# ---------------------------------------------------------------------------
# Main pipeline
# ---------------------------------------------------------------------------
def run():
    # ------------------------------------------------------------------
    # 1. Load raw datasets
    # ------------------------------------------------------------------
    print("=" * 60)
    print("Loading Datasets…")
    print("=" * 60)

    fake_df = pd.read_csv(FAKE_CSV)
    true_df = pd.read_csv(TRUE_CSV)

    print(f"\nFake News Dataset Shape : {fake_df.shape}")
    print(f"True News Dataset Shape : {true_df.shape}")

    # ------------------------------------------------------------------
    # 2. Add labels & merge
    # ------------------------------------------------------------------
    fake_df["label"] = 0
    true_df["label"] = 1

    df = pd.concat([fake_df, true_df], axis=0)
    df = df.sample(frac=1, random_state=42).reset_index(drop=True)

    print("\n" + "=" * 60)
    print("Datasets Merged & Shuffled")
    print("=" * 60)
    print(f"Dataset Shape : {df.shape}")

    # ------------------------------------------------------------------
    # 3. Remove missing values & duplicates
    # ------------------------------------------------------------------
    print("\n" + "=" * 60)
    print("Before Cleaning")
    print("=" * 60)
    print("Missing Values")
    print(df.isnull().sum())
    print(f"\nDuplicate Rows : {df.duplicated().sum()}")

    df.dropna(inplace=True)
    df.drop_duplicates(inplace=True)
    df.reset_index(drop=True, inplace=True)

    print("\n" + "=" * 60)
    print("After Cleaning")
    print("=" * 60)
    print(f"Dataset Shape : {df.shape}")
    print("Missing Values")
    print(df.isnull().sum())
    print(f"\nDuplicate Rows : {df.duplicated().sum()}")

    # ------------------------------------------------------------------
    # 4. Clean text column
    # ------------------------------------------------------------------
    print("\n" + "=" * 60)
    print("Cleaning News Articles…")
    print("=" * 60)

    df = df.dropna(subset=["text"])
    df["text"] = df["text"].astype(str)
    df["text"] = df["text"].apply(clean_text)

    print("Text Cleaning Completed Successfully")

    # ------------------------------------------------------------------
    # 5. Save processed dataset
    # ------------------------------------------------------------------
    os.makedirs(DATASET_DIR, exist_ok=True)
    df.to_csv(OUTPUT_CSV, index=False)

    print("\n" + "=" * 60)
    print("Processed Dataset Saved Successfully")
    print("=" * 60)
    print(f"Saved File : {OUTPUT_CSV}")

    return df


if __name__ == "__main__":
    run()
