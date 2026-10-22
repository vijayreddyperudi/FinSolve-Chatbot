
import json
from pathlib import Path

# Locate the saved chunks
file_path = Path("data/processed/all_chunks.json")

# Load the chunks
with file_path.open("r", encoding="utf-8") as file:
    chunks = json.load(file)

print("Chunk verification successful!")
print("Total chunks:", len(chunks))

# Display the first chunk's metadata
first_chunk = chunks[0]

print("\nFirst chunk details:")
print("Chunk ID:", first_chunk["chunk_id"])
print("Source:", first_chunk["source"])
print("Department:", first_chunk["department"])
print("Text preview:", first_chunk["text"][:200])

# Count chunks by department
department_counts = {}

for chunk in chunks:
    department = chunk["department"]
    department_counts[department] = department_counts.get(department, 0) + 1

print("\nChunks by department:")
for department, count in sorted(department_counts.items()):
    print(department, ":", count)
