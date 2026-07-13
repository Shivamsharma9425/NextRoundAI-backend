from pydantic import BaseModel
from typing import List, Dict, Any
from typing import Optional


# ---------------------------------
# Generic API Response
# ---------------------------------

class ApiResponse(BaseModel):
    success: bool
    message: str


# ---------------------------------
# Interview Create Response
# ---------------------------------

class InterviewSessionResponse(BaseModel):

    interview_id: str
    interview_title: str
    difficulty: str
    categories: List[str]
    total_questions: int
    estimated_duration: int
    instructions: List[str]
    status: str

# ---------------------------------
# Start Interview Response
# ---------------------------------

class StartInterviewResponse(BaseModel):

    interview_id: str

    status: str

    current_question: int

    total_questions: int
    

# ---------------------------------
# Question Response
# ---------------------------------

class InterviewQuestionResponse(BaseModel):

    question_number: int

    skill: str

    difficulty: str

    question: str


# ---------------------------------
# Answer Response
# ---------------------------------

class SubmitAnswerResponse(BaseModel):

    message: str


# ---------------------------------
# Evaluation Response
# ---------------------------------

class EvaluationResponse(BaseModel):

    question_number: int

    score: float

    strengths: List[str]

    missing_points: List[str]

    feedback: str

    ideal_answer: str


# ---------------------------------
# Interview Turn Response
# ---------------------------------



class InterviewTurnResponse(BaseModel):

    evaluation: Dict[str, Any]

    completed: bool

    next_question: Optional[Dict[str, Any]] = None

    report: Optional[Dict[str, Any]] = None
# ---------------------------------
# Interview Report Response
# ---------------------------------

class InterviewReportResponse(BaseModel):

    overall_score: float

    overall_rating: str

    strengths: List[str]

    improvement_areas: List[str]

    hiring_recommendation: str

    final_feedback: str