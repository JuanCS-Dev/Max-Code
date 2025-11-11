"""
Database client for MAXIMUS services.
Uses asyncpg for PostgreSQL and aioredis for Redis.
"""

import os
from typing import Optional, Any, Dict, List
import asyncpg
import redis.asyncio as aioredis
import structlog

logger = structlog.get_logger(__name__)


class DatabaseClient:
    """Async PostgreSQL client."""

    def __init__(
        self,
        host: str = "localhost",
        port: int = 5432,
        database: str = "maximus",
        user: str = "maximus",
        password: str = "maximus2024",
    ):
        self.host = host
        self.port = port
        self.database = database
        self.user = user
        self.password = password
        self.pool: Optional[asyncpg.Pool] = None

    async def connect(self):
        """Create connection pool."""
        self.pool = await asyncpg.create_pool(
            host=self.host,
            port=self.port,
            database=self.database,
            user=self.user,
            password=self.password,
            min_size=10,
            max_size=100,
        )
        logger.info("postgres_connected", database=self.database)

    async def close(self):
        """Close connection pool."""
        if self.pool:
            await self.pool.close()
            logger.info("postgres_disconnected")

    async def execute(self, query: str, *args) -> str:
        """Execute query (INSERT/UPDATE/DELETE)."""
        async with self.pool.acquire() as conn:
            return await conn.execute(query, *args)

    async def fetch(self, query: str, *args) -> List[Dict[str, Any]]:
        """Fetch multiple rows."""
        async with self.pool.acquire() as conn:
            rows = await conn.fetch(query, *args)
            return [dict(row) for row in rows]

    async def fetchrow(self, query: str, *args) -> Optional[Dict[str, Any]]:
        """Fetch single row."""
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(query, *args)
            return dict(row) if row else None


class CacheClient:
    """Async Redis client for caching."""

    def __init__(
        self,
        host: str = "localhost",
        port: int = 6379,
        password: str = "maximus2024",
        db: int = 0,
    ):
        self.host = host
        self.port = port
        self.password = password
        self.db = db
        self.client: Optional[aioredis.Redis] = None

    async def connect(self):
        """Connect to Redis."""
        self.client = await aioredis.from_url(
            f"redis://:{self.password}@{self.host}:{self.port}/{self.db}",
            encoding="utf-8",
            decode_responses=True,
        )
        logger.info("redis_connected", host=self.host)

    async def close(self):
        """Close Redis connection."""
        if self.client:
            await self.client.close()
            logger.info("redis_disconnected")

    async def get(self, key: str) -> Optional[str]:
        """Get value from cache."""
        return await self.client.get(key)

    async def set(self, key: str, value: str, ttl: int = 3600):
        """Set value in cache with TTL (seconds)."""
        await self.client.set(key, value, ex=ttl)

    async def delete(self, key: str):
        """Delete key from cache."""
        await self.client.delete(key)


# Singleton instances
_db: Optional[DatabaseClient] = None
_cache: Optional[CacheClient] = None


async def get_db() -> DatabaseClient:
    """Get database client singleton."""
    global _db
    if _db is None:
        _db = DatabaseClient()
        await _db.connect()
    return _db


async def get_cache() -> CacheClient:
    """Get cache client singleton."""
    global _cache
    if _cache is None:
        _cache = CacheClient()
        await _cache.connect()
    return _cache
