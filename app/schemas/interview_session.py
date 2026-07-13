from pydantic import BaseModel
from typing import List


class InterviewSession(BaseModel):

    interview_title: str

    difficulty: str

    estimated_duration: int

    total_questions: int

    categories: List[str]

    instructions: List[str]