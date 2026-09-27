import re

STOP_WORDS = {
    "what", "is", "are", "was", "were",
    "the", "a", "an", "of", "in", "on",
    "to", "for", "and", "or", "with",
    "how", "why", "when", "where",
    "does", "do", "can", "could"
}


def keyword_search(
    query: str,
    chunks: list[dict],
    top_k: int = 5
):
    """
    Simple keyword-based retrieval.

    Scores chunks based on how many query words
    appear in the chunk text.
    """

    query_words = {
    word
    for word in re.findall(r"\b\w+\b", query.lower())
    if word not in STOP_WORDS
    }
    if not query_words:
       return []

    results = []

    for chunk in chunks:

        chunk_words = set(
            re.findall(r"\b\w+\b", chunk["text"].lower())
        )

        matched_words = query_words.intersection(chunk_words)

        if matched_words:
            score = len(matched_words) / len(query_words)

            results.append({
                **chunk,
                "keyword_score": score
            })

    results.sort(
        key=lambda x: x["keyword_score"],
        reverse=True
    )

    return results[:top_k]

def hybrid_search(
    query: str,
    query_embedding,
    vector_store,
    top_k: int = 5,
    document_id: str | None = None
):
    """
    Combines semantic and keyword retrieval
    into a single ranked result list.
    """

    semantic_results = vector_store.search(
      query_embedding=query_embedding,
      top_k=top_k,
      document_id=document_id
)

    keyword_results = keyword_search(
    query=query,
    chunks=[
        chunk
        for chunk in vector_store.chunks
        if (
            document_id is None
            or chunk["document_id"] == document_id
        )
    ],
    top_k=top_k
)

    combined_results = combine_results(
        semantic_results=semantic_results,
        keyword_results=keyword_results,
        top_k=top_k
    )

    return combined_results

def combine_results(
    semantic_results: list[dict],
    keyword_results: list[dict],
    top_k: int = 5
):
    combined = {}

    for result in semantic_results:

        chunk_key = (
            result["document_id"],
            result["chunk_id"]
        )

        combined[chunk_key] = {
            **result,
            "semantic_score": result["score"],
            "keyword_score": 0.0
        }

    for result in keyword_results:

        chunk_key = (
            result["document_id"],
            result["chunk_id"]
        )

        if chunk_key not in combined:

            combined[chunk_key] = {
                **result,
                "semantic_score": 0.0,
                "keyword_score": result["keyword_score"]
            }

        else:

            combined[chunk_key]["keyword_score"] = (
                result["keyword_score"]
            )

    for result in combined.values():

        result["hybrid_score"] = (
            0.7 * result["semantic_score"]
            +
            0.3 * result["keyword_score"]
        )

    results = sorted(
        combined.values(),
        key=lambda x: x["hybrid_score"],
        reverse=True
    )

    return results[:top_k]