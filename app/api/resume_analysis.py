from fastapi import APIRouter, Depends # type: ignore

from app.core.dependencies import (
    get_current_user
)
from app.repositories.resume_repository import (
    get_resume_by_user
)
from app.repositories.analysis_repository import (
    save_analysis
)
from app.services.resume_analyzer import (
    analyze_resume
)
from app.models.resume_analysis import (
    analysis_document
)
from app.repositories.analysis_repository import (
    get_analysis
)
from fastapi import HTTPException # type: ignore

router = APIRouter()

@router.post("/analyze")
async def analyze(
    user=Depends(
        get_current_user
    )
):
    resume = await get_resume_by_user(
        str(user["_id"])
    )
    if not resume:

        raise HTTPException(

            status_code=404,

            detail="Resume not found."

        )
    analysis = await analyze_resume(
        resume["parsed_text"]
    )
    document = analysis_document(
        str(user["_id"]),
        analysis.model_dump()
    )
    await save_analysis(document)

    saved_analysis = await get_analysis(
        str(user["_id"])
    )

    return {
        "analysis_id": str(saved_analysis["_id"]),
        "analysis": analysis
    }
    
@router.get("/analysis")
async def get_analysis_route(
    user=Depends(get_current_user)
):
    analysis = await get_analysis(str(user["_id"]))

    if not analysis:
        raise HTTPException(
            status_code=404,
            detail="Analysis not found."
        )

    analysis["_id"] = str(analysis["_id"])

    return analysis