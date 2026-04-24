import json
import logging
from datetime import timedelta

logger = logging.getLogger(__name__)
SESSION_TTL = 3600  # 1 hour
_memory_sessions = {}  # fallback if Redis unavailable


def _get_redis():
    from app import redis_client
    return redis_client


def get_session(phone: str) -> dict:
    """Load session for a phone number."""
    redis = _get_redis()
    key = f"session:{phone}"
    
    if redis:
        try:
            data = redis.get(key)
            if data:
                return json.loads(data)
        except Exception as e:
            logger.warning(f"Redis get error: {e}")
    
    return _memory_sessions.get(key, {})


def save_session(phone: str, session: dict):
    """Save session. Expires in 1 hour of inactivity."""
    redis = _get_redis()
    key = f"session:{phone}"
    
    if redis:
        try:
            redis.setex(key, SESSION_TTL, json.dumps(session))
            return
        except Exception as e:
            logger.warning(f"Redis set error: {e}")
    
    _memory_sessions[key] = session


def clear_session(phone: str):
    """Clear session (after warranty flow completes, etc.)"""
    redis = _get_redis()
    key = f"session:{phone}"
    
    if redis:
        try:
            redis.delete(key)
        except Exception:
            pass
    
    _memory_sessions.pop(key, None)
