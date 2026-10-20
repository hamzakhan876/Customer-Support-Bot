
from fastapi import FastAPI
from app.models import ChatRequest, ChatResponse
from app.conversation import get_bot_response

app = FastAPI(
    title="Customer Support Bot API",
    description="A customer support chatbot with intent detection, knowledge retrieval, and fallback handling.",
    version="1.0.0",
)


@app.get("/")
def home():
    return {
        "message": "Customer Support Bot API is running",
        "docs": "/docs",
    }


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    return get_bot_response(request.message)
