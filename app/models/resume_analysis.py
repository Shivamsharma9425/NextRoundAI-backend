from datetime import datetime, timezone

def analysis_document(
    user_id: str,
    analysis: dict
):

    return {
        "user_id": user_id,
        "analysis": analysis,
        "created_at": datetime.now(timezone.utc)
    }