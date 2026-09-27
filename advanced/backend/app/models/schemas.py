
from pydantic import BaseModel, Field
from typing import Literal


class QuestionRequest(BaseModel):

    question: str = Field(
        ...,
        min_length=1,
        description="Question asked about the uploaded documents"
    )

    mode: Literal[
        "simple",
        "exam",
        "revision",
        "viva"
    ] = "simple"

    document_id: str | None = Field(
        default=None,
        description="Optional document ID to restrict retrieval"
    )


class Source(BaseModel):

    document_id: str
    filename: str
    chunk_id: int
    page: int | None = None
    content: str
    score: float


class AnswerResponse(BaseModel):

    question: str
    mode: str
    answer: str
    sources: list[Source]
    grounded: bool
    rewritten_query: str
    fallback_used: bool
