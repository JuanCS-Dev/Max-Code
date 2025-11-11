"""
Response caching decorator for FastAPI endpoints.
Reduces latency for frequently accessed data.
"""

import functools
import hashlib
import json
from typing import Any, Callable
import structlog

logger = structlog.get_logger(__name__)

# Import from persistence (if available)
# from persistence.db_client import get_cache


def cached(ttl: int = 60, key_prefix: str = "cache"):
    """
    Cache decorator for async functions.

    Args:
        ttl: Time-to-live in seconds
        key_prefix: Prefix for cache keys

    Example:
        @cached(ttl=300, key_prefix="consciousness")
        async def get_state():
            # Expensive operation
            return await fetch_state()
    """

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        async def wrapper(*args, **kwargs) -> Any:
            # Generate cache key from function name + args
            key_data = f"{func.__name__}:{args}:{kwargs}"
            cache_key = f"{key_prefix}:{hashlib.md5(key_data.encode()).hexdigest()}"

            try:
                # Try to get from cache (Redis)
                from persistence.db_client import get_cache

                cache = await get_cache()
                cached_value = await cache.get(cache_key)

                if cached_value:
                    logger.info("cache_hit", key=cache_key)
                    return json.loads(cached_value)

            except Exception as e:
                logger.warning("cache_error", error=str(e))
                # Fallback to function execution if cache fails

            # Cache miss - execute function
            logger.info("cache_miss", key=cache_key)
            result = await func(*args, **kwargs)

            # Store in cache
            try:
                cache = await get_cache()
                await cache.set(cache_key, json.dumps(result), ttl=ttl)
                logger.info("cache_set", key=cache_key, ttl=ttl)
            except Exception as e:
                logger.warning("cache_set_error", error=str(e))

            return result

        return wrapper

    return decorator


# Usage example
"""
from fastapi import FastAPI
from performance.cache_decorator import cached

app = FastAPI()

@app.get("/api/consciousness/state")
@cached(ttl=30, key_prefix="consciousness")
async def get_consciousness_state():
    # This will be cached for 30 seconds
    return await fetch_expensive_state()
"""
