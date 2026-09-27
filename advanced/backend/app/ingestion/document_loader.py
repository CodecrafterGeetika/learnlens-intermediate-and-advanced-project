import os
from pathlib import Path

import pymupdf 
def load_pdf(file_path: str) -> list[dict]:

    document = pymupdf.open(file_path)

    pages = []

    for page_number, page in enumerate(document, start=1):

        text = page.get_text("text").strip()

        if text:
            pages.append({
                "page": page_number,
                "text": text
            })

    document.close()

    return pages
def load_text(file_path: str) -> list[dict]:

    with open(file_path, "r", encoding="utf-8") as file:
        text = file.read().strip()

    if not text:
        return []

    return [{
        "page": None,
        "text": text
    }]
def load_markdown(file_path: str) -> list[dict]:

    with open(file_path, "r", encoding="utf-8") as file:
        text = file.read().strip()

    if not text:
        return []

    return [{
        "page": None,
        "text": text
    }]
def load_document(file_path: str) -> list[dict]:

    extension = Path(file_path).suffix.lower()

    if extension == ".pdf":
        pages = load_pdf(file_path)

    elif extension == ".txt":
        pages = load_text(file_path)

    elif extension == ".md":
        pages = load_markdown(file_path)

    else:
        raise ValueError(
            "Unsupported file type. Please upload a PDF, TXT, or Markdown file."
        )

    if not pages:
        raise ValueError("The uploaded document is empty.")

    return pages