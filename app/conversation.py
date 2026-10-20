
from app.intent_detection import detect_intent
from app.knowledge_base import search_knowledge_base
from app.semantic_search import semantic_search
from app.llm import generate_answer

FALLBACK_MESSAGE = (
    "I'm sorry, I couldn't find a reliable answer to that question. "
    "Could you please explain what you need help with? "
    "You can also ask about orders, returns, or refunds."
)


def get_bot_response(message: str) -> dict:
    intent = detect_intent(message)

    # First, try keyword-based search.
    record = search_knowledge_base(message, intent)

    # If keyword search fails, try semantic search.
    if record is None:
        semantic_result = semantic_search(message)

        if semantic_result["record"] is not None:
            record = semantic_result["record"]

    # If neither search finds a match, use the fallback.
    if record is None:
        return {
            "intent": intent,
            "answer": FALLBACK_MESSAGE,
            "source": None,
            "resolved": False,
        }

    # Give Groq the retrieved knowledge-base information.
    context = (
        f"Knowledge-base question: {record['question']}\n"
        f"Category: {record['category']}\n"
        f"Approved answer: {record['answer']}"
    )

    try:
        answer = generate_answer(
            message=message,
            context=context,
        )
    except Exception:
        # Keep the bot useful if the LLM service fails.
        answer = record["answer"]

    return {
        "intent": record["intent"],
        "answer": answer,
        "source": record["id"],
        "resolved": True,
    }
