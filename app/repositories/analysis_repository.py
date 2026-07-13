from app.database.database import db

async def save_analysis(data: dict):
    await db.resume_profiles.update_one(
        {"user_id": data["user_id"]},
        {"$set": data},
        upsert=True,
    )
async def get_analysis(
    user_id: str
):
    return await db.resume_profiles.find_one(
        {
            "user_id": user_id
        }
    )