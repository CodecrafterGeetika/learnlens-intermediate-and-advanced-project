from typing import TypedDict
from app.retrieval.query_rewriter import QueryRewriter
from app.retrieval.embeddings import EmbeddingService
from app.retrieval.hybrid_search import hybrid_search
from app.retrieval.vector_store import VectorStore
from app.retrieval.reranker import Reranker
from app.retrieval.groundedness import GroundednessChecker
from app.generation.llm import LLMService
from langgraph.graph import StateGraph, START, END




class RAGState(TypedDict):

    question: str
    mode: str
    rewritten_question: str
    document_id: str | None

    results: list[dict]
    reranked_results: list[dict]

    grounded: bool
    used_original_query: bool

    context: str
    answer: str

    sources: list[dict]

def rewrite_query(
    state: RAGState,
    query_rewriter
):

    question = state["question"]

    rewritten_question = query_rewriter.rewrite(
        question
    )
    print("ORIGINAL QUESTION:", question)
    print("REWRITTEN QUESTION:", rewritten_question)
    return {
        "rewritten_question": rewritten_question
    }

def retrieve_documents(
    state: RAGState,
    embedding_service,
    vector_store
):

    rewritten_question = state["rewritten_question"]
    document_id = state["document_id"]

    query_embedding = embedding_service.generate(
        [rewritten_question]
    )[0]

    results = hybrid_search(
        query=rewritten_question,
        query_embedding=query_embedding,
        vector_store=vector_store,
        top_k=5,
        document_id=document_id
    )

    return {
        "results": results
    }

def fallback_retrieve_documents(
    state: RAGState,
    embedding_service,
    vector_store
):

    original_question = state["question"]
    document_id = state["document_id"]

    query_embedding = embedding_service.generate(
        [original_question]
    )[0]

    results = hybrid_search(
        query=original_question,
        query_embedding=query_embedding,
        vector_store=vector_store,
        top_k=5,
        document_id=document_id
    )

    return {
        "results": results,
        "used_original_query": True
    }

def fallback_rerank_documents(
    state: RAGState,
    reranker
):

    question = state["question"]
    results = state["results"]

    reranked_results = reranker.rerank(
        query=question,
        results=results,
        top_k=3
    )

    return {
        "reranked_results": reranked_results
    }


def rerank_documents(state: RAGState, reranker):

    question = state["rewritten_question"]
    results = state["results"]

    reranked_results = reranker.rerank(
        query=question,
        results=results,
        top_k=3
    )

    return {
        "reranked_results": reranked_results
    }

def check_groundedness(state: RAGState, groundedness_checker):

    reranked_results = state["reranked_results"]

    grounded = groundedness_checker.check(
        reranked_results
    )

    return {
        "grounded": grounded
    }

def generate_answer(state: RAGState, llm_service):

    question = state["question"]
    mode = state["mode"]
    reranked_results = state["reranked_results"]

    context_parts = []

    for result in reranked_results:

        context_parts.append(
            f"""
Source: {result['filename']}
Page: {result['page']}

{result['text']}
"""
        )

    context = "\n\n".join(context_parts)

    answer = llm_service.generate(
        question=question,
        context=context,
        mode=mode
    )

    return {
        "context": context,
        "answer": answer
    }

def route_after_groundedness(state: RAGState):

    if state["grounded"]:
        return "generate"

    if not state["used_original_query"]:
        return "fallback"
    return "end"

def run_rag_graph(
    initial_state: RAGState,
    query_rewriter,
    embedding_service,
    vector_store,
    reranker,
    groundedness_checker,
    llm_service
):

    def retrieve_node(state: RAGState):

        return retrieve_documents(
            state,
            embedding_service,
            vector_store
        )

    def rerank_node(state: RAGState):

        return rerank_documents(
            state,
            reranker
        )
    def fallback_retrieve_node(state: RAGState):

        return fallback_retrieve_documents(
            state,
            embedding_service,
            vector_store
        )

    def fallback_rerank_node(state: RAGState):

        return fallback_rerank_documents(
            state,
            reranker
        )

    def groundedness_node(state: RAGState):

        return check_groundedness(
            state,
            groundedness_checker
        )

    def generate_node(state: RAGState):

        return generate_answer(
            state,
            llm_service
        )

    builder = StateGraph(RAGState)

    def rewrite_node(state: RAGState):

       return rewrite_query(
        state,
        query_rewriter
    )


    builder.add_node("rewrite", rewrite_node)
    builder.add_node("retrieve", retrieve_node)
    builder.add_node("rerank", rerank_node)
    builder.add_node(
        "fallback_retrieve",
        fallback_retrieve_node
    )

    builder.add_node(
        "fallback_rerank",
        fallback_rerank_node
    )
    builder.add_node("groundedness", groundedness_node)
    builder.add_node("generate", generate_node)

    builder.add_edge(START, "rewrite")
    builder.add_edge("rewrite", "retrieve")
    builder.add_edge("retrieve", "rerank")
    builder.add_edge("rerank", "groundedness")

    builder.add_conditional_edges(
        "groundedness",
        route_after_groundedness,
        {
            "generate": "generate",
            "fallback": "fallback_retrieve",
            "end": END
        }
    )

    builder.add_edge(
        "fallback_retrieve",
        "fallback_rerank"
    )

    builder.add_edge(
        "fallback_rerank",
        "groundedness"
    )

    builder.add_edge("generate", END)
    graph = builder.compile()

    return graph.invoke(initial_state)