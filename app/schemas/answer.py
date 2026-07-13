from pydantic import BaseModel


class AnswerRequest(BaseModel):

    question_number: int

    answer: str