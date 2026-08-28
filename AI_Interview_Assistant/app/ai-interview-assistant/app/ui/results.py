from pathlib import Path
import streamlit as st
import json

# Project Paths
BASE_DIR = Path.cwd()
EVALUATION_FILE = BASE_DIR / "data" / "evaluation_report.json"

def load_json_file(file_path):
    if not file_path.exists():
        return None
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)
    except Exception as e:
        st.error(f"Unable to load {file_path.name}: {e}")
        return None

def display_results():
    st.markdown(
        '<div class="section-title">'
        '📊 Interview Results'
        '</div>',
        unsafe_allow_html=True
    )

    evaluation_data = load_json_file(EVALUATION_FILE)

    if evaluation_data is None:
        st.warning("evaluation_report.json is not available yet.")
    else:
        st.success("Evaluation report loaded.")

        overall_score = evaluation_data.get("overall_score", evaluation_data.get("score", None))

        if overall_score is not None:
            st.metric("Overall Score", f"{overall_score}/100")

        st.divider()

        questions = evaluation_data.get("questions", evaluation_data.get("evaluations", []))

        if questions:
            st.subheader("Question-wise Evaluation")
            for index, item in enumerate(questions, start=1):
                with st.expander(f"Question {index}"):
                    question = item.get("question", "Question")
                    answer = item.get("answer", "Answer not available")
                    score = item.get("score", item.get("overall_score", "N/A"))

                    st.write(f"**Question:** {question}")
                    st.write(f"**Answer:** {answer}")
                    st.write(f"**Score:** {score}")