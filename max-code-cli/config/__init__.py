"""
Max-Code CLI Configuration System

Provides type-safe configuration with environment variable support,
multiple profiles (dev/prod/local), and validation.
"""

from config.settings import Settings, get_settings
from config.profiles import Profile, ProfileManager

__all__ = [
    'Settings',
    'get_settings',
    'Profile',
    'ProfileManager',
]
