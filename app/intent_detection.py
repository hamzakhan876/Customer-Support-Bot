
def detect_intent(message: str) -> str:
    """Identify customer intent using simple keyword rules."""
    text = message.lower().strip()

    intent_keywords = {
        "greeting": ["hello", "hi", "hey", "good morning"],
        "track_order": ["track", "tracking", "order status", "delivery"],
        "return_policy": ["return", "exchange", "send back"],
        "refund_status": ["refund", "money back", "refunded"],
        "complaint": ["complaint", "angry", "unhappy", "terrible"],
    }

    for intent, keywords in intent_keywords.items():
        if any(keyword in text for keyword in keywords):
            return intent

    return "unknown"
