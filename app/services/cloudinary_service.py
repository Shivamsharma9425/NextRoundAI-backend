import cloudinary # type: ignore
import cloudinary.uploader # type: ignore

from dotenv import load_dotenv
import os

load_dotenv()

CLOUDINARY_CLOUD_NAME = os.getenv(
    "CLOUDINARY_CLOUD_NAME"
)

CLOUDINARY_API_KEY = os.getenv(
    "CLOUDINARY_API_KEY"
)

CLOUDINARY_API_SECRET = os.getenv(
    "CLOUDINARY_API_SECRET"
)

if not CLOUDINARY_CLOUD_NAME:
    raise RuntimeError(
        "CLOUDINARY_CLOUD_NAME is missing."
    )

if not CLOUDINARY_API_KEY:
    raise RuntimeError(
        "CLOUDINARY_API_KEY is missing."
    )

if not CLOUDINARY_API_SECRET:
    raise RuntimeError(
        "CLOUDINARY_API_SECRET is missing."
    )

cloudinary.config(

    cloud_name=CLOUDINARY_CLOUD_NAME,

    api_key=CLOUDINARY_API_KEY,

    api_secret=CLOUDINARY_API_SECRET

)

def upload_resume(
    file_path
):

    result = cloudinary.uploader.upload(
        file_path,
        resource_type="raw",
        folder="nextround/resumes"
    )

    return result["secure_url"]