from datetime import datetime, timezone
from enum import StrEnum, auto
from typing import Any, Optional
from uuid import uuid4
from pydantic import BaseModel, Field
from schemas.modes import Mode



class MessageRole(StrEnum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"
    TOOL = "tool"

class Message(BaseModel):
    role: MessageRole
    content: str

    
class SessionStatus(StrEnum):
    NEW = auto()
    CLARIFICATION_NEEDED = auto()
    CLARIFICATION_IN_PROGRESS = auto()
    READY_TO_GENERATE = auto()
    GENERATING = auto()
    COMPLETED = auto()
    FAILED = auto()

class SessionModel(BaseModel):
    session_id: str = Field(default_factory=lambda: str(uuid4()))
    user_id: Optional[str] = None
    mode: Optional[Mode] = None
    status: SessionStatus = SessionStatus.NEW
    collected_fields: dict[str, Any] = Field(default_factory=dict)
    pending_fields: list[str] = Field(default_factory=list)
    messages: list[Message] = Field(default_factory=list)
    artifacts_ids: list[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    

    
    
    
    
# NEW → CLARIFICATION_NEEDED → CLARIFICATION_IN_PROGRESS → READY_TO_GENERATE → GENERATING → COMPLETED → FAILED
