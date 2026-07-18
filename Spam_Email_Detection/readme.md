# Email Spam Detection

## Project Overview

This repository contains an end-to-end Email/SMS spam classification project built with Natural Language Processing (NLP) and Machine Learning.

The system cleans raw text data, extracts features using TF-IDF, trains classification models, and prepares artifacts for deployment with Streamlit.

## Key Features

- Data cleaning and preprocessing
- Exploratory Data Analysis (EDA)
- TF-IDF feature extraction
- Binary classification for ham vs spam
- Model saving and inference artifacts
- Streamlit-ready app support
- Visualizations stored in `charts/`

## Tech Stack

- Python
- pandas
- NumPy
- Matplotlib
- Seaborn
- NLTK
- scikit-learn
- joblib
- Streamlit

## Folder Structure

- `app/` - Streamlit application files
- `charts/` - saved visualization outputs
- `dataset/` - raw and processed datasets
- `documents/` - project documentation files
- `model/` - trained model artifacts
- `notebook/` - exploratory notebook files
- `src/` - source code modules
- `venv/` - Python virtual environment

## Documentation

This repository includes the following documents:

- `documents/architecture.md` - system architecture and folder design
- `documents/phases.md` - project phase plan and workflow
- `documents/rules.md` - coding and repo rules

## Usage

1. Create or activate the Python environment.
2. Install dependencies with `pip install -r requirements.txt`.
3. Run the preprocessing script with `python src/preprocessing.py`.
4. Use `notebook/email_spam.ipynb` for EDA and visualization.

## Notes

- Save generated plots and charts into the `charts/` directory for reference.
- Keep dataset files inside `dataset/` and model artifacts inside `model/`.
- Use consistent snake_case naming in Python source files.
