from dataclasses import dataclass, field

@dataclass
class InterviewState:
    interview_started: bool = False
    current_question: int = 0
    answers: list = field(default_factory=list)
    interview_finished: bool = False
    candidate_name: str = "Candidate"
    resume_uploaded: bool = False
    interview_type: str = "Technical"
    difficulty: str = "Medium"

def reset_interview(state: InterviewState):
    state.interview_started = False
    state.current_question = 0
    state.answers = []
    state.interview_finished = False
    state.resume_uploaded = False
    return state