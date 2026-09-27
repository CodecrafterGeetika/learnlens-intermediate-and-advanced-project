

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import shutil
from app.ingestion.chunker import create_chunks
from app.ingestion.document_loader import load_document
from app.retrieval.embeddings import EmbeddingService
from app.retrieval.vector_store import VectorStore
from app.retrieval.hybrid_search import hybrid_search
from app.retrieval.reranker import Reranker
from app.generation.llm import LLMService
from app.models.schemas import QuestionRequest, AnswerResponse
from app.retrieval.groundedness import GroundednessChecker
from app.retrieval.query_rewriter import QueryRewriter
from app.workflow.rag_graph import run_rag_graph

app = FastAPI(
    title="LearnLens AI — Advanced RAG",
    description="Production-style document intelligence API",
    version="1.0.0"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

embedding_service = EmbeddingService()
vector_store = VectorStore()
reranker = Reranker()
llm_service = LLMService()
groundedness_checker = GroundednessChecker(threshold=0.5)
query_rewriter = QueryRewriter()

@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):

    allowed_extensions = {".pdf", ".txt", ".md"}

    extension = Path(file.filename).suffix.lower()

    if extension not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail="Unsupported file type. Please upload PDF, TXT, or Markdown."
        )

    upload_dir = Path("uploads")
    upload_dir.mkdir(exist_ok=True)

    file_path = upload_dir / file.filename

    with file_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        pages = load_document(str(file_path))
        document_id = file_path.stem

        chunks = create_chunks(
           pages=pages,
           document_id=document_id,
           filename=file.filename
        )
        texts = [chunk["text"] for chunk in chunks]

        embeddings = embedding_service.generate(texts)

        vector_store.add_documents(
        embeddings=embeddings,
        chunks=chunks
)

    except ValueError as error:
        file_path.unlink(missing_ok=True)

        raise HTTPException(
            status_code=400,
            detail=str(error)
        )

    return {
    "document_id": document_id,
    "filename": file.filename,
    "file_type": extension,
    "pages": len(pages),
    "chunks": len(chunks),
    "vectors_indexed": len(embeddings),
    "message": "Document uploaded, processed, chunked, and indexed successfully."
}

@app.post("/search")
async def search_documents(
    question: str,
    document_id: str | None = None
):

    if not question.strip():
        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty."
        )

    query_embedding = embedding_service.generate(
        [question]
    )[0]

    results = hybrid_search(
        query=question,
        query_embedding=query_embedding,
        vector_store=vector_store,
        top_k=5,
        document_id=document_id
    )

    reranked_results = reranker.rerank(
    query=question,
    results=results,
    top_k=3
   )
    return {
        "query": question,
        "results": reranked_results
    }

@app.post("/ask")
async def ask_question(request: QuestionRequest):

    question = request.question.strip()

    if not question:
        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty."
        )

    initial_state = {
        "question": question,
        "mode": request.mode,
        "rewritten_question": "",
        "document_id": request.document_id,
        "results": [],
        "reranked_results": [],
        "grounded": False,
        "used_original_query": False,
        "context": "",
        "answer": "",
        "sources": []
    }

    final_state = run_rag_graph(
        initial_state=initial_state,
        query_rewriter=query_rewriter,
        embedding_service=embedding_service,
        vector_store=vector_store,
        reranker=reranker,
        groundedness_checker=groundedness_checker,
        llm_service=llm_service
    )

    if not final_state["grounded"]:

        return AnswerResponse(
            question=question,
            mode=request.mode,
            answer="I could not find enough evidence in the provided documents.",
            sources=[],
            grounded=False,
            rewritten_query=final_state["rewritten_question"],
            fallback_used=final_state["used_original_query"]
        )

    sources = []

    for result in final_state["reranked_results"]:

        sources.append({
            "document_id": result["document_id"],
            "filename": result["filename"],
            "chunk_id": result["chunk_id"],
            "page": result["page"],
            "content": result["text"],
            "score": result["rerank_score"]
        })

    return AnswerResponse(
        question=question,
        mode=request.mode,
        answer=final_state["answer"],
        sources=sources,
        grounded=True,
        rewritten_query=final_state["rewritten_question"],
        fallback_used=final_state["used_original_query"]
    )