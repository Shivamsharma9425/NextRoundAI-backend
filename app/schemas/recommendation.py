from pydantic import BaseModel
from typing import List


class Recommendation(BaseModel):

    learning_roadmap: List[str]

    priority: List[str]

    project_suggestions: List[str]

    courses: List[str]