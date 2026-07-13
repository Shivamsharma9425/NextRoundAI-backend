from motor.motor_asyncio import AsyncIOMotorClient # type: ignore
from dotenv import load_dotenv
import os

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")

if not MONGO_URI:
    raise RuntimeError(
        "MONGO_URI is missing."
    )

client = AsyncIOMotorClient(MONGO_URI)

db = client["nextround"]