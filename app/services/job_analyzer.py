from app.services.llm_service import MODELS, get_llm
from app.schemas.job_analysis import JobAnalysis
import time
from app.core.logger import logger
from app.core.retry import retry_llm

@retry_llm()
async def analyze_job_description(
    jd_text: str
):

    prompt = f"""
        You are an expert ATS and technical recruiter.

        Analyze this Job Description.

        Extract the following information from the Job Description.

        Return structured JSON.

        Fields:

        1. title

        2. required_skills

        3. preferred_skills

        4. responsibilities

        5. education
        - degree
        - field

        6. experience
        - minimum_years
        - level

        Rules:

        - minimum_years should be an integer.
        - level should be one of:
        Internship
        Fresher
        Junior
        Mid
        Senior
        Lead

        If information is missing,
        infer the closest reasonable value.

        Return structured data.

        Job Description:

        {jd_text}
    """

    start = time.perf_counter()

    last_error = None

    for model in MODELS:
        try:
            llm = get_llm(model)

            structured_llm = llm.with_structured_output(JobAnalysis)

            analysis = await structured_llm.ainvoke(prompt)

            print(f"Using model: {model}")

            break

        except Exception as e:
            print(f"{model} failed. Trying next model...")
            last_error = e

    else:
        raise last_error

    end = time.perf_counter()

    logger.info(
        f"LLM response time: {end-start:.2f}s"
    )

    logger.info(
        "Job analyzed successfully."
    )

    return analysis