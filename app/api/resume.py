from fastapi import APIRouter, UploadFile, File, Depends # type: ignore
from app.core.dependencies import (
    get_current_user
)
from app.repositories.resume_repository import (
    get_resume_by_user
)
from app.services.cloudinary_service import (
    upload_resume
)
from app.services.pdf_parser import (
    extract_text_from_pdf
)
from app.models.resume import (
    resume_document
)
from app.repositories.resume_repository import (
    create_resume
)
from fastapi import ( # type: ignore
    APIRouter,
    UploadFile,
    File,
    Depends,
    HTTPException
)

# User Uploads PDF
# #         │
# #         ▼
# # Resume API
# #         │
# #         ▼
# # Verify JWT
# #         │
# #         ▼
# # Save PDF Temporarily
# #         │
# #         ▼
# # Extract PDF Text
# #         │
# #         ▼
# # Upload PDF To Cloudinary
# #         │
# #         ▼
# # Create Resume Document
# #         │
# #         ▼
# # Store In MongoDB
# #         │
# #         ▼
# # Return Resume URL# 

router = APIRouter()


@router.post("/upload")
async def upload_resume_route(

    file: UploadFile = File(...),

    user=Depends(
        get_current_user
    )

):

    # -------------------------
    # File Validation
    # -------------------------

    if not file.filename.lower().endswith(".pdf"):

        raise HTTPException(

            status_code=400,

            detail="Only PDF files are allowed."

        )

    if file.content_type != "application/pdf":

        raise HTTPException(

            status_code=400,

            detail="Invalid file type."

        )

    # -------------------------
    # Save Temporary File
    # -------------------------

    temp_path = f"temp_{file.filename}"

    with open(

        temp_path,

        "wb"

    ) as buffer:

        buffer.write(

            await file.read()

        )
     
    parsed_text = extract_text_from_pdf(
        temp_path
    )
    
    file_url = upload_resume(
        temp_path
    )
    
    resume_data = resume_document(
        str(user["_id"]),
        file.filename,
        file_url,
        parsed_text
    )
    
    resume_id = await create_resume(
        resume_data
    )
    
    return {
        "success": True,
        "resume_id": str(
            resume_id
        ),
        "file_url": file_url
    }
    
    
@router.get("/my-resume")
async def get_resume(
    user=Depends(get_current_user)
):
    resume = await get_resume_by_user(
        str(user["_id"])
    )

    if not resume:
        return None
        # or raise HTTPException(
        #     status_code=404,
        #     detail="Resume not found."
        # )

    resume["_id"] = str(resume["_id"])
    return resume