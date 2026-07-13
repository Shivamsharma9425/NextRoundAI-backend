from fastapi import APIRouter, Depends  # type: ignore

from app.core.dependencies import get_current_user

from app.repositories.job_repository import (
    get_job_description_by_id
)

from app.repositories.job_analysis_repository import (
    save_job_analysis
)

from app.models.job_analysis import (
    job_analysis_document
)

from app.services.job_analyzer import (
    analyze_job_description
)

router = APIRouter()

@router.post("/analyze/{job_id}")
async def analyze_job(
    job_id: str,
    user=Depends(get_current_user)
):

    job = await get_job_description_by_id(
        job_id
    )

    if not job:
        return {
            "message": "Job not found"
        }

    analysis = await analyze_job_description(
        job["jd_text"]
    )

    document = job_analysis_document(
        str(user["_id"]),
        job_id,
        analysis.model_dump()
    )

    analysis_id = await save_job_analysis(
        document
    )

    return {
        "analysis_id": str(analysis_id),
        "analysis": analysis
    }