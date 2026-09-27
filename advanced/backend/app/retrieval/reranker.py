from sentence_transformers import CrossEncoder


class Reranker:

    def __init__(self):

        self.model = CrossEncoder(
            "cross-encoder/ms-marco-MiniLM-L-12-v2"
        )

    def rerank(
        self,
        query: str,
        results: list[dict],
        top_k: int = 3
    ):

        if not results:
            return []

        pairs = [
            (query, result["text"])
            for result in results
        ]

        scores = self.model.predict(pairs)

        reranked = []

        for result, score in zip(results, scores):

            reranked.append({
                **result,
                "rerank_score": float(score)
            })

        reranked.sort(
            key=lambda x: x["rerank_score"],
            reverse=True
        )

        return reranked[:top_k]