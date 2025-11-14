"""create browser sessions and cognitive map tables

Revision ID: 001
Revises:
Create Date: 2025-11-14

Day 3: MABA Database Schema

Tables created:
- browser_sessions: Track active browser automation sessions
- cognitive_map_pages: Store page elements and navigation data
- browser_actions: Audit log of all browser actions
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID, JSONB
import uuid

# revision identifiers, used by Alembic.
revision: str = '001'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Create MABA database tables."""

    # ============================================================================
    # TABLE: browser_sessions
    # Purpose: Track browser automation sessions
    # ============================================================================
    op.create_table(
        'browser_sessions',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('now()')),
        sa.Column('last_active', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('now()')),
        sa.Column('closed_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('status', sa.String(20), nullable=False, server_default='active'),
        sa.Column('browser_type', sa.String(20), nullable=False, server_default='chromium'),
        sa.Column('viewport_width', sa.Integer, nullable=True),
        sa.Column('viewport_height', sa.Integer, nullable=True),
        sa.Column('user_agent', sa.String(500), nullable=True),
        sa.Column('context_data', JSONB, nullable=True),
        sa.Column('metadata', JSONB, nullable=True),
        sa.CheckConstraint("status IN ('active', 'idle', 'closed', 'error')", name='valid_session_status'),
        sa.CheckConstraint("browser_type IN ('chromium', 'firefox', 'webkit')", name='valid_browser_type')
    )

    # ============================================================================
    # TABLE: cognitive_map_pages
    # Purpose: Store visited pages and learned element selectors
    # ============================================================================
    op.create_table(
        'cognitive_map_pages',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('url', sa.String(2048), nullable=False),
        sa.Column('url_hash', sa.String(64), nullable=False, unique=True),  # SHA256 hash for fast lookup
        sa.Column('title', sa.String(500), nullable=True),
        sa.Column('domain', sa.String(255), nullable=True),
        sa.Column('visited_count', sa.Integer, nullable=False, server_default='0'),
        sa.Column('first_visited', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('now()')),
        sa.Column('last_visited', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('now()')),
        sa.Column('elements_snapshot', JSONB, nullable=True),  # Store learned selectors
        sa.Column('importance_score', sa.Float, nullable=False, server_default='0.0'),  # ML-based importance
        sa.Column('metadata', JSONB, nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('now()'))
    )

    # ============================================================================
    # TABLE: browser_actions
    # Purpose: Audit log of all browser automation actions
    # ============================================================================
    op.create_table(
        'browser_actions',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('session_id', UUID(as_uuid=True), sa.ForeignKey('browser_sessions.id', ondelete='CASCADE'), nullable=False),
        sa.Column('action_type', sa.String(50), nullable=False),
        sa.Column('url', sa.String(2048), nullable=True),
        sa.Column('selector', sa.String(500), nullable=True),
        sa.Column('parameters', JSONB, nullable=True),
        sa.Column('success', sa.Boolean, nullable=False),
        sa.Column('error_message', sa.Text, nullable=True),
        sa.Column('error_type', sa.String(100), nullable=True),
        sa.Column('duration_ms', sa.Integer, nullable=True),
        sa.Column('screenshot_path', sa.String(500), nullable=True),
        sa.Column('metadata', JSONB, nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('now()')),
        sa.CheckConstraint(
            "action_type IN ('navigate', 'click', 'type', 'screenshot', 'extract', 'scroll', 'wait', 'evaluate')",
            name='valid_action_type'
        )
    )

    # ============================================================================
    # TABLE: navigation_paths
    # Purpose: Store learned navigation sequences for cognitive map
    # ============================================================================
    op.create_table(
        'navigation_paths',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('from_url_hash', sa.String(64), nullable=False),
        sa.Column('to_url_hash', sa.String(64), nullable=False),
        sa.Column('action_sequence', JSONB, nullable=False),  # Array of actions taken
        sa.Column('success_count', sa.Integer, nullable=False, server_default='0'),
        sa.Column('failure_count', sa.Integer, nullable=False, server_default='0'),
        sa.Column('avg_duration_ms', sa.Integer, nullable=True),
        sa.Column('confidence_score', sa.Float, nullable=False, server_default='0.0'),
        sa.Column('last_used', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('now()')),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('now()')),
        sa.UniqueConstraint('from_url_hash', 'to_url_hash', name='unique_navigation_path')
    )

    # ============================================================================
    # INDEXES
    # ============================================================================

    # browser_sessions indexes
    op.create_index('idx_sessions_status', 'browser_sessions', ['status'])
    op.create_index('idx_sessions_created', 'browser_sessions', ['created_at'])
    op.create_index('idx_sessions_active', 'browser_sessions', ['last_active'], postgresql_where=sa.text("status = 'active'"))

    # browser_actions indexes
    op.create_index('idx_actions_session', 'browser_actions', ['session_id'])
    op.create_index('idx_actions_type', 'browser_actions', ['action_type'])
    op.create_index('idx_actions_created', 'browser_actions', ['created_at'])
    op.create_index('idx_actions_success', 'browser_actions', ['success'])

    # cognitive_map_pages indexes
    op.create_index('idx_cognitive_url_hash', 'cognitive_map_pages', ['url_hash'], unique=True)
    op.create_index('idx_cognitive_domain', 'cognitive_map_pages', ['domain'])
    op.create_index('idx_cognitive_visited', 'cognitive_map_pages', ['last_visited'])
    op.create_index('idx_cognitive_importance', 'cognitive_map_pages', ['importance_score'])

    # navigation_paths indexes
    op.create_index('idx_nav_from', 'navigation_paths', ['from_url_hash'])
    op.create_index('idx_nav_to', 'navigation_paths', ['to_url_hash'])
    op.create_index('idx_nav_confidence', 'navigation_paths', ['confidence_score'])
    op.create_index('idx_nav_last_used', 'navigation_paths', ['last_used'])


def downgrade() -> None:
    """Drop all MABA tables."""
    op.drop_table('navigation_paths')
    op.drop_table('browser_actions')
    op.drop_table('cognitive_map_pages')
    op.drop_table('browser_sessions')
