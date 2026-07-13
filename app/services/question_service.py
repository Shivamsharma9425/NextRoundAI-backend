import random
import time
from datetime import datetime, timezone
from app.schemas.question import InterviewQuestion
from app.repositories.interview_repository import (
    get_interview_session,
    append_question, update_interview_session
)
from app.repositories.skill_gap_repository import (
    get_skill_gap
)
from fastapi import HTTPException # type: ignore
from app.services.report_service import generate_report
from app.core.logger import logger
from app.core.retry import retry_llm
from app.services.llm_service import MODELS, get_llm


@retry_llm()
async def generate_next_question(
    interview_id: str
):

    # -------------------------
    # Interview Session
    # -------------------------

    interview = await get_interview_session(
        interview_id
    )
    # -------------------------
    # Interview Completed
    # -------------------------

    if len(interview["questions"]) >= interview["session"]["total_questions"]:
        logger.info("Interview completed. Generating report...")
        return await generate_report(
            interview_id
        )

    if not interview:
        raise HTTPException(

            status_code=404,

            detail="Interview session not found."

        )

    # -------------------------
    # Skill Gap
    # -------------------------

    skill_gap = await get_skill_gap(

        interview["user_id"],

        interview["job_id"]

    )

    if not skill_gap:
        raise HTTPException(

            status_code=404,

            detail="Skill gap not found."

        )

    # -------------------------
    # Already Asked Skills
    # -------------------------

    asked_skills = [

        question["skill"]

        for question in interview["questions"]

    ]

    # -------------------------
    # Select Next Skill
    # -------------------------

    selected_skill = None

    remaining_missing = [

        skill

        for skill in skill_gap["analysis"]["missing_skills"]

        if skill not in asked_skills

    ]

    if remaining_missing:

        top_skills = remaining_missing[:3]

        selected_skill = random.choice(
            top_skills
        )

    # Then matched skills

    if selected_skill is None:

        for skill in skill_gap["analysis"]["matched_skills"]:

            if skill not in asked_skills:

                selected_skill = skill

                break

    # -------------------------
    # Interview Finished
    # -------------------------

    if selected_skill is None:

        return await generate_report(
            interview_id
        )

    # -------------------------
    # Prompt
    # -------------------------

    prompt = f"""
You are a senior interviewer conducting a LIVE interview.

The interview should feel natural and conversational, exactly like a real interviewer speaking to a candidate.

Interview Information

Job Role:
{interview["session"]["interview_title"]}

Interview Difficulty:
{interview["session"]["difficulty"]}

Current Focus Area:
{selected_skill}

Question Number:
{len(interview["questions"]) + 1}

Instructions:

- Generate ONLY ONE interview question.

- The question should sound natural when spoken aloud.

- The candidate should be able to answer in about 30–90 seconds.

- Ask only ONE thing at a time.

- Keep the question concise (preferably under 30 words).

- Do NOT ask coding questions.

- Do NOT ask for complete system designs.

- Do NOT ask multipart questions.

- If the focus area is technical, ask a conceptual or practical question.

- If the focus area is behavioral or HR, ask an appropriate behavioral question.

- If the focus area name contains normalized words (for example "restapis" or "vectordatabases"), interpret them naturally before generating the question.

Examples:

Technical:
"What is a REST API?"
"Why would you use FastAPI?"
"What is dependency injection?"

Behavioral:
"Tell me about a challenging project you worked on."
"Describe a situation where you handled a conflict."

HR:
"Why do you want to join our company?"
"What motivates you as a software engineer?"

Return structured output only.
"""

    # -------------------------
    # LLM
    # -------------------------

    start = time.perf_counter()

    last_error = None

    for model in MODELS:
        try:
            llm = get_llm(model)

            structured_llm = llm.with_structured_output(InterviewQuestion)

            llm_question = await structured_llm.ainvoke(prompt)

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
    # Build Mongo Question
    # -------------------------

    question_document = {

        "question_number":

        len(interview["questions"]) + 1,

        "skill":

        selected_skill,

        "difficulty":

        interview["session"]["difficulty"],

        "question":

        llm_question.question,

        "answer":

        None,

        "evaluation":

        None,

        "created_at":

        datetime.now(timezone.utc)

    }

    # -------------------------
    # Save Question
    # -------------------------

    await append_question(

        interview_id,

        question_document

    )
    logger.info(

        f"Question {question_document['question_number']} generated | "

        f"Interview={interview_id} | "

        f"Skill={selected_skill}"

    )

    # -------------------------
    # Update Current Question
    # -------------------------

    await update_interview_session(

        interview_id,

        {

            "current_question": question_document["question_number"],

            "updated_at": datetime.now(timezone.utc)

        }

    )
    logger.info(
        f"Current question updated | interview_id={interview_id} | question={question_document['question_number']}"
    )
    # -------------------------
    # Response
    # -------------------------

    return {

        "question_number":

        question_document["question_number"],

        "skill":

        question_document["skill"],

        "difficulty":

        question_document["difficulty"],

        "question":

        question_document["question"]

    }