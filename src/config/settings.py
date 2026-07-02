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
    OPENAI_API_TIMEOUT = int(os.getenv("OPENAI_API_TIMEOUT", "60"))  # Timeout en segundos para llamadas a la API, ej. 60
    OPENAI_API_RETRY_ATTEMPTS = int(os.getenv("OPENAI_API_RETRY_ATTEMPTS", "3"))  # Reintentos para errores transitorios, ej. 3
    OPENAI_API_RETRY_BACKOFF = float(os.getenv("OPENAI_API_RETRY_BACKOFF", "2.0"))  # Delay base entre reintentos en segundos, ej. 2.0
