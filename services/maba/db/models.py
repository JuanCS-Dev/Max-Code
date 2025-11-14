"""MABA Database Models.

Day 3: SQLAlchemy async models for browser automation and cognitive map.

Constitution Compliance:
- P1 (Completude): Complete model definitions with all fields
- P2 (Validação): Type hints and constraints for all columns
- P4 (Rastreabilidade): Full audit trail via created_at/updated_at
- P5 (Consciência Sistêmica): Cognitive map learns from system behavior

Tables:
- BrowserSession: Track active browser automation sessions
- CognitiveMapPage: Store visited pages and learned selectors
- BrowserAction: Audit log of all actions
- NavigationPath: Learned navigation sequences

Author: Vértice Platform Team
License: Proprietary
"""
import hashlib
import uuid
from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.sql import func


# ============================================================================
# BASE
# ============================================================================

class Base(AsyncAttrs, DeclarativeBase):
    """Base class for all models with async support."""
    pass


# ============================================================================
# BROWSER SESSION MODEL
# ============================================================================

class BrowserSession(Base):
    """Browser automation session.

    Represents an active browser context with its configuration and state.

    Attributes:
        id: Unique session identifier
        created_at: Session creation timestamp
        last_active: Last activity timestamp
        closed_at: Session closure timestamp (None if active)
        status: Session status (active, idle, closed, error)
        browser_type: Browser engine (chromium, firefox, webkit)
        viewport_width: Browser viewport width in pixels
        viewport_height: Browser viewport height in pixels
        user_agent: Custom user agent string
        context_data: Additional context configuration (JSONB)
        metadata: Custom metadata (JSONB)
    """
    __tablename__ = 'browser_sessions'

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    last_active: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    closed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    status: Mapped[str] = mapped_column(String(20), nullable=False, server_default='active')
    browser_type: Mapped[str] = mapped_column(String(20), nullable=False, server_default='chromium')
    viewport_width: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    viewport_height: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    user_agent: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    context_data: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)
    metadata: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)

    # Relationships
    actions: Mapped[list["BrowserAction"]] = relationship(back_populates="session", cascade="all, delete-orphan")

    # Constraints
    __table_args__ = (
        CheckConstraint("status IN ('active', 'idle', 'closed', 'error')", name='valid_session_status'),
        CheckConstraint("browser_type IN ('chromium', 'firefox', 'webkit')", name='valid_browser_type'),
    )

    def __repr__(self) -> str:
        return f"<BrowserSession(id={self.id}, status={self.status}, browser={self.browser_type})>"

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "id": str(self.id),
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "last_active": self.last_active.isoformat() if self.last_active else None,
            "closed_at": self.closed_at.isoformat() if self.closed_at else None,
            "status": self.status,
            "browser_type": self.browser_type,
            "viewport": {
                "width": self.viewport_width,
                "height": self.viewport_height
            } if self.viewport_width else None,
            "user_agent": self.user_agent,
            "context_data": self.context_data,
            "metadata": self.metadata
        }


# ============================================================================
# COGNITIVE MAP PAGE MODEL
# ============================================================================

class CognitiveMapPage(Base):
    """Cognitive map page representation.

    Stores learned information about visited web pages, including
    element selectors, importance scores, and visit history.

    Attributes:
        id: Unique page identifier
        url: Full page URL
        url_hash: SHA256 hash of URL for fast lookups
        title: Page title
        domain: Page domain
        visited_count: Number of times visited
        first_visited: First visit timestamp
        last_visited: Last visit timestamp
        elements_snapshot: Learned element selectors (JSONB)
        importance_score: ML-based page importance (0.0-1.0)
        metadata: Custom metadata (JSONB)
        created_at: Record creation timestamp
        updated_at: Last update timestamp
    """
    __tablename__ = 'cognitive_map_pages'

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    url: Mapped[str] = mapped_column(String(2048), nullable=False)
    url_hash: Mapped[str] = mapped_column(String(64), nullable=False, unique=True)
    title: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    domain: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    visited_count: Mapped[int] = mapped_column(Integer, nullable=False, server_default='0')
    first_visited: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    last_visited: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    elements_snapshot: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)
    importance_score: Mapped[float] = mapped_column(Float, nullable=False, server_default='0.0')
    metadata: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    @staticmethod
    def hash_url(url: str) -> str:
        """Generate SHA256 hash of URL."""
        return hashlib.sha256(url.encode('utf-8')).hexdigest()

    def __repr__(self) -> str:
        return f"<CognitiveMapPage(url={self.url[:50]}, visited={self.visited_count})>"

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "id": str(self.id),
            "url": self.url,
            "title": self.title,
            "domain": self.domain,
            "visited_count": self.visited_count,
            "first_visited": self.first_visited.isoformat() if self.first_visited else None,
            "last_visited": self.last_visited.isoformat() if self.last_visited else None,
            "elements_snapshot": self.elements_snapshot,
            "importance_score": self.importance_score,
            "metadata": self.metadata
        }


# ============================================================================
# BROWSER ACTION MODEL
# ============================================================================

class BrowserAction(Base):
    """Browser action audit log.

    Records all browser automation actions for debugging,
    analytics, and learning.

    Attributes:
        id: Unique action identifier
        session_id: Related browser session
        action_type: Type of action (navigate, click, type, etc.)
        url: Target URL
        selector: CSS/XPath selector used
        parameters: Action parameters (JSONB)
        success: Whether action succeeded
        error_message: Error message if failed
        error_type: Error classification
        duration_ms: Action duration in milliseconds
        screenshot_path: Path to screenshot if captured
        metadata: Custom metadata (JSONB)
        created_at: Action timestamp
    """
    __tablename__ = 'browser_actions'

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('browser_sessions.id', ondelete='CASCADE'), nullable=False)
    action_type: Mapped[str] = mapped_column(String(50), nullable=False)
    url: Mapped[Optional[str]] = mapped_column(String(2048), nullable=True)
    selector: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    parameters: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)
    success: Mapped[bool] = mapped_column(Boolean, nullable=False)
    error_message: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    error_type: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    duration_ms: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    screenshot_path: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    metadata: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # Relationship
    session: Mapped["BrowserSession"] = relationship(back_populates="actions")

    # Constraints
    __table_args__ = (
        CheckConstraint(
            "action_type IN ('navigate', 'click', 'type', 'screenshot', 'extract', 'scroll', 'wait', 'evaluate')",
            name='valid_action_type'
        ),
    )

    def __repr__(self) -> str:
        return f"<BrowserAction(type={self.action_type}, success={self.success}, session={self.session_id})>"

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "id": str(self.id),
            "session_id": str(self.session_id),
            "action_type": self.action_type,
            "url": self.url,
            "selector": self.selector,
            "parameters": self.parameters,
            "success": self.success,
            "error_message": self.error_message,
            "error_type": self.error_type,
            "duration_ms": self.duration_ms,
            "screenshot_path": self.screenshot_path,
            "metadata": self.metadata,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }


# ============================================================================
# NAVIGATION PATH MODEL
# ============================================================================

class NavigationPath(Base):
    """Learned navigation path between pages.

    Stores successful navigation sequences for the cognitive map
    to learn optimal paths between pages.

    Attributes:
        id: Unique path identifier
        from_url_hash: Source page URL hash
        to_url_hash: Destination page URL hash
        action_sequence: Sequence of actions (JSONB array)
        success_count: Number of successful traversals
        failure_count: Number of failed attempts
        avg_duration_ms: Average traversal duration
        confidence_score: Path reliability score (0.0-1.0)
        last_used: Last usage timestamp
        created_at: Path discovery timestamp
    """
    __tablename__ = 'navigation_paths'

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    from_url_hash: Mapped[str] = mapped_column(String(64), nullable=False)
    to_url_hash: Mapped[str] = mapped_column(String(64), nullable=False)
    action_sequence: Mapped[dict] = mapped_column(JSONB, nullable=False)  # Array of actions
    success_count: Mapped[int] = mapped_column(Integer, nullable=False, server_default='0')
    failure_count: Mapped[int] = mapped_column(Integer, nullable=False, server_default='0')
    avg_duration_ms: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    confidence_score: Mapped[float] = mapped_column(Float, nullable=False, server_default='0.0')
    last_used: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    __table_args__ = (
        UniqueConstraint('from_url_hash', 'to_url_hash', name='unique_navigation_path'),
    )

    def __repr__(self) -> str:
        return f"<NavigationPath(from={self.from_url_hash[:8]}..., to={self.to_url_hash[:8]}..., confidence={self.confidence_score})>"

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "id": str(self.id),
            "from_url_hash": self.from_url_hash,
            "to_url_hash": self.to_url_hash,
            "action_sequence": self.action_sequence,
            "success_count": self.success_count,
            "failure_count": self.failure_count,
            "avg_duration_ms": self.avg_duration_ms,
            "confidence_score": self.confidence_score,
            "last_used": self.last_used.isoformat() if self.last_used else None,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }
