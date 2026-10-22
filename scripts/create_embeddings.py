
import json
from pathlib import Path
from sentence_transformers import SentenceTransformer

# Locate the saved chunks
input_file = Path("data/processed/all_chunks.json")

with input_file.open("r", encoding="utf-8") as file:
    chunks = json.load(file)

print("Total chunks loaded:", len(chunks))

# Load a pretrained embedding model
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

# Extract the text from each chunk
texts = [chunk["text"] for chunk in chunks]

# Convert the text into numerical embeddings
embeddings = model.encode(
    texts,
    show_progress_bar=True,
    normalize_embeddings=True
)

# Save each chunk together with its embedding
for chunk, embedding in zip(chunks, embeddings):
    chunk["embedding"] = embedding.tolist()

# Save the results
output_file = Path("data/processed/chunks_with_embeddings.json")

with output_file.open("w", encoding="utf-8") as file:
    json.dump(chunks, file, ensure_ascii=False)

print("\nEmbeddings created successfully!")
print("Total embedded chunks:", len(chunks))
print("Embedding dimensions:", len(chunks[0]["embedding"]))
print("Saved to:", output_file)
