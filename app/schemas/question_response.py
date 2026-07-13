from pydantic import BaseModel


class QuestionResponse(BaseModel):

    question_number: int

    skill: str

    difficulty: str

    question: str