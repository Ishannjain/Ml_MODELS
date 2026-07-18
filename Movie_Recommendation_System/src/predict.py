# ==========================================================
# MOVIE RECOMMENDATION SYSTEM
# PREDICTION MODULE
# ==========================================================

import os
import pickle
import pandas as pd

# ----------------------------------------------------------
# PATHS
# ----------------------------------------------------------

BASE_DIR  = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_DIR = os.path.join(BASE_DIR, "model")


# ----------------------------------------------------------
# LOAD ARTIFACTS
# ----------------------------------------------------------

def load_artifacts():
    """Load the serialised movies DataFrame and similarity matrix."""
    movies_path = os.path.join(MODEL_DIR, "movies.pkl")
    sim_path    = os.path.join(MODEL_DIR, "similarity.pkl")
    vec_path    = os.path.join(MODEL_DIR, "vectorizer.pkl")

    for p in [movies_path, sim_path, vec_path]:
        if not os.path.exists(p):
            raise FileNotFoundError(
                f"Model file not found: {p}\n"
                "Run src/train.py to generate the model."
            )

    with open(movies_path, "rb") as f:
        movies = pickle.load(f)

    with open(sim_path, "rb") as f:
        similarity = pickle.load(f)

    with open(vec_path, "rb") as f:
        vectorizer = pickle.load(f)

    return movies, similarity, vectorizer


# ----------------------------------------------------------
# CORE RECOMMENDATION LOGIC
# ----------------------------------------------------------

def recommend(movie_title: str, movies: pd.DataFrame, similarity, top_n: int = 5):
    """
    Return the top-N most similar movie titles for a given movie.

    Parameters
    ----------
    movie_title : str
        Exact title as it appears in the dataset.
    movies      : pd.DataFrame
        DataFrame with at least 'title' column (loaded from movies.pkl).
    similarity  : np.ndarray
        Pre-computed cosine similarity matrix.
    top_n       : int
        Number of recommendations to return (default 5).

    Returns
    -------
    list[str]
        List of recommended movie titles.
    """
    matches = movies[movies["title"] == movie_title]
    if matches.empty:
        raise ValueError(f"Movie not found in dataset: '{movie_title}'")

    movie_index = matches.index[0]
    distances   = similarity[movie_index]

    # Sort by similarity score (descending), skip the movie itself (index 0)
    ranked = sorted(enumerate(distances), key=lambda x: x[1], reverse=True)[1: top_n + 1]

    return [movies.iloc[i]["title"] for i, _ in ranked]


def recommend_with_scores(movie_title: str, movies: pd.DataFrame, similarity, top_n: int = 5):
    """
    Same as `recommend` but also returns similarity scores.

    Returns
    -------
    list[tuple[str, float]]
        List of (title, score) tuples.
    """
    matches = movies[movies["title"] == movie_title]
    if matches.empty:
        raise ValueError(f"Movie not found in dataset: '{movie_title}'")

    movie_index = matches.index[0]
    distances   = similarity[movie_index]

    ranked = sorted(enumerate(distances), key=lambda x: x[1], reverse=True)[1: top_n + 1]

    return [(movies.iloc[i]["title"], round(float(score), 4)) for i, score in ranked]


# ----------------------------------------------------------
# SEARCH HELPER
# ----------------------------------------------------------

def search_movies(query: str, movies: pd.DataFrame, max_results: int = 10):
    """
    Case-insensitive substring search over movie titles.

    Returns
    -------
    list[str]
    """
    q = query.strip().lower()
    if not q:
        return []
    mask = movies["title"].str.lower().str.contains(q, na=False)
    return movies[mask]["title"].head(max_results).tolist()


# ----------------------------------------------------------
# CLI DEMO
# ----------------------------------------------------------

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Movie Recommendation CLI")
    parser.add_argument("movie", nargs="?", default="Avatar",
                        help="Movie title to get recommendations for")
    parser.add_argument("--top", type=int, default=5,
                        help="Number of recommendations (default: 5)")
    args = parser.parse_args()

    movies, similarity, _ = load_artifacts()

    print(f"\n🎬 Recommendations for: '{args.movie}'\n" + "─" * 45)
    try:
        results = recommend_with_scores(args.movie, movies, similarity, top_n=args.top)
        for rank, (title, score) in enumerate(results, start=1):
            print(f"  {rank}. {title:<45}  (score: {score:.4f})")
    except ValueError as e:
        print(f"  ⚠  {e}")
        suggestions = search_movies(args.movie, movies)
        if suggestions:
            print("\n  Did you mean one of these?")
            for s in suggestions:
                print(f"    – {s}")
