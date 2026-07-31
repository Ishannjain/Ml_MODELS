# ==========================================================
# predict.py
# Fake News Detection – Single-article inference helper
# ==========================================================

import os
import re
import string

import joblib
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

# ---------------------------------------------------------------------------
# Paths (resolved relative to this file so the script works from anywhere)
# ---------------------------------------------------------------------------
BASE_DIR  = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_DIR = os.path.join(BASE_DIR, "model")

TFIDF_PATH      = os.path.join(MODEL_DIR, "tfidf_vectorizer.pkl")
MODEL_PATH      = os.path.join(MODEL_DIR, "fake_news_model.pkl")

# ---------------------------------------------------------------------------
# Text-cleaning helpers (must mirror preprocessing.py exactly)
# ---------------------------------------------------------------------------
nltk.download("stopwords", quiet=True)
_stop_words = set(stopwords.words("english"))
_stemmer    = PorterStemmer()


def clean_text(text: str) -> str:
    """Apply the same cleaning pipeline used during training."""
    text = str(text).lower()
    text = re.sub(r"http\S+", "", text)
    text = re.sub(r"www\S+",  "", text)
    text = re.sub(r"<.*?>",   "", text)
    text = re.sub(r"\d+",     "", text)
    text = text.translate(str.maketrans("", "", string.punctuation))
    words = [
        _stemmer.stem(w)
        for w in text.split()
        if w not in _stop_words
    ]
    return " ".join(words)


# ---------------------------------------------------------------------------
# Model loading (lazy, cached at module level)
# ---------------------------------------------------------------------------
_tfidf = None
_model = None


def _load_artifacts():
    global _tfidf, _model
    if _tfidf is None or _model is None:
        if not os.path.exists(TFIDF_PATH):
            raise FileNotFoundError(
                f"TF-IDF vectoriser not found at: {TFIDF_PATH}\n"
                "Please run  src/train.py  first."
            )
        if not os.path.exists(MODEL_PATH):
            raise FileNotFoundError(
                f"Trained model not found at: {MODEL_PATH}\n"
                "Please run  src/train.py  first."
            )
        _tfidf = joblib.load(TFIDF_PATH)
        _model = joblib.load(MODEL_PATH)


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------
def predict(text: str) -> dict:
    """
    Predict whether a news article is real or fake.

    Parameters
    ----------
    text : str
        Raw article text (title + body, or just body).

    Returns
    -------
    dict with keys:
        label       – 0 (Fake) or 1 (Real)
        prediction  – "FAKE" or "REAL"
        confidence  – float 0-100 (probability of the predicted class)
                      For models that don't support predict_proba the value
                      is None.
    """
    _load_artifacts()

    cleaned   = clean_text(text)
    vectorised = _tfidf.transform([cleaned])

    label = int(_model.predict(vectorised)[0])

    # Attempt probability estimate (not all sklearn models support it)
    confidence = None
    if hasattr(_model, "predict_proba"):
        proba      = _model.predict_proba(vectorised)[0]
        confidence = round(float(proba[label]) * 100, 2)
    elif hasattr(_model, "decision_function"):
        # Convert decision-function score to a rough 0-100 scale
        score      = _model.decision_function(vectorised)[0]
        # sigmoid approximation
        import math
        sigmoid    = 1 / (1 + math.exp(-score))
        confidence = round(float(sigmoid) * 100, 2)

    return {
        "label":      label,
        "prediction": "REAL" if label == 1 else "FAKE",
        "confidence": confidence,
    }


# ---------------------------------------------------------------------------
# CLI convenience
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python predict.py \"<article text>\"")
        sys.exit(1)

    article = " ".join(sys.argv[1:])
    result  = predict(article)

    print("=" * 60)
    print(f"Prediction  : {result['prediction']}")
    if result["confidence"] is not None:
        print(f"Confidence  : {result['confidence']:.2f}%")
    print("=" * 60)
