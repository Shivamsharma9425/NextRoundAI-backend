from fastapi import Depends # type: ignore
from fastapi import HTTPException # type: ignore
from fastapi.security import HTTPBearer  # type: ignore
from fastapi.security import HTTPAuthorizationCredentials  # type: ignore

from app.core.jwt_handler import (
    verify_access_token
)

from app.repositories.user_repository import (
    get_user_by_id
)

security = HTTPBearer()

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(
        security
    )
):

    token = credentials.credentials

    payload = verify_access_token(
        token
    )

    if not payload:

        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )

    user_id = payload.get("sub")

    if not user_id:

        raise HTTPException(
            status_code=401,
            detail="Invalid token payload"
        )

    user = await get_user_by_id(
        user_id
    )

    if not user:

        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return user