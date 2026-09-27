def chunk_text(
    text: str,
    chunk_size: int = 250,
    overlap: int = 50,
    source: str = "document",
    page: int | None = None
) -> list[dict]:

    words = text.split()
    chunks = []
    start = 0
    chunk_id = 0

    while start < len(words):

        end = start + chunk_size
        chunk = " ".join(words[start:end])

        chunks.append({
            "chunk_id": chunk_id,
            "text": chunk,
            "source": source,
            "page": page
        })

        chunk_id += 1
        start += chunk_size - overlap

    return chunks

if __name__ == "__main__":

    sample_text = """
    Database normalization is the process of organizing data
    in a relational database. It reduces redundancy and improves
    data integrity. First Normal Form requires atomic values.
    Second Normal Form removes partial dependencies.
    Third Normal Form removes transitive dependencies.
    """

    chunks = chunk_text(
        sample_text,
        chunk_size=20,
        overlap=5,
    )

    for i, chunk in enumerate(chunks, start=1):
        print(f"\n--- Chunk {i} ---")
        print(chunk)