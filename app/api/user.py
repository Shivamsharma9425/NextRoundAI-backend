from fastapi import APIRouter # type: ignore
from fastapi import Depends # type: ignore

from app.core.dependencies import (
    get_current_user
)

router = APIRouter()

@router.get("/me")
async def current_user(
    user=Depends(
        get_current_user
    )
):

    return {
        "id": str(user["_id"]),
        "name": user["name"],
        "email": user["email"]
    }
    
@router.get("/profile")
async def profile(
    user=Depends(
        get_current_user
    )
):

    return {
        "name": user["name"],
        "email": user["email"],
        "created_at": user["created_at"]
    }