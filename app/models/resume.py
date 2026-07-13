from datetime import datetime, timezone


def resume_document(
    user_id,
    file_name,
    file_url,
    parsed_text
):
    return {
        "user_id": user_id,
        "file_name": file_name,
        "file_url": file_url,
        "parsed_text": parsed_text,
        "created_at": datetime.now(timezone.utc)
    }