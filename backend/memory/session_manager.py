from datetime import datetime, timezone
import logging
from typing import Any

from memory.redis_client import get_redis_client
from schemas.modes import MODE_SCHEMAS, Mode
from schemas.session import SessionModel, SessionStatus
from config import get_settings


logger = logging.getLogger(__name__)
SESSION_KEY_PREFIX = "session:"
settings = get_settings()

def _session_key(session_id: str) -> str:
    return f"{SESSION_KEY_PREFIX}{session_id}"

# creates and stores a new session in Redis
async def create_session(user_id: str, mode: Mode) -> SessionModel:
    pending_fields =[field.name for field in MODE_SCHEMAS[mode] if field.required]
    session = SessionModel(
        user_id=user_id,
        mode=mode,
        status=SessionStatus.CLARIFICATION_NEEDED,
        pending_fields=pending_fields
    )
    serialized = session.model_dump_json()
    redis = get_redis_client()
    await redis.set(_session_key(session.session_id), serialized, ex=settings.session_ttl)  # set TTL for session expiry
    logger.debug(f"Created new session {session.session_id} for user {user_id} with mode {mode}")
    return session

# retrieves and deserializes a session from Redis
async def get_session(session_id: str) -> SessionModel | None:
    try:
        redis = get_redis_client()
        serialized = await redis.get(_session_key(session_id))
        if serialized is None:
            return None
        session = SessionModel.model_validate_json(serialized)
        logger.debug(f"Retrieved session {session_id} from Redis: {session}")
        return session
    except Exception as e:
        logger.exception(f"Error retrieving session {session_id}: {e}")
        raise

# updates fields, resets TTL, saves back to Redis
async def update_session(session: SessionModel, updates: dict[str, Any]) -> SessionModel:
    updates["updated_at"] = datetime.now(timezone.utc)  # update timestamp
    updated_session = session.model_copy(update=updates)
    serialized = updated_session.model_dump_json()
    redis = get_redis_client()
    await redis.set(_session_key(updated_session.session_id), serialized, ex=settings.session_ttl) 
    logger.debug(f"Session {updated_session.session_id} updated with fields: {list(updates.keys())}")
    return updated_session

# removes a session from Redis
async def delete_session(session_id: str) -> None:
    redis = get_redis_client()
    await redis.delete(_session_key(session_id))
    logger.info(f"Deleted session {session_id} from Redis")

# checks if a session key exists in Redis
async def session_exists(session_id: str) -> bool:
    redis = get_redis_client()
    return await redis.exists(_session_key(session_id)) != 0
