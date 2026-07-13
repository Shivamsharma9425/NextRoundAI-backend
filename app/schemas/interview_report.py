from pydantic import BaseModel
from typing import List


class InterviewReport(BaseModel):

    overall_score: float

    overall_rating: str

    strengths: List[str]

    improvement_areas: List[str]

    hiring_recommendation: str

    final_feedback: str