# System Architecture

## High Level Architecture

```
                User
                  │
                  ▼
         Streamlit Web App
                  │
                  ▼
         Movie Selection UI
                  │
                  ▼
     Recommendation Function
                  │
                  ▼
      Cosine Similarity Matrix
                  │
                  ▼
         Movie Metadata
                  │
                  ▼
     Recommended Movies List
```

---

# Data Flow

```
TMDB Dataset

↓

Movies Dataset

↓

Credits Dataset

↓

Merge

↓

Cleaning

↓

Feature Engineering

↓

Create Tags

↓

CountVectorizer

↓

Cosine Similarity

↓

Recommendation Engine

↓

Streamlit UI
```

---

# Folder Architecture

```
Movie-Recommendation-System/

dataset/

notebook/

src/

model/

app/

reports/

README.md

PHASES.md

ARCHITECTURE.md

PRD.md
```

---

# Components

## Dataset

Movies

Credits

---

## Processing

Cleaning

Merge

Feature Engineering

---

## NLP

Tokenization

Stemming

CountVectorizer

---

## Similarity

Cosine Similarity

---

## Recommendation

Top 5 Movies

---

## Deployment

Streamlit Community Cloud

---

# Machine Learning Workflow

Dataset

↓

Cleaning

↓

Feature Engineering

↓

NLP

↓

Vectorization

↓

Cosine Similarity

↓

Recommendation

↓

Deployment