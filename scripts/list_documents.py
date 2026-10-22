
from pathlib import Path

# Main folder containing the company dataset
data_dir = Path("data/raw/DS-RPC-01/data")

# Find Markdown documents in all subfolders
documents = list(data_dir.rglob("*.md"))

print("Total Markdown documents found:", len(documents))
print()

for document in documents:
    department = document.parent.name
    print("Department:", department)
    print("File:", document.name)
    print("-" * 40)
