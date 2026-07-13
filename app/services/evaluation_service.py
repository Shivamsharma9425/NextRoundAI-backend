from app.services.llm_service import MODELS, get_llm
from app.schemas.evaluation import Evaluation
from app.repositories.interview_repository import (
    get_interview_session,
    save_evaluation,
    update_interview_session
)
import time
from app.core.logger import logger
from app.core.retry import retry_llm
from fastapi import HTTPException # type: ignore





@retry_llm()
async def evaluate_answer(

    interview_id: str,

    question_number: int

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
    # Validate Question Number
    # -------------------------

    if question_number < 1:

        raise HTTPException(

            status_code=400,

            detail="Invalid question number."

        )

    if question_number > len(

        interview["questions"]

    ):

        raise HTTPException(

            status_code=404,

            detail="Question does not exist."

        )

    # -------------------------
    # Question
    # -------------------------

    question = interview["questions"][

        question_number - 1

    ]
    # -------------------------
    # Already Evaluated
    # -------------------------

    if question.get("evaluation") is not None:

        return {
            "question_number": question_number,
            **question["evaluation"]
        }
        
    if question["answer"] is None:

        raise HTTPException(

            status_code=400,

            detail="Answer not submitted."

        )

    # -------------------------
    # Prompt
    # -------------------------

    prompt = f"""
You are a senior software engineer conducting a live interview.

Evaluate the candidate's answer.

Question:

{question["question"]}

Candidate Answer:

{question["answer"]}

Skill Being Evaluated:

{question["skill"]}

Evaluation Rules:

- Be fair and objective.

- Score between 0 and 10.

- Mention what the candidate did well.

- Mention important concepts that were missed.

- Give concise feedback.

- Provide an ideal spoken answer that could reasonably be given in 30 to 90 seconds during a live interview.
Return:

1. score

2. strengths

3. missing_points

4. feedback

5. ideal_answer

Return structured output only.
"""

    # -------------------------
    # LLM
    # -------------------------

    start = time.perf_counter()


    for model in MODELS:
        try:
            llm = get_llm(model)

            structured_llm = llm.with_structured_output(Evaluation)

            evaluation = await structured_llm.ainvoke(prompt)

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
    # Save Evaluation
    # -------------------------

    await save_evaluation(

        interview_id,

        question_number,

        evaluation.model_dump()

    )
    logger.info(

        f"Question {question_number} evaluated | "

        f"Score={evaluation.score}/10"

    )

    # -------------------------
    # Recalculate Overall Score
    # -------------------------

    overall_score = 0

    for q in interview["questions"]:

        if q.get("evaluation"):

            overall_score += q["evaluation"]["score"]

    # Add current evaluation because it is not yet
    # present in the interview variable (it was just generated)

    overall_score += evaluation.score

    await update_interview_session(

        interview_id,

        {

            "overall_score": overall_score

        }

    )
    logger.info(
        f"Overall score updated | interview_id={interview_id} | score={overall_score}"
    )
        

    # -------------------------
    # Response
    # -------------------------

    return {

        "question_number": question_number,

        "score": evaluation.score,

        "strengths": evaluation.strengths,

        "missing_points": evaluation.missing_points,

        "feedback": evaluation.feedback,

        "ideal_answer": evaluation.ideal_answer

    }