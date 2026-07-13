from app.repositories.user_repository import (
    get_user_by_email
)

from app.core.security import (
    verify_password
)

async def authenticate_user(
    email: str,
    password: str
):

    user = await get_user_by_email(
        email
    )

    if not user:
        return None

    password_valid = verify_password(
        password,
        user["password"]
    )

    if not password_valid:
        return None

    return user