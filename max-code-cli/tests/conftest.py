"""Pytest configuration for max-code-cli tests."""

import sys
import os

# Add max-code-cli root to path so tests can import from integration/
cli_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if cli_root not in sys.path:
    sys.path.insert(0, cli_root)
