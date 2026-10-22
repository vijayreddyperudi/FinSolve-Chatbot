
import json
from pathlib import Path
import chromadb

# 1. Locate the file containing our embedded chunks
input_file = Path("data/processed/chunks_with_embeddings.json")

# 2. Load the chunks from the JSON file
with input_file.open("r", encoding="utf-8") as file:
    chunks = json.load(file)

print(f"Chunks loaded: {len(chunks)}")

# 3. Create a persistent ChromaDB database
client = chromadb.PersistentClient(path="data/chroma_db")

# 4. Create or open our document collection
collection = client.get_or_create_collection(
    name="finsolve_documents",
    metadata={"hnsw:space": "cosine"}
)

# 5. Prepare the information ChromaDB needs
ids = [
    f"{chunk['source']}::{chunk['chunk_id']}"
    for chunk in chunks
]

documents = [chunk["text"] for chunk in chunks]

metadatas = [
    {
        "source": chunk["source"],
        "department": chunk["department"],
        "chunk_id": chunk["chunk_id"]
    }
    for chunk in chunks
]

embeddings = [chunk["embedding"] for chunk in chunks]

# 6. Save the chunks, metadata, and embeddings
collection.upsert(
    ids=ids,
    documents=documents,
    metadatas=metadatas,
    embeddings=embeddings
)

print("Vector database created successfully!")
print(f"Chunks stored in ChromaDB: {collection.count()}")
print("Database location: data/chroma_db")
