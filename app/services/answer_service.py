from app.repositories.interview_repository import (

    get_interview_session,

    save_answer

)
from app.core.logger import logger
from fastapi import HTTPException # type: ignore


async def submit_answer(

    interview_id: str,

    question_number: int,

    answer: str

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
    
    if not answer.strip():

        raise HTTPException(

            status_code=400,

            detail="Answer cannot be empty."

        )
    if interview["completed"]:

        raise HTTPException(

            status_code=409,

            detail="Interview already completed."

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
    # Already Answered
    # -------------------------

    if question.get("answer") is not None:

        raise HTTPException(

            status_code=409,

            detail="Answer already submitted."

        )

    # -------------------------
    # Save Answer
    # -------------------------

    await save_answer(

        interview_id,

        question_number,

        answer

    )  
    logger.info(

        f"Answer submitted | "

        f"Interview={interview_id} | "

        f"Question={question_number}"

    )

    # -------------------------
    # Response
    # -------------------------

    return {

        "success": True,

        "message": "Answer submitted successfully."

    }