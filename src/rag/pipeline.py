from langchain_chroma import Chroma

from src.llm.ollama import create_llm
from src.embedding.embedder import create_embedding_model
from src.config.settings import CHROMA_PATH
from src.rag.prompt import create_prompt


SCORE_THRESHOLD = 0.5
TOP_K = 5


def ask_question(question: str) -> tuple[str, list]:

    embedding_model = create_embedding_model()

    vectorstore = Chroma(
        collection_name="zakat_knowledge",
        embedding_function=embedding_model,
        persist_directory=str(CHROMA_PATH),
    )

    results = vectorstore.similarity_search_with_relevance_scores(
        question,
        k=TOP_K,
    )

    print("\n=== DEBUG SCORES ===")

    for document, score in results:

        print(
            f"Score: {score:.4f} | "
            f"Source: {document.metadata.get('source')} | "
            f"Page: {document.metadata.get('page')}"
        )

    relevant_documents = [
        document
        for document, score in results
        if score >= SCORE_THRESHOLD
    ]

    print(
        f"Dokumen relevan: "
        f"{len(relevant_documents)}"
    )

    if not relevant_documents:

        return (
            "Maaf, informasi tersebut tidak ditemukan "
            "dalam dokumen yang tersedia.",
            [],
        )

    context = "\n\n".join(
        document.page_content
        for document in relevant_documents[:3]
    )

    print("\n=== DEBUG CONTEXT ===\n")
    print(context)

    llm = create_llm()

    prompt = create_prompt(
        question,
        context,
    )

    print("\n=== DEBUG PROMPT ===\n")
    print(prompt)

    response = llm.invoke(prompt)

    return (
        response.content,
        relevant_documents,
    )