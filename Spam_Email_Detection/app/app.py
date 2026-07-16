import os
import re
import string

import joblib
import nltk
import streamlit as st

from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

# Download required resources
nltk.download('stopwords', quiet=True)

# ==============================
# Resolve Paths
# ==============================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_DIR = os.path.join(BASE_DIR, "model")

# ==============================
# Load Models
# ==============================

model  = joblib.load(os.path.join(MODEL_DIR, "spam_model.pkl"))
tfidf  = joblib.load(os.path.join(MODEL_DIR, "tfidf.pkl"))
encoder = joblib.load(os.path.join(MODEL_DIR, "label_encoder.pkl"))

ps = PorterStemmer()
stop_words = set(stopwords.words("english"))

# ==============================
# Text Preprocessing Function
# ==============================

def transform_text(text: str) -> str:
    text = text.lower()
    text = re.sub(r'<.*?>', '', text)
    text = re.sub(r'https?://\S+|www\.\S+', '', text)
    text = re.sub(r'\d+', '', text)
    text = text.translate(str.maketrans('', '', string.punctuation))
    words = text.split()
    clean_words = [ps.stem(w) for w in words if w not in stop_words]
    return " ".join(clean_words)

# ==============================
# Page Config
# ==============================

st.set_page_config(
    page_title="Email Spam Detector",
    page_icon="📧",
    layout="wide"
)

# ==============================
# Sidebar
# ==============================

st.sidebar.title("📧 Email Spam Detector")

st.sidebar.info("""
Built using

- Python
- Streamlit
- NLP
- TF-IDF
- Machine Learning
""")

st.sidebar.success("Model Ready ✅")

# ==============================
# Main UI
# ==============================

st.title("📧 Email Spam Detection System")

st.write(
"""
Enter any Email or SMS message below.

The AI model will predict whether it is

✅ Ham (Safe)

or

🚨 Spam
"""
)

message = st.text_area(
    "Enter Message",
    height=200
)

# ==============================
# Prediction
# ==============================

if st.button("Predict"):

    if message.strip() == "":

        st.warning("Please enter a message.")

    else:

        transformed = transform_text(message)

        vector = tfidf.transform([transformed])

        prediction = model.predict(vector)[0]

        # Safely get probability — some models (e.g. SVC) don't support predict_proba
        supports_proba = hasattr(model, "predict_proba")
        if supports_proba:
            probability = model.predict_proba(vector)[0]
            ham_prob  = probability[0] * 100
            spam_prob = probability[1] * 100
            confidence = max(probability) * 100
        else:
            ham_prob  = None
            spam_prob = None
            confidence = None

        st.divider()

        if prediction == 1:
            st.error("🚨 SPAM MESSAGE")
        else:
            st.success("✅ HAM MESSAGE")

        if confidence is not None:
            st.metric("Confidence", f"{confidence:.2f}%")

            st.write("### Probability")

            st.write({
                "Ham":  f"{ham_prob:.2f}%",
                "Spam": f"{spam_prob:.2f}%"
            })
        else:
            st.info("ℹ️ This model does not support probability estimates.")

# ==============================
# Footer
# ==============================

st.divider()

st.caption("Built with ❤️ using Streamlit and Scikit-Learn")