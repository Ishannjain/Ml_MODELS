import json
from pathlib import Path

import joblib
import pandas as pd
import streamlit as st

st.set_page_config(page_title='House Price Prediction', layout='wide')

st.title('House Price Prediction')

model_path = Path('best_pipeline.joblib')
feature_path = Path('Charts/feature_info.json')
metadata_path = Path('Charts/model_metadata.json')
metrics_path = Path('Charts/model_metrics.csv')

model = None
feature_info = {}
metadata = {}
metrics_df = None

try:
    if model_path.exists():
        model = joblib.load(model_path)
    if feature_path.exists():
        with feature_path.open('r', encoding='utf-8') as f:
            feature_info = json.load(f)
    if metadata_path.exists():
        with metadata_path.open('r', encoding='utf-8') as f:
            metadata = json.load(f)
    if metrics_path.exists():
        metrics_df = pd.read_csv(metrics_path)
except Exception as exc:
    st.error(f'Error loading saved artifacts: {exc}')

with st.sidebar:
    st.header('Input features')
    st.markdown('Enter values for the selected features and click Predict.')
    if metadata:
        st.subheader('Model metadata')
        st.write(f"**Best model:** {metadata.get('best_model', 'Unknown')}")
        st.write(f"**Selected features:** {', '.join(metadata.get('selected_features', []))}")
        st.write(f"**Train rows:** {metadata.get('train_rows', '-')}")
        st.write(f"**Test rows:** {metadata.get('test_rows', '-')}")

st.sidebar.markdown('---')

if model is None:
    st.warning('No trained model found. Run the notebook training cells first to generate best_pipeline.joblib.')
    st.stop()

input_values = {}
for feature, info in feature_info.items():
    if info.get('type') == 'numeric':
        input_values[feature] = st.sidebar.number_input(feature, value=0.0, format='%.2f')
    else:
        options = info.get('options') or ['Unknown']
        input_values[feature] = st.sidebar.selectbox(feature, options)

if st.sidebar.button('Predict'):
    try:
        input_df = pd.DataFrame([input_values])
        prediction = model.predict(input_df)[0]
        st.success(f'Predicted house price: ${prediction:,.2f}')
        st.write('### Provided inputs')
        st.json(input_values)
    except Exception as exc:
        st.error(f'Prediction error: {exc}')

col1, col2 = st.columns([2, 1])
with col1:
    st.subheader('Model evaluation')
    if metrics_df is not None:
        st.dataframe(metrics_df)
    else:
        st.info('No metrics available yet. Train the notebook pipeline first.')
with col2:
    st.subheader('Saved charts')
    chart_dir = Path('Charts')
    if chart_dir.exists():
        chart_paths = sorted(chart_dir.glob('*.png'))
        if chart_paths:
            for chart_path in chart_paths:
                st.write(chart_path.name)
                st.image(str(chart_path), use_column_width=True)
        else:
            st.info('No chart images found in Charts/.')
    else:
        st.info('Charts/ directory not found.')

st.markdown('---')
st.markdown('### Notes')
st.markdown('- Run `housing.ipynb` first to create the saved pipeline and feature metadata.')
st.markdown('- The app uses `best_pipeline.joblib` from the project root and JSON metadata from `Charts/`.')
