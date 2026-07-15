import json
from pathlib import Path

import joblib
import pandas as pd
import streamlit as st

# -------------------------------------------------
# Page Configuration
# -------------------------------------------------
st.set_page_config(
    page_title="House Price Prediction",
    layout="wide"
)

st.title("🏠 House Price Prediction")

# -------------------------------------------------
# File Paths
# -------------------------------------------------
model_path = Path("best_pipeline.joblib")
feature_path = Path("Charts/feature_info.json")
metadata_path = Path("Charts/model_metadata.json")
metrics_path = Path("Charts/model_metrics.csv")

# -------------------------------------------------
# Load Saved Files
# -------------------------------------------------
model = None
feature_info = {}
metadata = {}
metrics_df = None

try:
    if model_path.exists():
        model = joblib.load(model_path)

    if feature_path.exists():
        with open(feature_path, "r", encoding="utf-8") as f:
            feature_info = json.load(f)

    if metadata_path.exists():
        with open(metadata_path, "r", encoding="utf-8") as f:
            metadata = json.load(f)

    if metrics_path.exists():
        metrics_df = pd.read_csv(metrics_path)

except Exception as e:
    st.error(f"Error loading files:\n{e}")

# -------------------------------------------------
# Stop if Model Doesn't Exist
# -------------------------------------------------
if model is None:
    st.warning(
        "No trained model found.\n\nRun housing.ipynb first to create best_pipeline.joblib."
    )
    st.stop()

# -------------------------------------------------
# Sidebar
# -------------------------------------------------
with st.sidebar:

    st.header("Input Features")
    st.write("Enter the values below.")

    input_values = {}

    for feature, info in feature_info.items():

        if info.get("type") == "numeric":
            input_values[feature] = st.number_input(
                feature,
                value=0.0,
                format="%.2f"
            )

        else:
            options = info.get("options", ["Unknown"])
            input_values[feature] = st.selectbox(
                feature,
                options
            )

    predict = st.button("Predict")

# -------------------------------------------------
# Tabs
# -------------------------------------------------
tab1, tab2, tab3 = st.tabs(
    [
        "🏠 Prediction",
        "📊 Model Statistics",
        "📈 Charts"
    ]
)

# =================================================
# TAB 1 : Prediction
# =================================================
with tab1:

    st.subheader("House Price Prediction")

    if predict:

        try:

            input_df = pd.DataFrame([input_values])

            prediction = model.predict(input_df)[0]

            st.success(
                f"Predicted House Price: **${prediction:,.2f}**"
            )

            st.markdown("### Input Values")

            st.dataframe(
                pd.DataFrame([input_values]),
                use_container_width=True
            )

        except Exception as e:

            st.error(f"Prediction Error:\n{e}")

# =================================================
# TAB 2 : Statistics
# =================================================
with tab2:

    st.subheader("Model Statistics")

    if metadata:

        col1, col2 = st.columns(2)

        with col1:

            st.metric(
                "Best Model",
                metadata.get("best_model", "-")
            )

            st.metric(
                "Training Rows",
                metadata.get("train_rows", "-")
            )

        with col2:

            st.metric(
                "Testing Rows",
                metadata.get("test_rows", "-")
            )

            st.metric(
                "Features",
                len(metadata.get("selected_features", []))
            )

        st.markdown("### Selected Features")

        st.write(metadata.get("selected_features", []))

    st.divider()

    st.subheader("Performance of Different Models")

    if metrics_df is not None:

        st.dataframe(
            metrics_df,
            use_container_width=True,
            hide_index=True
        )

        if "R2 Score" in metrics_df.columns:

            best = metrics_df.sort_values(
                "R2 Score",
                ascending=False
            ).iloc[0]

            st.success(
                f"🏆 Best Model: {best['Model']}  |  R² Score = {best['R2 Score']:.4f}"
            )

    else:

        st.info("No model statistics found.")

# =================================================
# TAB 3 : Charts
# =================================================
with tab3:

    st.subheader("Model Visualizations")

    chart_dir = Path("Charts")

    if chart_dir.exists():

        charts = sorted(chart_dir.glob("*.png"))

        if charts:

            cols = st.columns(2)

            for i, chart in enumerate(charts):

                with cols[i % 2]:

                    st.image(
                        str(chart),
                        caption=chart.stem.replace("_", " ").title(),
                        use_container_width=True
                    )

        else:

            st.info("No chart images found.")

    else:

        st.warning("Charts folder not found.")

# -------------------------------------------------
# Footer
# -------------------------------------------------
st.divider()

st.markdown("### Notes")

st.markdown("""
- Run **housing.ipynb** before using the app.
- The model is loaded from **best_pipeline.joblib**.
- Charts and metadata are loaded from the **Charts/** folder.
""")