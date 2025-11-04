"""Main entry point - imports app from api.py."""
from api import app  # api.py in the same directory

# Constitutional v3.0 imports
from libs.constitutional.metrics import MetricsExporter, auto_update_sabbath_status
from libs.constitutional.tracing import create_constitutional_tracer
from libs.constitutional.logging import configure_constitutional_logging
from libs.common.health import ConstitutionalHealthCheck


__all__ = ["app"]
