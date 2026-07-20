# ==========================================================
# CUSTOMER CHURN PREDICTION APP
# ==========================================================

import streamlit as st
import pandas as pd
import os
import sys

# Inject parent directory to path to allow importing from src/
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.predict import predict

# ==========================================================
# Page Configuration
# ==========================================================

st.set_page_config(
    page_title="Customer Churn Prediction",
    page_icon="📊",
    layout="centered"
)

# Custom premium styling using CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Outfit', sans-serif;
    }
    
    .stButton>button {
        background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%);
        color: white;
        border-radius: 8px;
        padding: 12px 28px;
        font-weight: 600;
        font-size: 16px;
        border: none;
        box-shadow: 0 4px 6px -1px rgba(79, 70, 229, 0.1), 0 2px 4px -1px rgba(79, 70, 229, 0.06);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        width: 100%;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 15px -3px rgba(124, 58, 237, 0.3), 0 4px 6px -2px rgba(124, 58, 237, 0.05);
        color: white !important;
        border: none !important;
    }
    
    .stButton>button:active {
        transform: translateY(1px);
    }
</style>
""", unsafe_allow_html=True)

st.title("📊 Customer Churn Prediction")
st.write("Predict whether a customer is likely to churn.")

st.markdown("---")

# ==========================================================
# User Inputs
# ==========================================================

gender = st.selectbox("Gender", ["Female", "Male"])

SeniorCitizen = st.selectbox(
    "Senior Citizen",
    [0, 1]
)

Partner = st.selectbox(
    "Partner",
    ["No", "Yes"]
)

Dependents = st.selectbox(
    "Dependents",
    ["No", "Yes"]
)

tenure = st.slider(
    "Tenure (Months)",
    0,
    72,
    12
)

PhoneService = st.selectbox(
    "Phone Service",
    ["No", "Yes"]
)

PaperlessBilling = st.selectbox(
    "Paperless Billing",
    ["No", "Yes"]
)

MonthlyCharges = st.number_input(
    "Monthly Charges",
    min_value=0.0,
    value=70.0
)

TotalCharges = st.number_input(
    "Total Charges",
    min_value=0.0,
    value=1000.0
)

MultipleLines = st.selectbox(
    "Multiple Lines",
    ["No","Yes","No phone service"]
)

InternetService = st.selectbox(
    "Internet Service",
    ["DSL","Fiber optic","No"]
)

OnlineSecurity = st.selectbox(
    "Online Security",
    ["No","Yes","No internet service"]
)

OnlineBackup = st.selectbox(
    "Online Backup",
    ["No","Yes","No internet service"]
)

DeviceProtection = st.selectbox(
    "Device Protection",
    ["No","Yes","No internet service"]
)

TechSupport = st.selectbox(
    "Tech Support",
    ["No","Yes","No internet service"]
)

StreamingTV = st.selectbox(
    "Streaming TV",
    ["No","Yes","No internet service"]
)

StreamingMovies = st.selectbox(
    "Streaming Movies",
    ["No","Yes","No internet service"]
)

Contract = st.selectbox(
    "Contract",
    ["Month-to-month","One year","Two year"]
)

PaymentMethod = st.selectbox(
    "Payment Method",
    [
        "Electronic check",
        "Mailed check",
        "Bank transfer (automatic)",
        "Credit card (automatic)"
    ]
)

# ==========================================================
# Prediction
# ==========================================================

if st.button("Predict Churn"):

    input_df = pd.DataFrame({

        "gender":[gender],
        "SeniorCitizen":[SeniorCitizen],
        "Partner":[Partner],
        "Dependents":[Dependents],
        "tenure":[tenure],
        "PhoneService":[PhoneService],
        "MultipleLines":[MultipleLines],
        "InternetService":[InternetService],
        "OnlineSecurity":[OnlineSecurity],
        "OnlineBackup":[OnlineBackup],
        "DeviceProtection":[DeviceProtection],
        "TechSupport":[TechSupport],
        "StreamingTV":[StreamingTV],
        "StreamingMovies":[StreamingMovies],
        "Contract":[Contract],
        "PaperlessBilling":[PaperlessBilling],
        "PaymentMethod":[PaymentMethod],
        "MonthlyCharges":[MonthlyCharges],
        "TotalCharges":[TotalCharges]

    })

    try:
        prediction, prob_churn = predict(input_df)

        st.markdown("---")

        if prediction == 1:
            st.error(
                f"⚠️ Customer is likely to Churn\n\nProbability : {prob_churn*100:.2f}%"
            )
        else:
            st.success(
                f"✅ Customer is NOT likely to Churn\n\nProbability : {(1.0 - prob_churn)*100:.2f}%"
            )
    except Exception as e:
        st.error(f"Prediction failed: {e}")