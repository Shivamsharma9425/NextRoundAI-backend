from fastapi import APIRouter # type: ignore

from app.services.skill_gap_service import analyze


router = APIRouter()


@router.post("/skill-gap/{job_id}")
async def skill_gap(
    job_id: str,
    resume_id: str,
    user_id: str
):

    result = await analyze(
        user_id=user_id,
        job_id=job_id,
        resume_id=resume_id
    )

    return result