# ==========================================================
# MOVIE RECOMMENDATION SYSTEM
# STREAMLIT APPLICATION  –  Deploy-Ready
# ==========================================================

import os
import sys
import pickle
import ast
from collections import Counter
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# ----------------------------------------------------------
# PATH FIX  (works whether run from root or app/)
# ----------------------------------------------------------

ROOT = os.path.dirname(os.path.abspath(__file__))
if os.path.basename(ROOT).lower() == "app":
    ROOT = os.path.dirname(ROOT)

MODEL_DIR  = os.path.join(ROOT, "model")
CHARTS_DIR = os.path.join(ROOT, "charts")
SRC_DIR    = os.path.join(ROOT, "src")

if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

# ----------------------------------------------------------
# PAGE CONFIG  (must be first Streamlit call)
# ----------------------------------------------------------

st.set_page_config(
    page_title="🎬 Movie Recommender",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ----------------------------------------------------------
# COLOUR PALETTE  (cinema gold / teal / charcoal)
# ----------------------------------------------------------

C_BG        = "#0a0e17"        # deep navy-black
C_BG2       = "#111827"        # card surface
C_ACCENT1   = "#f5a623"        # gold
C_ACCENT2   = "#00d4aa"        # teal
C_ACCENT3   = "#e05a5a"        # coral-red accent
C_TEXT      = "#e8eaf0"
C_MUTED     = "#7a8099"
C_BORDER    = "rgba(245,166,35,0.18)"
C_GLOW      = "rgba(245,166,35,0.22)"

# ----------------------------------------------------------
# CUSTOM CSS
# ----------------------------------------------------------

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;900&display=swap');

html, body, [class*="css"] {{
    font-family: 'Inter', sans-serif;
}}

/* ── Background ── */
.stApp {{
    background: linear-gradient(160deg, {C_BG} 0%, #0e1623 55%, #12151f 100%);
    color: {C_TEXT};
}}

/* ── Hero ── */
.hero-title {{
    font-size: 2.9rem;
    font-weight: 900;
    background: linear-gradient(90deg, {C_ACCENT1}, {C_ACCENT2}, {C_ACCENT1});
    background-size: 200%;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    text-align: center;
    margin-bottom: 0.25rem;
    animation: shimmer 4s linear infinite;
}}
@keyframes shimmer {{
    0%   {{ background-position: 0%   }}
    100% {{ background-position: 200% }}
}}
.hero-sub {{
    text-align: center;
    color: {C_MUTED};
    font-size: 1.05rem;
    margin-bottom: 2rem;
    letter-spacing: 0.3px;
}}

/* ── Recommendation cards ── */
.rec-card {{
    background: linear-gradient(135deg, rgba(245,166,35,0.06), rgba(0,212,170,0.04));
    border: 1px solid {C_BORDER};
    border-radius: 14px;
    padding: 1.2rem 1.6rem;
    margin-bottom: 0.9rem;
    transition: transform 0.2s, box-shadow 0.2s;
}}
.rec-card:hover {{
    transform: translateY(-3px);
    box-shadow: 0 8px 28px {C_GLOW};
}}
.rec-rank {{
    font-size: 1.9rem;
    font-weight: 900;
    color: {C_ACCENT1};
    float: left;
    margin-right: 1rem;
    line-height: 1.05;
}}
.rec-title {{
    font-size: 1.2rem;
    font-weight: 700;
    color: #ffffff;
}}
.rec-genre-tag {{
    display: inline-block;
    background: rgba(0,212,170,0.15);
    border: 1px solid rgba(0,212,170,0.3);
    color: {C_ACCENT2};
    border-radius: 999px;
    padding: 1px 10px;
    font-size: 0.72rem;
    font-weight: 600;
    margin: 4px 2px 0 0;
    letter-spacing: 0.3px;
    text-transform: uppercase;
}}
.rec-score {{
    font-size: 0.83rem;
    color: {C_ACCENT1};
    font-weight: 600;
    margin-top: 4px;
}}

/* ── Score bar ── */
.score-bar-wrap {{
    background: rgba(255,255,255,0.07);
    border-radius: 999px;
    height: 5px;
    margin-top: 9px;
}}
.score-bar-fill {{
    background: linear-gradient(90deg, {C_ACCENT1}, {C_ACCENT2});
    height: 5px;
    border-radius: 999px;
}}

/* ── Genre pill (search) ── */
.genre-pill {{
    display: inline-block;
    background: rgba(245,166,35,0.12);
    border: 1px solid rgba(245,166,35,0.35);
    color: {C_ACCENT1};
    border-radius: 999px;
    padding: 4px 14px;
    font-size: 0.78rem;
    font-weight: 700;
    margin: 3px;
    cursor: pointer;
    letter-spacing: 0.4px;
    text-transform: uppercase;
}}

/* ── Sidebar ── */
[data-testid="stSidebar"] {{
    background: linear-gradient(180deg, #0c0f1a 0%, #0e1320 100%);
    border-right: 1px solid rgba(245,166,35,0.12);
}}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {{
    gap: 6px;
    background: rgba(255,255,255,0.03);
    border-radius: 12px;
    padding: 4px;
    border: 1px solid rgba(245,166,35,0.1);
}}
.stTabs [data-baseweb="tab"] {{
    border-radius: 8px;
    color: {C_MUTED};
    font-weight: 600;
    font-size: 0.95rem;
}}
.stTabs [aria-selected="true"] {{
    background: linear-gradient(135deg, {C_ACCENT1}, #e08c00) !important;
    color: #0a0e17 !important;
    font-weight: 800 !important;
}}

/* ── Buttons ── */
.stButton > button {{
    background: linear-gradient(135deg, {C_ACCENT1}, #d48f00);
    color: #0a0e17;
    border: none;
    border-radius: 10px;
    padding: 0.55rem 2rem;
    font-weight: 800;
    font-size: 1rem;
    letter-spacing: 0.4px;
    transition: opacity 0.18s, transform 0.14s, box-shadow 0.18s;
    width: 100%;
}}
.stButton > button:hover {{
    opacity: 0.9;
    transform: scale(1.015);
    box-shadow: 0 6px 20px rgba(245,166,35,0.35);
}}

/* ── Metrics ── */
[data-testid="stMetric"] {{
    background: rgba(245,166,35,0.06);
    border: 1px solid rgba(245,166,35,0.15);
    border-radius: 12px;
    padding: 1rem;
}}
[data-testid="stMetricValue"] {{
    color: {C_ACCENT1} !important;
    font-weight: 800 !important;
}}

/* ── Selectbox ── */
.stSelectbox > div > div {{
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(245,166,35,0.2);
    border-radius: 10px;
}}

/* ── Radio buttons (mode switch) ── */
.stRadio > div {{
    background: rgba(255,255,255,0.03);
    border-radius: 10px;
    padding: 4px 10px;
}}

/* ── Divider accent ── */
.gold-divider {{
    height: 2px;
    background: linear-gradient(90deg, transparent, {C_ACCENT1}, {C_ACCENT2}, transparent);
    border: none;
    margin: 1.5rem 0;
    border-radius: 2px;
}}

/* ── Section label ── */
.section-label {{
    font-size: 0.7rem;
    font-weight: 700;
    color: {C_ACCENT1};
    letter-spacing: 1.5px;
    text-transform: uppercase;
    margin-bottom: 0.4rem;
}}
</style>
""", unsafe_allow_html=True)


# ----------------------------------------------------------
# LOAD MODELS  (cached)
# ----------------------------------------------------------

@st.cache_resource(show_spinner="Loading model…")
def load_models():
    movies_path = os.path.join(MODEL_DIR, "movies.pkl")
    sim_path    = os.path.join(MODEL_DIR, "similarity.pkl")

    if not os.path.exists(movies_path) or not os.path.exists(sim_path):
        return None, None

    with open(movies_path, "rb") as f:
        movies = pickle.load(f)
    with open(sim_path, "rb") as f:
        similarity = pickle.load(f)

    return movies, similarity


# ----------------------------------------------------------
# GENRE EXTRACTION  (from tags or feature CSV)
# ----------------------------------------------------------

KNOWN_GENRES = [
    "Action", "Adventure", "Animation", "Comedy", "Crime", "Documentary",
    "Drama", "Family", "Fantasy", "History", "Horror", "Music", "Mystery",
    "Romance", "Science Fiction", "ScienceFiction", "Thriller", "War", "Western",
    "Foreign", "TV Movie",
]

@st.cache_data(show_spinner=False)
def extract_genres_from_tags(_movies_df):
    """Best-effort genre extraction from the 'tags' column."""
    genre_tokens = {g.lower().replace(" ", "") for g in KNOWN_GENRES}

    movie_genres = {}
    for _, row in _movies_df.iterrows():
        tags   = str(row.get("tags", "")).split()
        genres = [g for g in tags if g.lower() in genre_tokens]
        # Map collapsed token back to display name
        display = []
        for g in genres:
            for gn in KNOWN_GENRES:
                if gn.lower().replace(" ", "") == g.lower():
                    display.append(gn)
                    break
        movie_genres[row["title"]] = list(dict.fromkeys(display))

    return movie_genres


@st.cache_data(show_spinner=False)
def load_genre_map_from_csv():
    """Load genre data from feature CSV if available."""
    feat_path = os.path.join(ROOT, "datasets", "feature_engineered_movies.csv")
    raw_path  = os.path.join(ROOT, "datasets", "tmdb_5000_movies.csv")

    for p in [feat_path, raw_path]:
        if os.path.exists(p):
            df = pd.read_csv(p)
            if "genres" in df.columns and "title" in df.columns:
                genre_map = {}
                for _, row in df.iterrows():
                    try:
                        g_list = ast.literal_eval(str(row["genres"]))
                        names = [item["name"] for item in g_list if isinstance(item, dict)]
                    except Exception:
                        names = []
                    genre_map[row["title"]] = names
                return genre_map
    return None


# ----------------------------------------------------------
# RECOMMENDATION FUNCTIONS
# ----------------------------------------------------------

def recommend(movie_title, movies, similarity, top_n=5):
    matches = movies[movies["title"] == movie_title]
    if matches.empty:
        return []
    idx    = matches.index[0]
    dists  = similarity[idx]
    ranked = sorted(enumerate(dists), key=lambda x: x[1], reverse=True)[1: top_n + 1]
    return [(movies.iloc[i]["title"], round(float(s), 4)) for i, s in ranked]


def recommend_by_genre(genre, movies, similarity, genre_map, top_n=10):
    """Return top-N movies filtered by genre, ranked by their mean similarity to all others."""
    genre_lower = genre.lower().replace(" ", "")

    # Collect movies matching the genre
    matched_titles = []
    for title, genres in genre_map.items():
        if any(g.lower().replace(" ", "") == genre_lower for g in genres):
            matched_titles.append(title)

    if not matched_titles:
        return []

    # Filter to titles that exist in the model
    valid = movies[movies["title"].isin(matched_titles)]
    if valid.empty:
        return []

    # Rank by average similarity score to all other movies in the genre
    indices = valid.index.tolist()
    scores  = []
    for idx in indices:
        row_scores = similarity[idx][indices]
        mean_score = float(np.mean(row_scores))
        title = movies.iloc[idx]["title"]
        scores.append((title, round(mean_score, 4)))

    scores.sort(key=lambda x: x[1], reverse=True)
    return scores[:top_n]


def get_available_genres(genre_map):
    """Return sorted list of genres that have at least 3 movies."""
    genre_counts = Counter()
    for genres in genre_map.values():
        for g in genres:
            genre_counts[g] += 1
    return sorted([g for g, c in genre_counts.items() if c >= 3])


# ----------------------------------------------------------
# CHART HELPERS
# ----------------------------------------------------------

def get_charts():
    if not os.path.isdir(CHARTS_DIR):
        return {}
    files = sorted(f for f in os.listdir(CHARTS_DIR) if f.endswith(".png"))
    labels = {
        "genre_distribution.png":            "Genre Distribution",
        "vote_distribution.png":             "Vote Average Distribution",
        "popularity_vs_rating.png":          "Popularity vs Rating",
        "language_distribution.png":         "Language Distribution",
        "movies_per_year.png":               "Movies Per Year",
        "top_keywords.png":                  "Top Keywords",
        "similarity_heatmap.png":            "Similarity Heatmap",
        "tag_length_distribution.png":       "Tag Length Distribution",
        "similarity_score_distribution.png": "Score Distribution",
        "top_similar_movies.png":            "Top Similar Movies",
    }
    return {labels.get(f, f.replace("_", " ").title()): os.path.join(CHARTS_DIR, f)
            for f in files}


def _savefig(name):
    os.makedirs(CHARTS_DIR, exist_ok=True)
    path = os.path.join(CHARTS_DIR, name)
    plt.tight_layout()
    plt.savefig(path, dpi=150, bbox_inches="tight")
    plt.close()
    return path


def _safe_eval(obj):
    try:
        return ast.literal_eval(obj)
    except Exception:
        return []


def _extract_names(obj, limit=None):
    data = _safe_eval(obj) if isinstance(obj, str) else obj
    if not isinstance(data, list):
        return []
    names = [item["name"] for item in data if isinstance(item, dict) and "name" in item]
    return names[:limit] if limit else names


def generate_all_charts(movies_df, similarity_matrix, progress_cb=None):
    """Generate all EDA + model charts and save them to charts/."""
    BG    = "#0a0e17"
    CARD  = "#111520"
    GOLD  = "#f5a623"
    TEAL  = "#00d4aa"
    CORAL = "#e05a5a"
    sns.set_theme(style="dark", palette="deep")
    generated = []

    feat_path = os.path.join(ROOT, "datasets", "feature_engineered_movies.csv")
    raw_path  = os.path.join(ROOT, "datasets", "tmdb_5000_movies.csv")
    feat_df   = None
    if os.path.exists(feat_path):
        feat_df = pd.read_csv(feat_path)
    elif os.path.exists(raw_path):
        feat_df = pd.read_csv(raw_path)

    cinema_palette = [GOLD, TEAL, CORAL, "#a78bfa", "#38bdf8", "#fb7185",
                      "#34d399", "#fbbf24", "#60a5fa", "#f472b6"]

    def _style(fig, ax):
        fig.patch.set_facecolor(BG)
        ax.set_facecolor(CARD)
        ax.tick_params(colors=C_TEXT)
        for spine in ax.spines.values():
            spine.set_edgecolor("rgba(255,255,255,0.08)")

    # 1. Genre Distribution
    if progress_cb: progress_cb(10, "Genre distribution…")
    genres_flat = []
    if feat_df is not None and "genres" in feat_df.columns:
        for g in feat_df["genres"]:
            genres_flat.extend(_extract_names(g) if isinstance(g, str) else [])
    if not genres_flat and "tags" in movies_df.columns:
        for t in movies_df["tags"].dropna():
            genres_flat.extend(t.split()[:5])
    if genres_flat:
        top = Counter(genres_flat).most_common(15)
        labels_, values_ = zip(*top)
        fig, ax = plt.subplots(figsize=(12, 6))
        _style(fig, ax)
        palette = sns.color_palette([GOLD, TEAL, CORAL] * 6, len(labels_))
        bars = ax.barh(labels_, values_, color=palette, edgecolor="none")
        ax.invert_yaxis()
        ax.set_title("Top 15 Genres by Movie Count", fontsize=15, fontweight="bold", color=C_TEXT, pad=12)
        ax.set_xlabel("Number of Movies", color=C_MUTED)
        ax.bar_label(bars, padding=4, color=GOLD, fontsize=10, fontweight="bold")
        generated.append(_savefig("genre_distribution.png"))

    # 2. Vote Average Distribution
    if progress_cb: progress_cb(22, "Vote distribution…")
    if feat_df is not None and "vote_average" in feat_df.columns:
        vc = feat_df["vote_average"].dropna()
        vc = vc[vc > 0]
        if len(vc) > 0:
            fig, ax = plt.subplots(figsize=(10, 5))
            _style(fig, ax)
            ax.hist(vc, bins=30, color=TEAL, edgecolor=BG, alpha=0.9)
            ax.axvline(vc.mean(), color=GOLD, linewidth=2.5, linestyle="--",
                       label=f"Mean: {vc.mean():.2f}")
            ax.set_title("Vote Average Distribution", fontsize=15, fontweight="bold", color=C_TEXT, pad=12)
            ax.set_xlabel("Vote Average (0–10)", color=C_MUTED)
            ax.set_ylabel("Number of Movies", color=C_MUTED)
            ax.legend(facecolor="#1a1e2e", labelcolor=C_TEXT)
            generated.append(_savefig("vote_distribution.png"))

    # 3. Popularity vs Rating
    if progress_cb: progress_cb(34, "Popularity scatter…")
    if feat_df is not None and {"popularity", "vote_average", "vote_count"}.issubset(feat_df.columns):
        s = feat_df[["popularity", "vote_average", "vote_count"]].dropna()
        s = s[(s["vote_average"] > 0) & (s["popularity"] < 500)]
        fig, ax = plt.subplots(figsize=(11, 6))
        _style(fig, ax)
        sc = ax.scatter(s["popularity"], s["vote_average"],
                        c=s["vote_count"], cmap="YlOrRd", alpha=0.55, s=18)
        cb = plt.colorbar(sc, ax=ax)
        cb.set_label("Vote Count", color=C_MUTED)
        cb.ax.yaxis.set_tick_params(color=C_MUTED)
        ax.set_title("Popularity vs Vote Average", fontsize=15, fontweight="bold", color=C_TEXT, pad=12)
        ax.set_xlabel("Popularity", color=C_MUTED)
        ax.set_ylabel("Vote Average", color=C_MUTED)
        generated.append(_savefig("popularity_vs_rating.png"))

    # 4. Language Distribution
    if progress_cb: progress_cb(44, "Language pie…")
    if feat_df is not None and "original_language" in feat_df.columns:
        top_lang = feat_df["original_language"].value_counts().head(8)
        fig, ax = plt.subplots(figsize=(7, 7))
        fig.patch.set_facecolor(BG)
        ax.set_facecolor(BG)
        ax.pie(top_lang.values, labels=top_lang.index, autopct="%1.1f%%",
               colors=cinema_palette[:len(top_lang)], startangle=140, pctdistance=0.82,
               wedgeprops=dict(edgecolor=BG, linewidth=2))
        ax.set_title("Language Distribution (Top 8)", fontsize=14, fontweight="bold", color=C_TEXT, pad=14)
        generated.append(_savefig("language_distribution.png"))

    # 5. Movies Per Year
    if progress_cb: progress_cb(54, "Movies per year…")
    if feat_df is not None and "release_date" in feat_df.columns:
        years = pd.to_datetime(feat_df["release_date"], errors="coerce").dt.year
        yearly = years.dropna().astype(int).value_counts().sort_index()
        yearly = yearly[yearly.index >= 1970]
        fig, ax = plt.subplots(figsize=(12, 5))
        _style(fig, ax)
        ax.fill_between(yearly.index, yearly.values, alpha=0.25, color=GOLD)
        ax.plot(yearly.index, yearly.values, color=GOLD, linewidth=2.2)
        ax.set_title("Movies Released Per Year (1970+)", fontsize=15, fontweight="bold", color=C_TEXT, pad=12)
        ax.set_xlabel("Year", color=C_MUTED)
        ax.set_ylabel("Count", color=C_MUTED)
        generated.append(_savefig("movies_per_year.png"))

    # 6. Top Keywords
    if progress_cb: progress_cb(64, "Top keywords…")
    if "tags" in movies_df.columns:
        stopwords = {"the","a","an","of","in","and","to","is","it","for","with","on","at",
                     "by","from","as","this","that","are","was","his","her","who","they"}
        all_words = " ".join(movies_df["tags"].fillna("")).split()
        filtered  = [w for w in all_words if w not in stopwords and len(w) > 3]
        top_kw    = Counter(filtered).most_common(20)
        if top_kw:
            kw_labels, kw_values = zip(*top_kw)
            fig, ax = plt.subplots(figsize=(13, 5))
            _style(fig, ax)
            bar_colors = [TEAL if i % 2 == 0 else GOLD for i in range(len(kw_labels))]
            ax.bar(kw_labels, kw_values, color=bar_colors, edgecolor="none")
            ax.set_title("Top 20 Keywords in Tags", fontsize=15, fontweight="bold", color=C_TEXT, pad=12)
            ax.set_xlabel("Keyword", color=C_MUTED)
            ax.set_ylabel("Frequency", color=C_MUTED)
            plt.xticks(rotation=40, ha="right", color=C_TEXT, fontsize=9)
            generated.append(_savefig("top_keywords.png"))

    # 7. Similarity Heatmap
    if progress_cb: progress_cb(74, "Similarity heatmap…")
    n   = min(40, similarity_matrix.shape[0])
    sub = similarity_matrix[:n, :n]
    fig, ax = plt.subplots(figsize=(9, 7))
    fig.patch.set_facecolor(BG)
    sns.heatmap(sub, cmap="YlOrBr", ax=ax, xticklabels=False, yticklabels=False,
                cbar_kws={"label": "Cosine Similarity"})
    ax.set_title(f"Similarity Heatmap (first {n} movies)", fontsize=14, fontweight="bold",
                 color=C_TEXT, pad=12)
    generated.append(_savefig("similarity_heatmap.png"))

    # 8. Tag Length Distribution
    if progress_cb: progress_cb(82, "Tag lengths…")
    if "tags" in movies_df.columns:
        lengths = movies_df["tags"].fillna("").apply(lambda x: len(x.split()))
        fig, ax = plt.subplots(figsize=(10, 5))
        _style(fig, ax)
        ax.hist(lengths, bins=40, color=CORAL, edgecolor=BG, alpha=0.9)
        ax.axvline(lengths.mean(), color=GOLD, linewidth=2.5, linestyle="--",
                   label=f"Mean: {lengths.mean():.1f} words")
        ax.set_title("Tag Length Distribution", fontsize=14, fontweight="bold", color=C_TEXT, pad=12)
        ax.set_xlabel("Words in Tags", color=C_MUTED)
        ax.set_ylabel("Count", color=C_MUTED)
        ax.legend(facecolor="#1a1e2e", labelcolor=C_TEXT)
        generated.append(_savefig("tag_length_distribution.png"))

    # 9. Similarity Score Distribution
    if progress_cb: progress_cb(90, "Score distribution…")
    n2   = min(500, similarity_matrix.shape[0])
    sub2 = similarity_matrix[:n2, :n2]
    tri  = sub2[np.triu_indices(n2, k=1)]
    fig, ax = plt.subplots(figsize=(10, 5))
    _style(fig, ax)
    ax.hist(tri, bins=60, color=TEAL, edgecolor=BG, alpha=0.9)
    ax.set_title("Pairwise Cosine Similarity Distribution", fontsize=14, fontweight="bold",
                 color=C_TEXT, pad=12)
    ax.set_xlabel("Cosine Similarity", color=C_MUTED)
    ax.set_ylabel("Frequency", color=C_MUTED)
    generated.append(_savefig("similarity_score_distribution.png"))

    # 10. Top Similar Movies (to first movie)
    if progress_cb: progress_cb(96, "Top similar movies bar…")
    sample_idx = 0
    scores_top = sorted(enumerate(similarity_matrix[sample_idx]),
                        key=lambda x: x[1], reverse=True)[1:11]
    sim_titles = [movies_df.iloc[i]["title"] for i, _ in scores_top]
    sim_values = [v for _, v in scores_top]
    fig, ax = plt.subplots(figsize=(11, 6))
    _style(fig, ax)
    bar_c = [GOLD if i == 0 else TEAL for i in range(len(sim_titles))]
    bars = ax.barh(sim_titles[::-1], sim_values[::-1], color=bar_c[::-1], edgecolor="none")
    ax.set_xlim(0, 1)
    ax.set_title(f"Top 10 Similar to '{movies_df.iloc[sample_idx]['title']}'",
                 fontsize=13, fontweight="bold", color=C_TEXT, pad=12)
    ax.set_xlabel("Cosine Similarity", color=C_MUTED)
    ax.bar_label(bars, fmt="%.3f", color=GOLD, padding=4, fontweight="bold")
    generated.append(_savefig("top_similar_movies.png"))

    if progress_cb: progress_cb(100, "Done!")
    return generated


# ----------------------------------------------------------
# SIDEBAR
# ----------------------------------------------------------

with st.sidebar:
    st.markdown(f"""
    <div style="text-align:center; padding: 0.5rem 0 1rem;">
        <div style="font-size:2.4rem;">🎬</div>
        <div style="font-size:1.25rem; font-weight:900; color:{C_ACCENT1}; letter-spacing:1px;">
            Movie Recommender
        </div>
        <div style="font-size:0.75rem; color:{C_MUTED}; margin-top:2px;">
            AI · NLP · Content-Based
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="gold-divider"></div>', unsafe_allow_html=True)

    # Model status
    movies_loaded, _ = load_models()
    if movies_loaded is not None:
        st.success(f"✅ {len(movies_loaded):,} movies loaded")
    else:
        st.error("⚠ Model not found. Run `src/train.py`.")

    st.markdown('<div class="gold-divider"></div>', unsafe_allow_html=True)

    # Tech stack
    st.markdown(f'<div class="section-label">Powered By</div>', unsafe_allow_html=True)
    tech_items = [
        ("🐍", "Python 3"),
        ("📐", "CountVectorizer"),
        ("📏", "Cosine Similarity"),
        ("🧠", "NLP / NLTK"),
        ("📊", "Matplotlib / Seaborn"),
        ("🚀", "Streamlit"),
    ]
    for icon, label in tech_items:
        st.markdown(
            f'<div style="padding:3px 0; color:{C_TEXT}; font-size:0.88rem;">'
            f'{icon} &nbsp; {label}</div>',
            unsafe_allow_html=True,
        )

    st.markdown('<div class="gold-divider"></div>', unsafe_allow_html=True)

    # Dataset info
    st.markdown(f'<div class="section-label">Dataset</div>', unsafe_allow_html=True)
    st.markdown(
        f'<div style="color:{C_MUTED}; font-size:0.85rem;">TMDB 5000 Movie Dataset</div>',
        unsafe_allow_html=True,
    )

    st.markdown('<div class="gold-divider"></div>', unsafe_allow_html=True)

    # ── About section (moved from tab) ──
    with st.expander("ℹ️  About This Project", expanded=False):
        st.markdown(f"""
**Movie Recommendation System**

An end-to-end AI-powered content-based filtering system.

**How it Works**

| Step | Detail |
|------|--------|
| Data | TMDB 5000 Dataset |
| Clean | Merge + parse JSON |
| Features | Genres, Cast, Keywords, Director |
| NLP | Unified "tags" string |
| Vectorize | CountVectorizer 5k-dim |
| Similarity | Cosine Similarity |
| Recommend | Rank top-N |

**Project Structure**
```
├── app.py           ← Entry point
├── src/
│   ├── preprocessing.py
│   ├── train.py
│   └── predict.py
├── model/           ← pkl files
├── charts/          ← Visualisations
└── datasets/        ← Raw CSVs
```

**Deployment:** Streamlit Community Cloud
""")

    st.markdown('<div class="gold-divider"></div>', unsafe_allow_html=True)
    st.caption(
        f'<div style="text-align:center; color:{C_MUTED}; font-size:0.75rem;">'
        "Built with ❤️ by Ishan<br>B.Tech CSE · AI/ML Portfolio"
        "</div>",
        unsafe_allow_html=True,
    )


# ----------------------------------------------------------
# MAIN CONTENT
# ----------------------------------------------------------

st.markdown('<div class="hero-title">🎬 Movie Recommendation System</div>', unsafe_allow_html=True)
st.markdown(
    f'<div class="hero-sub">AI-powered &nbsp;·&nbsp; Content-Based Filtering &nbsp;·&nbsp; '
    f'NLP + Cosine Similarity</div>',
    unsafe_allow_html=True,
)

movies, similarity = load_models()

if movies is None:
    st.error(
        "**Model files not found.**\n\n"
        "Please run:\n"
        "```bash\n"
        "python src/preprocessing.py\n"
        "python src/train.py\n"
        "```"
    )
    st.stop()

# Load genre mapping once
genre_map = load_genre_map_from_csv()
if genre_map is None:
    genre_map = extract_genres_from_tags(movies)

available_genres = get_available_genres(genre_map)

# ----------------------------------------------------------
# TABS  (Recommend | Genre Search | Analytics)
# ----------------------------------------------------------

tab_recommend, tab_genre, tab_charts = st.tabs([
    "🏠  Recommend", "🎭  Genre Search", "📊  Analytics"
])


# ══════════════════════════════════════════════════════════
# TAB 1 ── MOVIE-BASED RECOMMENDATION
# ══════════════════════════════════════════════════════════
with tab_recommend:

    st.markdown(f'<div class="section-label">Select a Movie</div>', unsafe_allow_html=True)

    col_left, col_right = st.columns([4, 1])
    with col_left:
        movie_name = st.selectbox(
            "Movie",
            movies["title"].sort_values().values,
            label_visibility="collapsed",
            key="movie_select",
        )
    with col_right:
        top_n = st.number_input("Results", min_value=1, max_value=20, value=5, step=1,
                                key="top_n_movie")

    st.markdown("")
    _, btn_col, _ = st.columns([1, 2, 1])
    with btn_col:
        clicked = st.button("🎥  Get Recommendations", use_container_width=True,
                            key="btn_recommend")

    st.markdown('<div class="gold-divider"></div>', unsafe_allow_html=True)

    if clicked:
        with st.spinner("Finding similar movies…"):
            results = recommend(movie_name, movies, similarity, top_n=int(top_n))

        if not results:
            st.warning("No recommendations found for this title.")
        else:
            # Show genres of selected movie
            sel_genres = genre_map.get(movie_name, [])
            if sel_genres:
                genre_html = "".join(
                    f'<span class="rec-genre-tag">{g}</span>' for g in sel_genres
                )
                st.markdown(
                    f'<div style="margin-bottom:0.5rem;">'
                    f'<span style="color:{C_MUTED}; font-size:0.8rem;">Selected: </span>'
                    f'<strong style="color:{C_ACCENT1};">{movie_name}</strong> '
                    f'&nbsp;{genre_html}</div>',
                    unsafe_allow_html=True,
                )

            st.markdown(
                f'<div style="font-size:1.15rem; font-weight:700; color:{C_ACCENT2}; '
                f'margin-bottom:1rem;">🌟 Top {len(results)} Similar Movies</div>',
                unsafe_allow_html=True,
            )

            for rank, (title, score) in enumerate(results, start=1):
                pct       = int(score * 100)
                genres_   = genre_map.get(title, [])
                genre_html = "".join(f'<span class="rec-genre-tag">{g}</span>' for g in genres_)
                st.markdown(f"""
                <div class="rec-card">
                    <span class="rec-rank">#{rank}</span>
                    <div class="rec-title">{title}</div>
                    <div style="margin: 4px 0 2px 0;">{genre_html}</div>
                    <div class="rec-score">Similarity: {score:.4f} &nbsp;|&nbsp; {pct}%</div>
                    <div class="score-bar-wrap">
                        <div class="score-bar-fill" style="width:{pct}%"></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

            # Mini bar chart
            titles_list = [t for t, _ in results]
            scores_list = [s for _, s in results]

            fig, ax = plt.subplots(figsize=(8, max(3, len(results) * 0.6)))
            fig.patch.set_facecolor(C_BG)
            ax.set_facecolor("#111520")
            cmap   = plt.get_cmap("YlOrBr")
            colors = [cmap(0.3 + 0.6 * i / max(len(scores_list) - 1, 1))
                      for i in range(len(scores_list))]
            bars = ax.barh(titles_list[::-1], scores_list[::-1],
                           color=colors[::-1], edgecolor="none", height=0.6)
            ax.set_xlim(0, max(scores_list) * 1.15)
            ax.tick_params(colors=C_TEXT, labelsize=9)
            ax.set_xlabel("Cosine Similarity", color=C_MUTED, fontsize=10)
            ax.set_title("Recommendation Scores", color=C_ACCENT1,
                         fontweight="bold", fontsize=12)
            
            ax.bar_label(bars, fmt="%.3f", color=C_ACCENT1, padding=4,
                         fontweight="bold", fontsize=9)
            st.pyplot(fig, use_container_width=True)

    else:
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("🎞 Total Movies", f"{len(movies):,}")
        with col2:
            st.metric("🧮 Algorithm", "Cosine Similarity")
        with col3:
            st.metric("🎭 Genres Available", str(len(available_genres)))
        st.info("👆 Select a movie above and click **Get Recommendations** to start.")


# ══════════════════════════════════════════════════════════
# TAB 2 ── GENRE-BASED SEARCH
# ══════════════════════════════════════════════════════════
with tab_genre:

    st.markdown(
        f'<div style="font-size:1.05rem; color:{C_MUTED}; margin-bottom:1rem;">'
        "Browse movies by genre — ranked by how similar they are to other movies in the same genre."
        "</div>",
        unsafe_allow_html=True,
    )

    if not available_genres:
        st.warning(
            "Genre data not available. Make sure `datasets/tmdb_5000_movies.csv` "
            "or `datasets/feature_engineered_movies.csv` is present."
        )
    else:
        # Genre grid pills (for display)
        st.markdown(f'<div class="section-label">Available Genres ({len(available_genres)})</div>',
                    unsafe_allow_html=True)
        pill_html = "".join(
            f'<span class="genre-pill">{g}</span>' for g in available_genres
        )
        st.markdown(f'<div style="margin-bottom:1.2rem;">{pill_html}</div>',
                    unsafe_allow_html=True)

        st.markdown('<div class="gold-divider"></div>', unsafe_allow_html=True)

        # Controls
        col_g1, col_g2, col_g3 = st.columns([3, 1, 1])
        with col_g1:
            selected_genre = st.selectbox(
                "Choose a Genre",
                available_genres,
                label_visibility="collapsed",
                key="genre_select",
            )
        with col_g2:
            genre_top_n = st.number_input(
                "Results", min_value=3, max_value=30, value=10, step=1, key="top_n_genre"
            )
        with col_g3:
            st.markdown("")
            genre_clicked = st.button(
                "🎭  Browse Genre", use_container_width=True, key="btn_genre"
            )

        st.markdown('<div class="gold-divider"></div>', unsafe_allow_html=True)

        if genre_clicked:
            with st.spinner(f"Finding top {genre_top_n} **{selected_genre}** movies…"):
                genre_results = recommend_by_genre(
                    selected_genre, movies, similarity, genre_map, top_n=int(genre_top_n)
                )

            if not genre_results:
                st.warning(f"No movies found for genre **{selected_genre}**.")
            else:
                total_in_genre = sum(
                    1 for genres in genre_map.values()
                    if any(g.lower() == selected_genre.lower() for g in genres)
                )
                st.markdown(
                    f'<div style="font-size:1.15rem; font-weight:700; color:{C_ACCENT2}; '
                    f'margin-bottom:1rem;">'
                    f'🎭 Top {len(genre_results)} <span style="color:{C_ACCENT1};">'
                    f'{selected_genre}</span> Movies '
                    f'<span style="color:{C_MUTED}; font-size:0.85rem; font-weight:400;">'
                    f'({total_in_genre} total in genre)</span></div>',
                    unsafe_allow_html=True,
                )

                # Two-column card layout for genre results
                mid = (len(genre_results) + 1) // 2
                left_results  = genre_results[:mid]
                right_results = genre_results[mid:]

                col_l, col_r = st.columns(2)
                for col, results_half in [(col_l, left_results), (col_r, right_results)]:
                    with col:
                        for rank, (title, score) in enumerate(results_half, start=1):
                            real_rank = (genre_results.index((title, score)) + 1)
                            pct       = int(score * 100)
                            genres_   = genre_map.get(title, [])
                            gh = "".join(f'<span class="rec-genre-tag">{g}</span>'
                                         for g in genres_)
                            st.markdown(f"""
                            <div class="rec-card">
                                <span class="rec-rank">#{real_rank}</span>
                                <div class="rec-title">{title}</div>
                                <div style="margin:4px 0 2px 0;">{gh}</div>
                                <div class="rec-score">Genre Score: {score:.4f}</div>
                                <div class="score-bar-wrap">
                                    <div class="score-bar-fill" style="width:{pct}%"></div>
                                </div>
                            </div>
                            """, unsafe_allow_html=True)

                # Genre bar chart
                g_titles = [t for t, _ in genre_results]
                g_scores = [s for _, s in genre_results]

                fig, ax = plt.subplots(figsize=(10, max(4, len(g_titles) * 0.55)))
                fig.patch.set_facecolor(C_BG)
                ax.set_facecolor("#111520")
                bar_colors = [C_ACCENT1 if i == 0 else C_ACCENT2 for i in range(len(g_titles))]
                bars = ax.barh(g_titles[::-1], g_scores[::-1],
                               color=bar_colors[::-1], edgecolor="none", height=0.65)
                ax.set_title(f"Top {selected_genre} Movies — Genre Cohesion Score",
                             color=C_ACCENT1, fontweight="bold", fontsize=12)
                ax.set_xlabel("Mean Intra-Genre Cosine Similarity", color=C_MUTED, fontsize=10)
                ax.tick_params(colors=C_TEXT, labelsize=9)
                for spine in ax.spines.values():
                    spine.set_edgecolor("rgba(255,255,255,0.06)")
                ax.bar_label(bars, fmt="%.4f", color=C_ACCENT1, padding=4,
                             fontweight="bold", fontsize=9)
                st.pyplot(fig, use_container_width=True)

        else:
            # Stats overview grid
            st.markdown(
                f'<div class="section-label">Genre Overview</div>', unsafe_allow_html=True
            )
            # Count movies per genre and show top ones
            genre_counts = Counter()
            for genres in genre_map.values():
                for g in genres:
                    genre_counts[g] += 1

            top_genres = genre_counts.most_common(9)
            cols_ = st.columns(3)
            for idx, (genre, count) in enumerate(top_genres):
                with cols_[idx % 3]:
                    st.metric(f"🎭 {genre}", f"{count} movies")

            st.markdown("")
            st.info("👆 Select a genre above and click **Browse Genre** to explore.")


# ══════════════════════════════════════════════════════════
# TAB 3 ── ANALYTICS / CHARTS
# ══════════════════════════════════════════════════════════
with tab_charts:
    st.markdown(f'<div class="section-label">Dataset & Model Analytics</div>', unsafe_allow_html=True)

    _, gen_col, _ = st.columns([1, 2, 1])
    with gen_col:
        gen_btn = st.button(
            "⚡  Generate & Save All Charts", use_container_width=True, key="gen_charts_btn"
        )

    if gen_btn:
        prog_bar = st.progress(0, text="Starting chart generation…")

        def _prog(pct, msg):
            prog_bar.progress(pct, text=msg)

        with st.spinner("Generating charts — this may take a moment…"):
            paths = generate_all_charts(movies, similarity, progress_cb=_prog)

        prog_bar.empty()
        st.success(f"✅ {len(paths)} charts generated and saved to `charts/`")
        st.rerun()

    charts = get_charts()
    st.markdown('<div class="gold-divider"></div>', unsafe_allow_html=True)

    if not charts:
        st.info(
            "Click **Generate & Save All Charts** above to create all analytics visualisations.\n\n"
            "Charts will be saved to the `charts/` folder and displayed here."
        )
    else:
        st.markdown(
            f'<div style="color:{C_MUTED}; font-size:0.9rem; margin-bottom:1rem;">'
            f"Showing <strong style='color:{C_ACCENT1};'>{len(charts)}</strong> analytics charts. "
            "Click the button above to regenerate.</div>",
            unsafe_allow_html=True,
        )

        chart_items = list(charts.items())
        for i in range(0, len(chart_items), 2):
            cols = st.columns(2)
            for j, (label, path) in enumerate(chart_items[i: i + 2]):
                with cols[j]:
                    st.markdown(
                        f'<div style="font-size:0.82rem; font-weight:700; color:{C_ACCENT1}; '
                        f'letter-spacing:0.5px; text-transform:uppercase; margin-bottom:6px;">'
                        f'{label}</div>',
                        unsafe_allow_html=True,
                    )
                    st.image(path, use_container_width=True)
            st.markdown("")


# ----------------------------------------------------------
# FOOTER
# ----------------------------------------------------------

st.markdown('<div class="gold-divider"></div>', unsafe_allow_html=True)
st.markdown(
    f'<div style="text-align:center; color:{C_MUTED}; font-size:0.8rem; padding-bottom:1rem;">'
    "🎬 Movie Recommendation System &nbsp;·&nbsp; Python · Scikit-Learn · Streamlit"
    f"&nbsp;·&nbsp; <span style='color:{C_ACCENT1};'>© 2024 Ishan</span></div>",
    unsafe_allow_html=True,
)
