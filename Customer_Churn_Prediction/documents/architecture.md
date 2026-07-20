# Customer Churn Prediction Architecture

```
                  +--------------------+
                  |  Customer Dataset  |
                  +--------------------+
                            |
                            |
                            ▼
                 Data Preprocessing
      (Cleaning, Encoding, Scaling)
                            |
                            ▼
                Processed Dataset
                            |
                            ▼
               Train-Test Split
                            |
                            ▼
         Multiple Machine Learning Models
      ┌───────────────────────────────────┐
      │ Logistic Regression               │
      │ Decision Tree                     │
      │ Random Forest                     │
      │ KNN                               │
      │ SVM                               │
      │ Gradient Boosting                 │
      └───────────────────────────────────┘
                            |
                            ▼
                Model Evaluation
                            |
                            ▼
                Best Trained Model
                            |
                            ▼
                  Streamlit Web App
                            |
                            ▼
                    Customer Prediction
```

## Components

### Dataset
IBM Telco Customer Churn Dataset.

### Data Preprocessing
- Missing value handling
- Feature scaling
- Feature encoding

### Machine Learning
Multiple supervised classification algorithms.

### Evaluation
Performance comparison using various metrics.

### Deployment
Interactive Streamlit application.