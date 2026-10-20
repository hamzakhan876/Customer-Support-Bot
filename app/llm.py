
import os

from dotenv import load_dotenv
from groq import Groq

# Load environment variables from the project-root .env file
load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise RuntimeError(
        "GROQ_API_KEY is missing. Add it to your project-root .env file."
    )

client = Groq(api_key=api_key)

MODEL_NAME = "openai/gpt-oss-120b"


def generate_answer(message: str, context: str) -> str:
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a professional customer support assistant. "
                    "Answer using only the supplied knowledge-base context. "
                    "Do not invent company policies, order details, or refund "
                    "information. If the context does not answer the question, "
                    "say that the customer should contact customer support."
                ),
            },
            {
                "role": "user",
                "content": (
                    f"Knowledge-base context:\n{context}\n\n"
                    f"Customer question:\n{message}"
                ),
            },
        ],
        temperature=0.2,
        max_tokens=250,
    )

    answer = response.choices[0].message.content

    if not answer:
        raise RuntimeError("The Groq model returned an empty response.")

    return answer.strip()

