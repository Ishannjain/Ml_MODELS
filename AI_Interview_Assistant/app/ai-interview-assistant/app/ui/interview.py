from datetime import datetime
import streamlit as st

def interview_configuration():
    st.markdown(
        '<div class="section-title">'
        '🎯 Interview Configuration'
        '</div>',
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)

    with col1:
        candidate_name = st.text_input(
            "Candidate Name",
            value=st.session_state.candidate_name
        )
        st.session_state.candidate_name = candidate_name

    with col2:
        number_questions = st.number_input(
            "Number of Questions",
            min_value=3,
            max_value=30,
            value=10
        )

    st.write(
        f"Interview Type: **{st.session_state.interview_type}**"
    )

    st.write(
        f"Difficulty: **{st.session_state.difficulty}**"
    )

    st.divider()

    if st.button(
        "▶️ Start Interview",
        type="primary",
        use_container_width=True
    ):
        st.session_state.interview_started = True
        st.session_state.current_question = 0
        st.session_state.answers = []
        st.session_state.interview_finished = False

        st.success(
            "Interview started successfully!"
        )
        st.rerun()

def interview_room():
    st.divider()
    st.subheader("🎤 Interview Room")

    question_number = st.session_state.current_question + 1
    st.progress(min(question_number / 10, 1.0))
    st.write(f"Question {question_number}")

    questions = [
        "Tell me about yourself.",
        "Explain one important project you have worked on.",
        "What are your strongest technical skills?",
        "How would you debug a production issue?",
        "Explain a difficult technical problem you solved."
    ]

    question_index = st.session_state.current_question % len(questions)
    current_question = questions[question_index]

    st.markdown(f"### ❓ {current_question}")

    answer = st.text_area(
        "Your Answer",
        height=220,
        placeholder="Type your answer here..."
    )

    if st.button("Submit Answer", type="primary", use_container_width=True):
        if not answer.strip():
            st.warning("Please provide an answer before submitting.")
        else:
            st.session_state.answers.append({
                "question": current_question,
                "answer": answer,
                "timestamp": datetime.now().isoformat()
            })

            st.session_state.current_question += 1

            if st.session_state.current_question >= 5:
                st.session_state.interview_finished = True
                st.success("Interview completed!")
            else:
                st.success("Answer submitted successfully.")
            st.rerun()