import os
import re
import string

import joblib
import numpy as np
import pandas as pd
import nltk

from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder

# Download required NLTK resources if not already available.
nltk.download("punkt")
nltk.download("stopwords")

# Resolve paths relative to the project root regardless of cwd.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "dataset")
MODEL_DIR = os.path.join(BASE_DIR, "model")
OUTPUT_PATH = os.path.join(DATA_DIR, "preprocessed_spam.csv")

# Prefer a cleaned dataset if it exists, otherwise use the raw dataset.
CLEANED_DATA_PATH = os.path.join(DATA_DIR, "cleaned_spam.csv")
RAW_DATA_PATH = os.path.join(DATA_DIR, "spam.csv")
DATA_PATH = CLEANED_DATA_PATH if os.path.exists(CLEANED_DATA_PATH) else RAW_DATA_PATH

# Initialize the Porter stemmer and stopword list.
ps = PorterStemmer()
stop_words = set(stopwords.words("english"))


def transform_text(text: str) -> str:
    """Clean and normalize a single text message.

    The function applies lowercasing, HTML removal, URL removal,
    numeric stripping, punctuation removal, tokenization, stopword
    removal, and stemming.
    """

    # Convert the text to lowercase for uniform processing.
    text = text.lower()

    # Remove HTML tags, if any.
    text = re.sub(r"<.*?>", "", text)

    # Remove URLs such as http://..., https://..., and www....
    text = re.sub(r"https?://\S+|www\.\S+", "", text)

    # Remove digits and numeric tokens.
    text = re.sub(r"\d+", "", text)

    # Remove punctuation characters.
    text = text.translate(str.maketrans("", "", string.punctuation))

    # Split text into tokens for further processing.
    words = text.split()

    # Remove stopwords and apply stemming.
    clean_words = [ps.stem(word) for word in words if word not in stop_words]

    return " ".join(clean_words)


def preprocess_dataset(input_path: str, output_path: str) -> None:
    """Load the dataset, clean text messages, and save preprocessed output."""

    df = pd.read_csv(input_path)

    # Apply text cleaning to the Message column.
    df["Transformed_Message"] = df["Message"].apply(transform_text)

    # Add derived features useful for analysis.
    df["Clean_Length"] = df["Transformed_Message"].apply(len)

    # Save the processed dataset for reuse.
    df.to_csv(output_path, index=False)


def build_features(df: pd.DataFrame, max_features: int = 3000):
    """Extract TF-IDF features and encode labels."""

    tfidf = TfidfVectorizer(max_features=max_features)

    # Fill NaN values before vectorisation to avoid ValueError.
    X = tfidf.fit_transform(df["Transformed_Message"].fillna("")).toarray()

    # Encode labels: ham=0, spam=1.
    y = df["Label"].map({"ham": 0, "spam": 1}).values
    encoder = LabelEncoder()
    y_encoded = encoder.fit_transform(y)

    return X, y_encoded, tfidf, encoder


def save_artifacts(tfidf_model, label_encoder, model_dir: str) -> None:
    """Save TF-IDF and label encoder artifacts to disk."""

    os.makedirs(model_dir, exist_ok=True)
    joblib.dump(tfidf_model, os.path.join(model_dir, "tfidf.pkl"))
    joblib.dump(label_encoder, os.path.join(model_dir, "label_encoder.pkl"))


if __name__ == "__main__":
    df = pd.read_csv(DATA_PATH)
    preprocess_dataset(DATA_PATH, OUTPUT_PATH)

    df_preprocessed = pd.read_csv(OUTPUT_PATH)
    X, y, tfidf, encoder = build_features(df_preprocessed, max_features=3000)

    save_artifacts(tfidf, encoder, MODEL_DIR)

    print("Preprocessing complete.")
    print("Dataset shape:", df_preprocessed.shape)
    print("Feature matrix shape:", X.shape)
    print("Label vector shape:", y.shape)
    print("Saved artifacts:", os.listdir(MODEL_DIR))
