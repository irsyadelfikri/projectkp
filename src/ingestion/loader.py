from pathlib import Path
import pymupdf


def load_pdf(file_path: Path) -> list[dict]:
    """Load PDF text while preserving page metadata."""

    document = pymupdf.open(file_path)

    pages = []

    for page_number, page in enumerate(document, start=1):
        text = page.get_text()

        if text.strip():
            pages.append({
                "text": text,
                "page": page_number,
                "source": file_path.name,
            })

    document.close()

    return pages


def load_all_pdfs(directory: Path) -> dict[str, list[dict]]:
    """Load all PDF files from a directory."""

    documents = {}

    for pdf_path in directory.glob("*.pdf"):
        documents[pdf_path.name] = load_pdf(pdf_path)

    return documents