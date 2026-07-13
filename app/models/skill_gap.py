from datetime import datetime, timezone


def skill_gap_document(
    user_id: str,
    job_id: str,
    resume_id: str,
    analysis: dict
):

    return {

        "user_id": user_id,

        "job_id": job_id,

        "resume_id": resume_id,

        "analysis": analysis,

        "created_at": datetime.now(timezone.utc),

        "updated_at": datetime.now(timezone.utc)

    }