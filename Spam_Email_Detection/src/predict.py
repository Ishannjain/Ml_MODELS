# ==========================================================
# PHASE 5 : HYPERPARAMETER TUNING
# ==========================================================

import os

import joblib
import matplotlib
matplotlib.use("Agg")          # non-interactive backend — no blocking plt.show()
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
)
from sklearn.naive_bayes import MultinomialNB

# ==========================================================
# Resolve Paths
# ==========================================================

BASE_DIR    = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATASET_PATH = os.path.join(BASE_DIR, "dataset", "preprocessed_spam.csv")
MODEL_DIR   = os.path.join(BASE_DIR, "model")
CHARTS_DIR  = os.path.join(BASE_DIR, "charts")
os.makedirs(CHARTS_DIR, exist_ok=True)

# ==========================================================
# Load Dataset
# ==========================================================

df = pd.read_csv(DATASET_PATH)

print("=" * 60)
print("Dataset Loaded Successfully")
print("=" * 60)
print(df.head())

# ==========================================================
# Load TF-IDF Vectorizer
# ==========================================================

tfidf = joblib.load(os.path.join(MODEL_DIR, "tfidf.pkl"))

# ==========================================================
# Prepare Features  (fillna guards against empty rows)
# ==========================================================

X = tfidf.transform(df["Transformed_Message"].fillna("")).toarray()

# ==========================================================
# Prepare Labels  (direct map — no LabelEncoder needed)
# ==========================================================

y = df["Label"].map({"ham": 0, "spam": 1}).fillna(0).astype(int).values

print("\nFeature Matrix Shape :", X.shape)
print("Target Shape         :", y.shape)

# ==========================================================
# Train-Test Split
# ==========================================================

X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

print("\nTraining Samples :", len(X_train))
print("Testing  Samples :", len(X_test))

# ==========================================================
# Model  &  Hyperparameter Grid
# ==========================================================

model = MultinomialNB()

params = {
    "alpha": [0.01, 0.05, 0.1, 0.5, 1, 2, 5]
}

# ==========================================================
# Grid Search CV
# ==========================================================

grid = GridSearchCV(
    estimator=model,
    param_grid=params,
    cv=5,
    scoring="accuracy",
    n_jobs=-1
)

print("\n")
print("=" * 60)
print("Searching Best Parameters...")
print("=" * 60)

grid.fit(X_train, y_train)

print("\nBest Parameters          :", grid.best_params_)
print("Best CV Accuracy Score   :", round(grid.best_score_, 4))

# ==========================================================
# Best Estimator  &  Predictions
# ==========================================================

best_model = grid.best_estimator_

y_pred = best_model.predict(X_test)

# ==========================================================
# Evaluation Metrics
# ==========================================================

accuracy  = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred, zero_division=0)
recall    = recall_score(y_test, y_pred, zero_division=0)
f1        = f1_score(y_test, y_pred, zero_division=0)

print("\n")
print("=" * 60)
print("FINAL TUNED MODEL PERFORMANCE")
print("=" * 60)
print("Accuracy  :", round(accuracy,  4))
print("Precision :", round(precision, 4))
print("Recall    :", round(recall,    4))
print("F1 Score  :", round(f1,        4))

# ==========================================================
# Classification Report
# ==========================================================

print("\n")
print("=" * 60)
print("CLASSIFICATION REPORT")
print("=" * 60)
print(classification_report(y_test, y_pred, zero_division=0))

# ==========================================================
# Confusion Matrix  →  saved to charts/
# ==========================================================

cm = confusion_matrix(y_test, y_pred)

print("Confusion Matrix\n")
print(cm)

plt.figure(figsize=(6, 5))
sns.heatmap(cm, annot=True, fmt="d", cmap="Blues",
            xticklabels=["Ham", "Spam"],
            yticklabels=["Ham", "Spam"])
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.title("Confusion Matrix – Tuned Naive Bayes")
plt.tight_layout()

cm_path = os.path.join(CHARTS_DIR, "tuned_confusion_matrix.png")
plt.savefig(cm_path)
plt.close()
print(f"\nConfusion matrix saved to: {cm_path}")

# ==========================================================
# Save Tuned Model
# (saved separately so it doesn't overwrite the best
#  multi-model result produced by train.py)
# ==========================================================

tuned_model_path = os.path.join(MODEL_DIR, "spam_model_tuned.pkl")

joblib.dump(best_model, tuned_model_path)

print("\n")
print("=" * 60)
print("Tuned Model Saved Successfully")
print("=" * 60)
print("Saved File :", tuned_model_path)