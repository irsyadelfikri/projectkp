from langchain_text_splitters import RecursiveCharacterTextSplitter


def split_documents(pages: list[dict]) -> list[dict]:
    """Split PDF pages into chunks while preserving metadata."""

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1200,
        chunk_overlap=250,
        separators=[
            "\n\n",
            "\n",
            ". ",
            " ",
        ],
    )

    chunks = []

    for page in pages:

        page_chunks = splitter.split_text(
            page["text"]
        )

        for chunk in page_chunks:
            chunks.append({
                "text": chunk,
                "source": page["source"],
                "page": page["page"],
            })

    return chunks