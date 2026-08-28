from pathlib import Path
import streamlit as st

# Project Paths
BASE_DIR = Path.cwd()

# Sidebar UI Components
def render_sidebar():
    st.title("🤖 AI Interviewer")
    st.divider()

    st.subheader("Interview Settings")
    st.session_state.interview_type = st.selectbox(
        "Interview Type",
        [
            "Technical",
            "Behavioral",
            "Mixed",
            "HR",
            "Technical + HR"
        ]
    )

    st.session_state.difficulty = st.selectbox(
        "Difficulty",
        [
            "Easy",
            "Medium",
            "Hard",
            "Adaptive"
        ],
        index=1
    )

    st.divider()

    st.subheader("Navigation")
    page = st.radio(
        "Go to",
        [
            "🏠 Home",
            "📄 Resume",
            "🎯 Interview",
            "📊 Results",
            "🤖 AI Feedback"
        ]
    )

    st.divider()

    if st.button("🔄 Reset Interview", use_container_width=True):
        reset_interview()

    return page

def reset_interview():
    st.session_state.interview_started = False
    st.session_state.current_question = 0
    st.session_state.answers = []
    st.session_state.interview_finished = False
    st.session_state.resume_uploaded = False
    st.rerun()