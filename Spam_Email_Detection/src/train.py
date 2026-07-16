# ==========================================================
# PHASE 4 : MODEL TRAINING & EVALUATION
# ==========================================================

# Import Libraries
import os

import joblib
import matplotlib
matplotlib.use("Agg")          # non-interactive — saves files, no blocking show()
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
)
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier

# ==========================================================
# Resolve Paths
# ==========================================================

BASE_DIR     = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATASET_PATH = os.path.join(BASE_DIR, "dataset", "preprocessed_spam.csv")
MODEL_DIR    = os.path.join(BASE_DIR, "model")
CHARTS_DIR   = os.path.join(BASE_DIR, "charts")
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
# Load Saved TF-IDF Vectorizer
# ==========================================================

tfidf = joblib.load(os.path.join(MODEL_DIR, "tfidf.pkl"))

# ==========================================================
# Prepare Features  (fillna guards against empty rows)
# ==========================================================

X = tfidf.transform(df["Transformed_Message"].fillna("")).toarray()

# ==========================================================
# Prepare Target Variable  (direct map — no LabelEncoder needed)
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
# Initialize Models
# ==========================================================

models = {
    "Multinomial Naive Bayes": MultinomialNB(),
    "Logistic Regression":     LogisticRegression(max_iter=1000),
    "Support Vector Machine":  SVC(),
    "Decision Tree":           DecisionTreeClassifier(random_state=42),
    "Random Forest":           RandomForestClassifier(random_state=42),
    "Gradient Boosting":       GradientBoostingClassifier(random_state=42),
    "K-Nearest Neighbors":     KNeighborsClassifier(),
}

# ==========================================================
# Train Models
# ==========================================================

results        = []
trained_models = {}

print("\nTraining Models...\n")

for name, model in models.items():

    model.fit(X_train, y_train)
    predictions = model.predict(X_test)

    acc  = accuracy_score(y_test, predictions)
    prec = precision_score(y_test, predictions, zero_division=0)
    rec  = recall_score(y_test, predictions, zero_division=0)
    f1   = f1_score(y_test, predictions, zero_division=0)

    trained_models[name] = model
    results.append({
        "Model":     name,
        "Accuracy":  acc,
        "Precision": prec,
        "Recall":    rec,
        "F1 Score":  f1,
    })

    print(f"{name} Trained Successfully")

# ==========================================================
# Model Comparison Table
# ==========================================================

results_df = pd.DataFrame(results).sort_values(by="Accuracy", ascending=False)

print("\n")
print("=" * 70)
print("MODEL COMPARISON")
print("=" * 70)
print(results_df.to_string(index=False))

# ==========================================================
# Best Model
# ==========================================================

best_model_name = results_df.iloc[0]["Model"]
best_model      = trained_models[best_model_name]

print("\nBest Model :", best_model_name)

# ==========================================================
# Predictions with Best Model
# ==========================================================

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
print("BEST MODEL PERFORMANCE")
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
# Chart 1 — Confusion Matrix  →  charts/confusion_matrix.png
# ==========================================================

cm = confusion_matrix(y_test, y_pred)

print("Confusion Matrix\n")
print(cm)

plt.figure(figsize=(6, 5))
sns.heatmap(
    cm,
    annot=True,
    fmt="d",
    cmap="Blues",
    xticklabels=["Ham", "Spam"],
    yticklabels=["Ham", "Spam"],
)
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.title(f"Confusion Matrix — {best_model_name}")
plt.tight_layout()

cm_path = os.path.join(CHARTS_DIR, "confusion_matrix.png")
plt.savefig(cm_path, dpi=150)
plt.close()
print(f"\nSaved: {cm_path}")

# ==========================================================
# Chart 2 — Model Comparison Bar Chart  →  charts/model_comparison.png
# ==========================================================

fig, ax = plt.subplots(figsize=(12, 6))

results_df.plot(
    x="Model",
    y=["Accuracy", "Precision", "Recall", "F1 Score"],
    kind="bar",
    ax=ax,
)

ax.set_title("Model Comparison — All Metrics")
ax.set_ylabel("Score")
ax.set_xlabel("")
ax.set_xticklabels(results_df["Model"], rotation=25, ha="right")
ax.legend(loc="lower right")
ax.set_ylim(0, 1.05)
plt.tight_layout()

comp_path = os.path.join(CHARTS_DIR, "model_comparison.png")
plt.savefig(comp_path, dpi=150)
plt.close()
print(f"Saved: {comp_path}")

# ==========================================================
# Chart 3 — Accuracy Ranking  →  charts/accuracy_ranking.png
# ==========================================================

rank_df = results_df.sort_values("Accuracy", ascending=True)

plt.figure(figsize=(8, 5))
bars = plt.barh(rank_df["Model"], rank_df["Accuracy"], color="steelblue")
plt.bar_label(bars, fmt="%.4f", padding=3)
plt.xlabel("Accuracy")
plt.title("Model Accuracy Ranking")
plt.xlim(0, 1.05)
plt.tight_layout()

rank_path = os.path.join(CHARTS_DIR, "accuracy_ranking.png")
plt.savefig(rank_path, dpi=150)
plt.close()
print(f"Saved: {rank_path}")

# ==========================================================
# Chart 4 — F1 Score Comparison  →  charts/f1_score_comparison.png
# ==========================================================

f1_df = results_df.sort_values("F1 Score", ascending=True)

plt.figure(figsize=(8, 5))
bars = plt.barh(f1_df["Model"], f1_df["F1 Score"], color="darkorange")
plt.bar_label(bars, fmt="%.4f", padding=3)
plt.xlabel("F1 Score")
plt.title("Model F1 Score Comparison")
plt.xlim(0, 1.05)
plt.tight_layout()

f1_path = os.path.join(CHARTS_DIR, "f1_score_comparison.png")
plt.savefig(f1_path, dpi=150)
plt.close()
print(f"Saved: {f1_path}")

# ==========================================================
# Save Best Model
# ==========================================================

model_path = os.path.join(MODEL_DIR, "spam_model.pkl")
joblib.dump(best_model, model_path)

print("\n")
print("=" * 60)
print("Best Model Saved Successfully")
print("=" * 60)
print("Saved File :", model_path)

# ==========================================================
# Final Summary
# ==========================================================

print("\n")
print("=" * 60)
print("PROJECT SUMMARY")
print("=" * 60)
print("Dataset Shape    :", df.shape)
print("Training Samples :", len(X_train))
print("Testing  Samples :", len(X_test))
print("Best Model       :", best_model_name)
print("Accuracy         :", round(accuracy * 100, 2), "%")
print("Charts saved to  :", CHARTS_DIR)
print("=" * 60)