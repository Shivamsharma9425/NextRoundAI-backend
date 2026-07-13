from fastapi import APIRouter # type: ignore
from app.schemas.user import UserCreate
from app.repositories.user_repository import (
    get_user_by_email,
    create_user
)
from app.core.security import (
    hash_password
)
from app.models.user import (
    user_document
)
from app.schemas.auth import LoginRequest

from app.services.auth_service import (
    authenticate_user
)
from app.core.jwt_handler import (
    create_access_token
)

router = APIRouter()
 
@router.post("/signup")
async def signup(
    user: UserCreate
):

    existing_user = await get_user_by_email(
        user.email
    )

    if existing_user:

        return {
            "message":
            "User already exists"
        }

    hashed_password = hash_password(
        user.password
    )

    user_data = user_document(
        user.name,
        user.email,
        hashed_password
    )

    user_id = await create_user(
        user_data
    )

    return {
        "success": True,
        "message": "Account created",
        "user": {
            "id": str(user_id),
            "name": user.name,
            "email": user.email
        }
    }   
    
@router.post("/login")
async def login(
    credentials: LoginRequest
):

    user = await authenticate_user(
        credentials.email,
        credentials.password
    )

    if not user:
        return {
            "success": False,
            "message": "Invalid email or password"
        }

    token = create_access_token(
        {
            "sub": str(user["_id"]),
            "email": user["email"]
        }
    )

    return {
        "success": True,
        "access_token": token,
        "token_type": "bearer"
    }
    
