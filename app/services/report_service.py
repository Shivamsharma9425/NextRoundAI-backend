from app.schemas.interview_report import InterviewReport
from app.repositories.interview_repository import (
    get_interview_session,
    save_report
)
from app.core.logger import logger
from fastapi import HTTPException # type: ignore
import time
from app.core.retry import retry_llm
from app.services.llm_service import MODELS, get_llm




@retry_llm()
async def generate_report(
    interview_id: str
):

    # -------------------------
    # Interview Session
    # -------------------------

    interview = await get_interview_session(
        interview_id
    )

    if not interview:
        raise HTTPException(

            status_code=404,

            detail="Interview session not found."

        )

    # -------------------------
    # Overall Score
    # -------------------------

    total_questions = len(interview["questions"])

    if total_questions == 0:
        raise HTTPException(

            status_code=400,

            detail="Interview contains no questions."

        )

    overall_score = round(

        (
            interview["overall_score"]
            /
            (total_questions * 10)
        ) * 100,

        2

    )

    # -------------------------
    # Evaluation Summary
    # -------------------------

    evaluation_summary = ""

    for question in interview["questions"]:

        evaluation = question.get("evaluation")

        if evaluation is None:
            continue

        evaluation_summary += f"""

Skill:
{question["skill"]}

Score:
{evaluation["score"]}/10

Strengths:
{", ".join(evaluation["strengths"])}

Missing Points:
{", ".join(evaluation["missing_points"])}

Feedback:
{evaluation["feedback"]}

---------------------------------------

"""

    # -------------------------
    # Prompt
    # -------------------------

    prompt = f"""
You are a senior engineering hiring manager.

Overall Candidate Score:

{overall_score}/100

Below are evaluations from each interview question.

{evaluation_summary}

Generate the final interview report.

Rules:

- Do NOT change the overall score.

- Overall rating must be one of:
Excellent
Good
Average
Needs Improvement

- Summarize recurring strengths.

- Summarize recurring improvement areas.

- Hiring recommendation must be one of:
Strong Hire
Hire
Borderline
Reject

- Final feedback should be concise and professional.

Return structured output only.
"""

    # -------------------------
    # LLM
    # -------------------------
    logger.info(
       f"Generating final report | Interview={interview_id}"
    )
    start = time.perf_counter()
    
    
    last_error = None

    for model in MODELS:
        try:
            llm = get_llm(model)

            structured_llm = llm.with_structured_output(InterviewReport)

            report = await structured_llm.ainvoke(prompt)

            print(f"Using model: {model}")

            break

        except Exception as e:
            print(f"{model} failed. Trying next model...")
            last_error = e

    else:
        raise last_error
    
    
    
    end = time.perf_counter()
    logger.info(

        f"Report generated in {end-start:.2f} seconds | "

        f"Interview={interview_id}"

    )   
    
    # -------------------------
    # Save Report
    # -------------------------

    report_data = report.model_dump()
    report_data["overall_score"] = overall_score
    report_data["total_questions"] = total_questions
    report_data["duration"] = interview["session"]["estimated_duration"]
    skill_scores = []

    for question in interview["questions"]:

        evaluation = question.get("evaluation")

        if not evaluation:
            continue

        skill_scores.append(
            {
                "name": question["skill"],
                "score": evaluation["score"] * 10
            }
        )

    report_data["skill_scores"] = skill_scores

    await save_report(

        interview_id,

        report_data

    )
    logger.info(

        f"Final report saved | "

        f"Interview={interview_id}"

    )

    # -------------------------
    # Response
    # -------------------------

    return report_data