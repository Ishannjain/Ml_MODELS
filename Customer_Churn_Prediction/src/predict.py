import os
import sys
import joblib
import pandas as pd
import json

# Robust import pattern to support direct execution and importing as a module
try:
    from src.preprocessing import preprocess_input
except ImportError:
    try:
        from preprocessing import preprocess_input
    except ImportError:
        # Append parent directory and local directory to sys.path
        current_dir = os.path.dirname(os.path.abspath(__file__))
        sys.path.append(os.path.join(current_dir, '..'))
        sys.path.append(current_dir)
        from preprocessing import preprocess_input

# Define absolute paths based on this script's directory
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
MODEL_PATH = os.path.join(BASE_DIR, 'model', 'churn_model.pkl')
SCALER_PATH = os.path.join(BASE_DIR, 'model', 'scaler.pkl')

# Cache objects in memory to speed up multiple predictions
_model = None
_scaler = None

def load_artifacts():
    """
    Loads and caches the model and scaler from disk.
    """
    global _model, _scaler
    if _model is None:
        if not os.path.exists(MODEL_PATH):
            raise FileNotFoundError(f"Model file not found at {MODEL_PATH}. Please run train.py first.")
        _model = joblib.load(MODEL_PATH)
    if _scaler is None:
        if not os.path.exists(SCALER_PATH):
            raise FileNotFoundError(f"Scaler file not found at {SCALER_PATH}. Please run train.py first.")
        _scaler = joblib.load(SCALER_PATH)
    return _model, _scaler

def predict(input_df):
    """
    input_df: pd.DataFrame containing raw user features
    Returns: 
      prediction (int): 1 if likely to churn, 0 otherwise
      probability (float): Churn probability (class 1)
    """
    model, scaler = load_artifacts()
    
    # Preprocess raw input dataframe
    processed_df = preprocess_input(input_df, scaler)
    
    # Predict outcomes
    pred = model.predict(processed_df)[0]
    prob = model.predict_proba(processed_df)[0]
    
    return int(pred), float(prob[1])

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Predict Customer Churn from CSV file or JSON string.")
    parser.add_argument("--input", type=str, required=True, 
                        help="JSON string of customer details or path to a CSV file.")
    args = parser.parse_args()
    
    # Check if input is a file or JSON string
    if os.path.exists(args.input):
        print(f"Reading input from file: {args.input}")
        df_input = pd.read_csv(args.input)
    else:
        try:
            data = json.loads(args.input)
            if not isinstance(data, list):
                data = [data]
            df_input = pd.DataFrame(data)
        except json.JSONDecodeError:
            print("Error: Input must be a valid file path or JSON string.")
            sys.exit(1)
            
    try:
        model, scaler = load_artifacts()
        processed = preprocess_input(df_input, scaler)
        preds = model.predict(processed)
        probs = model.predict_proba(processed)
        
        print("\n" + "=" * 60)
        print("Prediction Results")
        print("=" * 60)
        for idx, (pred, prob) in enumerate(zip(preds, probs)):
            churn_status = "Likely to Churn ⚠️" if pred == 1 else "Not likely to Churn ✅"
            print(f"Customer {idx+1}: {churn_status} (Probability of Churn: {prob[1]*100:.2f}%)")
        print("=" * 60)
    except Exception as e:
        print(f"Prediction failed: {e}")
        sys.exit(1)
