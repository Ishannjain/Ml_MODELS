# Customer Churn Prediction - Project Phases

## Phase 1 – Project Setup

### Objective
Create the project structure and install all required libraries.

### Tasks
- Create project folders
- Create virtual environment
- Install dependencies
- Initialize Git repository

### Deliverables
- Project structure
- requirements.txt
- Git initialized

---

## Phase 2 – Dataset Understanding

### Objective
Understand the dataset before preprocessing.

### Tasks
- Load dataset
- Explore columns
- Identify data types
- Check missing values
- Check duplicates
- Study target variable

### Deliverables
- Dataset summary
- Initial observations

---

## Phase 3 – Data Preprocessing

### Objective
Prepare clean data for machine learning.

### Tasks
- Remove unnecessary columns
- Handle missing values
- Encode categorical variables
- Scale numerical features
- Split features and target
- Save processed dataset

### Deliverables
- processed_customer_churn.csv
- scaler.pkl

---

## Phase 4 – Exploratory Data Analysis

### Objective
Visualize customer behavior and churn patterns.

### Tasks
- Churn distribution
- Contract vs Churn
- Monthly Charges analysis
- Tenure distribution
- Correlation heatmap

### Deliverables
- Saved charts
- Business insights

---

## Phase 5 – Feature Preparation

### Objective
Prepare processed data for model training.

### Tasks
- Load processed dataset
- Separate X and y
- Train-test split

### Deliverables
- X_train
- X_test
- y_train
- y_test

---

## Phase 6 – Model Training & Evaluation

### Objective
Train multiple ML algorithms and select the best one.

### Models
- Logistic Regression
- Decision Tree
- Random Forest
- KNN
- SVM
- Gradient Boosting

### Evaluation
- Accuracy
- Precision
- Recall
- F1 Score
- Confusion Matrix

### Deliverables
- churn_model.pkl

---

## Phase 7 – Streamlit Application

### Objective
Develop an interactive web application.

### Tasks
- Load trained model
- User input form
- Predict churn
- Display probability

---

## Phase 8 – Deployment

### Objective
Deploy the application online.

### Tasks
- Prepare requirements.txt
- Create Procfile (if needed)
- Deploy using Streamlit Cloud

---

## Phase 9 – Documentation

### Objective
Complete professional documentation.

### Files
- README.md
- Architecture.md
- PRD.md
- Rules.md