"""Configuration utilities for Maximus services."""

import os
from typing import Any, Optional
from pathlib import Path


def get_env(key: str, default: Optional[str] = None, required: bool = False) -> str:
    """
    Get environment variable with optional default and required check.

    Args:
        key: Environment variable name
        default: Default value if not set
        required: If True, raise error if not set and no default

    Returns:
        Environment variable value

    Raises:
        ValueError: If required=True and variable not set
    """
    value = os.getenv(key, default)

    if required and value is None:
        raise ValueError(f"Required environment variable '{key}' is not set")

    return value


def load_config(config_file: Optional[str] = None) -> dict[str, Any]:
    """
    Load configuration from file.

    Args:
        config_file: Path to config file (supports .env, .json, .yaml)

    Returns:
        Configuration dictionary
    """
    config = {}

    if config_file is None:
        # Try default locations
        for default_path in [".env", "config.yaml", "config.json"]:
            if Path(default_path).exists():
                config_file = default_path
                break

    if config_file and Path(config_file).exists():
        ext = Path(config_file).suffix.lower()

        if ext == ".env":
            # Load .env file
            with open(config_file) as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#") and "=" in line:
                        key, value = line.split("=", 1)
                        config[key.strip()] = value.strip()

        elif ext in [".yaml", ".yml"]:
            try:
                import yaml
                with open(config_file) as f:
                    config = yaml.safe_load(f) or {}
            except ImportError:
                raise ImportError("PyYAML not installed. Install with: pip install pyyaml")

        elif ext == ".json":
            import json
            with open(config_file) as f:
                config = json.load(f)

    return config
