"""
Fast Import Module - Ultra-optimized lazy imports

This module provides the absolute fastest way to get UI components
by deferring ALL heavy imports until actually needed.

Usage:
    from ui.fast_import import fast_banner, fast_formatter

    # Only imports when you call it
    banner = fast_banner()
    banner.show("3.0")
"""

from typing import Any, Callable


def _lazy_import(module_path: str, class_name: str) -> Callable:
    """Create a lazy import function."""
    def _importer(*args, **kwargs) -> Any:
        # Import only when called
        parts = module_path.split('.')
        module = __import__(module_path, fromlist=[class_name])
        cls = getattr(module, class_name)
        return cls(*args, **kwargs)
    return _importer


# Fast import functions (no imports until called)
fast_banner = _lazy_import('ui.banner', 'MaxCodeBanner')
fast_formatter = _lazy_import('ui.formatter', 'MaxCodeFormatter')
fast_progress = _lazy_import('ui.progress', 'MaxCodeProgress')
fast_agent_display = _lazy_import('ui.agents', 'AgentDisplay')
fast_selection_menu = _lazy_import('ui.menus', 'SelectionMenu')
fast_config_menu = _lazy_import('ui.menus', 'ConfigMenu')
fast_command_palette = _lazy_import('ui.menus', 'CommandPalette')
fast_thought_tree = _lazy_import('ui.tree_of_thoughts', 'ThoughtTree')
fast_reasoning_steps = _lazy_import('ui.tree_of_thoughts', 'ReasoningSteps')
fast_constitutional_analysis = _lazy_import('ui.tree_of_thoughts', 'ConstitutionalAnalysis')
fast_streaming_display = _lazy_import('ui.streaming', 'StreamingDisplay')
fast_log_viewer = _lazy_import('ui.streaming', 'LiveLogViewer')
fast_progress_stream = _lazy_import('ui.streaming', 'ProgressStream')


__all__ = [
    'fast_banner',
    'fast_formatter',
    'fast_progress',
    'fast_agent_display',
    'fast_selection_menu',
    'fast_config_menu',
    'fast_command_palette',
    'fast_thought_tree',
    'fast_reasoning_steps',
    'fast_constitutional_analysis',
    'fast_streaming_display',
    'fast_log_viewer',
    'fast_progress_stream',
]
