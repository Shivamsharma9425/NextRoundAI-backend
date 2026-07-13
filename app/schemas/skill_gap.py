from pydantic import BaseModel
from typing import List


class SkillGapAnalysis(BaseModel):
    match_score: float

    matched_skills: List[str]

    missing_skills: List[str]

    extra_skills: List[str]

    recommendations: List[str]