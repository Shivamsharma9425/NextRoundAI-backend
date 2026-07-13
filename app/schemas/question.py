from pydantic import BaseModel


class InterviewQuestion(BaseModel):

    question: str