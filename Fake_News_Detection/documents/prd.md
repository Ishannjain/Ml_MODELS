# Product Requirements Document (PRD)

# Project Name

Fake News Detection

---

## Problem Statement

The rapid spread of fake news on digital platforms makes it difficult for users to distinguish between reliable and misleading information. An automated fake news detection system can help classify articles before they spread widely.

---

## Objective

Develop a machine learning application capable of identifying whether a news article is Fake or Real using Natural Language Processing techniques.

---

## Goals

- Detect fake news accurately.
- Provide a simple prediction interface.
- Demonstrate NLP workflow.
- Deploy a production-ready application.

---

## Functional Requirements

### Dataset

- Load Fake.csv
- Load True.csv
- Merge datasets

### NLP

- Clean text
- Remove stopwords
- Perform stemming
- TF-IDF Vectorization

### Machine Learning

Train multiple classification models.

### Deployment

Predict fake or real news from user input.

---

## Non Functional Requirements

- Fast prediction
- Scalable
- Reusable code
- Deployment ready

---

## Success Criteria

- High prediction accuracy
- Robust NLP preprocessing
- Professional Streamlit application

---

## Target Users

- Journalists
- News Readers
- Researchers
- Students
- Data Scientists

---

## Risks

- Overfitting
- Dataset bias
- Imbalanced data
- Noisy text

---

## Future Scope

- BERT
- RoBERTa
- LSTM
- Transformers
- Explainable AI
- Cloud Deployment