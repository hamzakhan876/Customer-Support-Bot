import json
from pathlib import Path

from sentence_transformers import SentenceTransformer, util

# Load the semantic model once
model = SentenceTransformer("all-MiniLM-L6-v2")

# Find the knowledge-base JSON file
BASE_DIR = Path(__file__).resolve().parent.parent
KB_PATH = BASE_DIR / "data" / "knowledge_base.json"

# Load knowledge-base records
with open(KB_PATH, "r", encoding="utf-8") as file:
    knowledge_base = json.load(file)["records"]

# Extract the questions that the model will compare
questions = [record["question"] for record in knowledge_base]

# Convert all knowledge-base questions into embeddings
question_embeddings = model.encode(questions)

def semantic_search(message: str) -> dict:
    # Convert the customer's message into an embedding
    message_embedding = model.encode(message)

    # Compare it with all knowledge-base question embeddings
    similarities = util.cos_sim(
        message_embedding,
        question_embeddings,
    )[0]

    # Find the index of the most similar question
    best_index = similarities.argmax().item()

    # Get its similarity score
    best_score = similarities[best_index].item()
    threshold = 0.30

    if best_score < threshold:
        return {
            "record": None,
            "score": best_score,
        }
    # Return the matching record and score
    return {
        "record": knowledge_base[best_index],
        "score": best_score,
    }



if __name__ == "__main__":
    test_messages = [
        "Where is my package right now?",
        "I want my money back.",
        "How can I return a product?",
        "Tell me a joke about cats.",
    ]

    for message in test_messages:
        result = semantic_search(message)

        print(f"\nCustomer: {message}")
        print(f"Similarity: {result['score']:.3f}")

        if result["record"] is None:
            print("Result: No reliable match — use fallback")
        else:
            print(f"Best match: {result['record']['question']}")
            print(f"Record: {result['record']['id']}")
