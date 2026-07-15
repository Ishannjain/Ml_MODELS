# Project Summary: House Price Prediction

## What This Project Does
This project builds a machine learning model to predict house prices based on property features such as area, number of bedrooms, bathrooms, location-related attributes, and furnishing status.

## Purpose
The goal is to create a practical AI solution that helps users estimate the likely price of a house quickly and easily.

## Who Can Use It
- Homebuyers who want an approximate property value
- Real estate agents who need quick price estimates
- Students and developers learning machine learning
- Researchers studying housing market trends

## How It Works
1. The model is trained using a structured housing dataset.
2. The training process includes data cleaning, preprocessing, and model evaluation.
3. The best-performing model is saved for later use.
4. A Streamlit web app loads the trained model and allows users to enter property details.
5. The app displays the predicted house price instantly.

## Main Files
- `housing.csv` — training dataset
- `housing.ipynb` — notebook for model training and evaluation
- `app.py` — web app for prediction
- `best_pipeline.joblib` — trained model file
- `Charts/` — charts and metadata used by the app

## Technologies Used
- Python
- pandas
- numpy
- scikit-learn
- joblib
- Streamlit
- matplotlib / seaborn

## How to Run
1. Install dependencies:
   ```bash
   pip install -r requirements.txt