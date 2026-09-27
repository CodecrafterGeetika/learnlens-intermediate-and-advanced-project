from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pathlib import Path
import pymupdf

from app.chunker import chunk_text
from app.vector_store import create_index, search_index
from app.llm import generate_answer


app = FastAPI(
    title="LearnLens AI",
    description="Evidence-grounded document learning assistant",
    version="1.0.0"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

current_chunks = []
current_index = None


@app.get("/")
def root():
    return {
        "message": "LearnLens AI backend is running!"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }


@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):

    global current_chunks, current_index

    # 1. Validate file type
    allowed_types = {
        "application/pdf",
        "text/plain"
    }

    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=400,
            detail="Only PDF and TXT files are supported."
        )

    # 2. Save uploaded file
    file_path = UPLOAD_DIR / file.filename

    file_content = await file.read()

    with open(file_path, "wb") as f:
        f.write(file_content)

    # 3. Extract text while preserving page information
    extracted_text = ""
    page_texts = []

    if file.content_type == "application/pdf":

        document = pymupdf.open(file_path)

        for page_number, page in enumerate(document, start=1):

            page_text = page.get_text()

            if page_text.strip():
                page_texts.append({
                    "page": page_number,
                    "text": page_text
                })

            extracted_text += page_text

        document.close()

    elif file.content_type == "text/plain":

        extracted_text = file_content.decode("utf-8")

        page_texts.append({
            "page": None,
            "text": extracted_text
        })

    # 4. Validate extracted text
    if not extracted_text.strip():
        raise HTTPException(
            status_code=400,
            detail="The uploaded document contains no readable text."
        )

    # 5. Create chunks while preserving page numbers
    chunks = []

    for page_data in page_texts:

        page_chunks = chunk_text(
            page_data["text"],
            chunk_size=250,
            overlap=50,
            source=file.filename,
            page=page_data["page"]
        )

        chunks.extend(page_chunks)

    # 6. Reassign chunk IDs globally
    for chunk_id, chunk in enumerate(chunks):
        chunk["chunk_id"] = chunk_id

    # 7. Create vector index
    current_chunks = chunks
    current_index = create_index(chunks)

    # 8. Return upload information
    return {
        "filename": file.filename,
        "characters": len(extracted_text),
        "chunk_count": len(chunks),
        "chunks": chunks[:3]
    }


class QuestionRequest(BaseModel):
    question: str
    mode: str = "simple"

@app.post("/ask")
async def ask_question(request: QuestionRequest):

    # 1. Make sure a document has been uploaded
    if current_index is None or not current_chunks:
        raise HTTPException(
            status_code=400,
            detail="Please upload a document first."
        )

    # 2. Validate question
    if not request.question.strip():
        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty."
        )

    # 3. Retrieve relevant chunks
    results = search_index(
        current_index,
        request.question,
        current_chunks,
        top_k=3
    )

    # 4. Check evidence strength
    best_score = results[0]["combined_score"]

    if best_score < 0.40:
        return {
            "question": request.question,
            "answer": "I couldn't find the answer in the uploaded document.",
            "sources": results
        }

    # 5. Build context for the LLM
    context = "\n\n".join(
        result["chunk"]
        for result in results
    )

    # 6. Generate grounded answer
    answer = generate_answer(
        request.question,
        context,
        request.mode
    )

    # 7. Return answer + sources
    return {
        "question": request.question,
        "answer": answer,
        "sources": results
    }