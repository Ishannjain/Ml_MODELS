# ==========================================================
# Plant Disease Detection - Streamlit App
# ==========================================================

import streamlit as st
import tensorflow as tf
import joblib
import numpy as np
from PIL import Image

# ----------------------------------------------------------
# Page Configuration
# ----------------------------------------------------------

st.set_page_config(
    page_title="Plant Disease Detection",
    page_icon="🌿",
    layout="centered"
)

# ----------------------------------------------------------
# Load Model
# ----------------------------------------------------------

@st.cache_resource
def load_model():

    model = tf.keras.models.load_model(
        "model/best_plant_disease_model.keras"
    )

    class_names = joblib.load(
        "model/class_names.pkl"
    )

    return model, class_names


model, class_names = load_model()

# ----------------------------------------------------------
# Prediction Function
# ----------------------------------------------------------

def predict(image):

    image = image.resize((224,224))

    image = np.array(image)

    image = image / 255.0

    image = np.expand_dims(image, axis=0)

    prediction = model.predict(image, verbose=0)

    predicted_class = np.argmax(prediction)

    confidence = np.max(prediction)

    return class_names[predicted_class], confidence

# ----------------------------------------------------------
# UI
# ----------------------------------------------------------

st.title("🌿 Plant Disease Detection")

st.write(
    "Upload a plant leaf image to detect the disease."
)

uploaded_file = st.file_uploader(

    "Choose an Image",

    type=["jpg","jpeg","png"]

)

if uploaded_file is not None:

    image = Image.open(uploaded_file).convert("RGB")

    st.image(
        image,
        caption="Uploaded Image",
        use_container_width=True
    )

    if st.button("Predict Disease"):

        disease, confidence = predict(image)

        st.success(f"Prediction : {disease}")

        st.info(f"Confidence : {confidence:.2%}")