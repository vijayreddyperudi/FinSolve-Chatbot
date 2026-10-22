
import json
from pathlib import Path

# Locate the saved JSON file
file_path = Path("data/processed/handbook_chunks.json")

# Check whether the file exists
if file_path.exists():
    # Read the saved JSON data
    with file_path.open("r", encoding="utf-8") as file:
        chunk_records = json.load(file)

    print("JSON file loaded successfully!")
    print("Total chunk records:", len(chunk_records))

    # Display information about the first chunk
    first_chunk = chunk_records[0]

    print("Source:", first_chunk["source"])
    print("Department:", first_chunk["department"])
    print("Chunk ID:", first_chunk["chunk_id"])
    print("Text preview:", first_chunk["text"][:150])

else:
    print("JSON file not found. Check the file path.")
