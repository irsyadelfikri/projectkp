import os
from pathlib import Path
from dotenv import load_dotenv


load_dotenv()


BASE_DIR = Path(__file__).resolve().parents[2]

LLM_MODEL = os.getenv(
    "LLM_MODEL",
    "qwen2.5:3b",
)

EMBEDDING_MODEL = os.getenv(
    "EMBEDDING_MODEL",
    "BAAI/bge-m3",
)

CHROMA_PATH = BASE_DIR / os.getenv(
    "CHROMA_PATH",
    "data/chroma_db",
)

DOCUMENT_PATH = BASE_DIR / os.getenv(
    "DOCUMENT_PATH",
    "data/raw",
)

TOP_K = int(
    os.getenv("TOP_K", "5")
)