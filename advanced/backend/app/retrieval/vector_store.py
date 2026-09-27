import faiss
import numpy as np


class VectorStore:

    def __init__(self, dimension: int = 384):

        self.dimension = dimension

        self.index = faiss.IndexFlatIP(dimension)

        self.chunks = []

    def add_documents(
        self,
        embeddings,
        chunks: list[dict]
    ):

        vectors = np.asarray(
            embeddings,
            dtype="float32"
        )

        self.index.add(vectors)

        self.chunks.extend(chunks)

    def search(
        self,
        query_embedding,
        top_k: int = 5,
        document_id: str | None = None
    ):

        if self.index.ntotal == 0:
            return []

        query_vector = np.asarray(
            [query_embedding],
            dtype="float32"
        )

        # If no document is selected,
        # search across all documents.
        if document_id is None:

            scores, indices = self.index.search(
                query_vector,
                min(top_k, self.index.ntotal)
            )

            results = []

            for score, index in zip(scores[0], indices[0]):

                chunk = self.chunks[index]

                results.append({
                    **chunk,
                    "score": float(score)
                })

            return results

        # Document-scoped retrieval
        # Search enough candidates first,
        # then keep only chunks belonging
        # to the selected document.
        search_k = self.index.ntotal

        scores, indices = self.index.search(
            query_vector,
            search_k
        )

        results = []

        for score, index in zip(scores[0], indices[0]):

            chunk = self.chunks[index]

            if chunk["document_id"] != document_id:
                continue

            results.append({
                **chunk,
                "score": float(score)
            })

            if len(results) >= top_k:
                break

        return results