# House Price Prediction

## Overview

This project predicts house prices from structured housing data using a complete ML workflow. It includes dataset preparation, feature engineering, model training, tuning, evaluation, and a Streamlit app for live predictions.

## Files

- `housing.csv` — source dataset.
- `housing.ipynb` — notebook with end-to-end model pipeline.
- `app.py` — Streamlit app that loads the trained model and accepts user input.
- `Charts/` — generated charts, metrics, and feature metadata.
- `best_pipeline.joblib` — serialized best model pipeline saved after training.
- `requirements.txt` — Python dependencies.

## Installation

Install required packages with:

```bash
pip install -r requirements.txt
```

## Usage

1. Open and run `housing.ipynb` to train models and generate artifacts.
2. Run the Streamlit app:

```bash
streamlit run app.py
```

3. Use the sidebar to enter inputs and click `Predict`.

## Notes

- Ensure `best_pipeline.joblib` exists in the project root before runninge `app.py`.
- The app loads feature metadata from `Charts/feature_info.json`.

# Live Demo
https://housepriceprediction698.streamlit.app/