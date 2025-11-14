"""
Health Check Module for Maximus AI Services
============================================

Comprehensive health check utilities with dependency testing.

Constitution Compliance:
- P1 (Completude): Complete health check implementations
- P2 (Validação): Validate all dependencies before reporting healthy
- P5 (Consciência Sistêmica): System-wide health awareness

Features:
- PostgreSQL connectivity check
- Redis connectivity check
- Neo4j connectivity check
- HTTP service health check
- Aggregated health status
- Timeout controls
- Graceful degradation

Usage:
    from libs.health import HealthChecker
    from fastapi import FastAPI

    app = FastAPI()
    health_checker = HealthChecker(
        service_name="maximus-core",
        version="1.0.0"
    )

    # Register dependencies
    health_checker.add_postgres_check()
    health_checker.add_redis_check()

    @app.get("/health")
    async def health():
        return await health_checker.check_all()
"""

import asyncio
import logging
import os
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional, Callable, Any

logger = logging.getLogger(__name__)


# ============================================================================
# HEALTH STATUS ENUM
# ============================================================================

class HealthStatus(str, Enum):
    """Health status values."""
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"


# ============================================================================
# DEPENDENCY CHECKERS
# ============================================================================

async def check_postgres(
    host: Optional[str] = None,
    port: Optional[int] = None,
    user: Optional[str] = None,
    password: Optional[str] = None,
    database: Optional[str] = None,
    timeout: int = 5
) -> Dict[str, str]:
    """
    Check PostgreSQL connectivity.

    Args:
        host: PostgreSQL host (default: from POSTGRES_HOST env)
        port: PostgreSQL port (default: from POSTGRES_PORT env)
        user: PostgreSQL user (default: from POSTGRES_USER env)
        password: PostgreSQL password (default: from POSTGRES_PASSWORD env)
        database: Database name (default: from POSTGRES_DB env)
        timeout: Connection timeout in seconds

    Returns:
        Dict with "postgres": "healthy" or "postgres": "unhealthy: <reason>"
    """
    # Get from env if not provided
    host = host or os.getenv("POSTGRES_HOST", "localhost")
    port = port or int(os.getenv("POSTGRES_PORT", "5432"))
    user = user or os.getenv("POSTGRES_USER", "maximus")
    password = password or os.getenv("POSTGRES_PASSWORD", "")
    database = database or os.getenv("POSTGRES_DB", "maximus")

    try:
        # Import asyncpg only when needed
        import asyncpg

        conn = await asyncio.wait_for(
            asyncpg.connect(
                host=host,
                port=port,
                user=user,
                password=password,
                database=database,
            ),
            timeout=timeout
        )

        # Simple query to verify connectivity
        await conn.execute("SELECT 1")
        await conn.close()

        logger.debug("PostgreSQL health check: healthy")
        return {"postgres": "healthy"}

    except asyncio.TimeoutError:
        logger.warning(f"PostgreSQL health check: timeout after {timeout}s")
        return {"postgres": f"unhealthy: connection timeout ({timeout}s)"}

    except ImportError:
        logger.warning("PostgreSQL health check: asyncpg not installed")
        return {"postgres": "degraded: asyncpg not installed"}

    except Exception as e:
        logger.warning(f"PostgreSQL health check failed: {e}")
        return {"postgres": f"unhealthy: {str(e)[:100]}"}


async def check_redis(
    host: Optional[str] = None,
    port: Optional[int] = None,
    password: Optional[str] = None,
    timeout: int = 5
) -> Dict[str, str]:
    """
    Check Redis connectivity.

    Args:
        host: Redis host (default: from REDIS_HOST env)
        port: Redis port (default: from REDIS_PORT env)
        password: Redis password (default: from REDIS_PASSWORD env)
        timeout: Connection timeout in seconds

    Returns:
        Dict with "redis": "healthy" or "redis": "unhealthy: <reason>"
    """
    # Get from env if not provided
    host = host or os.getenv("REDIS_HOST", "localhost")
    port = port or int(os.getenv("REDIS_PORT", "6379"))
    password = password or os.getenv("REDIS_PASSWORD")

    try:
        # Import redis only when needed
        import redis.asyncio as redis

        client = redis.Redis(
            host=host,
            port=port,
            password=password,
            socket_connect_timeout=timeout,
            decode_responses=True
        )

        # Ping with timeout
        await asyncio.wait_for(client.ping(), timeout=timeout)
        await client.close()

        logger.debug("Redis health check: healthy")
        return {"redis": "healthy"}

    except asyncio.TimeoutError:
        logger.warning(f"Redis health check: timeout after {timeout}s")
        return {"redis": f"unhealthy: connection timeout ({timeout}s)"}

    except ImportError:
        logger.warning("Redis health check: redis-py[asyncio] not installed")
        return {"redis": "degraded: redis library not installed"}

    except Exception as e:
        logger.warning(f"Redis health check failed: {e}")
        return {"redis": f"unhealthy: {str(e)[:100]}"}


async def check_neo4j(
    uri: Optional[str] = None,
    user: Optional[str] = None,
    password: Optional[str] = None,
    timeout: int = 5
) -> Dict[str, str]:
    """
    Check Neo4j connectivity.

    Args:
        uri: Neo4j URI (default: from NEO4J_URI env)
        user: Neo4j user (default: from NEO4J_USER env)
        password: Neo4j password (default: from NEO4J_PASSWORD env)
        timeout: Connection timeout in seconds

    Returns:
        Dict with "neo4j": "healthy" or "neo4j": "unhealthy: <reason>"
    """
    # Get from env if not provided
    uri = uri or os.getenv("NEO4J_URI", "bolt://localhost:7687")
    user = user or os.getenv("NEO4J_USER", "neo4j")
    password = password or os.getenv("NEO4J_PASSWORD", "")

    try:
        # Import neo4j only when needed
        from neo4j import AsyncGraphDatabase

        driver = AsyncGraphDatabase.driver(uri, auth=(user, password))

        # Verify connectivity with simple query
        async with driver.session() as session:
            await asyncio.wait_for(
                session.run("RETURN 1 AS result"),
                timeout=timeout
            )

        await driver.close()

        logger.debug("Neo4j health check: healthy")
        return {"neo4j": "healthy"}

    except asyncio.TimeoutError:
        logger.warning(f"Neo4j health check: timeout after {timeout}s")
        return {"neo4j": f"unhealthy: connection timeout ({timeout}s)"}

    except ImportError:
        logger.warning("Neo4j health check: neo4j driver not installed")
        return {"neo4j": "degraded: neo4j driver not installed"}

    except Exception as e:
        logger.warning(f"Neo4j health check failed: {e}")
        return {"neo4j": f"unhealthy: {str(e)[:100]}"}


async def check_http_service(
    name: str,
    url: str,
    timeout: int = 5
) -> Dict[str, str]:
    """
    Check HTTP service health endpoint.

    Args:
        name: Service name for reporting
        url: Health check URL
        timeout: Request timeout in seconds

    Returns:
        Dict with "{name}": "healthy" or "{name}": "unhealthy: <reason>"
    """
    try:
        # Import httpx only when needed
        import httpx

        async with httpx.AsyncClient(timeout=timeout) as client:
            response = await client.get(url)

            if response.status_code == 200:
                logger.debug(f"{name} health check: healthy")
                return {name: "healthy"}
            else:
                logger.warning(f"{name} health check: HTTP {response.status_code}")
                return {name: f"unhealthy: HTTP {response.status_code}"}

    except asyncio.TimeoutError:
        logger.warning(f"{name} health check: timeout after {timeout}s")
        return {name: f"unhealthy: timeout ({timeout}s)"}

    except ImportError:
        logger.warning(f"{name} health check: httpx not installed")
        return {name: "degraded: httpx not installed"}

    except Exception as e:
        logger.warning(f"{name} health check failed: {e}")
        return {name: f"unhealthy: {str(e)[:100]}"}


# ============================================================================
# HEALTH CHECKER CLASS
# ============================================================================

class HealthChecker:
    """
    Aggregated health checker for services.

    Manages multiple dependency checks and aggregates results.

    Example:
        checker = HealthChecker(
            service_name="maximus-core",
            version="1.0.0"
        )

        # Register dependency checks
        checker.add_postgres_check()
        checker.add_redis_check()
        checker.add_http_check("maba", "http://maba:8152/health")

        # Use in FastAPI endpoint
        @app.get("/health")
        async def health():
            return await checker.check_all()
    """

    def __init__(
        self,
        service_name: str,
        version: str = "1.0.0",
        timeout: int = 5
    ):
        """
        Initialize health checker.

        Args:
            service_name: Name of this service
            version: Service version (semver)
            timeout: Default timeout for all checks (seconds)
        """
        self.service_name = service_name
        self.version = version
        self.timeout = timeout
        self.checks: List[Callable] = []

    def add_postgres_check(
        self,
        host: Optional[str] = None,
        port: Optional[int] = None,
        user: Optional[str] = None,
        password: Optional[str] = None,
        database: Optional[str] = None
    ):
        """Add PostgreSQL connectivity check."""
        async def check():
            return await check_postgres(host, port, user, password, database, self.timeout)
        self.checks.append(check)

    def add_redis_check(
        self,
        host: Optional[str] = None,
        port: Optional[int] = None,
        password: Optional[str] = None
    ):
        """Add Redis connectivity check."""
        async def check():
            return await check_redis(host, port, password, self.timeout)
        self.checks.append(check)

    def add_neo4j_check(
        self,
        uri: Optional[str] = None,
        user: Optional[str] = None,
        password: Optional[str] = None
    ):
        """Add Neo4j connectivity check."""
        async def check():
            return await check_neo4j(uri, user, password, self.timeout)
        self.checks.append(check)

    def add_http_check(self, name: str, url: str):
        """Add HTTP service health check."""
        async def check():
            return await check_http_service(name, url, self.timeout)
        self.checks.append(check)

    def add_custom_check(self, check_func: Callable):
        """Add custom check function."""
        self.checks.append(check_func)

    async def check_all(self) -> Dict[str, Any]:
        """
        Run all registered health checks.

        Returns:
            Health response dict with status and dependency results
        """
        # Run all checks concurrently
        results = await asyncio.gather(*[check() for check in self.checks])

        # Aggregate dependency statuses
        dependencies = {}
        for result in results:
            dependencies.update(result)

        # Determine overall status
        if not dependencies:
            # No dependencies to check
            overall_status = HealthStatus.HEALTHY
        elif all("healthy" in v for v in dependencies.values()):
            # All dependencies healthy
            overall_status = HealthStatus.HEALTHY
        elif any("unhealthy" in v for v in dependencies.values()):
            # At least one dependency unhealthy
            overall_status = HealthStatus.UNHEALTHY
        else:
            # Some dependencies degraded
            overall_status = HealthStatus.DEGRADED

        return {
            "status": overall_status.value,
            "service": self.service_name,
            "version": self.version,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "dependencies": dependencies if dependencies else None
        }


# ============================================================================
# SIMPLIFIED HEALTH CHECK (No Dependencies)
# ============================================================================

def simple_health_response(service_name: str, version: str = "1.0.0") -> Dict[str, Any]:
    """
    Create simple health response without dependency checks.

    Use for services with no external dependencies or when
    dependency checking is not critical.

    Args:
        service_name: Name of the service
        version: Service version

    Returns:
        Basic health response dict
    """
    return {
        "status": HealthStatus.HEALTHY.value,
        "service": service_name,
        "version": version,
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }
