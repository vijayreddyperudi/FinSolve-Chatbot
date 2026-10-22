
import os
from pathlib import Path

from dotenv import load_dotenv
from groq import Groq

PROJECT_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(PROJECT_ROOT / ".env")

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    print("API key not found. Check your .env file.")
    raise SystemExit(1)

client = Groq(api_key=api_key)

try:
    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {
                "role": "user",
                "content": "Explain Retrieval Augmented Generation (RAG) in 3 simple sentences."
            }
        ],
        temperature=0.2,
        max_tokens=150,
    )

    print("\nAI Response:\n")
    print(response.choices[0].message.content)

except Exception as error:
    print("AI response failed.")
    print(f"Error: {error}")
