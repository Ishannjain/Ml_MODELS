# System Architecture

The Email Spam Detection project consists of a user-facing Streamlit interface, a preprocessing pipeline, feature extraction, and a classification model.

## Architecture Flow

```text
User Input
↓
Streamlit UI
↓
Text Preprocessing
↓
Feature Extraction (TF-IDF)
↓
Machine Learning Model
↓
Prediction Output
↓
Spam / Ham
```

## Folder Architecture

```text
Spam_Email_Detection/
├── app/                  # Streamlit application files
├── charts/               # Generated charts and visualizations
├── dataset/              # Raw and processed datasets
├── documents/            # Documentation files
├── model/                # Saved model artifacts
├── notebook/             # Jupyter notebooks for EDA and analysis
├── src/                  # Source code modules
└── venv/                 # Python virtual environment
```

## Machine Learning Workflow

1. Dataset collection and inspection
2. Text cleaning and preprocessing
3. Feature engineering with TF-IDF
4. Model training
5. Evaluation and validation
6. Deployment via Streamlit

## Components

- **Dataset:** raw email/SMS data in `dataset/`
- **Preprocessing:** text normalization, tokenization, stopword removal, stemming
- **Feature Extraction:** TF-IDF vector generation
- **Modeling:** classification algorithms such as Naive Bayes and Logistic Regression
- **Deployment:** Streamlit interface for predictions

