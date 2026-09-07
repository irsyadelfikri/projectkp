from langchain_chroma import Chroma
from langchain_core.documents import Document

from src.config.settings import CHROMA_PATH
from src.embedding.embedder import create_embedding_model


def create_vectorstore(chunks: list[dict]) -> Chroma:
    """Create and store document embeddings in ChromaDB."""

    embedding_model = create_embedding_model()

    documents = [
        Document(
            page_content=chunk["text"],
            metadata={
                "source": chunk["source"],
                "page": chunk["page"],
            },
        )
        for chunk in chunks
    ]

    vectorstore = Chroma.from_documents(
        documents=documents,
        embedding=embedding_model,
        persist_directory=str(CHROMA_PATH),
        collection_name="zakat_knowledge",
    )

    return vectorstore