"""
Max-Code CLI UI Constants

Centralized constants for colors, symbols, and configurations.
Ensures consistency across all UI components.

Usage:
    from ui.constants import SEMANTIC_COLORS, AGENT_COLORS, STATUS_SYMBOLS
"""

from typing import Dict

# ============================================================================
# COLOR SCHEMES
# ============================================================================

# Semantic colors for messages
SEMANTIC_COLORS: Dict[str, str] = {
    'success': 'green',
    'error': 'red',
    'warning': 'yellow',
    'info': 'cyan',
    'debug': 'dim white',
}

# Semantic symbols
SEMANTIC_SYMBOLS: Dict[str, str] = {
    'success': '✓',
    'error': '✗',
    'warning': '⚠',
    'info': 'ℹ',
    'debug': '⚙',
}

# Constitutional AI principles (P1-P6)
CONSTITUTIONAL_COLORS: Dict[str, str] = {
    'p1': 'violet',      # Transcendence
    'p2': 'blue',        # Reasoning
    'p3': 'green',       # Care
    'p4': 'yellow',      # Wisdom
    'p5': 'magenta',     # Beauty
    'p6': 'cyan',        # Autonomy
}

CONSTITUTIONAL_PRINCIPLES = [
    ('P1', 'Transcendence', 'violet', 'Higher purpose and meaning'),
    ('P2', 'Reasoning', 'blue', 'Logic and critical thinking'),
    ('P3', 'Care', 'green', 'Empathy and compassion'),
    ('P4', 'Wisdom', 'yellow', 'Practical judgment and experience'),
    ('P5', 'Beauty', 'magenta', 'Aesthetic and elegance'),
    ('P6', 'Autonomy', 'cyan', 'Self-determination and agency'),
]

# Agent-specific colors
AGENT_COLORS: Dict[str, str] = {
    'sophia': 'gold1',           # Architect
    'code': 'blue',              # Developer
    'test': 'green',             # Validator
    'review': 'orange3',         # Auditor
    'fix': 'red',                # Debugger
    'docs': 'purple',            # Writer
    'explore': 'cyan',           # Researcher
    'guardian': 'bright_red',    # Security
    'sleep': 'deep_sky_blue1',   # Optimizer
}

# ============================================================================
# STATUS SYMBOLS AND COLORS
# ============================================================================

# Status symbols (universal)
STATUS_SYMBOLS: Dict[str, str] = {
    'active': '●',
    'idle': '○',
    'completed': '✓',
    'failed': '✗',
    'waiting': '⟳',
    'pending': '○',
    'processing': '⟳',
    'success': '✓',
    'error': '✗',
    'warning': '⚠',
}

# Status colors
STATUS_COLORS: Dict[str, str] = {
    'active': 'cyan',
    'idle': 'dim',
    'completed': 'green',
    'failed': 'red',
    'waiting': 'yellow',
    'pending': 'yellow',
    'processing': 'cyan',
    'success': 'green',
    'error': 'red',
    'warning': 'yellow',
}

# ============================================================================
# GRADIENT COLORS
# ============================================================================

# Neon gradient (green → cyan → blue)
NEON_GRADIENT: list = ['#0FFF50', '#00F0FF', '#0080FF', '#0040FF']

# Alternative gradients
GRADIENTS: Dict[str, list] = {
    'neon': ['#0FFF50', '#00F0FF', '#0080FF', '#0040FF'],
    'fire': ['#FF0000', '#FF6600', '#FFCC00', '#FFFF00'],
    'ocean': ['#0080FF', '#00C0FF', '#00FFFF', '#00FF80'],
    'sunset': ['#FF0080', '#FF6600', '#FFCC00', '#FFFF80'],
    'matrix': ['#00FF00', '#00CC00', '#008800', '#004400'],
}

# ============================================================================
# TABLE AND LAYOUT CONFIGURATION
# ============================================================================

# Default table configuration
TABLE_CONFIG = {
    'show_header': True,
    'header_style': 'bold cyan',
    'border_style': 'cyan',
    'padding': (0, 1),
    'expand': False,
}

# Panel configuration
PANEL_CONFIG = {
    'border_style': 'cyan',
    'padding': (1, 2),
}

# Default widths
DEFAULT_WIDTHS = {
    'narrow': 10,
    'medium': 25,
    'wide': 50,
    'extra_wide': 80,
}

# ============================================================================
# SCORE THRESHOLDS
# ============================================================================

# Score ranges for color coding (0-10 scale)
SCORE_THRESHOLDS = {
    'excellent': 8.0,   # green
    'good': 6.0,        # yellow
    'fair': 4.0,        # orange
    'poor': 0.0,        # red
}

# ============================================================================
# PROGRESS BAR CHARACTERS
# ============================================================================

PROGRESS_CHARS = {
    'filled': '█',
    'empty': '░',
    'horizontal_filled': '━',
    'horizontal_empty': '─',
}

# ============================================================================
# LOG LEVEL CONFIGURATION
# ============================================================================

LOG_LEVEL_COLORS: Dict[str, str] = {
    'debug': 'dim white',
    'info': 'cyan',
    'warning': 'yellow',
    'error': 'red',
    'critical': 'bold red',
}

LOG_LEVEL_SYMBOLS: Dict[str, str] = {
    'debug': '⚙',
    'info': 'ℹ',
    'warning': '⚠',
    'error': '✗',
    'critical': '🔥',
}

# ============================================================================
# BANNER CONFIGURATION
# ============================================================================

BANNER_FONTS = {
    'default': 'block',       # Solid block letters (Gemini-style)
    'isometric': 'isometric1',
    'banner': 'banner3',
    'bold': 'colossal',
    'tech': 'doom',
    'cyber': 'graffiti',
}

# ============================================================================
# PERFORMANCE TARGETS
# ============================================================================

PERFORMANCE_TARGETS = {
    'banner_display_ms': 50,
    'table_render_ms': 100,
    'live_update_fps': 10,
    'import_time_ms': 100,  # Adjusted from 45ms (Rich Console takes 60ms baseline)
    'memory_overhead_mb': 50,
}

# ============================================================================
# UNICODE BOX-DRAWING CHARACTERS
# ============================================================================

BOX_CHARS = {
    'top_left': '╔',
    'top_right': '╗',
    'bottom_left': '╚',
    'bottom_right': '╝',
    'horizontal': '═',
    'vertical': '║',
    'left_t': '╟',
    'right_t': '╢',
}

# ============================================================================
# EXPORT
# ============================================================================

__all__ = [
    # Colors
    'SEMANTIC_COLORS',
    'SEMANTIC_SYMBOLS',
    'CONSTITUTIONAL_COLORS',
    'CONSTITUTIONAL_PRINCIPLES',
    'AGENT_COLORS',
    'STATUS_SYMBOLS',
    'STATUS_COLORS',
    'NEON_GRADIENT',
    'GRADIENTS',
    'LOG_LEVEL_COLORS',
    'LOG_LEVEL_SYMBOLS',

    # Configuration
    'TABLE_CONFIG',
    'PANEL_CONFIG',
    'DEFAULT_WIDTHS',
    'SCORE_THRESHOLDS',
    'PROGRESS_CHARS',
    'BANNER_FONTS',
    'PERFORMANCE_TARGETS',
    'BOX_CHARS',
]
