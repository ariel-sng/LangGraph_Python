from dotenv import load_dotenv
from pathlib import Path

import os

load_dotenv()

class Settings:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")
    OPENAI_HIGH_MODEL= os.getenv("OPENAI_HIGH_MODEL", "gpt-5-mini")
    OPENAI_LOW_MODEL = os.getenv("OPENAI_LOW_MODEL", "gpt-5-nano")
    MAX_PROMPT_TOKENS = int(os.getenv("MAX_PROMPT_TOKENS", "4096"))
