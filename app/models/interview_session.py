from datetime import datetime, timezone


def interview_session_document(

    user_id: str,

    job_id: str,

    session: dict

):

    return {

        "user_id": user_id,

        "job_id": job_id,

        "session": session,

        "status": "created",

        "current_question": 0,

        "overall_score": 0,

        "completed": False,

        "questions": [],

        "created_at": datetime.now(timezone.utc),

        "updated_at": datetime.now(timezone.utc)

    }