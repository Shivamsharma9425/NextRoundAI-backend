from app.services.recommendation_service import generate_recommendations

from app.repositories.analysis_repository import get_analysis
from app.repositories.job_analysis_repository import get_job_analysis
from app.repositories.skill_gap_repository import save_skill_gap
from fastapi import HTTPException # type: ignore
from app.core.logger import logger
from app.models.skill_gap import skill_gap_document


def normalize_skills(skills: list[str]):

    normalized = []

    for skill in skills:

        skill = skill.lower().strip().replace(" ", "")

        normalized.append(skill)

    return list(set(normalized))


def compare_skills(
    resume_skills,
    job_skills
):

    resume_set = set(resume_skills)

    job_set = set(job_skills)

    return {

        "matched": list(resume_set & job_set),

        "missing": list(job_set - resume_set),

        "extra": list(resume_set - job_set)

    }


def calculate_score(
    matched,
    required
):

    if len(required) == 0:
        return 0

    return round(

        (len(matched) / len(required)) * 100,

        2

    )


async def analyze(

    user_id: str,

    job_id: str,

    resume_id: str

):

    # -------------------------
    # Resume Analysis
    # -------------------------

    resume_analysis = await get_analysis(
        user_id
    )

    if not resume_analysis:
        raise HTTPException(

            status_code=404,

            detail="Resume analysis not found."

        )
    # -------------------------
    # Job Analysis
    # -------------------------

    job_analysis = await get_job_analysis(
        job_id
    )

    if not job_analysis:
        raise HTTPException(

            status_code=404,

            detail="Job analysis not found."

        )   

    # -------------------------
    # Extract Skills
    # -------------------------

    resume_skills = resume_analysis["analysis"]["skills"]

    job_skills = job_analysis["analysis"]["required_skills"]

    # -------------------------
    # Normalize Skills
    # -------------------------

    resume_skills = normalize_skills(
        resume_skills
    )

    job_skills = normalize_skills(
        job_skills
    )

    # -------------------------
    # Compare Skills
    # -------------------------

    comparison = compare_skills(

        resume_skills,

        job_skills

    )

    # -------------------------
    # Calculate Match Score
    # -------------------------

    score = calculate_score(

        comparison["matched"],

        job_skills

    )

    # -------------------------
    # Generate Recommendations
    # -------------------------

    recommendations = await generate_recommendations(

        comparison["missing"]

    )

    # -------------------------
    # Merge Result
    # -------------------------

    analysis = {

        "match_score": score,

        "matched_skills": comparison["matched"],

        "missing_skills": comparison["missing"],

        "extra_skills": comparison["extra"],

        "recommendations": recommendations.model_dump()

    }

    # -------------------------
    # Create Mongo Document
    # -------------------------

    document = skill_gap_document(

        user_id=user_id,

        job_id=job_id,

        resume_id=resume_id,

        analysis=analysis

    )

    # -------------------------
    # Save to MongoDB
    # -------------------------

    await save_skill_gap(
        document
    )
    logger.info(
        "Skill gap generated successfully."
    )
    # -------------------------
    # Return Response
    # -------------------------

    return analysis