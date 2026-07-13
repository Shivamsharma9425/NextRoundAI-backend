from app.services.llm_service import MODELS, get_llm
from app.schemas.interview_session import InterviewSession
from app.repositories.analysis_repository import get_analysis
from app.repositories.job_analysis_repository import get_job_analysis
from app.repositories.skill_gap_repository import get_skill_gap
from app.repositories.interview_repository import save_interview_session
from app.core.logger import logger
from app.models.interview_session import interview_session_document
from fastapi import HTTPException # type: ignore
import time
from app.core.retry import retry_llm
from app.repositories.interview_repository import (
    get_interviews_by_user,
    get_interview_session,
    delete_interview,
    update_interview_session

)
# start interview service
from datetime import datetime, timezone



@retry_llm()
async def create_interview_session(

    user_id: str,

    job_id: str

):

    # -------------------------
    # Resume Analysis
    # -------------------------

    resume = await get_analysis(
        user_id
    )

    if not resume:
        raise HTTPException(

            status_code=404,

            detail="Resume analysis not found."

        )

    # -------------------------
    # Job Analysis
    # -------------------------

    job = await get_job_analysis(
        job_id
    )

    if not job:
        raise HTTPException(

            status_code=404,

            detail="Job analysis not found."

        )

    # -------------------------
    # Skill Gap
    # -------------------------

    skill_gap = await get_skill_gap(

        user_id,

        job_id

    )

    if not skill_gap:
        raise HTTPException(

            status_code=404,

            detail="Skill gap analysis not found."

        )

    # -------------------------
    # Prompt
    # -------------------------

    prompt = f"""
You are an experienced technical interviewer.

Candidate Resume:

{resume["analysis"]}

Job Description:

{job["analysis"]}

Skill Gap Analysis:

{skill_gap["analysis"]}

Design an interview session.

Do NOT generate interview questions.

Generate ONLY:

1. interview_title
2. difficulty
3. estimated_duration
4. total_questions
5. categories
6. instructions

Rules:

- estimated_duration MUST be between 5 and 8 minutes.

- total_questions MUST be between 5 and 8.

- Difficulty must be one of:
Easy
Medium
Hard

- Categories should only contain:
Technical
Projects
Behavioral
HR
Problem Solving
System Design

- Instructions should contain exactly 3 short tips.

Do NOT generate interview questions.

Return structured output only.
"""

    # -------------------------
    # LLM
    # -------------------------

    start = time.perf_counter()

    for model in MODELS:
        try:
            llm = get_llm(model)

            structured_llm = llm.with_structured_output(InterviewSession)

            session = await structured_llm.ainvoke(prompt)

            print(f"Using model: {model}")

            break

        except Exception as e:
            print(f"{model} failed. Trying next model...")
            last_error = e

    else:
        raise last_error

    end = time.perf_counter()

    logger.info(
        f"LLM response time: {end - start:.2f}s"
    )
    
    # -------------------------
    # Validate Interview Session
    # -------------------------

   # Duration: minimum 5, maximum 8 minutes
    session.estimated_duration = min(
        max(session.estimated_duration, 5),
        8
    )

    # Questions: minimum 5, maximum 8
    session.total_questions = min(
        max(session.total_questions, 5),
        8
    )

    # -------------------------
    # Mongo Document
    # -------------------------

    document = interview_session_document(

        user_id=user_id,

        job_id=job_id,

        session=session.model_dump()

    )

    interview_id = await save_interview_session(
        document
    )
    logger.info(
        f"Interview session created | interview_id={interview_id}"
    )
    # -------------------------
    # Response
    # -------------------------

    return {

    "interview_id": str(interview_id),

    "interview_title": session.interview_title,

    "difficulty": session.difficulty,

    "categories": session.categories,

    "total_questions": session.total_questions,

    "estimated_duration": session.estimated_duration,

    "instructions": session.instructions,

    "status": "created"

}
    
  
  
  


async def start_interview(

    interview_id: str

):

    interview = await get_interview_session(

        interview_id

    )

    if not interview:

        raise HTTPException(

            status_code=404,

            detail="Interview session not found."

        )

    if interview["status"] == "completed":

        raise HTTPException(

            status_code=409,

            detail="Interview already completed."

        )

    if interview["status"] == "in_progress":

        raise HTTPException(

            status_code=409,

            detail="Interview already started."

        )

    await update_interview_session(

        interview_id,

        {

            "status": "in_progress",

            "updated_at": datetime.now(

                timezone.utc

            )

        }

    )
    logger.info(

        f"Interview started | "

        f"Interview={interview_id}"

    )
    

    updated = await get_interview_session(

        interview_id

    )

    return {

        "interview_id": str(updated["_id"]),

        "status": updated["status"],

        "current_question": updated["current_question"],

        "total_questions": updated["session"]["total_questions"]

    }
    
async def get_interview_history(
    user_id: str
):
    interviews = await get_interviews_by_user(
        user_id
    )

    history = []

    for interview in interviews:

        session = interview.get("session", {})
        report = interview.get("report", {})

        history.append(
        {
            "interview_id": str(interview["_id"]),

            "title": session.get(
                "interview_title",
                "Untitled Interview"
            ),

            "difficulty": session.get(
                "difficulty",
                "Medium"
            ),

            "score": report.get(
                "overall_score",
                None
            ),

            "status": interview.get(
                "status",
                "created"
            ),

            "questions": session.get(
                "total_questions",
                0
            ),

            "duration": session.get(
                "estimated_duration",
                0
            ),

            # 👇 ADD THESE
            "categories": session.get(
                "categories",
                []
            ),

            "instructions": session.get(
                "instructions",
                []
            ),

            "created_at": interview.get(
                "created_at"
            )
        }
    )
            

    return history

async def get_interview_report(
    interview_id: str,
    user_id: str
):
    interview = await get_interview_session(
        interview_id
    )

    if not interview:

        raise HTTPException(
            status_code=404,
            detail="Interview not found."
        )

    if interview["user_id"] != user_id:

        raise HTTPException(
            status_code=403,
            detail="Unauthorized."
        )

    return interview["report"]

async def delete_interview_session(
    interview_id: str,
    user_id: str
):
    interview = await get_interview_session(
        interview_id
    )

    if not interview:

        raise HTTPException(
            status_code=404,
            detail="Interview not found."
        )

    if interview["user_id"] != user_id:

        raise HTTPException(
            status_code=403,
            detail="Unauthorized."
        )

    await delete_interview(
        interview_id
    )

    return {
        "success": True,
        "message": "Interview deleted."
    }
    
async def get_dashboard_stats(
    user_id: str
):
    interviews = await get_interviews_by_user(
        user_id
    )

    completed = [
        i
        for i in interviews
        if i.get("completed")
    ]

    total = len(completed)

    if total == 0:

        return {
            "total_interviews": 0,
            "average_score": 0,
            "best_score": 0
        }

    scores = [
        i["report"]["overall_score"]
        for i in completed
    ]

    return {
        "total_interviews": total,

        "average_score": round(
            sum(scores) / total,
            2
        ),

        "best_score": max(scores)
    }