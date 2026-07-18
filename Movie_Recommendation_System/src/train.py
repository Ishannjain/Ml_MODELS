# ==========================================================
# MOVIE RECOMMENDATION SYSTEM
# TRAINING PIPELINE
# ==========================================================

import os
import pickle
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Try NLTK stemming (optional – skip gracefully if unavailable)
try:
    import nltk
    from nltk.stem.porter import PorterStemmer
    try:
        nltk.data.find("tokenizers/punkt")
    except LookupError:
        nltk.download("punkt", quiet=True)
    STEMMER = PorterStemmer()
    USE_STEM = True
except ImportError:
    USE_STEM = False

sns.set_theme(style="darkgrid", palette="magma")

# ----------------------------------------------------------
# PATHS
# ----------------------------------------------------------

BASE_DIR   = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR   = os.path.join(BASE_DIR, "datasets")
MODEL_DIR  = os.path.join(BASE_DIR, "model")
CHARTS_DIR = os.path.join(BASE_DIR, "charts")

os.makedirs(MODEL_DIR,  exist_ok=True)
os.makedirs(CHARTS_DIR, exist_ok=True)


# ----------------------------------------------------------
# STEMMING
# ----------------------------------------------------------

def stem(text):
    if USE_STEM:
        return " ".join(STEMMER.stem(w) for w in text.split())
    return text


# ----------------------------------------------------------
# LOAD NLP DATASET
# ----------------------------------------------------------

def load_nlp():
    path = os.path.join(DATA_DIR, "nlp_movies.csv")
    if not os.path.exists(path):
        raise FileNotFoundError(
            f"NLP dataset not found at {path}.\n"
            "Run src/preprocessing.py first."
        )
    df = pd.read_csv(path)
    print(f"[load]  NLP dataset loaded: {df.shape}")
    return df


# ----------------------------------------------------------
# BUILD VECTORIZER & SIMILARITY MATRIX
# ----------------------------------------------------------

def build_model(df):
    """Vectorise tags and compute the cosine-similarity matrix."""
    df = df.copy()

    # Apply stemming to tags
    df["tags"] = df["tags"].fillna("").apply(stem)

    vectorizer = CountVectorizer(max_features=5000, stop_words="english")
    vectors    = vectorizer.fit_transform(df["tags"])

    print(f"[vectorize]  Vocabulary size : {len(vectorizer.vocabulary_)}")
    print(f"[vectorize]  Matrix shape    : {vectors.shape}")

    similarity = cosine_similarity(vectors)
    print(f"[similarity] Matrix shape    : {similarity.shape}")

    return vectorizer, similarity, df


# ----------------------------------------------------------
# SAVE MODELS
# ----------------------------------------------------------

def save_models(df, vectorizer, similarity):
    # Save movies DataFrame (id + title + tags)
    movies_path = os.path.join(MODEL_DIR, "movies.pkl")
    with open(movies_path, "wb") as f:
        pickle.dump(df[["id", "title", "tags"]], f)

    # Save similarity matrix
    sim_path = os.path.join(MODEL_DIR, "similarity.pkl")
    with open(sim_path, "wb") as f:
        pickle.dump(similarity, f)

    # Save vectorizer
    vec_path = os.path.join(MODEL_DIR, "vectorizer.pkl")
    with open(vec_path, "wb") as f:
        pickle.dump(vectorizer, f)

    print(f"[save]  Models saved → {MODEL_DIR}")


# ----------------------------------------------------------
# TRAINING CHARTS
# ----------------------------------------------------------

def _savefig(name):
    path = os.path.join(CHARTS_DIR, name)
    plt.tight_layout()
    plt.savefig(path, dpi=150)
    plt.close()
    print(f"[chart]  Saved → {path}")


def plot_similarity_heatmap(similarity, n=30):
    """Heatmap of the first n×n similarity scores."""
    sub = similarity[:n, :n]

    fig, ax = plt.subplots(figsize=(10, 8))
    sns.heatmap(sub, cmap="magma", ax=ax, xticklabels=False, yticklabels=False,
                cbar_kws={"label": "Cosine Similarity"})
    ax.set_title(f"Similarity Heatmap (first {n} movies)", fontsize=15, fontweight="bold")
    _savefig("similarity_heatmap.png")


def plot_top_similar_movies(similarity, df, movie_title, top_n=10):
    """Horizontal bar chart – most similar movies to a given title."""
    matches = df[df["title"] == movie_title]
    if matches.empty:
        print(f"[chart]  '{movie_title}' not found – skipping bar chart.")
        return

    idx = matches.index[0]
    scores = list(enumerate(similarity[idx]))
    scores = sorted(scores, key=lambda x: x[1], reverse=True)[1: top_n + 1]

    titles  = [df.iloc[i]["title"] for i, _ in scores]
    values  = [v for _, v in scores]

    fig, ax = plt.subplots(figsize=(11, 6))
    colors = sns.color_palette("magma", len(titles))
    bars = ax.barh(titles[::-1], values[::-1], color=colors[::-1])
    ax.set_xlim(0, 1)
    ax.set_title(f"Top {top_n} Movies Similar to '{movie_title}'",
                 fontsize=15, fontweight="bold")
    ax.set_xlabel("Cosine Similarity Score")
    ax.bar_label(bars, fmt="%.3f", padding=3)
    _savefig("top_similar_movies.png")


def plot_tag_length_distribution(df):
    """Histogram – distribution of tag string lengths."""
    lengths = df["tags"].fillna("").apply(lambda x: len(x.split()))

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.hist(lengths, bins=40, color="#9b59b6", edgecolor="white", alpha=0.85)
    ax.axvline(lengths.mean(), color="gold", linewidth=2,
               linestyle="--", label=f"Mean: {lengths.mean():.1f} words")
    ax.set_title("Tag Length Distribution (word count per movie)",
                 fontsize=15, fontweight="bold")
    ax.set_xlabel("Number of Words in Tags")
    ax.set_ylabel("Number of Movies")
    ax.legend()
    _savefig("tag_length_distribution.png")


def plot_similarity_score_distribution(similarity):
    """Histogram – all pairwise similarity scores (sample)."""
    # Use upper triangle of a sample to keep it tractable
    n   = min(500, similarity.shape[0])
    sub = similarity[:n, :n]
    tri = sub[np.triu_indices(n, k=1)]

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.hist(tri, bins=60, color="#e74c3c", edgecolor="white", alpha=0.85)
    ax.set_title("Pairwise Cosine Similarity Score Distribution",
                 fontsize=15, fontweight="bold")
    ax.set_xlabel("Cosine Similarity")
    ax.set_ylabel("Frequency")
    _savefig("similarity_score_distribution.png")


# ----------------------------------------------------------
# MAIN
# ----------------------------------------------------------

def run_training():
    print("=" * 55)
    print(" TRAINING PIPELINE")
    print("=" * 55)

    df = load_nlp()

    vectorizer, similarity, df = build_model(df)

    save_models(df, vectorizer, similarity)

    # --- Generate Training Charts ---
    print("\n--- Generating Training Charts ---")
    plot_similarity_heatmap(similarity)
    plot_tag_length_distribution(df)
    plot_similarity_score_distribution(similarity)

    # Use the most popular movie for the bar chart
    sample_movie = df.iloc[0]["title"]
    plot_top_similar_movies(similarity, df, sample_movie)

    print("\n[done]  Training complete.")
    return df, similarity


if __name__ == "__main__":
    run_training()
