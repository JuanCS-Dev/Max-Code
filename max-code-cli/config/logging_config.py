"""
Centralized Logging Configuration

Implements Python logging best practices for 2025:
- Structured logging with JSON support
- Environment-aware configuration
- Appropriate log levels (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- Protection of sensitive data
- Cloud-native: logs to stdout for container environments

Biblical Foundation:
"Tudo tem o seu tempo determinado, e há tempo para todo o propósito debaixo do céu"
(Eclesiastes 3:1)
Proper logging reveals the appointed time of each event.

References:
- PEP 282: A Logging System
- https://betterstack.com/community/guides/logging/python/python-logging-best-practices/
- https://signoz.io/guides/python-logging-best-practices/
"""

import logging
import sys
import json
from typing import Dict, Any, Optional
from datetime import datetime
from pathlib import Path

from config.settings import get_settings


# ============================================================================
# LOG LEVELS
# ============================================================================

class LogLevel:
    """Standard log levels"""
    DEBUG = logging.DEBUG        # 10 - Detailed information, typically for debugging
    INFO = logging.INFO          # 20 - General informational messages
    WARNING = logging.WARNING    # 30 - Warning messages for potentially harmful situations
    ERROR = logging.ERROR        # 40 - Error messages for serious problems
    CRITICAL = logging.CRITICAL  # 50 - Critical messages for very serious errors


# ============================================================================
# STRUCTURED LOGGING FORMATTER
# ============================================================================

class StructuredFormatter(logging.Formatter):
    """
    JSON formatter for structured logging.

    Outputs logs in JSON format for easy parsing by log aggregation tools
    (Elasticsearch, Kibana, CloudWatch, etc).

    Example output:
    {
        "timestamp": "2025-11-05T10:30:45.123Z",
        "level": "INFO",
        "logger": "agents.code_agent",
        "message": "Code generation completed",
        "task_id": "abc123",
        "duration_ms": 1500
    }
    """

    def format(self, record: logging.LogRecord) -> str:
        """Format log record as JSON"""

        # Base log entry
        log_entry: Dict[str, Any] = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }

        # Add exception info if present
        if record.exc_info:
            log_entry["exception"] = self.formatException(record.exc_info)

        # Add extra fields (from logger.info(..., extra={...}))
        for key, value in record.__dict__.items():
            if key not in [
                "name", "msg", "args", "created", "filename", "funcName",
                "levelname", "levelno", "lineno", "module", "msecs",
                "message", "pathname", "process", "processName", "relativeCreated",
                "thread", "threadName", "exc_info", "exc_text", "stack_info"
            ]:
                log_entry[key] = value

        # Sanitize sensitive data
        log_entry = self._sanitize(log_entry)

        return json.dumps(log_entry)

    def _sanitize(self, log_entry: Dict[str, Any]) -> Dict[str, Any]:
        """
        Sanitize sensitive data from log entries.

        Redacts:
        - API keys
        - Passwords
        - Tokens
        - Email addresses (partial redaction)
        """
        sensitive_keys = [
            "api_key", "apikey", "api-key",
            "password", "passwd", "pwd",
            "token", "access_token", "refresh_token",
            "secret", "authorization"
        ]

        for key in list(log_entry.keys()):
            # Check key names
            if any(sensitive in key.lower() for sensitive in sensitive_keys):
                log_entry[key] = "[REDACTED]"

            # Check string values that might contain sensitive data
            elif isinstance(log_entry[key], str):
                # Partial email redaction: u***@example.com
                if "@" in log_entry[key] and "." in log_entry[key]:
                    parts = log_entry[key].split("@")
                    if len(parts) == 2 and len(parts[0]) > 2:
                        log_entry[key] = f"{parts[0][0]}***@{parts[1]}"

        return log_entry


# ============================================================================
# HUMAN-READABLE FORMATTER
# ============================================================================

class HumanReadableFormatter(logging.Formatter):
    """
    Human-readable formatter for development.

    Outputs colored logs with emojis for better readability during development.

    Example output:
    2025-11-05 10:30:45 | INFO    | agents.code_agent | ✅ Code generation completed
    2025-11-05 10:30:46 | ERROR   | agents.test_agent | ❌ Test execution failed
    """

    # Level colors (using ANSI codes for terminal)
    COLORS = {
        'DEBUG': '\033[36m',      # Cyan
        'INFO': '\033[32m',       # Green
        'WARNING': '\033[33m',    # Yellow
        'ERROR': '\033[31m',      # Red
        'CRITICAL': '\033[35m',   # Magenta
    }
    RESET = '\033[0m'

    # Level emojis
    EMOJIS = {
        'DEBUG': '🔍',
        'INFO': 'ℹ️',
        'WARNING': '⚠️',
        'ERROR': '❌',
        'CRITICAL': '🚨',
    }

    def format(self, record: logging.LogRecord) -> str:
        """Format log record with colors and emojis"""

        # Get color and emoji
        color = self.COLORS.get(record.levelname, '')
        emoji = self.EMOJIS.get(record.levelname, '')

        # Format timestamp
        timestamp = datetime.fromtimestamp(record.created).strftime('%Y-%m-%d %H:%M:%S')

        # Format log entry
        log_entry = (
            f"{timestamp} | "
            f"{color}{record.levelname:8}{self.RESET} | "
            f"{record.name:30} | "
            f"{emoji} {record.getMessage()}"
        )

        # Add exception info if present
        if record.exc_info:
            log_entry += "\n" + self.formatException(record.exc_info)

        return log_entry


# ============================================================================
# LOGGER CONFIGURATION
# ============================================================================

def configure_logging(
    level: Optional[int] = None,
    format_style: str = "human",  # "human" or "json"
    log_file: Optional[Path] = None,
) -> None:
    """
    Configure logging for the entire application.

    Should be called once at application startup (e.g., in cli/main.py).

    Args:
        level: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
               If None, uses level from settings
        format_style: "human" for development, "json" for production
        log_file: Optional file path for logging to file

    Example:
        # Development
        configure_logging(level=logging.DEBUG, format_style="human")

        # Production
        configure_logging(level=logging.INFO, format_style="json")
    """
    settings = get_settings()

    # Determine log level
    if level is None:
        # Use level from settings (default: INFO)
        level_name = getattr(settings, 'log_level', 'INFO').upper()
        level = getattr(logging, level_name, logging.INFO)

    # Create root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(level)

    # Clear existing handlers
    root_logger.handlers.clear()

    # Choose formatter
    if format_style == "json":
        formatter = StructuredFormatter()
    else:
        formatter = HumanReadableFormatter()

    # Console handler (stdout)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)

    # File handler (optional)
    if log_file:
        log_file.parent.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)
        root_logger.addHandler(file_handler)

    # Silence noisy third-party loggers
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("aiohttp").setLevel(logging.WARNING)
    logging.getLogger("anthropic").setLevel(logging.WARNING)
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("httpcore").setLevel(logging.WARNING)

    # Log successful configuration
    root_logger.info(
        f"Logging configured: level={logging.getLevelName(level)}, "
        f"format={format_style}, file={log_file or 'none'}"
    )


def get_logger(name: str) -> logging.Logger:
    """
    Get logger for a module.

    Best practice: Use __name__ as the logger name.

    Example:
        # In agents/code_agent.py
        from config.logging_config import get_logger

        logger = get_logger(__name__)  # Creates logger named "agents.code_agent"

        logger.info("Starting code generation")
        logger.error("Code generation failed", extra={"task_id": "abc123"})

    Args:
        name: Logger name (use __name__)

    Returns:
        Logger instance
    """
    return logging.getLogger(name)


# ============================================================================
# CONVENIENCE FUNCTIONS
# ============================================================================

def log_agent_start(logger: logging.Logger, agent_name: str, task_id: str) -> None:
    """Log agent start with consistent format"""
    logger.info(
        f"Agent '{agent_name}' starting",
        extra={"event": "agent_start", "agent": agent_name, "task_id": task_id}
    )


def log_agent_complete(
    logger: logging.Logger,
    agent_name: str,
    task_id: str,
    duration_ms: float,
    success: bool
) -> None:
    """Log agent completion with metrics"""
    level = logging.INFO if success else logging.ERROR
    logger.log(
        level,
        f"Agent '{agent_name}' {'completed' if success else 'failed'}",
        extra={
            "event": "agent_complete",
            "agent": agent_name,
            "task_id": task_id,
            "duration_ms": duration_ms,
            "success": success
        }
    )


def log_maximus_call(
    logger: logging.Logger,
    service: str,
    endpoint: str,
    success: bool,
    duration_ms: Optional[float] = None
) -> None:
    """Log MAXIMUS service call"""
    level = logging.DEBUG if success else logging.WARNING
    logger.log(
        level,
        f"MAXIMUS {service} call: {endpoint} ({'success' if success else 'failed'})",
        extra={
            "event": "maximus_call",
            "service": service,
            "endpoint": endpoint,
            "success": success,
            "duration_ms": duration_ms
        }
    )


def log_validation_error(logger: logging.Logger, error: str, details: Dict[str, Any]) -> None:
    """Log validation error with details"""
    logger.error(
        f"Validation error: {error}",
        extra={"event": "validation_error", "error": error, "details": details}
    )


# ============================================================================
# MIGRATION HELPERS
# ============================================================================

# Mapping of common print patterns to log levels
PRINT_TO_LOG_PATTERNS = {
    # Emojis that indicate log level
    "✅": logging.INFO,     # Success
    "❌": logging.ERROR,    # Failure
    "⚠️": logging.WARNING,  # Warning
    "🔍": logging.DEBUG,    # Debug/inspection
    "💡": logging.INFO,     # Insight
    "🚀": logging.INFO,     # Start
    "✨": logging.INFO,     # Complete
    "🔒": logging.INFO,     # Security
    "📊": logging.INFO,     # Metrics
    "🧪": logging.DEBUG,    # Test
    "⏱️": logging.DEBUG,    # Timing
}


def migrate_print_to_log(message: str) -> int:
    """
    Helper to determine appropriate log level from print message.

    Used during migration from print() to logging.

    Args:
        message: Original print message

    Returns:
        Appropriate log level (logging.DEBUG, INFO, WARNING, ERROR)

    Example:
        message = "   ✅ Parameters validated"
        level = migrate_print_to_log(message)  # Returns logging.INFO
        logger.log(level, message.strip())
    """
    for emoji, level in PRINT_TO_LOG_PATTERNS.items():
        if emoji in message:
            return level

    # Default: INFO for general messages
    return logging.INFO
