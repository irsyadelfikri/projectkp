from src.config.settings import DOCUMENT_PATH
from src.ingestion.loader import load_all_pdfs
from src.ingestion.chunker import split_documents
from src.vectorstore.chroma import create_vectorstore


def main() -> None:

    print("=== MEMULAI INGESTION ===")

    documents = load_all_pdfs(DOCUMENT_PATH)

    all_chunks = []

    for source, pages in documents.items():

        print(f"\nMemproses: {source}")

        chunks = split_documents(pages)

        print(f"Jumlah halaman: {len(pages)}")
        print(f"Jumlah chunks: {len(chunks)}")

        all_chunks.extend(chunks)

    print(f"\nTotal chunks: {len(all_chunks)}")

    create_vectorstore(all_chunks)

    print("\n=== INGESTION SELESAI ===")


if __name__ == "__main__":
    main()