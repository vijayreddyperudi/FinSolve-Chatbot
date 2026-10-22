
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.auth.access_control import can_access_document

# Test 1: Finance user accessing Finance documents
print(
    "Finance accessing finance:",
    can_access_document("finance", "finance")
)

# Test 2: Employee accessing Finance documents
print(
    "Employee accessing finance:",
    can_access_document("employee", "finance")
)

# Test 3: Executive accessing Engineering documents
print(
    "Executive accessing engineering:",
    can_access_document("executive", "engineering")
)

# Test 4: Unknown department should be denied
print(
    "Employee accessing unknown department:",
    can_access_document("employee", "unknown")
)
