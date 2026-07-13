from fastapi import FastAPI # type: ignore

from app.api.interview import router as interview_router
from app.api.job import router as job_router
from app.api.test_llm import router as test_llm
from app.api.resume_analysis import router as analysis_router
from app.api.health import router as health_router
from app.api.auth import router as auth_router
from app.api.skill_gap import router as skill_gap_router
from app.api.user import (
    router as user_router
)
from app.api.resume import (
    router as resume_router
)
from app.api.job_analysis import (
    router as job_analysis_router
)
from fastapi.middleware.cors import CORSMiddleware



app = FastAPI(
    title="NextRound AI API"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://next-round-ai-frontend.vercel.app",  # replace later
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(
    health_router,
    prefix="/api"
)


app.include_router(
    test_llm,
    prefix="/api/test_llm",
    tags=["Testing"]
)

app.include_router(
    auth_router,
    prefix="/api/auth",
    tags=["Auth"]
)
app.include_router(
    user_router,
    prefix="/api/users",
    tags=["Users"]
)

app.include_router(
    resume_router,
    prefix="/api/resume",
    tags=["Resume"]
)

app.include_router(
    analysis_router,
    prefix="/api/resume",
    tags=["Resume Analysis"]
)

app.include_router(

    job_router,

    prefix="/api/job",

    tags=["Job Description"]

)

app.include_router(
    job_analysis_router,
    prefix="/api/job",
    tags=["Job Analysis"]
)

app.include_router(
    skill_gap_router,
    prefix="/api/job",
    tags=["Skill Gap"]
)

app.include_router(

    interview_router,

    prefix="/api/interview",

    tags=["Interview"]

)
# 6a3d4f5298ca79d902ca2e86
# 6a3cab825afa9013ee5969fd


# Error Code Guide--
# | Situation             |                   Status Code |
# | --------------------- | ----------------------------: |
# | Invalid request/body  |           **400 Bad Request** |
# | Unauthorized          |          **401 Unauthorized** |
# | Forbidden             |             **403 Forbidden** |
# | Resource not found    |             **404 Not Found** |
# | Duplicate/conflict    |              **409 Conflict** |
# | Internal server error | **500 Internal Server Error** |
