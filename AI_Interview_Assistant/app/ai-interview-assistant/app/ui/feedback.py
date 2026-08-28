from pathlib import Path
import streamlit as st
import json

# Project Paths
BASE_DIR = Path.cwd()
FEEDBACK_FILE = BASE_DIR / "data" / "feedback_report.json"

def load_feedback_report():
    if not FEEDBACK_FILE.exists():
        return None

    try:
        with open(FEEDBACK_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except Exception as e:
        st.error(f"Unable to load {FEEDBACK_FILE.name}: {e}")
        return None

def display_feedback():
    feedback_data = load_feedback_report()

    if feedback_data is None:
        st.warning("feedback_report.json is not available yet.")
        st.info("Complete the interview first to generate the AI feedback report.")
    else:
        st.markdown('<div class="section-title">🤖 AI Interview Feedback</div>', unsafe_allow_html=True)

        # Overall Feedback
        st.subheader("📌 Overall Feedback")
        st.info(feedback_data.get("overall_feedback", "No overall feedback available."))

        # Assessment
        assessment = feedback_data.get("overall_assessment", {})
        if assessment:
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Performance Level", assessment.get("performance_level", "N/A"))
            with col2:
                st.write(assessment.get("summary", ""))

        st.divider()

        # Strengths
        st.subheader("💪 Strengths")
        strengths = feedback_data.get("strengths", [])
        if strengths:
            for strength in strengths:
                st.success(f"✓ {strength}")
        else:
            st.write("No strengths available.")

        # Weaknesses
        st.subheader("⚠️ Areas to Improve")
        weaknesses = feedback_data.get("weaknesses", [])
        if weaknesses:
            for weakness in weaknesses:
                st.warning(f"⚠ {weakness}")

        # Technical Feedback
        st.subheader("💻 Technical Feedback")
        technical_feedback = feedback_data.get("technical_feedback", [])
        for item in technical_feedback:
            st.write(f"• {item}")

        # Communication Feedback
        st.subheader("🗣️ Communication Feedback")
        communication_feedback = feedback_data.get("communication_feedback", [])
        for item in communication_feedback:
            st.write(f"• {item}")

        # Improvement Areas
        st.subheader("📚 Improvement Areas")
        improvement_areas = feedback_data.get("improvement_areas", [])
        for area in improvement_areas:
            if isinstance(area, dict):
                st.markdown(f"**{area.get('area', 'Unknown')}**\n\nPriority: **{area.get('priority', 'N/A')}**\n\n{area.get('reason', '')}")
                st.divider()

        # Recommended Topics
        st.subheader("📖 Recommended Topics")
        recommended_topics = feedback_data.get("recommended_topics", [])
        for topic in recommended_topics:
            if isinstance(topic, dict):
                st.write(f"### {topic.get('topic', 'Topic')}")
                st.write(topic.get("reason", ""))

        # Study Plan
        st.subheader("🗓️ Personalized Study Plan")
        study_plan = feedback_data.get("study_plan", [])
        for plan in study_plan:
            if isinstance(plan, dict):
                day = plan.get("day", "?")
                focus = plan.get("focus", "Focus")
                action = plan.get("action", "")
                st.markdown(f"### Day {day} — {focus}\n\n{action}")

        # Interview Advice
        st.subheader("🎯 Interview Advice")
        interview_advice = feedback_data.get("interview_advice", [])
        for advice in interview_advice:
            st.write(f"• {advice}")