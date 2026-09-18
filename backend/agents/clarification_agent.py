import logging

from memory.session_manager import update_session
from schemas.modes import MODE_SCHEMAS
from schemas.session import SessionModel, SessionStatus


logger = logging.getLogger(__name__)

def get_next_question(session: SessionModel) -> tuple[str, str] | None:
    if not session.pending_fields:
        return None
    field = session.pending_fields[0]
    fdm = MODE_SCHEMAS[session.mode]
    for field_def in fdm:
        if field_def.name == field:
            return (field_def.description, field)
    return None

async def process_answer(session: SessionModel, answer: str) -> SessionModel:
    if session.current_field is None:
        logger.warning(f"Session {session.session_id} has no current field set while processing answer.")
        return session
    
    updated_collected_fields = {**session.collected_fields, session.current_field: answer}
    
    updated_pending_fields = [field for field in session.pending_fields if field != session.current_field]
    new_status = SessionStatus.READY_TO_GENERATE if not updated_pending_fields else SessionStatus.CLARIFICATION_IN_PROGRESS
    
    updated_session = await update_session(session, {
        "collected_fields": updated_collected_fields,
        "pending_fields": updated_pending_fields,
        "status": new_status,
        "current_field": None
    })
    logger.debug(f"Processed answer for session {session.session_id}. Updated collected_fields: {updated_collected_fields}, pending_fields: {updated_pending_fields}, status: {new_status}")
    
    return updated_session