from app.database.database import db


async def save_job_analysis(data: dict):

    result = await db.job_analysis.insert_one(
        data
    )

    return result.inserted_id


async def get_job_analysis(job_id: str):

    return await db.job_analysis.find_one(
        {
            "job_id": job_id
        }
    )