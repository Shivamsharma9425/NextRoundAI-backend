from pydantic import BaseModel


class JobDescriptionCreate(BaseModel):

    title: str

    company: str

    jd_text: str


class JobDescriptionResponse(BaseModel):

    id: str

    title: str

    company: str