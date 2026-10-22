
import json
from pathlib import Path

# Find the dataset folder
data_dir = Path("data/raw/DS-RPC-01/data")

# Find every Markdown document
documents = list(data_dir.rglob("*.md"))

# Store the documents we read
document_records = []

for document in documents:
    # Read the document's text
    text = document.read_text(encoding="utf-8")

    # Identify its department
    department = document.parent.name

    # Store text and metadata together
    record = {
        "source": document.name,
        "department": department,
        "text": text
    }

    document_records.append(record)

# Create a folder for processed data
output_dir = Path("data/processed")
output_dir.mkdir(parents=True, exist_ok=True)

# Choose the output JSON file
output_file = output_dir / "all_documents.json"

# Save all document records
with output_file.open("w", encoding="utf-8") as file:
    json.dump(document_records, file, indent=2, ensure_ascii=False)

print("\nAll documents saved successfully!")
print("Saved to:", output_file)
print("Documents saved:", len(document_records))


# Show the results
print("Total documents ingested:", len(document_records))

for record in document_records:
    print(
        "Department:", record["department"],
        "| Source:", record["source"],
        "| Characters:", len(record["text"])
    )
