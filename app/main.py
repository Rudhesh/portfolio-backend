
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from app.rag import ask_question



app = FastAPI(
    title="Personal AI Assistant",
    description="An AI assistant that answers questions about me.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request format
class ChatRequest(BaseModel):
    question: str


# Response format
class ChatResponse(BaseModel):
    answer: str


@app.get("/")
def home():
    return {
        "message": "Personal AI Backend is running!"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):

    try:
        answer = ask_question(request.question)

        return ChatResponse(answer=answer)

    except Exception as error:
        print(f"Chat error: {error}")

        raise HTTPException(
            status_code=500,
            detail="Something went wrong while generating the answer."
        )
