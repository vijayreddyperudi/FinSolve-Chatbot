
import sys
import re
from pathlib import Path

# --------------------------------------------------
# STEP 1: Configure the project path
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


# --------------------------------------------------
# STEP 2: Import required libraries
# --------------------------------------------------

import chromadb
from sentence_transformers import SentenceTransformer

from app.auth.access_control import can_access_document


# --------------------------------------------------
# STEP 3: Search settings
# --------------------------------------------------

COLLECTION_NAME = "finsolve_documents"
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

MAX_RESULTS = 5
MAX_COSINE_DISTANCE = 0.80

ALL_DEPARTMENTS = [
    "engineering",
    "finance",
    "hr",
    "marketing",
    "general",
]

VALID_ROLES = {
    "employee",
    "finance",
    "marketing",
    "hr",
    "engineering",
    "executive",
}

STOP_WORDS = {
    "what", "when", "where", "which", "who", "whom",
    "does", "did", "was", "were", "the", "and", "for",
    "from", "with", "that", "this", "have", "has", "had",
    "are", "our", "their", "company", "about", "tell",
    "me", "please", "can", "you", "how", "much", "many",
    "in", "on", "of", "to", "is", "it", "its", "a", "an",
    "be", "by", "as", "at", "or", "during", "year",
}

# Use clear, department-specific terms.
# Do not classify ambiguous words such as "performance"
# as belonging to just one department.
TOPIC_DEPARTMENTS = {
    "finance": {
        "finance", "financial", "revenue", "profit",
        "profits", "income", "margin", "margins",
        "quarterly", "budget", "budgets", "expense",
        "expenses", "reimbursement", "reimbursements",
        "cost", "costs", "financially",
    },
    "marketing": {
        "marketing", "campaign", "campaigns",
        "customer", "customers", "feedback",
        "advertising", "conversion", "conversions",
    },
    "hr": {
        "hr", "payroll", "salary", "salaries",
        "attendance", "recruitment", "employee",
        "employees", "leave", "leaves", "hiring",
        "onboarding", "appraisal", "appraisals",
    },
    "engineering": {
        "engineering", "architecture", "technical",
        "code", "deployment", "deployments", "system",
        "systems", "infrastructure", "developer",
        "developers", "software", "api", "apis",
    },
}


# --------------------------------------------------
# STEP 4: Helper functions
# --------------------------------------------------

def extract_words(text):
    """Extract lowercase words from text."""
    return set(
        re.findall(r"\b[a-zA-Z0-9]+\b", text.lower())
    )


def get_question_keywords(question):
    """Remove common words from the question."""
    return {
        word
        for word in extract_words(question)
        if len(word) > 2 and word not in STOP_WORDS
    }


def get_allowed_departments(role):
    """Return departments allowed by access-control rules."""
    return [
        department
        for department in ALL_DEPARTMENTS
        if can_access_document(role, department)
    ]


def detect_requested_departments(question):
    """Detect explicit department-related topics."""
    words = extract_words(question)
    requested = set()

    for department, topic_words in TOPIC_DEPARTMENTS.items():
        if words.intersection(topic_words):
            requested.add(department)

    return requested


# --------------------------------------------------
# STEP 5: Connect to ChromaDB
# --------------------------------------------------

try:
    client = chromadb.PersistentClient(
        path=str(PROJECT_ROOT / "data" / "chroma_db")
    )

    collection = client.get_collection(
        name=COLLECTION_NAME
    )

    print("ChromaDB connected successfully!")

except Exception as error:
    print("Could not connect to ChromaDB.")
    print(f"Details: {error}")
    raise SystemExit(1)


# --------------------------------------------------
# STEP 6: Load the embedding model
# --------------------------------------------------

try:
    model = SentenceTransformer(MODEL_NAME)
    print("Embedding model loaded successfully!")

except Exception as error:
    print("Could not load the embedding model.")
    print(f"Details: {error}")
    raise SystemExit(1)


# --------------------------------------------------
# STEP 7: Get the role and question
# --------------------------------------------------

role = input(
    "\nEnter role "
    "(employee, finance, marketing, hr, engineering, executive): "
).strip().lower()

if role not in VALID_ROLES:
    print("Access denied: invalid role.")
    raise SystemExit(1)

question = input("Enter your question: ").strip()

if not question:
    print("Please enter a question.")
    raise SystemExit(1)


# --------------------------------------------------
# STEP 8: Determine department permissions
# --------------------------------------------------

allowed_departments = get_allowed_departments(role)

if not allowed_departments:
    print("Access denied: no permitted departments.")
    raise SystemExit(1)

print(f"\nRole: {role}")
print(f"Allowed departments: {allowed_departments}")

requested_departments = detect_requested_departments(question)

# Only block when the question contains a specific topic
# associated with a department the role cannot access.
restricted_departments = (
    requested_departments - set(allowed_departments)
)

if restricted_departments:
    print(
        "\nAccess restricted: this question appears to request "
        "restricted departmental information."
    )
    print(
        "Restricted department(s): "
        + ", ".join(sorted(restricted_departments))
    )
    print("No document search was performed.")
    raise SystemExit(0)


# --------------------------------------------------
# STEP 9: Create the question embedding
# --------------------------------------------------

question_keywords = get_question_keywords(question)

if not question_keywords:
    print("Please ask a more specific question.")
    raise SystemExit(0)

question_embedding = model.encode(
    question,
    normalize_embeddings=True
).tolist()


# --------------------------------------------------
# STEP 10: Search only permitted departments
# --------------------------------------------------

try:
    results = collection.query(
        query_embeddings=[question_embedding],
        n_results=MAX_RESULTS,
        where={
            "department": {
                "$in": allowed_departments
            }
        },
        include=[
            "documents",
            "metadatas",
            "distances",
        ],
    )

except Exception as error:
    print("Document search failed.")
    print(f"Details: {error}")
    raise SystemExit(1)


documents = results.get("documents", [[]])[0]
metadatas = results.get("metadatas", [[]])[0]
distances = results.get("distances", [[]])[0]


# --------------------------------------------------
# STEP 11: Filter results
# --------------------------------------------------

relevant_results = []

for index, document_text in enumerate(documents):
    metadata = metadatas[index] or {}

    department = metadata.get("department", "").lower()
    distance = distances[index]

    # Always check document permission before displaying it.
    if not can_access_document(role, department):
        continue

    if distance is None or distance > MAX_COSINE_DISTANCE:
        continue

    document_words = extract_words(document_text)

    matched_keywords = question_keywords.intersection(
        document_words
    )

    # Avoid requiring two matches when the question contains
    # only one meaningful keyword.
    minimum_matches = min(2, len(question_keywords))

    if len(matched_keywords) < minimum_matches:
        continue

    relevant_results.append({
        "department": department,
        "source": metadata.get("source", "Unknown"),
        "distance": distance,
        "matched_keywords": sorted(matched_keywords),
        "text": document_text,
        "match_count": len(matched_keywords),
    })


# --------------------------------------------------
# STEP 12: Rank results
# --------------------------------------------------

relevant_results.sort(
    key=lambda item: (
        -item["match_count"],
        item["distance"],
    )
)

if not relevant_results:
    print("\nNo sufficiently relevant documents found.")
    print(
        "Check the question, document metadata, and whether "
        "the relevant files have been ingested."
    )
    raise SystemExit(0)


# --------------------------------------------------
# STEP 13: Display permitted results
# --------------------------------------------------

print("\nRelevant permitted search results:\n")

for result_number, result in enumerate(
    relevant_results, start=1
):
    print(f"Result: {result_number}")
    print(f"Department: {result['department']}")
    print(f"Source: {result['source']}")
    print(f"Cosine distance: {result['distance']:.4f}")
    print(f"Matched keywords: {result['matched_keywords']}")
    print(f"Text: {result['text'][:500]}")
    print("-" * 60)

print(f"Total relevant results: {len(relevant_results)}")
