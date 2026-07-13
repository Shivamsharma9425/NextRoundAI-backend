from pydantic import BaseModel


class ResumeResponse(BaseModel):
    file_url: str
    parsed_text: str