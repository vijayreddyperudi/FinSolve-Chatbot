
from pathlib import Path

file_path = Path(
    "data/raw/DS-RPC-01/data/general/employee_handbook.md"
)

if file_path.exists():
    text = file_path.read_text(encoding="utf-8")

    print("Document loaded successfully!")
    print(text[:1000])
else:
    print("Document not found. Check the file path.")

print("Total characters:", len(text))
print("Total words:", len(text.split()))


# Maximum characters in each chunk
chunk_size = 500

# Number of characters shared between neighboring chunks
overlap = 100

# Store all chunks here
chunks = []

# Move forward by 400 characters each time
step = chunk_size - overlap

for start in range(0, len(text), step):
    chunk = text[start:start + chunk_size]
    chunks.append(chunk)

print("Total chunks:", len(chunks))
print("\nFirst chunk:\n")
print(chunks[0])

print("\nSecond chunk:\n")
print(chunks[1])

# Store each chunk with information about its source
chunk_records = []

for i, chunk in enumerate(chunks):
    record = {
        "chunk_id": i,
        "text": chunk,
        "source": "employee_handbook.md",
        "department": "general"
    }

    chunk_records.append(record)

print("\nTotal chunk records:", len(chunk_records))
print("\nFirst chunk record:")
print(chunk_records[0])

import json

# Create the output folder if it does not exist
output_dir = Path("data/processed")
output_dir.mkdir(parents=True, exist_ok=True)

# Save the chunk records as JSON
output_file = output_dir / "handbook_chunks.json"

with output_file.open("w", encoding="utf-8") as file:
    json.dump(chunk_records, file, indent=2, ensure_ascii=False)

print("\nChunks saved successfully!")
print("Saved file:", output_file)
