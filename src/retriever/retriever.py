from langchain_chroma import Chroma

from src.config.settings import (
    CHROMA_PATH,
    TOP_K,
)

from src.embedding.embedder import create_embedding_model


def create_retriever():
    embedding_model = create_embedding_model()

    vectorstore = Chroma(
        collection_name="zakat_knowledge",
        embedding_function=embedding_model,
        persist_directory=str(CHROMA_PATH),
    )

    return vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={
            "k": TOP_K,
        },
    )