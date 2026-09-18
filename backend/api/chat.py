from fastapi import APIRouter
from fastapi.params import Depends
from pydantic import BaseModel

from agents.clarification_agent import get_next_question, process_answer
from agents.intent_classifier import classify_intent
from schemas.session import SessionStatus
from memory.session_manager import get_session

class ChatRequest(BaseModel):
    message: str
    session_id: str | None = None

class ChatResponse(BaseModel):
    message: str
    session_id: str
    status: str
    requires_input: bool
    
def get_current_user_id():
    # Placeholder for actual authentication logic
    return "default"

router = APIRouter()

async def _handle_existing_session(session, message) -> ChatResponse:
    session = await process_answer(session, message)
    next_question, field_name = await get_next_question(session)
    if next_question:
        pass
    else:
        intent = await classify_intent(message)
        if intent.needs_clarification:
            return ChatResponse(
                message=intent.clarification_message or "I need more information to assist you.",
                session_id=None,
                status=session.status.value,
                requires_input=True
            )
        if intent.output is not None and intent.output.mode is not None:
            session_id = 
            return ChatResponse(
                message=intent.output.reasoning,
                session_id=None,
                status=session.status.value,
                requires_input=False
            )
            

async def _handle_new_session(user_id, message) -> ChatResponse:
    pass

@router.post("/chat")
async def chat(request: ChatRequest, user_id=Depends(get_current_user_id())):
    session = await get_session(request.session_id) if request.session_id else None
    
    if session and session.status in (SessionStatus.CLARIFICATION_IN_PROGRESS, SessionStatus.CLARIFICATION_NEEDED):
        return await _handle_existing_session(session, request.message)
    
    return await _handle_new_session(user_id, request.message)