from app.database.database import db


async def save_skill_gap(
    skill_gap_data: dict
):
    result = await db.skill_gap_analysis.insert_one(
        skill_gap_data
    )

    return result.inserted_id


async def get_skill_gap(
    user_id: str,
    job_id: str
):
    return await db.skill_gap_analysis.find_one(
        {
            "user_id": user_id,
            "job_id": job_id
        }
    )


async def update_skill_gap(
    user_id: str,
    job_id: str,
    data: dict
):
    return await db.skill_gap_analysis.update_one(
        {
            "user_id": user_id,
            "job_id": job_id
        },
        {
            "$set": data
        }
    )


async def delete_skill_gap(
    user_id: str,
    job_id: str
):
    return await db.skill_gap_analysis.delete_one(
        {
            "user_id": user_id,
            "job_id": job_id
        }
    )