"""Unit tests for database functions.

Day 4: Testing database utilities and health checks.

Tests cover:
- get_db() dependency
- init_db() initialization
- check_db_health() monitoring
- Connection pooling
- Error handling

Author: Vértice Platform Team
License: Proprietary
"""
import pytest
from unittest.mock import AsyncMock, patch

from db.database import (
    get_database_url,
    get_engine,
    get_session_factory,
    init_db,
    close_db,
    check_db_health,
)


# ============================================================================
# CONFIGURATION TESTS
# ============================================================================

@pytest.mark.unit
class TestDatabaseConfiguration:
    """Test database configuration."""

    def test_get_database_url_defaults(self, monkeypatch):
        """Test database URL with default values."""
        # Clear environment
        for key in ["POSTGRES_USER", "POSTGRES_PASSWORD", "POSTGRES_HOST", "POSTGRES_PORT", "POSTGRES_DB"]:
            monkeypatch.delenv(key, raising=False)

        url = get_database_url()

        assert "postgresql+asyncpg://" in url
        assert "maximus:maximus_password" in url
        assert "postgres:5432" in url
        assert "maba_db" in url

    def test_get_database_url_custom(self, monkeypatch):
        """Test database URL with custom environment variables."""
        monkeypatch.setenv("POSTGRES_USER", "custom_user")
        monkeypatch.setenv("POSTGRES_PASSWORD", "custom_pass")
        monkeypatch.setenv("POSTGRES_HOST", "custom_host")
        monkeypatch.setenv("POSTGRES_PORT", "5433")
        monkeypatch.setenv("POSTGRES_DB", "custom_db")

        url = get_database_url()

        assert "custom_user:custom_pass" in url
        assert "custom_host:5433" in url
        assert "custom_db" in url


# ============================================================================
# ENGINE TESTS
# ============================================================================

@pytest.mark.unit
class TestDatabaseEngine:
    """Test database engine creation."""

    def test_get_engine_singleton(self):
        """Test that get_engine returns same instance."""
        engine1 = get_engine()
        engine2 = get_engine()

        # Should return same instance (singleton pattern)
        assert engine1 is engine2

    def test_get_session_factory(self):
        """Test session factory creation."""
        factory = get_session_factory()

        assert factory is not None
        assert callable(factory)


# ============================================================================
# HEALTH CHECK TESTS
# ============================================================================

@pytest.mark.unit
@pytest.mark.database
class TestDatabaseHealth:
    """Test database health checks."""

    async def test_check_db_health_success(self, test_engine):
        """Test successful health check."""
        with patch("db.database.get_engine", return_value=test_engine):
            health = await check_db_health()

            assert health["status"] == "healthy"
            assert health["database"] == "postgres"
            assert health["driver"] == "asyncpg"
            assert "pool_size" in health

    async def test_check_db_health_failure(self):
        """Test health check with database error."""
        # Mock engine that raises error
        mock_engine = AsyncMock()
        mock_engine.begin = AsyncMock(side_effect=Exception("Connection failed"))

        with patch("db.database.get_engine", return_value=mock_engine):
            health = await check_db_health()

            assert health["status"] == "unhealthy"
            assert "error" in health
            assert "Connection failed" in health["error"]


# ============================================================================
# INITIALIZATION TESTS
# ============================================================================

@pytest.mark.unit
class TestDatabaseInitialization:
    """Test database initialization."""

    async def test_init_db_without_create_tables(self, test_engine):
        """Test init_db without creating tables."""
        with patch("db.database.get_engine", return_value=test_engine):
            # Should not raise
            await init_db(create_tables=False)

    async def test_close_db(self, test_engine):
        """Test database cleanup."""
        with patch("db.database.get_engine", return_value=test_engine):
            # Should not raise
            await close_db()
