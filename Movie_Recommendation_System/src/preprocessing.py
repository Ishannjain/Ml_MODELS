# ==========================================================
# MOVIE RECOMMENDATION SYSTEM
# PREPROCESSING PIPELINE
# ==========================================================

import os
import ast
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")   # non-interactive backend – safe for scripts & servers
import matplotlib.pyplot as plt
import seaborn as sns

# ----------------------------------------------------------
# PATHS
# ----------------------------------------------------------

BASE_DIR   = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR   = os.path.join(BASE_DIR, "datasets")
CHARTS_DIR = os.path.join(BASE_DIR, "charts")

os.makedirs(CHARTS_DIR, exist_ok=True)

PALETTE = sns.color_palette("magma", 10)
sns.set_theme(style="darkgrid", palette="magma")

# ----------------------------------------------------------
# HELPERS
# ----------------------------------------------------------

def _safe_eval(obj):
    """Safely parse a stringified Python list / dict."""
    try:
        return ast.literal_eval(obj)
    except (ValueError, SyntaxError):
        return []


def extract_names(obj, limit=None):
    """Return a list of 'name' values from a JSON-like column."""
    data = _safe_eval(obj) if isinstance(obj, str) else obj
    if not isinstance(data, list):
        return []
    names = [item["name"] for item in data if "name" in item]
    return names[:limit] if limit else names


def extract_director(obj):
    """Return the director's name from the crew column."""
    data = _safe_eval(obj) if isinstance(obj, str) else obj
    if not isinstance(data, list):
        return []
    return [
        item["name"]
        for item in data
        if isinstance(item, dict) and item.get("job") == "Director"
    ]


def collapse(tokens):
    """Remove spaces inside tokens so 'Sam Raimi' → 'SamRaimi'."""
    return [str(t).replace(" ", "") for t in tokens]


# ----------------------------------------------------------
# LOAD RAW DATA
# ----------------------------------------------------------

def load_raw():
    movies_path  = os.path.join(DATA_DIR, "tmdb_5000_movies.csv")
    credits_path = os.path.join(DATA_DIR, "tmdb_5000_credits.csv")

    movies  = pd.read_csv(movies_path)
    credits = pd.read_csv(credits_path)

    # The credits file may use 'movie_id' or 'id'
    if "movie_id" in credits.columns:
        credits.rename(columns={"movie_id": "id"}, inplace=True)

    df = movies.merge(credits, on="id")

    # Keep only the title from credits if duplicated
    if "title_x" in df.columns:
        df.rename(columns={"title_x": "title"}, inplace=True)
        df.drop(columns=["title_y"], inplace=True, errors="ignore")

    print(f"[load_raw]  Shape after merge: {df.shape}")
    return df


# ----------------------------------------------------------
# CLEAN DATA
# ----------------------------------------------------------

def clean_data(df):
    # Select relevant columns
    keep = ["id", "title", "overview", "genres", "keywords", "cast", "crew",
            "vote_average", "vote_count", "popularity", "release_date",
            "runtime", "budget", "revenue", "original_language"]
    existing = [c for c in keep if c in df.columns]
    df = df[existing].copy()

    # Drop nulls & duplicates
    df.dropna(subset=["title", "overview"], inplace=True)
    df.drop_duplicates(subset="id", inplace=True)
    df.reset_index(drop=True, inplace=True)

    print(f"[clean]     Shape: {df.shape}")
    return df


# ----------------------------------------------------------
# FEATURE ENGINEERING
# ----------------------------------------------------------

def engineer_features(df):
    # Parse JSON-like columns
    df["genres"]   = df["genres"].apply(lambda x: extract_names(x))
    df["keywords"] = df["keywords"].apply(lambda x: extract_names(x))
    df["cast"]     = df["cast"].apply(lambda x: extract_names(x, limit=3))
    df["director"] = df["crew"].apply(extract_director)
    df.drop(columns=["crew"], inplace=True, errors="ignore")

    print(f"[features]  Shape: {df.shape}")
    return df


# ----------------------------------------------------------
# NLP – BUILD TAGS
# ----------------------------------------------------------

def build_tags(df):
    df = df.copy()

    # Tokenize overview
    df["overview"] = df["overview"].fillna("").apply(lambda x: x.split())

    # Collapse multi-word tokens
    df["genres"]   = df["genres"].apply(collapse)
    df["keywords"] = df["keywords"].apply(collapse)
    df["cast"]     = df["cast"].apply(collapse)
    df["director"] = df["director"].apply(collapse)

    # Combine all into a single 'tags' list
    df["tags"] = (
        df["overview"]
        + df["genres"]
        + df["keywords"]
        + df["cast"]
        + df["director"]
    )

    # Lower-case string version
    df["tags"] = df["tags"].apply(lambda x: " ".join(x).lower())

    # Final NLP dataframe
    nlp_df = df[["id", "title", "tags"]].copy()
    print(f"[nlp]       Shape: {nlp_df.shape}")
    return nlp_df, df


# ----------------------------------------------------------
# SAVE INTERMEDIATE DATASETS
# ----------------------------------------------------------

def save_datasets(clean_df, feat_df, nlp_df):
    clean_df.to_csv(os.path.join(DATA_DIR, "clean_movies.csv"), index=False)
    feat_df.to_csv(os.path.join(DATA_DIR, "feature_engineered_movies.csv"), index=False)
    nlp_df.to_csv(os.path.join(DATA_DIR, "nlp_movies.csv"), index=False)
    print("[save]      All CSVs saved to datasets/")


# ----------------------------------------------------------
# CHART HELPERS
# ----------------------------------------------------------

def _savefig(name):
    path = os.path.join(CHARTS_DIR, name)
    plt.tight_layout()
    plt.savefig(path, dpi=150)
    plt.close()
    print(f"[chart]     Saved → {path}")


# ----------------------------------------------------------
# EDA CHARTS
# ----------------------------------------------------------

def plot_genre_distribution(df):
    """Bar chart – top 15 genres by movie count."""
    from collections import Counter

    genres_flat = []
    for g_list in df["genres"]:
        if isinstance(g_list, list):
            genres_flat.extend(g_list)
        else:
            genres_flat.extend(str(g_list).split())

    genre_counts = Counter(genres_flat).most_common(15)
    labels, values = zip(*genre_counts)

    fig, ax = plt.subplots(figsize=(12, 6))
    bars = ax.barh(labels, values, color=sns.color_palette("magma", len(labels)))
    ax.invert_yaxis()
    ax.set_title("Top 15 Genres by Movie Count", fontsize=16, fontweight="bold")
    ax.set_xlabel("Number of Movies")
    ax.bar_label(bars, padding=3)
    _savefig("genre_distribution.png")


def plot_vote_distribution(df):
    """Histogram – distribution of vote averages."""
    col = "vote_average"
    if col not in df.columns:
        return
    valid = df[col].dropna()
    valid = valid[valid > 0]

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.hist(valid, bins=30, color="#c0392b", edgecolor="white", alpha=0.85)
    ax.axvline(valid.mean(), color="gold", linewidth=2,
               linestyle="--", label=f"Mean: {valid.mean():.2f}")
    ax.set_title("Vote Average Distribution", fontsize=16, fontweight="bold")
    ax.set_xlabel("Vote Average (0–10)")
    ax.set_ylabel("Number of Movies")
    ax.legend()
    _savefig("vote_distribution.png")


def plot_popularity_vs_rating(df):
    """Scatter – popularity vs vote average, coloured by vote count."""
    needed = {"popularity", "vote_average", "vote_count"}
    if not needed.issubset(df.columns):
        return

    sample = df[list(needed)].dropna()
    sample = sample[(sample["vote_average"] > 0) & (sample["popularity"] < 500)]

    fig, ax = plt.subplots(figsize=(11, 6))
    sc = ax.scatter(
        sample["popularity"], sample["vote_average"],
        c=sample["vote_count"], cmap="magma", alpha=0.5, s=15
    )
    plt.colorbar(sc, ax=ax, label="Vote Count")
    ax.set_title("Popularity vs Vote Average", fontsize=16, fontweight="bold")
    ax.set_xlabel("Popularity Score")
    ax.set_ylabel("Vote Average")
    _savefig("popularity_vs_rating.png")


def plot_language_distribution(df):
    """Pie chart – top 8 original languages."""
    if "original_language" not in df.columns:
        return
    top = df["original_language"].value_counts().head(8)

    fig, ax = plt.subplots(figsize=(8, 8))
    ax.pie(
        top.values,
        labels=top.index,
        autopct="%1.1f%%",
        colors=sns.color_palette("magma", len(top)),
        startangle=140,
        pctdistance=0.82,
    )
    ax.set_title("Original Language Distribution (Top 8)", fontsize=15, fontweight="bold")
    _savefig("language_distribution.png")


def plot_movies_per_year(df):
    """Line chart – number of movies released per year."""
    if "release_date" not in df.columns:
        return
    df = df.copy()
    df["year"] = pd.to_datetime(df["release_date"], errors="coerce").dt.year
    yearly = df["year"].dropna().astype(int).value_counts().sort_index()
    yearly = yearly[yearly.index >= 1970]

    fig, ax = plt.subplots(figsize=(12, 5))
    ax.fill_between(yearly.index, yearly.values, alpha=0.35, color="#8e44ad")
    ax.plot(yearly.index, yearly.values, color="#8e44ad", linewidth=2)
    ax.set_title("Movies Released Per Year (1970+)", fontsize=16, fontweight="bold")
    ax.set_xlabel("Year")
    ax.set_ylabel("Number of Movies")
    _savefig("movies_per_year.png")


def plot_top_keywords(nlp_df):
    """Bar chart – top 20 keywords across all tag corpora."""
    from collections import Counter

    all_words = " ".join(nlp_df["tags"].fillna("")).split()
    # Filter generic stop-words
    stopwords = {"the","a","an","of","in","and","to","is","it","for",
                 "with","on","at","by","from","as","this","that","are","was"}
    filtered = [w for w in all_words if w not in stopwords and len(w) > 3]
    top = Counter(filtered).most_common(20)
    labels, values = zip(*top)

    fig, ax = plt.subplots(figsize=(12, 6))
    ax.bar(labels, values, color=sns.color_palette("magma", len(labels)))
    ax.set_title("Top 20 Most Frequent Keywords in Tags", fontsize=16, fontweight="bold")
    ax.set_xlabel("Keyword")
    ax.set_ylabel("Frequency")
    plt.xticks(rotation=45, ha="right")
    _savefig("top_keywords.png")


# ----------------------------------------------------------
# MAIN
# ----------------------------------------------------------

def run_preprocessing():
    print("=" * 55)
    print(" PREPROCESSING PIPELINE")
    print("=" * 55)

    raw_df   = load_raw()
    clean_df = clean_data(raw_df)
    feat_df  = engineer_features(clean_df.copy())
    nlp_df, full_feat_df = build_tags(feat_df)

    save_datasets(clean_df, full_feat_df, nlp_df)

    # --- Generate EDA Charts ---
    print("\n--- Generating EDA Charts ---")
    plot_genre_distribution(full_feat_df)
    plot_vote_distribution(full_feat_df)
    plot_popularity_vs_rating(full_feat_df)
    plot_language_distribution(full_feat_df)
    plot_movies_per_year(full_feat_df)
    plot_top_keywords(nlp_df)

    print("\n[done]  Preprocessing complete.")
    return nlp_df


if __name__ == "__main__":
    run_preprocessing()
