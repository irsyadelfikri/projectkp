from langchain_huggingface import HuggingFaceEmbeddings
from src.config.settings import EMBEDDING_MODEL


def create_embedding_model() -> HuggingFaceEmbeddings:
    """Create local embedding model."""

    return HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL,
        model_kwargs={
            "device": "cpu",
        },
        encode_kwargs={
            "normalize_embeddings": True,
        },
    )