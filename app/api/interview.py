from fastapi import APIRouter, Depends # type: ignore

from app.services.interview_session_service import (
    create_interview_session, start_interview
)
from app.services.question_service import (
    generate_next_question
)

from app.schemas.question_response import (
    QuestionResponse
)

from app.schemas.answer import (
    AnswerRequest
)

from app.services.answer_service import (
    submit_answer
)
from app.services.interview_engine_service import (
    interview_turn
)


from app.core.dependencies import get_current_user

from app.services.interview_session_service import (
    get_interview_history,
    get_interview_report,
    delete_interview_session,
    get_dashboard_stats
)
from app.schemas.response import (

    ApiResponse,

    InterviewSessionResponse,

    InterviewQuestionResponse,

    SubmitAnswerResponse,

    InterviewTurnResponse,
    StartInterviewResponse

)


router = APIRouter()

@router.post(

    "/create/{job_id}",

    response_model=InterviewSessionResponse

)
async def create_interview(

    job_id: str,

    user_id: str

):

    return await create_interview_session(

        user_id=user_id,

        job_id=job_id

    )




@router.post(

    "/start/{interview_id}",

    response_model=StartInterviewResponse

)
async def start(

    interview_id: str

):

    return await start_interview(

        interview_id

    )




@router.post(

    "/next/{interview_id}",

    response_model=InterviewQuestionResponse

)
async def next_question(

    interview_id: str

):

    return await generate_next_question(

        interview_id

    )




@router.post(

    "/answer/{interview_id}",

    response_model=SubmitAnswerResponse

)
async def answer(

    interview_id: str,

    request: AnswerRequest

):

    return await submit_answer(

        interview_id,

        request.question_number,

        request.answer

    )




# Frontend only calls this endpoint.
# It internally saves answer, evaluates it,
# and generates the next question/report.

@router.post(

    "/respond/{interview_id}",

    response_model=InterviewTurnResponse

)
async def respond(

    interview_id: str,

    request: AnswerRequest

):

    return await interview_turn(

        interview_id,

        request.question_number,

        request.answer

    )
    
@router.get("/my-interviews")
async def my_interviews(
    user=Depends(get_current_user)
):
    return await get_interview_history(
        str(user["_id"])
    )
    
@router.get("/report/{interview_id}")
async def report(
    interview_id: str,
    user=Depends(get_current_user)
):
    return await get_interview_report(
        interview_id,
        str(user["_id"])
    )
    
@router.delete("/{interview_id}")
async def delete(
    interview_id: str,
    user=Depends(get_current_user)
):
    return await delete_interview_session(
        interview_id,
        str(user["_id"])
    )
    
@router.get("/stats")
async def stats(
    user=Depends(get_current_user)
):
    return await get_dashboard_stats(
        str(user["_id"])
    )