# 📜 RULES.md

# Movie Recommendation System

Version: 1.0.0

---

# 📖 Purpose

This document defines the coding standards, project conventions, folder structure, Git workflow, documentation requirements, and deployment guidelines for the **Movie Recommendation System**.

Following these rules ensures the project remains maintainable, scalable, and production-ready.

---

# 📁 Project Structure Rules

The project must follow the below folder structure.

```
Movie-Recommendation-System/

│
├── app/
├── dataset/
├── model/
├── notebook/
├── reports/
├── screenshots/
├── src/
│
├── README.md
├── PRD.md
├── PHASES.md
├── ARCHITECTURE.md
├── RULES.md
├── requirements.txt
├── LICENSE
├── .gitignore
```

Do not place files outside their designated folders.

---

# 📂 Folder Responsibilities

## dataset/

Store only datasets.

Allowed Files

- tmdb_5000_movies.csv
- tmdb_5000_credits.csv
- clean_movies.csv

---

## notebook/

Contains only Jupyter notebooks.

Example

MovieRecommendation.ipynb

---

## src/

Contains reusable Python modules.

Example

- preprocessing.py
- feature_engineering.py
- recommendation.py
- utils.py

---

## model/

Contains serialized machine learning files.

Allowed Files

- movies.pkl
- similarity.pkl

Never store datasets here.

---

## app/

Contains Streamlit application.

Example

- app.py
- assets/

---

## reports/

Contains reports and generated outputs.

Examples

- confusion_matrix.png
- evaluation_report.pdf
- charts

---

## screenshots/

Contains project screenshots for GitHub README.

---

# 🐍 Python Coding Standards

Follow PEP-8.

Maximum line length:

88 characters

Use meaningful variable names.

Example

Good

```python
movie_index = 25
```

Bad

```python
x = 25
```

---

# 🔤 Naming Convention

Variables

snake_case

Example

```python
movie_list
similarity_matrix
recommended_movies
```

Functions

snake_case

Example

```python
recommend_movies()
clean_data()
extract_director()
```

Classes

PascalCase

Example

```python
MovieRecommender
```

Constants

UPPER_CASE

Example

```python
MODEL_PATH
SIMILARITY_FILE
```

---

# 📦 Import Rules

Follow this order.

1. Standard Library

```python
import os
import ast
```

2. Third-party Libraries

```python
import pandas as pd
import numpy as np
```

3. Project Modules

```python
from src.preprocessing import clean_data
```

Separate each section with one blank line.

---

# 📊 Dataset Rules

Never modify the original dataset.

Always create

clean_movies.csv

Keep original dataset unchanged.

Always verify

- Missing values
- Duplicate values
- Data types

before preprocessing.

---

# 🧹 Data Cleaning Rules

Always

Remove duplicates

Handle missing values

Reset index

Select required columns only

Save cleaned dataset

Never train models on raw data.

---

# 🧠 Feature Engineering Rules

Use only relevant features.

Example

✔ Overview

✔ Genres

✔ Keywords

✔ Cast

✔ Director

Avoid unnecessary features.

---

# 🔤 NLP Rules

Always

Convert to lowercase

Remove spaces

Tokenize text

Apply stemming

Keep preprocessing consistent across training and prediction.

---

# 🤖 Recommendation Rules

Use

CountVectorizer

Cosine Similarity

Never hardcode recommendations.

Recommendation function must always use the similarity matrix.

---

# 💾 Model Rules

Save models using Joblib or Pickle.

Required Files

```
movies.pkl

similarity.pkl
```

Never overwrite models without validation.

---

# 📒 Notebook Rules

Notebook purpose

EDA

Experiments

Visualization

Training

Avoid writing reusable production code in notebooks.

Move reusable logic to

src/

---

# 🎨 Streamlit Rules

Always use

Page Config

Sidebar

Professional Title

Footer

Responsive Layout

Handle invalid movie names gracefully.

Display friendly messages.

---

# 🔥 Git Rules

Commit after every phase.

Commit Format

```
Phase-1 Environment Setup

Phase-2 Dataset Collection

Phase-3 Data Cleaning

Phase-4 EDA

Phase-5 Feature Engineering

Phase-6 NLP

Phase-7 Vectorization

Phase-8 Similarity Matrix

Phase-9 Recommendation Engine

Phase-10 Streamlit

Phase-11 Deployment
```

Never commit

```
__pycache__/

.ipynb_checkpoints/

*.pkl

*.csv (large datasets if unnecessary)

.env
```

---

# 🌐 Deployment Rules

Deploy only after

Model testing

README completion

requirements.txt updated

Application tested locally

Deployment Platform

Streamlit Community Cloud

---

# 📚 Documentation Rules

Every project must contain

```
README.md

PRD.md

PHASES.md

ARCHITECTURE.md

RULES.md

LICENSE

requirements.txt
```

Documentation must be updated after each completed phase.

---

# 🧪 Testing Rules

Before deployment verify

Dataset loads correctly

Movie search works

Recommendations are accurate

No runtime errors

All required files exist

---

# 🔒 Security Rules

Never commit

API Keys

Passwords

Tokens

Secrets

Use environment variables if API integration is added.

---

# 🚀 Performance Rules

Keep preprocessing efficient.

Avoid unnecessary loops.

Use vectorized operations whenever possible.

Reuse saved similarity matrix.

---

# 📈 Version Control

Version Format

Major.Minor.Patch

Example

```
v1.0.0
```

Update version after major milestones.

---

# 🎯 Project Completion Checklist

Environment Setup

Dataset Collection

Data Cleaning

EDA

Feature Engineering

NLP

Vectorization

Cosine Similarity

Recommendation Engine

Model Saving

Streamlit Application

Deployment

Documentation

GitHub Repository

Resume Update

LinkedIn Post

---

# 🏆 Final Goal

The completed project should be

✅ Modular

✅ Well Documented

✅ Production Ready

✅ Deployment Ready

✅ Scalable

✅ Easy to Maintain

✅ Portfolio Ready

✅ Interview Ready

✅ Open Source Friendly

---

# 👨‍💻 Development Principles

- Write clean and readable code.
- Keep functions small and reusable.
- Document every major component.
- Test before committing.
- Follow a consistent folder structure.
- Maintain version control throughout development.
- Prioritize simplicity, maintainability, and reproducibility.