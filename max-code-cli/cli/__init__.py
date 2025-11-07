"""
Max-Code CLI Command System

Click-based CLI commands with rich UI integration.
"""

# Load .env before any imports to ensure environment variables are available
from pathlib import Path
from dotenv import load_dotenv

# Find .env in project root
project_root = Path(__file__).parent.parent
env_file = project_root / ".env"
if env_file.exists():
    load_dotenv(env_file)

from cli.main import cli

__all__ = ['cli']
