
import json
from pathlib import Path
from typing import Any

KNOWLEDGE_BASE_PATH = (
    Path(__file__).resolve().parent.parent
    / "data"
    / "knowledge_base.json"
)


def load_knowledge_base() -> list[dict[str, Any]]:
    """Load support records from the JSON knowledge base."""
    with KNOWLEDGE_BASE_PATH.open("r", encoding="utf-8") as file:
        data = json.load(file)

    return data.get("records", [])


def search_knowledge_base(
    query: str,
    intent: str | None = None,
) -> dict[str, Any] | None:
    """Find the best matching support record."""
    records = load_knowledge_base()
    query_words = set(query.lower().split())

    best_record = None
    best_score = 0

    for record in records:
        if intent and record["intent"] != intent:
            continue

        searchable_text = " ".join(
            [
                record.get("question", ""),
                " ".join(record.get("keywords", [])),
            ]
        ).lower()

        searchable_words = set(searchable_text.split())
        score = len(query_words & searchable_words)

        if score > best_score:
            best_score = score
            best_record = record

    if best_score == 0:
        return None

    return best_record
