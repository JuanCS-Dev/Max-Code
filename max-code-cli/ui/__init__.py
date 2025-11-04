"""
Max-Code CLI UI/UX Module

A visual masterpiece for terminal interfaces.
Combines speed with stunning aesthetics.

Components:
- banner: Magnificent ASCII art banners with gradient
  - PyFiglet style (BLOCK font, Gemini-inspired)
  - vCLI-Go style (Unicode box-drawing, production-focused)
- formatter: Beautiful output formatting
- progress: Progress indicators and spinners
- agent_display: Multi-agent system visualization
- tree_of_thoughts: Tree of Thoughts reasoning visualization
- streaming: Real-time streaming output
- validation: Code quality and security validation
- exceptions: User-friendly error display
- utils: UI utilities and helpers
"""

__version__ = "1.0.0"
__all__ = [
    # Core components
    "show_banner",
    "MaxCodeFormatter",
    "ProgressTracker",
    "AgentActivityDisplay",
    "TreeOfThoughts",
    "StreamingDisplay",
    "ValidationDisplay",
    "ExceptionDisplay",

    # Utility functions
    "get_console",
    "print_header",
    "print_success",
    "print_error",
    "print_warning",
    "print_info",
]

# Lazy imports for performance
def get_banner():
    """Get banner instance (lazy import)."""
    from .banner import MaxCodeBanner
    return MaxCodeBanner()

def get_formatter():
    """Get formatter instance (lazy import)."""
    from .formatter import MaxCodeFormatter
    return MaxCodeFormatter()

def get_progress():
    """Get progress instance (lazy import)."""
    from .progress import MaxCodeProgress
    return MaxCodeProgress()

def get_vcli_banner():
    """Get vCLI-style banner function (lazy import)."""
    from .banner_vcli_style import show_banner
    return show_banner

def get_agent_display():
    """Get agent display instance (lazy import)."""
    from .agents import AgentDisplay
    return AgentDisplay()

def get_selection_menu():
    """Get selection menu instance (lazy import)."""
    from .menus import SelectionMenu
    return SelectionMenu()

def get_config_menu():
    """Get config menu instance (lazy import)."""
    from .menus import ConfigMenu
    return ConfigMenu()

def get_command_palette():
    """Get command palette instance (lazy import)."""
    from .menus import CommandPalette
    return CommandPalette()

def get_thought_tree():
    """Get thought tree visualizer (lazy import)."""
    from .tree_of_thoughts import ThoughtTree
    return ThoughtTree()

def get_reasoning_steps():
    """Get reasoning steps display (lazy import)."""
    from .tree_of_thoughts import ReasoningSteps
    return ReasoningSteps()

def get_constitutional_analysis():
    """Get constitutional analysis display (lazy import)."""
    from .tree_of_thoughts import ConstitutionalAnalysis
    return ConstitutionalAnalysis()

def get_streaming_display():
    """Get streaming display instance (lazy import)."""
    from .streaming import StreamingDisplay
    return StreamingDisplay()

def get_log_viewer():
    """Get live log viewer instance (lazy import)."""
    from .streaming import LiveLogViewer
    return LiveLogViewer()

def get_progress_stream():
    """Get progress stream instance (lazy import)."""
    from .streaming import ProgressStream
    return ProgressStream()
