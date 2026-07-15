# Architecture Document - House Price Prediction Model

## 1. Purpose
This document describes the architecture, workflow, folder structure, and technology stack for the House Price Prediction project.

## 2. Project Goal
The system predicts house prices using structured housing data and provides a web-based interface for users to enter property features and receive instant price estimates.

## 3. High-Level Architecture

The project is built using a simple machine learning pipeline with three main layers:

1. Data Layer
   - Stores the raw dataset in `housing.csv`
   - Contains housing-related features such as location, size, rooms, and other attributes

2. Model Layer
   - Built in `housing.ipynb`
   - Performs data preprocessing, feature engineering, model training, evaluation, and model saving

3. Application Layer
   - Built with `app.py`
   - Loads the trained model and shows a user interface for prediction

## 4. End-to-End Flow

1. Load dataset from `housing.csv`
2. Clean and preprocess the data
3. Perform feature engineering if needed
4. Split data into training and testing sets
5. Train a regression model using scikit-learn
6. Evaluate the model and select the best-performing pipeline
7. Save the trained model as `best_pipeline.joblib`
8. Store feature metadata and charts in the `Charts/` folder
9. Run the Streamlit app
10. Accept user input from the UI
11. Predict and display the house price

## 5. Architecture Diagram (Text Flow)

```text
User Input
   ↓
Streamlit App (app.py)
   ↓
Trained Model (best_pipeline.joblib)
   ↓
Prediction Output
```

And the training side:

```text
housing.csv
   ↓
housing.ipynb
   ↓
Data Preprocessing + Feature Engineering
   ↓
Model Training + Evaluation
   ↓
best_pipeline.joblib + Charts/
```

## 6. Components and Responsibilities

- `housing.csv`
  - Raw input dataset used for training

- `housing.ipynb`
  - Notebook for end-to-end ML workflow:
    - data exploration
    - preprocessing
    - model training
    - evaluation
    - artifact generation

- `app.py`
  - Streamlit app for user interaction
  - Loads the trained model
  - Collects property details
  - Returns predicted price

- `best_pipeline.joblib`
  - Serialized trained machine learning pipeline

- `Charts/`
  - Stores charts, metrics, and feature metadata

- `requirements.txt`
  - Python dependencies for the project

## 7. Folder and File Structure

```text
House_Price_Prediction/
├── app.py
├── housing.csv
├── housing.ipynb
├── best_pipeline.joblib
├── requirements.txt
├── README.md
├── prd.md
├── architecture.md
└── Charts/
    ├── feature_info.json
    ├── metrics.json
    └── generated_plots/
```

## 8. Tech Stack

- Python 3.x
- Jupyter Notebook
- pandas
- numpy
- scikit-learn
- joblib
- Streamlit
- Matplotlib / Seaborn
- JSON for metadata handling

## 9. Model Design

The model is designed as a regression-based machine learning pipeline:

- Input: structured housing features
- Processing:
  - data cleaning
  - missing value handling
  - feature transformation
  - scaling or encoding where required
- Output: continuous numeric house price prediction

## 10. Deployment Considerations

- Local development:
  - Run the notebook to train the model
  - Run the Streamlit app using `streamlit run app.py`

- Optional deployment:
  - The app can be deployed on Streamlit Cloud or a similar platform

- Important note:
  - `best_pipeline.joblib` must exist before running the app

## 11. Summary

This architecture keeps the project modular and easy to understand:

- Training logic is separated in the notebook
- Prediction logic is handled by the Streamlit app
- Model artifacts are stored separately for reuse
- Charts and metadata are organized in the `Charts/` folder