
from pathlib import Path

data_folder = Path("data/raw/DS-RPC-01/data")

print("Checking FinSolve dataset...")

if data_folder.exists():
    print("Dataset folder found!")

    files = list(data_folder.rglob("*"))

    for file in files:
        if file.is_file():
            print(file.name)
else:
    print("Dataset folder not found. Check the folder path.")
