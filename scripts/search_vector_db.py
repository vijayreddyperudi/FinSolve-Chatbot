
import chromadb
from sentence_transformers import SentenceTransformer

# 1. Open the saved ChromaDB database
client = chromadb.PersistentClient(path="data/chroma_db")

# 2. Open the collection containing our documents
collection = client.get_collection(name="finsolve_documents")

# 3. Load the same embedding model used earlier
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

# 4. Ask a question
question = input("Ask a question about FinSolve: ")

# 5. Convert the question into an embedding
question_embedding = model.encode(
    question,
    normalize_embeddings=True
).tolist()

# 6. Search for the three most relevant chunks
results = collection.query(
    query_embeddings=[question_embedding],
    n_results=3
)

# 7. Display the retrieved information
print("\nMost relevant results:\n")

for i, text in enumerate(results["documents"][0]):
    metadata = results["metadatas"][0][i]
    distance = results["distances"][0][i]

    print(f"Result {i + 1}")
    print(f"Department: {metadata['department']}")
    print(f"Source: {metadata['source']}")
    print(f"Cosine distance: {distance:.4f}")
    print(f"Text: {text[:700]}")
    print("-" * 60)
