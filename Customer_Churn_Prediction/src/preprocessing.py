import pandas as pd
from sklearn.preprocessing import StandardScaler

# The exact list of 30 features expected by the trained model (in order)
EXPECTED_FEATURES = [
    'gender', 'SeniorCitizen', 'Partner', 'Dependents', 'tenure', 'PhoneService',
    'PaperlessBilling', 'MonthlyCharges', 'TotalCharges',
    'MultipleLines_No phone service', 'MultipleLines_Yes',
    'InternetService_Fiber optic', 'InternetService_No',
    'OnlineSecurity_No internet service', 'OnlineSecurity_Yes',
    'OnlineBackup_No internet service', 'OnlineBackup_Yes',
    'DeviceProtection_No internet service', 'DeviceProtection_Yes',
    'TechSupport_No internet service', 'TechSupport_Yes',
    'StreamingTV_No internet service', 'StreamingTV_Yes',
    'StreamingMovies_No internet service', 'StreamingMovies_Yes',
    'Contract_One year', 'Contract_Two year',
    'PaymentMethod_Credit card (automatic)', 'PaymentMethod_Electronic check',
    'PaymentMethod_Mailed check'
]

# Computed median of TotalCharges on the IBM Telco Churn raw dataset
TOTAL_CHARGES_MEDIAN = 1397.475

def clean_data(df, is_training=True):
    """
    Cleans raw customer data. Drops customerID, handles missing TotalCharges,
    and removes duplicates for training data.
    """
    df = df.copy()
    
    # Drop customerID if present
    if 'customerID' in df.columns:
        df = df.drop('customerID', axis=1)
        
    # Coerce TotalCharges to numeric
    if 'TotalCharges' in df.columns:
        df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')
        # Impute missing values with training median
        df['TotalCharges'] = df['TotalCharges'].fillna(TOTAL_CHARGES_MEDIAN)
        
    # Drop duplicates for training data only
    if is_training:
        df = df.drop_duplicates()
        
    return df

def encode_binary_features(df):
    """
    Encodes binary columns using deterministic mappings matching alphabetical LabelEncoder values.
    """
    df = df.copy()
    
    gender_map = {'Female': 0, 'Male': 1}
    yes_no_map = {'No': 0, 'Yes': 1}
    
    if 'gender' in df.columns:
        df['gender'] = df['gender'].map(gender_map)
        
    for col in ['Partner', 'Dependents', 'PhoneService', 'PaperlessBilling', 'Churn']:
        if col in df.columns:
            df[col] = df[col].map(yes_no_map)
            
    return df

def one_hot_encode_features(df):
    """
    Applies pd.get_dummies to convert remaining object/categorical columns to one-hot columns.
    """
    df = df.copy()
    
    # Identify object columns excluding columns we mapped to integers
    object_cols = df.select_dtypes(include=['object']).columns.tolist()
    
    if object_cols:
        df = pd.get_dummies(df, columns=object_cols, drop_first=True)
        
    # Cast all float/boolean columns from get_dummies to int
    for col in df.columns:
        if col not in ['tenure', 'MonthlyCharges', 'TotalCharges'] and df[col].dtype in ['bool', 'float64']:
            df[col] = df[col].astype(int)
            
    return df

def align_features(df, expected_features=EXPECTED_FEATURES):
    """
    Ensures the dataframe contains exactly the expected features in the correct order.
    Pads missing features with 0.
    """
    df = df.copy()
    
    # Add any missing expected feature columns with value 0
    for col in expected_features:
        if col not in df.columns:
            df[col] = 0
            
    # Retain only the expected feature columns in the exact order
    df = df[expected_features]
    
    return df

def preprocess_train_data(raw_df):
    """
    Preprocesses raw dataset for training. 
    Returns: X_scaled (DataFrame), y (Series), and fitted scaler.
    """
    # Clean data & drop duplicates
    df_clean = clean_data(raw_df, is_training=True)
    
    # Encode binary columns
    df_encoded = encode_binary_features(df_clean)
    
    # Separate features and target
    if 'Churn' not in df_encoded.columns:
        raise ValueError("Target column 'Churn' not found in raw training dataset.")
    
    X = df_encoded.drop('Churn', axis=1)
    y = df_encoded['Churn']
    
    # One-hot encode categorical features
    X_encoded = one_hot_encode_features(X)
    
    # Align features
    X_aligned = align_features(X_encoded, EXPECTED_FEATURES)
    
    # Scale features
    scaler = StandardScaler()
    X_scaled_np = scaler.fit_transform(X_aligned)
    X_scaled = pd.DataFrame(X_scaled_np, columns=EXPECTED_FEATURES)
    
    return X_scaled, y, scaler

def preprocess_input(input_df, scaler):
    """
    Preprocesses input data for prediction.
    Returns: X_scaled (DataFrame) ready for model inference.
    """
    # Clean data without dropping duplicates
    df_clean = clean_data(input_df, is_training=False)
    
    # Encode binary columns
    df_encoded = encode_binary_features(df_clean)
    
    # One-hot encode categorical features
    X_encoded = one_hot_encode_features(df_encoded)
    
    # Align features to ensure exact columns & ordering
    X_aligned = align_features(X_encoded, EXPECTED_FEATURES)
    
    # Scale features using pre-fitted scaler
    X_scaled_np = scaler.transform(X_aligned)
    X_scaled = pd.DataFrame(X_scaled_np, columns=EXPECTED_FEATURES)
    
    return X_scaled
