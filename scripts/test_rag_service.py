
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from app.services.rag_service import ask_finsolve

question = input("Ask a question about FinSolve: ")

# Test with the Finance role first
role = "marketing"

try:
    result = ask_finsolve(question, role)

    print("\nAI Answer:\n")
    print(result["answer"])

    print("\nSources:\n")

    for source in result["sources"]:
        print(
            f"- {source['source']} "
            f"(Department: {source['department']})"
        )

except Exception as error:
    print("\nError:")
    print(error)
