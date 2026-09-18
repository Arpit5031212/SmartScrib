from pydantic import BaseModel

from schemas.session import SessionStatus


class ChatRequest(BaseModel):
    message: str
    session_id: str | None = None
    user_id: str = "default"

class ChatResponse(BaseModel):
    message: str
    session_id: str
    status: SessionStatus
    requires_input: bool