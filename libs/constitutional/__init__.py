"""
Maximus AI - Constitutional Framework
Standalone implementation of constitutional compliance, tracing, and metrics.

Based on CONSTITUIÇÃO VÉRTICE v3.0 - Framework DETER-AGENT
"""

from .tracing import create_tracer, ConstitutionalTracer
from .metrics import MetricsExporter, ConstitutionalMetrics
from .logging import setup_constitutional_logging, get_logger

__all__ = [
    'create_tracer',
    'ConstitutionalTracer',
    'MetricsExporter',
    'ConstitutionalMetrics',
    'setup_constitutional_logging',
    'get_logger',
]

__version__ = '3.0.0'
