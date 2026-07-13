from datetime import datetime, timezone


def job_analysis_document(
    user_id: str,
    job_id: str,
    analysis: dict
):

    return {

        "user_id": user_id,

        "job_id": job_id,

        "analysis": analysis,

        "created_at": datetime.now(timezone.utc),

        "updated_at": datetime.now(timezone.utc)

    }