from dotenv import load_dotenv
from pathlib import Path

import os

load_dotenv()

class Settings:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")
    MAX_PROMPT_TOKENS = int(os.getenv("MAX_PROMPT_TOKENS", "4096"))
    OUTPUT_DIRECTORY = Path(os.getenv("OUTPUT_DIRECTORY", "output"))
    RAG_RESULT_FILE = str(OUTPUT_DIRECTORY / "rag_result.json")