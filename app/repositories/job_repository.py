from app.database.database import db
from bson import ObjectId # type: ignore
from bson.errors import InvalidId # type: ignore
from fastapi import HTTPException # type: ignore


async def create_job_description(
    data: dict
):

    result = await db.job_descriptions.insert_one(
        data
    )

    return result.inserted_id


async def get_job_description_by_id(
    job_id: str
):

    try:

        object_id = ObjectId(job_id)

    except InvalidId:

        raise HTTPException(

            status_code=400,

            detail="Invalid job ID."

        )

    return await db.job_descriptions.find_one(

        {
            "_id": object_id
        }

    )


async def get_jobs_by_user(
    user_id: str
):

    jobs = []

    cursor = db.job_descriptions.find(
        {
            "user_id": user_id
        }
    )

    async for job in cursor:

        job["_id"] = str(job["_id"])

        jobs.append(job)

    return jobs