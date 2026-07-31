# Fake News Detection Architecture

```
                +-------------------+
                | Fake.csv          |
                | True.csv          |
                +-------------------+
                          |
                          ▼
                  Merge Datasets
                          |
                          ▼
                 Data Cleaning
                          |
                          ▼
               Text Preprocessing
    (Lowercase, Stopwords, Stemming)
                          |
                          ▼
               TF-IDF Vectorization
                          |
                          ▼
                 Train-Test Split
                          |
                          ▼
            Multiple ML Classification Models
      ┌──────────────────────────────────────┐
      │ Logistic Regression                  │
      │ Multinomial Naive Bayes              │
      │ Decision Tree                        │
      │ Random Forest                        │
      │ Passive Aggressive                   │
      │ Linear SVM                           │
      └──────────────────────────────────────┘
                          |
                          ▼
                  Model Evaluation
                          |
                          ▼
                   Best ML Model
                          |
                          ▼
                 Streamlit Web App
                          |
                          ▼
                  Fake / Real Prediction
```

## Components

### Dataset

Fake and Real News Dataset

### Data Cleaning

- Remove duplicates
- Remove missing values
- Merge datasets

### NLP

- Lowercase conversion
- Remove punctuation
- Remove stopwords
- Stemming

### Feature Engineering

TF-IDF Vectorization

### Machine Learning

Multiple supervised classification algorithms.

### Deployment

Streamlit Application