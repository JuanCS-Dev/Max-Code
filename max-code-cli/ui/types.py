"""
Max-Code CLI UI Type Definitions

Type hints and protocols for UI components.
Ensures type safety across the UI system.

Usage:
    from ui.types import ConsoleProtocol, RenderableType
"""

from typing import Protocol, Union, Any, TypeVar, TypedDict
from typing_extensions import NotRequired


# ============================================================================
# CONSOLE PROTOCOL
# ============================================================================

class ConsoleProtocol(Protocol):
    """Protocol for console-like objects."""

    def print(self, *args: Any, **kwargs: Any) -> None:
        """Print to console."""
        ...


# ============================================================================
# RENDERABLE TYPES
# ============================================================================

# Type for Rich renderable objects
RenderableType = Union[str, Any]  # Rich accepts many types

# Generic type variable
T = TypeVar('T')

# ============================================================================
# CONFIGURATION TYPES
# ============================================================================

class BannerConfig(TypedDict, total=False):
    """Banner configuration options."""
    version: str
    build_date: NotRequired[str]
    context: NotRequired[dict[str, Any]]
    style: NotRequired[str]
    show_principles: NotRequired[bool]


class TableConfig(TypedDict, total=False):
    """Table configuration options."""
    title: NotRequired[str]
    show_header: bool
    header_style: str
    border_style: str
    padding: tuple[int, int]
    expand: bool


class PanelConfig(TypedDict, total=False):
    """Panel configuration options."""
    title: NotRequired[str]
    border_style: str
    padding: tuple[int, int]


class ProgressConfig(TypedDict, total=False):
    """Progress bar configuration."""
    total: int
    description: str
    color: NotRequired[str]
    show_time: NotRequired[bool]


# ============================================================================
# DATA STRUCTURES
# ============================================================================

class AgentData(TypedDict):
    """Agent data structure."""
    name: str
    role: str
    status: str
    task: NotRequired[str]
    progress: NotRequired[float]
    time_elapsed: NotRequired[float]
    cpu_usage: NotRequired[float]
    memory_usage: NotRequired[float]


class LogEntryData(TypedDict):
    """Log entry data structure."""
    timestamp: str
    level: str
    message: str
    source: NotRequired[str]
    metadata: NotRequired[dict[str, Any]]


class MenuItemData(TypedDict):
    """Menu item data structure."""
    label: str
    value: Any
    description: NotRequired[str]
    color: NotRequired[str]


class ThoughtNodeData(TypedDict):
    """Thought node data structure."""
    id: str
    content: str
    score: float
    status: str
    parent_id: NotRequired[str]
    depth: NotRequired[int]
    reasoning: NotRequired[str]
    metadata: NotRequired[dict[str, Any]]


class StreamUpdateData(TypedDict):
    """Stream update data structure."""
    stream_id: str
    description: str
    current: int
    total: int
    status: NotRequired[str]
    metadata: NotRequired[dict[str, Any]]


# ============================================================================
# STYLE TYPES
# ============================================================================

ColorType = str  # Rich color string
StyleType = str  # Rich style string

# Score range (0-10)
ScoreType = float

# Percentage (0-100)
PercentageType = float

# ============================================================================
# EXPORT
# ============================================================================

__all__ = [
    # Protocols
    'ConsoleProtocol',

    # Generic types
    'RenderableType',
    'T',

    # Config types
    'BannerConfig',
    'TableConfig',
    'PanelConfig',
    'ProgressConfig',

    # Data types
    'AgentData',
    'LogEntryData',
    'MenuItemData',
    'ThoughtNodeData',
    'StreamUpdateData',

    # Style types
    'ColorType',
    'StyleType',
    'ScoreType',
    'PercentageType',
]
