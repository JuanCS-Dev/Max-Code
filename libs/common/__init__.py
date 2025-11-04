"""
Maximus AI - Common Utilities
Shared utilities and helpers for all Maximus services.
"""

from .health import HealthChecker
from .config import load_config, get_env

__all__ = ['HealthChecker', 'load_config', 'get_env']

__version__ = '1.0.0'
