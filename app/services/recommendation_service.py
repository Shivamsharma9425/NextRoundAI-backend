from app.schemas.recommendation import Recommendation
import time
from app.core.logger import  logger
from app.core.retry import retry_llm
from app.services.llm_service import MODELS, get_llm




@retry_llm()
async def generate_recommendations(
    missing_skills: list[str]
):

    if not missing_skills:

        return Recommendation(

            learning_roadmap=[],

            priority=[],

            project_suggestions=[],

            courses=[]

        )

    prompt = f"""
You are an experienced software engineering career mentor.

A candidate is missing these skills:

{", ".join(missing_skills)}

Generate recommendations.

IMPORTANT:

Return ONLY the information requested.

learning_roadmap:
- A list of learning steps.

priority:
- A list of skills ordered from highest priority to lowest.

project_suggestions:
- A list of project ideas.

courses:
- A list of recommended courses.

Keep every item short.
"""

    start = time.perf_counter()

    last_error = None

    for model in MODELS:
        try:
            llm = get_llm(model)

            structured_llm = llm.with_structured_output(Recommendation)

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
        f"LLM response time: {end - start:.2f}s"
    )

    return result