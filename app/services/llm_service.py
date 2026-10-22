
import os
from pathlib import Path

from dotenv import load_dotenv
from groq import Groq

PROJECT_ROOT = Path(__file__).resolve().parents[2]
load_dotenv(PROJECT_ROOT / ".env")


def generate_answer(prompt: str) -> str:
    """Send a prompt to Groq and return the generated answer."""

    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise ValueError("GROQ_API_KEY is missing from the .env file.")

    client = Groq(api_key=api_key)

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        max_completion_tokens=800,
    )

    choice = response.choices[0]
    answer = choice.message.content

    if not answer or not answer.strip():
        raise RuntimeError(
            f"Groq returned an empty answer. "
            f"Finish reason: {choice.finish_reason}"
        )

    return answer.strip()
