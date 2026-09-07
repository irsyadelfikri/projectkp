from src.rag.pipeline import ask_question


def main() -> None:
    question = input("Pertanyaan: ")

    answer, documents = ask_question(question)

    print("\n=== JAWABAN ===\n")
    print(answer)

    if documents:
        print("\n=== SUMBER ===\n")

        sources = set(
            (
                document.metadata.get("source"),
                document.metadata.get("page"),
            )
            for document in documents
        )

        for source, page in sorted(sources):
            print(f"- {source}, halaman {page}")


if __name__ == "__main__":
    main()