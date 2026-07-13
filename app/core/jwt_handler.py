from jose import jwt , JWTError# type: ignore
from datetime import datetime, timezone
from datetime import timedelta
from dotenv import load_dotenv
import os

load_dotenv()

SECRET_KEY = os.getenv(
    "JWT_SECRET"
)

if not SECRET_KEY:
    raise RuntimeError(
        "JWT_SECRET is missing."
    )
ALGORITHM = "HS256"

def create_access_token(
    data: dict
):

    payload = data.copy()

    expire = datetime.now(timezone.utc)+ timedelta(
        days=1
    )

    payload.update(
        {
            "exp": expire
        }
    )

    encoded_jwt = jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return encoded_jwt

def verify_access_token(
    token: str
):

    try:

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        return payload

    except JWTError:
        return None