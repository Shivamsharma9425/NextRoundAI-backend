from pydantic import BaseModel

class ExperienceRequirement(BaseModel):
    minimum_years: int
    level: str


class EducationRequirement(BaseModel):
    degree: str
    field: str


class JobAnalysis(BaseModel):

    title: str

    required_skills: list[str]

    preferred_skills: list[str]

    responsibilities: list[str]

    education: EducationRequirement

    experience: ExperienceRequirement