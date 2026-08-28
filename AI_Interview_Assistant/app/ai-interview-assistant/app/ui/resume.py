from pathlib import Path
import streamlit as st
from datetime import datetime

import json
# Project Paths
BASE_DIR = Path.cwd()
EVALUATION_FILE = BASE_DIR / "data" / "evaluation_report.json"
FEEDBACK_FILE = BASE_DIR / "data" / "feedback_report.json"

def load_json_file(file_path):
    if not file_path.exists():
        return None
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)
    except Exception as e:
        st.error(f"Unable to load {file_path.name}: {e}")
        return None

def upload_resume():
    st.markdown('<div class="section-title">📄 Resume</div>', unsafe_allow_html=True)
    st.write("Upload your resume to prepare your personalized interview.")
    
    uploaded_file = st.file_uploader("Upload Resume", type=["pdf", "docx", "txt"])
    
    if uploaded_file:
        st.session_state.resume_uploaded = True
        st.success(f"Resume uploaded: {uploaded_file.name}")
        st.write(f"File size: {uploaded_file.size / 1024:.2f} KB")
        
        if st.button("🚀 Process Resume", use_container_width=True):
            with st.spinner("Processing resume..."):
                st.success("Resume processing completed.")
                st.session_state.resume_uploaded = True

def display_resume_page():
    if st.session_state.resume_uploaded:
        upload_resume()