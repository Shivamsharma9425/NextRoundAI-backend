from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

MODELS = [
    os.getenv("PRIMARY_MODEL"),
    os.getenv("FALLBACK_MODEL_1"),
    os.getenv("FALLBACK_MODEL_2"),
]

MODELS = [m for m in MODELS if m]


def get_llm(model: str):
    return ChatOpenAI(
        api_key=OPENROUTER_API_KEY,
        base_url="https://openrouter.ai/api/v1",
        model=model,
        temperature=0,
    )