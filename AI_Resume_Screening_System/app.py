import streamlit as st
import joblib
import numpy as np

from utils import (
    extract_text,
    clean_resume,
    extract_skills
)

# --------------------------------------------------
# Page Configuration
# --------------------------------------------------

st.set_page_config(

    page_title="AI Resume Screening System",

    page_icon="📄",

    layout="wide"

)

# --------------------------------------------------
# Load Models
# --------------------------------------------------

model = joblib.load("model/resume_classifier.pkl")

tfidf = joblib.load("model/tfidf_vectorizer.pkl")

encoder = joblib.load("model/label_encoder.pkl")

# --------------------------------------------------
# Header
# --------------------------------------------------

st.title("📄 AI Resume Screening System")

st.markdown(
"""
Upload a Resume and predict the most suitable job category using Machine Learning.
"""
)

uploaded_file = st.file_uploader(

    "Upload Resume",

    type=["pdf","txt"]

)

if uploaded_file is not None:

    resume = extract_text(uploaded_file)

    st.subheader("Resume Preview")

    st.text_area(

        "",

        resume,

        height=250

    )

    cleaned = clean_resume(resume)

    vector = tfidf.transform([cleaned])

    prediction = model.predict(vector)

    category = encoder.inverse_transform(prediction)[0]

    st.success(f"Predicted Category : {category}")

    # Confidence

    if hasattr(model,"predict_proba"):

        probability = model.predict_proba(vector)[0]

        confidence = np.max(probability)*100

        st.metric(

            "Confidence",

            f"{confidence:.2f}%"

        )

        st.subheader("Top Predictions")

        indices = probability.argsort()[-5:][::-1]

        for i in indices:

            st.write(

                f"{encoder.classes_[i]} : {probability[i]*100:.2f}%"

            )

    st.subheader("Detected Skills")

    skills = extract_skills(resume)

    if len(skills)==0:

        st.warning("No predefined skills detected.")

    else:

        st.write(", ".join(skills))

    st.subheader("Resume Statistics")

    col1,col2,col3 = st.columns(3)

    col1.metric(

        "Characters",

        len(resume)

    )

    col2.metric(

        "Words",

        len(resume.split())

    )

    col3.metric(

        "Detected Skills",

        len(skills)

    )

