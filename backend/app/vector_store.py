import faiss
import numpy as np
import re

from app.embeddings import generate_embeddings


def create_index(chunks: list[str]):
    texts = [chunk["text"] for chunk in chunks]

    embeddings = generate_embeddings(texts)

    embeddings = np.array(embeddings).astype("float32")
    faiss.normalize_L2(embeddings)

    dimension = embeddings.shape[1]

    index = faiss.IndexFlatIP(dimension)

    index.add(embeddings)

    return index

def keyword_score(query: str, text: str):

    query_words = set(
        re.findall(r"\b[a-zA-Z]+\b", query.lower())
    )

    text_words = set(
        re.findall(r"\b[a-zA-Z]+\b", text.lower())
    )

    if not query_words:
        return 0

    return len(query_words & text_words) / len(query_words)


def search_index(
    index,
    query: str,
    chunks: list[dict],
    top_k: int = 3
):

    query_embedding = generate_embeddings([query])

    query_embedding = np.array(
        query_embedding
    ).astype("float32")

    faiss.normalize_L2(query_embedding)

    # Retrieve more candidates first
    distances, indices = index.search(
        query_embedding,
        min(8, len(chunks))
    )

    candidates = []

    for similarity, index_id in zip(
        distances[0],
        indices[0]
    ):

        chunk = chunks[index_id]

        score = keyword_score(
            query,
            chunk["text"]
        )

        combined_score = (
            0.7 * float(similarity)
            + 0.3 * score
        )

        candidates.append({
            "chunk_id": chunk["chunk_id"],
            "chunk": chunk["text"],
            "source": chunk["source"],
            "page": chunk["page"],
            "similarity": float(similarity),
            "keyword_score": score,
            "combined_score": combined_score
        })

    candidates.sort(
        key=lambda x: x["combined_score"],
        reverse=True
    )

    return candidates[:top_k]