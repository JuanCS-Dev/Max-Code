"""
MAXIMUS Response Cache

Caches MAXIMUS API responses to reduce latency and load.

Supports:
- In-memory cache (fast, simple)
- Redis cache (distributed, persistent)

Cache keys are based on:
- API endpoint
- Request payload (hashed)

TTL varies by analysis type:
- Systemic analysis: 10 minutes (stable)
- Ethical review: 30 minutes (very stable)
- Edge cases: 5 minutes (changes with code)
"""

import hashlib
import json
import time
from typing import Any, Dict, Optional
from dataclasses import dataclass
from enum import Enum


# ============================================================================
# ENUMS
# ============================================================================

class CacheBackend(str, Enum):
    """Cache backend types"""
    MEMORY = "memory"
    REDIS = "redis"


# ============================================================================
# DATA MODELS
# ============================================================================

@dataclass
class CacheEntry:
    """Cache entry"""
    key: str
    value: Any
    timestamp: float
    ttl: int  # seconds
    hits: int = 0

    def is_expired(self) -> bool:
        """Check if entry is expired"""
        return (time.time() - self.timestamp) > self.ttl


@dataclass
class CacheStats:
    """Cache statistics"""
    hits: int = 0
    misses: int = 0
    evictions: int = 0
    size: int = 0

    @property
    def hit_rate(self) -> float:
        """Calculate hit rate"""
        total = self.hits + self.misses
        return self.hits / total if total > 0 else 0.0


# ============================================================================
# MEMORY CACHE
# ============================================================================

class MemoryCache:
    """
    In-memory cache (fast, simple).

    Good for:
    - Single-process applications
    - Development/testing
    - Low-latency requirements

    Limitations:
    - Not distributed (per-process)
    - Lost on restart
    """

    def __init__(self, default_ttl: int = 300, max_size: int = 1000):
        """
        Initialize memory cache.

        Args:
            default_ttl: Default TTL in seconds (default: 300 = 5 minutes)
            max_size: Maximum cache size (default: 1000 entries)
        """
        self.default_ttl = default_ttl
        self.max_size = max_size
        self._cache: Dict[str, CacheEntry] = {}
        self._stats = CacheStats()

    def get(self, key: str) -> Optional[Any]:
        """
        Get value from cache.

        Returns:
            Cached value or None if not found/expired
        """
        if key not in self._cache:
            self._stats.misses += 1
            return None

        entry = self._cache[key]

        # Check expiration
        if entry.is_expired():
            del self._cache[key]
            self._stats.misses += 1
            self._stats.evictions += 1
            return None

        # Hit
        entry.hits += 1
        self._stats.hits += 1
        return entry.value

    def set(self, key: str, value: Any, ttl: Optional[int] = None):
        """
        Set value in cache.

        Args:
            key: Cache key
            value: Value to cache
            ttl: TTL in seconds (uses default if None)
        """
        ttl = ttl or self.default_ttl

        # Evict if full
        if len(self._cache) >= self.max_size:
            self._evict_lru()

        # Store entry
        self._cache[key] = CacheEntry(
            key=key,
            value=value,
            timestamp=time.time(),
            ttl=ttl,
        )

        self._stats.size = len(self._cache)

    def delete(self, key: str):
        """Delete entry from cache"""
        if key in self._cache:
            del self._cache[key]
            self._stats.size = len(self._cache)

    def clear(self):
        """Clear all cache entries"""
        self._cache.clear()
        self._stats.size = 0

    def _evict_lru(self):
        """Evict least recently used entry"""
        if not self._cache:
            return

        # Find LRU (entry with oldest timestamp + fewest hits)
        lru_key = min(
            self._cache.keys(),
            key=lambda k: (self._cache[k].hits, self._cache[k].timestamp)
        )

        del self._cache[lru_key]
        self._stats.evictions += 1

    def get_stats(self) -> CacheStats:
        """Get cache statistics"""
        return self._stats


# ============================================================================
# REDIS CACHE (Optional)
# ============================================================================

class RedisCache:
    """
    Redis cache (distributed, persistent).

    Good for:
    - Multi-process/multi-server deployments
    - Persistence across restarts
    - Distributed caching

    Requires:
    - Redis server running
    - redis-py library
    """

    def __init__(
        self,
        redis_url: str = "redis://localhost:6379",
        db: int = 0,
        default_ttl: int = 300,
    ):
        """
        Initialize Redis cache.

        Args:
            redis_url: Redis URL (default: redis://localhost:6379)
            db: Redis database number (default: 0)
            default_ttl: Default TTL in seconds (default: 300)
        """
        try:
            import redis
            self.redis = redis.from_url(redis_url, db=db, decode_responses=True)
            self.default_ttl = default_ttl
            self._stats = CacheStats()
        except ImportError:
            raise ImportError(
                "Redis cache requires redis-py. Install with: pip install redis"
            )

    def get(self, key: str) -> Optional[Any]:
        """Get value from Redis"""
        try:
            value = self.redis.get(key)

            if value is None:
                self._stats.misses += 1
                return None

            # Deserialize
            self._stats.hits += 1
            return json.loads(value)

        except Exception:
            self._stats.misses += 1
            return None

    def set(self, key: str, value: Any, ttl: Optional[int] = None):
        """Set value in Redis"""
        ttl = ttl or self.default_ttl

        # Serialize
        serialized = json.dumps(value)

        # Store with TTL
        self.redis.setex(key, ttl, serialized)

    def delete(self, key: str):
        """Delete entry from Redis"""
        self.redis.delete(key)

    def clear(self):
        """Clear all cache entries (WARNING: clears entire DB)"""
        self.redis.flushdb()

    def get_stats(self) -> CacheStats:
        """Get cache statistics"""
        info = self.redis.info("stats")
        self._stats.hits = info.get("keyspace_hits", 0)
        self._stats.misses = info.get("keyspace_misses", 0)
        self._stats.evictions = info.get("evicted_keys", 0)

        # Get size (number of keys)
        self._stats.size = self.redis.dbsize()

        return self._stats


# ============================================================================
# MAXIMUS CACHE (Facade)
# ============================================================================

class MaximusCache:
    """
    Facade for MAXIMUS response caching.

    Automatically selects backend (memory or redis) and provides
    convenient methods for caching MAXIMUS API responses.

    Example:
        cache = MaximusCache(backend="memory")

        # Try to get from cache
        result = cache.get_systemic_analysis(action, context)

        if result is None:
            # Cache miss - call MAXIMUS
            result = await maximus_client.analyze_systemic_impact(action, context)

            # Store in cache
            cache.set_systemic_analysis(action, context, result)
    """

    def __init__(
        self,
        backend: CacheBackend = CacheBackend.MEMORY,
        redis_url: str = "redis://localhost:6379",
        default_ttl: int = 300,
    ):
        """
        Initialize MAXIMUS cache.

        Args:
            backend: Cache backend (memory or redis)
            redis_url: Redis URL (if using redis)
            default_ttl: Default TTL in seconds
        """
        self.backend = backend

        if backend == CacheBackend.MEMORY:
            self._cache = MemoryCache(default_ttl=default_ttl)
        elif backend == CacheBackend.REDIS:
            self._cache = RedisCache(redis_url=redis_url, default_ttl=default_ttl)
        else:
            raise ValueError(f"Unknown cache backend: {backend}")

        # TTL by analysis type (from config)
        self.ttl_by_type = {
            "systemic_analysis": 600,    # 10 minutes
            "ethical_review": 1800,      # 30 minutes
            "edge_case_prediction": 300, # 5 minutes
            "code_healing": 60,          # 1 minute
            "web_search": 3600,          # 1 hour
            "narrative": 1800,           # 30 minutes
        }

    # ========================================================================
    # CACHE KEY GENERATION
    # ========================================================================

    def _generate_key(self, prefix: str, payload: Dict[str, Any]) -> str:
        """
        Generate cache key from prefix + payload hash.

        Args:
            prefix: Key prefix (e.g., "systemic_analysis")
            payload: Request payload (will be hashed)

        Returns:
            Cache key (e.g., "systemic_analysis:a1b2c3d4")
        """
        # Serialize payload (sorted keys for consistency)
        serialized = json.dumps(payload, sort_keys=True)

        # Hash
        hash_obj = hashlib.sha256(serialized.encode())
        payload_hash = hash_obj.hexdigest()[:16]  # First 16 chars

        return f"{prefix}:{payload_hash}"

    # ========================================================================
    # SYSTEMIC ANALYSIS CACHE
    # ========================================================================

    def get_systemic_analysis(
        self,
        action: Dict[str, Any],
        context: Dict[str, Any]
    ) -> Optional[Any]:
        """Get cached systemic analysis"""
        key = self._generate_key("systemic_analysis", {"action": action, "context": context})
        return self._cache.get(key)

    def set_systemic_analysis(
        self,
        action: Dict[str, Any],
        context: Dict[str, Any],
        result: Any
    ):
        """Cache systemic analysis"""
        key = self._generate_key("systemic_analysis", {"action": action, "context": context})
        ttl = self.ttl_by_type["systemic_analysis"]
        self._cache.set(key, result, ttl=ttl)

    # ========================================================================
    # ETHICAL REVIEW CACHE
    # ========================================================================

    def get_ethical_review(self, code: str, context: Dict[str, Any]) -> Optional[Any]:
        """Get cached ethical review"""
        key = self._generate_key("ethical_review", {"code": code, "context": context})
        return self._cache.get(key)

    def set_ethical_review(self, code: str, context: Dict[str, Any], result: Any):
        """Cache ethical review"""
        key = self._generate_key("ethical_review", {"code": code, "context": context})
        ttl = self.ttl_by_type["ethical_review"]
        self._cache.set(key, result, ttl=ttl)

    # ========================================================================
    # EDGE CASE PREDICTION CACHE
    # ========================================================================

    def get_edge_cases(
        self,
        function_code: str,
        test_suite: list
    ) -> Optional[Any]:
        """Get cached edge cases"""
        key = self._generate_key(
            "edge_case_prediction",
            {"function_code": function_code, "test_suite": test_suite}
        )
        return self._cache.get(key)

    def set_edge_cases(
        self,
        function_code: str,
        test_suite: list,
        result: Any
    ):
        """Cache edge cases"""
        key = self._generate_key(
            "edge_case_prediction",
            {"function_code": function_code, "test_suite": test_suite}
        )
        ttl = self.ttl_by_type["edge_case_prediction"]
        self._cache.set(key, result, ttl=ttl)

    # ========================================================================
    # CODE HEALING CACHE
    # ========================================================================

    def get_healing(
        self,
        broken_code: str,
        error_trace: str,
    ) -> Optional[Any]:
        """Get cached healing suggestion"""
        key = self._generate_key(
            "code_healing",
            {"broken_code": broken_code, "error_trace": error_trace}
        )
        return self._cache.get(key)

    def set_healing(
        self,
        broken_code: str,
        error_trace: str,
        result: Any
    ):
        """Cache healing suggestion"""
        key = self._generate_key(
            "code_healing",
            {"broken_code": broken_code, "error_trace": error_trace}
        )
        ttl = self.ttl_by_type["code_healing"]
        self._cache.set(key, result, ttl=ttl)

    # ========================================================================
    # WEB SEARCH CACHE
    # ========================================================================

    def get_search(self, query: str, context: str) -> Optional[Any]:
        """Get cached search results"""
        key = self._generate_key("web_search", {"query": query, "context": context})
        return self._cache.get(key)

    def set_search(self, query: str, context: str, result: Any):
        """Cache search results"""
        key = self._generate_key("web_search", {"query": query, "context": context})
        ttl = self.ttl_by_type["web_search"]
        self._cache.set(key, result, ttl=ttl)

    # ========================================================================
    # NARRATIVE CACHE
    # ========================================================================

    def get_narrative(self, code_changes: list, context: Dict[str, Any]) -> Optional[Any]:
        """Get cached narrative"""
        key = self._generate_key(
            "narrative",
            {"code_changes": code_changes, "context": context}
        )
        return self._cache.get(key)

    def set_narrative(self, code_changes: list, context: Dict[str, Any], result: Any):
        """Cache narrative"""
        key = self._generate_key(
            "narrative",
            {"code_changes": code_changes, "context": context}
        )
        ttl = self.ttl_by_type["narrative"]
        self._cache.set(key, result, ttl=ttl)

    # ========================================================================
    # CACHE MANAGEMENT
    # ========================================================================

    def clear(self):
        """Clear all cache entries"""
        self._cache.clear()

    def get_stats(self) -> CacheStats:
        """Get cache statistics"""
        return self._cache.get_stats()

    def print_stats(self):
        """Print cache statistics"""
        stats = self.get_stats()

        print("\n" + "="*60)
        print("MAXIMUS Cache Statistics")
        print("="*60)
        print(f"Backend:     {self.backend.value}")
        print(f"Hits:        {stats.hits}")
        print(f"Misses:      {stats.misses}")
        print(f"Hit Rate:    {stats.hit_rate:.1%}")
        print(f"Evictions:   {stats.evictions}")
        print(f"Size:        {stats.size} entries")
        print("="*60 + "\n")
