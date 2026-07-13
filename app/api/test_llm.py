from fastapi import APIRouter # type: ignore
from app.services.llm_service import MODELS, get_llm

router = APIRouter()

@router.get("/test")
async def test_llm():

    for model in MODELS:
        try:
            llm = get_llm(model)



            result = await llm.ainvoke("hi, how r u")

            print(f"Using model: {model}")
            # print(result)

            break

        except Exception as e:
            print(f"{model} failed. Trying next model...")
            last_error = e

    else:
        raise last_error