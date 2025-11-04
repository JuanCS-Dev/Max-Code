"""
Maximus AI - Service Registry Client
Standalone service discovery and registration (optional component).

This module provides graceful degradation:
- If registry is available: full service discovery
- If registry is unavailable: falls back to environment variables
"""

from .client import RegistryClient, ServiceInfo

__all__ = ['RegistryClient', 'ServiceInfo']

__version__ = '1.0.0'
