from pydantic import BaseModel

class Experience(BaseModel):
    company: str
    role: str
    
class Education(BaseModel):
    degree: str
    college: str
    cgpa: str
    
    
class ResumeAnalysis(BaseModel):
    name: str
    email: str
    phone: str
    skills: list[str]
    projects: list[str]
    experience: list[Experience]
    education: Education
    
