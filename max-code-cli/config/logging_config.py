"""
Structured Logging Configuration
Boris Cherny Standard: Replace print() with proper logging.
"""

import logging
import logging.config
from pathlib import Path
from typing import Optional


LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "detailed": {
            "format": "[{asctime}] [{levelname:8}] [{name}:{lineno}] - {message}",
            "style": "{",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
        "simple": {
            "format": "[{levelname:8}] {name} - {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "INFO",
            "formatter": "simple",
            "stream": "ext://sys.stdout",
        },
    },
    "loggers": {
        "": {"level": "INFO", "handlers": ["console"]},
        "sdk": {"level": "DEBUG", "handlers": ["console"], "propagate": False},
        "cli": {"level": "INFO", "handlers": ["console"], "propagate": False},
    },
}


def setup_logging(level: Optional[str] = None) -> None:
    """Set up structured logging."""
    config = LOGGING_CONFIG.copy()
    if level:
        level_value = getattr(logging, level.upper(), logging.INFO)
        config["handlers"]["console"]["level"] = level_value
    logging.config.dictConfig(config)


def get_logger(name: str) -> logging.Logger:
    """Get a logger with the specified name."""
    return logging.getLogger(name)
