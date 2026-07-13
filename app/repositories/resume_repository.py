from app.database.database import db

async def create_resume(
    resume_data: dict
):
    result = await db.resumes.insert_one(
        resume_data
    )

    return result.inserted_id

async def get_resume_by_user(
    user_id: str
):

    return await db.resumes.find_one(
        {
            "user_id": user_id
        }
    )