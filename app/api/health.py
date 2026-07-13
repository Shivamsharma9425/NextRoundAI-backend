from fastapi import APIRouter # type: ignore
from app.database.database import db

router = APIRouter()


@router.get("/health")
async def health_check():

    collections = await db.list_collection_names()

    return {
        "status": "healthy",
        "collections": collections
    }