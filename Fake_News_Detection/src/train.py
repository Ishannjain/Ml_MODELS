# ==========================================================
# train.py
# Fake News Detection – Feature Engineering, Model Training
# & Evaluation
# ==========================================================

import os

import joblib
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression, PassiveAggressiveClassifier
from sklearn.metrics import (
    ConfusionMatrixDisplay,
    accuracy_score,
    classification_report,
    f1_score,
    precision_score,
    recall_score,
)
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import LinearSVC
from sklearn.tree import DecisionTreeClassifier

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
BASE_DIR    = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATASET_DIR = os.path.join(BASE_DIR, "dataset")
MODEL_DIR   = os.path.join(BASE_DIR, "model")
CHARTS_DIR  = os.path.join(BASE_DIR, "charts")

PROCESSED_CSV     = os.path.join(DATASET_DIR, "processed_fake_news.csv")
TFIDF_PATH        = os.path.join(MODEL_DIR, "tfidf_vectorizer.pkl")
BEST_MODEL_PATH   = os.path.join(MODEL_DIR, "fake_news_model.pkl")
CONF_MATRIX_PATH  = os.path.join(CHARTS_DIR, "confusion_matrix.png")


# ---------------------------------------------------------------------------
# Main pipeline
# ---------------------------------------------------------------------------
def run():
    # ------------------------------------------------------------------
    # 1. Load processed dataset
    # ------------------------------------------------------------------
    print("=" * 60)
    print("Loading Processed Dataset…")
    print("=" * 60)

    df = pd.read_csv(PROCESSED_CSV)
    print(f"Dataset Shape : {df.shape}")

    # ------------------------------------------------------------------
    # 2. Features & target
    # ------------------------------------------------------------------
    X = df["text"].fillna("").astype(str)   # ← fixes np.nan ValueError
    y = df["label"]

    print("\n" + "=" * 60)
    print("Feature & Target Created")
    print("=" * 60)
    print(f"Number of News Articles : {len(X)}")
    print(f"Target Shape : {y.shape}")
    print("\nTarget Distribution")
    print(y.value_counts())

    # ------------------------------------------------------------------
    # 3. TF-IDF vectorisation
    # ------------------------------------------------------------------
    tfidf = TfidfVectorizer(
        stop_words="english",
        max_df=0.7,
        min_df=2,
        max_features=5000,
    )
    X_tfidf = tfidf.fit_transform(X)

    print("\n" + "=" * 60)
    print("TF-IDF Vectorization Completed")
    print("=" * 60)
    print(f"Feature Matrix Shape : {X_tfidf.shape}")

    # ------------------------------------------------------------------
    # 4. Train / test split
    # ------------------------------------------------------------------
    X_train, X_test, y_train, y_test = train_test_split(
        X_tfidf, y,
        test_size=0.20,
        random_state=42,
        stratify=y,
    )

    print("\n" + "=" * 60)
    print("Train Test Split Completed")
    print("=" * 60)
    print(f"Training Samples : {X_train.shape}")
    print(f"Testing Samples  : {X_test.shape}")

    # ------------------------------------------------------------------
    # 5. Save TF-IDF vectoriser
    # ------------------------------------------------------------------
    os.makedirs(MODEL_DIR, exist_ok=True)
    joblib.dump(tfidf, TFIDF_PATH)

    print("\n" + "=" * 60)
    print("TF-IDF Vectorizer Saved Successfully")
    print("=" * 60)
    print(f"Saved File : {TFIDF_PATH}")

    # ------------------------------------------------------------------
    # 6. Train & evaluate all models
    # ------------------------------------------------------------------
    models = {
        "Logistic Regression":      LogisticRegression(max_iter=1000),
        "Multinomial Naive Bayes":  MultinomialNB(),
        "Decision Tree":            DecisionTreeClassifier(random_state=42),
        "Random Forest":            RandomForestClassifier(n_estimators=100, random_state=42),
        "Passive Aggressive":       PassiveAggressiveClassifier(max_iter=1000, random_state=42),
        "Linear SVM":               LinearSVC(random_state=42),
    }

    results        = []
    trained_models = {}

    print("\n" + "=" * 60)
    print("Models Initialized Successfully")
    print("=" * 60)

    for name, model in models.items():
        print("\n" + "=" * 60)
        print(f"Training {name}")
        print("=" * 60)

        model.fit(X_train, y_train)
        prediction = model.predict(X_test)

        accuracy  = accuracy_score(y_test, prediction)
        precision = precision_score(y_test, prediction)
        recall    = recall_score(y_test, prediction)
        f1        = f1_score(y_test, prediction)

        results.append({
            "Model":     name,
            "Accuracy":  accuracy,
            "Precision": precision,
            "Recall":    recall,
            "F1 Score":  f1,
        })
        trained_models[name] = model

        print(f"Accuracy : {accuracy:.4f}")
        print(f"Precision: {precision:.4f}")
        print(f"Recall   : {recall:.4f}")
        print(f"F1 Score : {f1:.4f}")

    print("\n" + "=" * 60)
    print("All Models Trained Successfully")
    print("=" * 60)

    # ------------------------------------------------------------------
    # 7. Compare models
    # ------------------------------------------------------------------
    results_df = (
        pd.DataFrame(results)
        .sort_values(by=["Accuracy", "F1 Score"], ascending=False)
        .reset_index(drop=True)
    )

    print("\n" + "=" * 60)
    print("Model Comparison")
    print("=" * 60)
    print(results_df.to_string(index=False))

    # ------------------------------------------------------------------
    # 8. Best model evaluation
    # ------------------------------------------------------------------
    best_model_name = results_df.iloc[0]["Model"]
    best_model      = trained_models[best_model_name]
    prediction      = best_model.predict(X_test)

    print("\n" + "=" * 60)
    print(f"Best Model : {best_model_name}")
    print("=" * 60)
    print(classification_report(y_test, prediction))

    os.makedirs(CHARTS_DIR, exist_ok=True)
    ConfusionMatrixDisplay.from_predictions(y_test, prediction, cmap="Blues")
    plt.title(f"Confusion Matrix - {best_model_name}")
    plt.savefig(CONF_MATRIX_PATH, dpi=300)
    plt.show()

    # ------------------------------------------------------------------
    # 9. Save best model
    # ------------------------------------------------------------------
    joblib.dump(best_model, BEST_MODEL_PATH)

    print("\n" + "=" * 60)
    print("Best Model Saved Successfully")
    print("=" * 60)
    print(f"Model Name  : {best_model_name}")
    print(f"Saved File  : {BEST_MODEL_PATH}")

    # ------------------------------------------------------------------
    # 10. Final summary
    # ------------------------------------------------------------------
    print("\n" + "=" * 60)
    print("FAKE NEWS DETECTION MODEL TRAINING COMPLETED")
    print("=" * 60)
    print(f"""
Selected Model : {best_model_name}
Dataset        : Fake & Real News
Vectorizer     : TF-IDF
Model Saved    : fake_news_model.pkl
Vectorizer     : tfidf_vectorizer.pkl
""")
    print(results_df.to_string(index=False))


if __name__ == "__main__":
    run()
