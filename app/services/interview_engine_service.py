from app.services.answer_service import submit_answer

from app.services.evaluation_service import evaluate_answer

from app.services.question_service import generate_next_question
from fastapi import HTTPException # type: ignore


async def interview_turn(

    interview_id: str,

    question_number: int,

    answer: str

):

    # -------------------------
    # Save Candidate Answer
    # -------------------------

    await submit_answer(

        interview_id,

        question_number,

        answer

    )

    # -------------------------
    # Evaluate Answer
    # -------------------------

    evaluation = await evaluate_answer(

        interview_id,

        question_number

    )

    # -------------------------
    # Generate Next Question
    # -------------------------

    next = await generate_next_question(
    interview_id
    )

    # Interview finished
    if "overall_score" in next:

        return {
            "evaluation": evaluation,
            "completed": True,
            "report": next
        }

    # Continue interview
    return {
        "evaluation": evaluation,
        "completed": False,
        "next_question": next
    }