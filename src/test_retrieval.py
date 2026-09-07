from langchain_chroma import Chroma

from src.config.settings import CHROMA_PATH
from src.embedding.embedder import create_embedding_model


def main():

    embedding_model = create_embedding_model()

    vectorstore = Chroma(
        collection_name="zakat_knowledge",
        embedding_function=embedding_model,
        persist_directory=str(CHROMA_PATH),
    )

    query = (
        "Apakah zakat penghasilan boleh dibayarkan "
        "sebelum terpenuhi syarat wajib?"
    )

    results = (
        vectorstore
        .similarity_search_with_relevance_scores(
            query,
            k=5,
        )
    )

    print("\n=== HASIL RETRIEVAL ===\n")

    for document, score in results:

        print(f"Score  : {score:.4f}")
        print(
            f"Source : "
            f"{document.metadata.get('source')}"
        )
        print(
            f"Page   : "
            f"{document.metadata.get('page')}"
        )
        print(
            f"Text   : "
            f"{document.page_content[:200]}"
        )

        print("-" * 60)


if __name__ == "__main__":
    main()