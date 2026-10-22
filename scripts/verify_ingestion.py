
import json
from pathlib import Path

# Locate the saved ingestion output
file_path = Path("data/processed/all_documents.json")

# Load the JSON file
with file_path.open("r", encoding="utf-8") as file:
    documents = json.load(file)

print("Ingestion verification successful!")
print("Total documents:", len(documents))

# Show the departments found
departments = sorted({
    document["department"] for document in documents
})

print("Departments:", departments)

# Check the first document
print("\nFirst document:")
print("Source:", documents[0]["source"])
print("Department:", documents[0]["department"])
print("Characters:", len(documents[0]["text"]))
