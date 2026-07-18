# Project Phases

## Phase 1: Environment Setup

- Create a Python virtual environment
- Install required libraries
- Define the folder structure

## Phase 2: Exploratory Data Analysis (EDA)

- Inspect the dataset
- Check for missing values
- Identify duplicate rows
- Visualize target distribution and message statistics

## Phase 3: NLP Preprocessing

- Convert text to lowercase
- Remove URLs and HTML tags
- Strip numbers and punctuation
- Tokenize text
- Remove stopwords
- Apply stemming

## Phase 4: Feature Engineering

- Compute message length
- Extract cleaned text features
- Generate TF-IDF feature matrix

## Phase 5: Model Training

- Train classification models such as:
  - Naive Bayes
  - Logistic Regression
  - Support Vector Machine
  - Random Forest
  - XGBoost

## Phase 6: Model Evaluation

- Evaluate using:
  - Accuracy
  - Precision
  - Recall
  - F1 score
  - ROC-AUC

## Phase 7: Hyperparameter Tuning

- Tune model parameters using GridSearchCV or similar techniques

## Phase 8: Model Saving

- Save trained artifacts:
  - `spam_model.pkl`
  - `tfidf.pkl`
  - `label_encoder.pkl`

## Phase 9: Streamlit Application

- Build the user interface for predictions
- Display spam/ham results and confidence

## Phase 10: Deployment

- Deploy the app using Streamlit Cloud or another hosting service

## Phase 11: Documentation

- Maintain README and supporting documentation files

## Phase 12: Portfolio Completion

- Add the project to portfolio materials
- Update LinkedIn and resume with the project details
