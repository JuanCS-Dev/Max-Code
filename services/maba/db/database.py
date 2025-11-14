"""MABA Database Configuration.

Day 3: Async PostgreSQL connection management with SQLAlchemy 2.0.

Features:
- Async engine with connection pooling
- Context manager for sessions
- Automatic connection cleanup
- Environment-based configuration

Constitution Compliance:
- P1 (Completude): Complete async database implementation
- P2 (Validação): Proper connection validation and error handling
- P5 (Consciência Sistêmica): Connection pool monitoring

Author: Vértice Platform Team
License: Proprietary
"""
import logging
import os
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.pool import NullPool

from .models import Base

logger = logging.getLogger(__name__)

# ============================================================================
# DATABASE CONFIGURATION
# ============================================================================

def get_database_url() -> str:
    """Get database URL from environment variables.

    Returns:
        PostgreSQL connection string with asyncpg driver
    """
    user = os.getenv("POSTGRES_USER", "maximus")
    password = os.getenv("POSTGRES_PASSWORD", "maximus_password")
    host = os.getenv("POSTGRES_HOST", "postgres")
    port = os.getenv("POSTGRES_PORT", "5432")
    database = os.getenv("POSTGRES_DB", "maba_db")

    return f"postgresql+asyncpg://{user}:{password}@{host}:{port}/{database}"


# ============================================================================
# ENGINE AND SESSION FACTORY
# ============================================================================

# Global engine instance
_engine: AsyncEngine | None = None
_session_factory: async_sessionmaker[AsyncSession] | None = None


def get_engine(echo: bool = False) -> AsyncEngine:
    """Get or create async database engine.

    Args:
        echo: Enable SQL query logging

    Returns:
        AsyncEngine instance
    """
    global _engine

    if _engine is None:
        database_url = get_database_url()

        _engine = create_async_engine(
            database_url,
            echo=echo or os.getenv("SQL_ECHO", "false").lower() == "true",
            pool_pre_ping=True,  # Verify connections before using
            pool_size=int(os.getenv("DB_POOL_SIZE", "5")),
            max_overflow=int(os.getenv("DB_MAX_OVERFLOW", "10")),
            pool_timeout=int(os.getenv("DB_POOL_TIMEOUT", "30")),
            # For development: use NullPool to avoid connection issues
            # poolclass=NullPool if os.getenv("ENV") == "development" else None,
        )

        logger.info(f"✅ Database engine created: {database_url.split('@')[1]}")  # Hide credentials

    return _engine


def get_session_factory() -> async_sessionmaker[AsyncSession]:
    """Get or create async session factory.

    Returns:
        Session factory for creating database sessions
    """
    global _session_factory

    if _session_factory is None:
        engine = get_engine()
        _session_factory = async_sessionmaker(
            engine,
            class_=AsyncSession,
            expire_on_commit=False,  # Don't expire objects after commit
            autocommit=False,
            autoflush=False,
        )

        logger.info("✅ Database session factory created")

    return _session_factory


# ============================================================================
# SESSION DEPENDENCY
# ============================================================================

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Get database session for dependency injection.

    Usage in FastAPI:
        @app.get("/endpoint")
        async def endpoint(db: AsyncSession = Depends(get_db)):
            # Use db session here
            pass

    Yields:
        AsyncSession instance

    Raises:
        Exception: If database connection fails
    """
    factory = get_session_factory()
    async with factory() as session:
        try:
            yield session
        except Exception as e:
            logger.error(f"Database session error: {e}")
            await session.rollback()
            raise
        finally:
            await session.close()


# ============================================================================
# DATABASE INITIALIZATION
# ============================================================================

async def init_db(create_tables: bool = False) -> None:
    """Initialize database connection and optionally create tables.

    Args:
        create_tables: If True, create all tables (use only in development)

    Note:
        In production, use Alembic migrations instead of create_tables=True
    """
    engine = get_engine()

    # Test connection
    async with engine.begin() as conn:
        logger.info("✅ Database connection successful")

        if create_tables:
            logger.warning("⚠️ Creating all tables (development mode)")
            await conn.run_sync(Base.metadata.create_all)
            logger.info("✅ All tables created")


async def close_db() -> None:
    """Close database engine and cleanup connections.

    Call this during application shutdown.
    """
    global _engine, _session_factory

    if _engine:
        await _engine.dispose()
        logger.info("✅ Database engine closed")
        _engine = None
        _session_factory = None


# ============================================================================
# HEALTH CHECK
# ============================================================================

async def check_db_health() -> dict[str, any]:
    """Check database connection health.

    Returns:
        Health status dict with connection info

    Raises:
        Exception: If database is unreachable
    """
    try:
        engine = get_engine()
        async with engine.begin() as conn:
            # Simple query to test connection
            result = await conn.execute("SELECT 1 as health_check")
            row = result.fetchone()

            return {
                "status": "healthy",
                "database": "postgres",
                "driver": "asyncpg",
                "pool_size": engine.pool.size(),
                "checked_in": engine.pool.checkedin(),
                "checked_out": engine.pool.checkedout(),
                "overflow": engine.pool.overflow(),
            }
    except Exception as e:
        logger.error(f"Database health check failed: {e}")
        return {
            "status": "unhealthy",
            "error": str(e),
            "database": "postgres",
        }
