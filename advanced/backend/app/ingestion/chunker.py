def create_chunks(
    pages: list[dict],
    document_id: str,
    filename: str,
    chunk_size: int = 300,
    overlap: int = 50
) -> list[dict]:

    chunks = []
    chunk_id = 0

    for page_data in pages:

        page_number = page_data["page"]
        text = page_data["text"]

        words = text.split()

        start = 0

        while start < len(words):

            end = start + chunk_size

            chunk_text = " ".join(words[start:end])

            chunks.append({
                "document_id": document_id,
                "filename": filename,
                "chunk_id": chunk_id,
                "page": page_number,
                "text": chunk_text,
                "word_count": len(chunk_text.split())
            })

            chunk_id += 1

            start += chunk_size - overlap

    return chunks