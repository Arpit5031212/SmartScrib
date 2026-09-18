from functools import lru_cache

from config import get_settings
import redis.asyncio as redis


@lru_cache
def get_redis_client() -> redis.Redis:
    settings = get_settings()

    pool = redis.ConnectionPool(
        host=settings.redis_host,
        port=settings.redis_port,
        password=settings.redis_password,
        db=settings.redis_db,
        decode_responses=True,
        max_connections=settings.redis_max_connections
    )

    return redis.Redis(connection_pool=pool)
