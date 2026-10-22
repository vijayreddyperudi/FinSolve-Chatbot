
import sys
from pathlib import Path

# Add the main project folder to Python's import path
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from app.services.llm_service import generate_answer

question = "What is Retrieval Augmented Generation (RAG)? Explain in 3 simple sentences."

try:
    answer = generate_answer(question)

    print("\nQuestion:")
    print(question)

    print("\nAI Answer:")
    print(answer)

except Exception as error:
    print("\nSomething went wrong:")
    print(error)
