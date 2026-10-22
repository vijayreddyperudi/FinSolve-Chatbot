from typing import Any

from fastapi import FastAPI, Header, HTTPException, status
from pydantic import BaseModel, Field

app = FastAPI(title="FinSolve RAG API")


class AskRequest(BaseModel):
    question: str = Field(min_length=1, max_length=2000)


class Source(BaseModel):
    source: str
    department: str


class AskResponse(BaseModel):
    answer: str
    sources: list[Source]


ALLOWED_ROLES = {
    "employee",
    "engineering",
    "finance",
    "hr",
    "marketing",
    "executive",
}


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/ask", response_model=AskResponse)
def ask(
    body: AskRequest,
    x_user_role: str | None = Header(default=None),
) -> dict[str, Any]:
    if not x_user_role or not x_user_role.strip():
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Provide the X-User-Role header for development testing.",
        )

    user_role = x_user_role.strip().lower()

    if user_role not in ALLOWED_ROLES:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid user role.",
        )

    from app.services.rag_service import ask_finsolve

    try:
        return ask_finsolve(body.question, user_role)
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error),
        ) from error
    except PermissionError as error:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(error),
        ) from error
