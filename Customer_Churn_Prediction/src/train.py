import os
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report
)

# Import our custom preprocessing module
from preprocessing import preprocess_train_data, EXPECTED_FEATURES

# Define absolute paths based on this script's directory
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
DATASET_PATH = os.path.join(BASE_DIR, 'dataset', 'customer_churn.csv')
PROCESSED_DATASET_PATH = os.path.join(BASE_DIR, 'dataset', 'processed_customer_churn.csv')
MODEL_DIR = os.path.join(BASE_DIR, 'model')
MODEL_PATH = os.path.join(MODEL_DIR, 'churn_model.pkl')
SCALER_PATH = os.path.join(MODEL_DIR, 'scaler.pkl')

def train_and_evaluate():
    print("=" * 60)
    print("Starting Model Training Pipeline")
    print("=" * 60)
    
    # 1. Load raw dataset
    if not os.path.exists(DATASET_PATH):
        raise FileNotFoundError(f"Raw dataset not found at {DATASET_PATH}")
        
    print(f"Loading raw dataset from {DATASET_PATH}...")
    raw_df = pd.read_csv(DATASET_PATH)
    
    # 2. Run preprocessing
    print("Preprocessing raw dataset...")
    X_scaled, y, scaler = preprocess_train_data(raw_df)
    
    # 3. Save processed dataset and scaler
    os.makedirs(MODEL_DIR, exist_ok=True)
    joblib.dump(scaler, SCALER_PATH)
    print(f"Scaler saved to {SCALER_PATH}")
    
    processed_df = X_scaled.copy()
    processed_df['Churn'] = y.values
    processed_df.to_csv(PROCESSED_DATASET_PATH, index=False)
    print(f"Processed dataset saved to {PROCESSED_DATASET_PATH}")
    
    # 4. Separate training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(
        X_scaled,
        y,
        test_size=0.20,
        random_state=42,
        stratify=y
    )
    
    print(f"Train-Test Split Completed:")
    print(f"  Training samples: {X_train.shape[0]}")
    print(f"  Testing samples: {X_test.shape[0]}")
    print("=" * 60)
    
    # 5. Define ML Models
    models = {
        "Logistic Regression": LogisticRegression(max_iter=1000),
        "Decision Tree": DecisionTreeClassifier(random_state=42),
        "Random Forest": RandomForestClassifier(n_estimators=200, random_state=42),
        "KNN": KNeighborsClassifier(),
        "Support Vector Machine": SVC(probability=True, random_state=42),
        "Gradient Boosting": GradientBoostingClassifier(random_state=42)
    }
    
    # 6. Train and evaluate each model
    results = []
    trained_models = {}
    
    for name, model in models.items():
        print(f"Training {name}...")
        model.fit(X_train, y_train)
        preds = model.predict(X_test)
        
        trained_models[name] = model
        acc = accuracy_score(y_test, preds)
        prec = precision_score(y_test, preds)
        rec = recall_score(y_test, preds)
        f1 = f1_score(y_test, preds)
        
        results.append({
            "Model": name,
            "Accuracy": acc,
            "Precision": prec,
            "Recall": rec,
            "F1 Score": f1
        })
        
    # 7. Print and select best model
    results_df = pd.DataFrame(results).sort_values(by="Accuracy", ascending=False).reset_index(drop=True)
    print("\n" + "=" * 60)
    print("Model Evaluation Summary")
    print("=" * 60)
    print(results_df.to_string(index=False))
    print("=" * 60)
    
    best_model_name = results_df.iloc[0]["Model"]
    best_model = trained_models[best_model_name]
    print(f"\nBest Model selected: {best_model_name}")
    print(f"Accuracy: {results_df.iloc[0]['Accuracy']:.4f}")
    
    # 8. Print Classification Report for Best Model
    best_preds = best_model.predict(X_test)
    print("\n" + "=" * 60)
    print(f"Classification Report for Best Model ({best_model_name})")
    print("=" * 60)
    print(classification_report(y_test, best_preds))
    print("=" * 60)
    
    print("Confusion Matrix:")
    print(confusion_matrix(y_test, best_preds))
    print("=" * 60)
    
    # 9. Save Best Model
    joblib.dump(best_model, MODEL_PATH)
    print(f"Best model saved to {MODEL_PATH}")
    print("=" * 60)

if __name__ == "__main__":
    train_and_evaluate()
