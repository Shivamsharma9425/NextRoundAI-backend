from datetime import datetime, timezone


def job_description_document(
    user_id: str,
    title: str,
    company: str,
    jd_text: str
):

    return {

        "user_id": user_id,

        "title": title,

        "company": company,

        "jd_text": jd_text,

        "created_at": datetime.now(timezone.utc)

    }