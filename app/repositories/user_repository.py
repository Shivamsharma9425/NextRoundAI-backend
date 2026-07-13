from app.database.database import db
from bson import ObjectId # type: ignore

async def get_user_by_email(
    email: str
):
    return await db.users.find_one(
        {"email": email}
    )


async def get_user_by_id(
    user_id: str
):
    return await db.users.find_one(
        {
            "_id": ObjectId(user_id)
        }
    )

async def create_user(
    user_data: dict
):
    result = await db.users.insert_one(
        user_data
    )

    return result.inserted_id