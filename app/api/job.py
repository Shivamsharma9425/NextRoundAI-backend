from fastapi import APIRouter,Depends # type:ignore

from app.core.dependencies import get_current_user

from app.schemas.job_description import JobDescriptionCreate

from app.models.job_description import (
    job_description_document
)

from app.repositories.job_repository import (
    create_job_description,
    get_jobs_by_user
)

router = APIRouter()

@router.post("/upload")
async def upload_job_description(

    job: JobDescriptionCreate,

    user=Depends(get_current_user)

):

    document = job_description_document(

        str(user["_id"]),

        job.title,

        job.company,

        job.jd_text

    )

    job_id = await create_job_description(
        document
    )

    return {

        "success": True,

        "job_id": str(job_id)

    }
    
@router.get("/my-jobs")
async def get_my_jobs(

    user=Depends(get_current_user)

):

    jobs = await get_jobs_by_user(
        str(user["_id"])
    )

    return jobs