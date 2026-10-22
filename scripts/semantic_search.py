
import json
from pathlib import Path
from sentence_transformers import SentenceTransformer, util

# Load the saved chunks and embeddings
input_file = Path("data/processed/chunks_with_embeddings.json")

with input_file.open("r", encoding="utf-8") as file:
    chunks = json.load(file)

print("Loaded chunks:", len(chunks))

# Load the same embedding model
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

# Enter a question to search for
question = input("Ask a question about FinSolve: ")

# Convert the question into an embedding
question_embedding = model.encode(
    question,
    convert_to_tensor=True,
    normalize_embeddings=True
)

# Load the stored chunk embeddings
chunk_embeddings = [
    chunk["embedding"] for chunk in chunks
]

# Compare the question with every chunk
scores = util.cos_sim(
    question_embedding,
    chunk_embeddings
)[0]

# Get the three most relevant chunks
top_results = scores.topk(min(3, len(chunks)))

print("\nMost relevant results:\n")

for rank, index in enumerate(top_results.indices, start=1):
    chunk = chunks[index.item()]
    score = scores[index].item()

    print(f"Result {rank}")
    print("Department:", chunk["department"])
    print("Source:", chunk["source"])
    print("Similarity score:", round(score, 4))
    print("Text:", chunk["text"][:500])
    print("-" * 50)
