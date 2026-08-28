# filepath: ai-interview-assistant/app/main.py

import streamlit as st
from app.config import BASE_DIR
from app.state import initialize_session_state
from app.file_handlers import load_evaluation_report, load_feedback_report
from app.ui.sidebar import render_sidebar
from app.ui.home import render_home
from app.ui.resume import render_resume
from app.ui.interview import render_interview
from app.ui.results import render_results
from app.ui.feedback import render_feedback

def main():
    # Initialize session state
    initialize_session_state()

    # Set up the Streamlit app layout
    st.set_page_config(
        page_title="AI Interview Assistant",
        page_icon="🤖",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # Render the sidebar
    render_sidebar()

    # Main application flow
    page = st.session_state.page

    if page == "🏠 Home":
        render_home()
    elif page == "📄 Resume":
        render_resume()
    elif page == "🎯 Interview":
        render_interview()
    elif page == "📊 Results":
        render_results()
    elif page == "🤖 AI Feedback":
        render_feedback()

if __name__ == "__main__":
    main()