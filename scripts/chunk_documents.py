
import json
from pathlib import Path

# Locate the ingested documents
input_file = Path("data/processed/all_documents.json")

# Load all documents
with input_file.open("r", encoding="utf-8") as file:
    documents = json.load(file)

# Configure chunking
chunk_size = 1000
overlap = 200
step = chunk_size - overlap

# Store chunks from every document
all_chunks = []

for document in documents:
    text = document["text"]
    start = 0
    chunk_id = 0

    while start < len(text):
        chunk_text = text[start:start + chunk_size]

        # Store text together with its metadata
        chunk_record = {
            "chunk_id": chunk_id,
            "source": document["source"],
            "department": document["department"],
            "text": chunk_text
        }

        all_chunks.append(chunk_record)

        chunk_id += 1
        start += step

# Save all chunks
output_dir = Path("data/processed")
output_dir.mkdir(parents=True, exist_ok=True)

output_file = output_dir / "all_chunks.json"

with output_file.open("w", encoding="utf-8") as file:
    json.dump(all_chunks, file, indent=2, ensure_ascii=False)

print("Documents processed:", len(documents))
print("Total chunks created:", len(all_chunks))
print("Saved to:", output_file)
