import time
from app.core.logger import logger
from app.core.retry import retry_llm
from app.schemas.resume_analysis import ResumeAnalysis
from app.services.llm_service import MODELS, get_llm


@retry_llm()
async def analyze_resume(
    resume_text: str
):

    prompt = f"""
    You are an expert resume parser.

    Extract:

    - Name
    - Email
    - Phone
    - Skills
    - Projects
    - Education
    - Experience

    Return structured data.

    Resume:

    {resume_text}
    """

    start = time.perf_counter()
    
    
    last_error = None

    for model in MODELS:
        try:
            llm = get_llm(model)

            structured_llm = llm.with_structured_output(ResumeAnalysis)

            result = await structured_llm.ainvoke(prompt)

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
        "Resume analysis completed."
    )

    return result