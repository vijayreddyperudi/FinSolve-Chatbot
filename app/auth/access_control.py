DEPARTMENT_ACCESS = {
    "engineering": ["engineering", "executive"],
    "finance": ["finance", "executive"],
    "hr": ["hr", "executive"],
    "marketing": ["marketing", "executive"],
    "general": [
        "employee",
        "engineering",
        "finance",
        "hr",
        "marketing",
        "executive",
    ],
}


def can_access_document(user_role: str, document_department: str) -> bool:
    allowed_roles = DEPARTMENT_ACCESS.get(document_department.lower(), [])
    return user_role.lower() in allowed_roles
