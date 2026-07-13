from pydantic import BaseModel
from typing import List


class Evaluation(BaseModel):

    score: int

    strengths: List[str]

    missing_points: List[str]

    feedback: str

    ideal_answer: str
    
    