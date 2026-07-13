from datetime import datetime, timezone

def user_document(
    name: str,
    email: str,
    password: str
):
    return {
        "name": name,
        "email": email,
        "password": password,
        "created_at": datetime.now(timezone.utc)
    }