from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from src.graph import ask_question


# =========================================================
# FASTAPI APPLICATION
# =========================================================

app = FastAPI(
    title="Agentic AI RAG Chatbot",
    description=(
        "A document-grounded RAG chatbot built using "
        "Gemini, Pinecone, LangGraph and FastAPI."
    ),
    version="1.0.0",
)


# =========================================================
# REQUEST MODEL
# =========================================================

class ChatRequest(BaseModel):
    question: str = Field(
        ...,
        min_length=1,
        description="Question to ask about the Agentic AI ebook.",
    )


# =========================================================
# RESPONSE MODEL
# =========================================================

class RetrievedChunk(BaseModel):
    content: str
    metadata: dict
    score: float


class ChatResponse(BaseModel):
    query: str
    final_answer: str
    retrieved_context_chunks: list[RetrievedChunk]
    confidence_score: float


# =========================================================
# ROOT ENDPOINT
# =========================================================

@app.get("/")
def root():
    return {
        "message": "Agentic AI RAG Chatbot API is running.",
        "docs": "/docs",
        "chat_endpoint": "/chat",
    }


# =========================================================
# CHAT ENDPOINT
# =========================================================

@app.post(
    "/chat",
    response_model=ChatResponse,
)
def chat(request: ChatRequest):

    try:

        result = ask_question(
            request.question
        )

        return {
            "query": request.question,
            "final_answer": result["answer"],
            "retrieved_context_chunks": result["context"],
            "confidence_score": result["score"],
        }

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=f"RAG pipeline error: {str(error)}",
        )