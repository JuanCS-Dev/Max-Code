"""
Smart Error Messages - Contextual Error Handling

Inspired by Python 3.14 "did you mean" suggestions.
Context-aware error messages with actionable suggestions.

Biblical Foundation:
"O homem prudente prevê o mal e esconde-se" (Provérbios 22:3)
Anticipating and guiding through errors.

Research findings:
- Python 3.14: "did you mean" keyword suggestions
- Argparse deprecation warnings
- Levenshtein distance for fuzzy matching
- Contextual suggestions based on error type

Architecture:
1. ErrorContext: captures error details + context
2. ErrorSuggester: generates "did you mean" suggestions
3. SmartErrorDisplay: Rich formatting with actions
4. Registry of common errors with suggestions
"""

import logging
import difflib
import traceback
from typing import Dict, List, Optional, Callable, Any
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path

from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.table import Table
from rich.syntax import Syntax

from ui.constants import NERD_ICONS, NEON_PALETTE

logger = logging.getLogger(__name__)


class ErrorSeverity(str, Enum):
    """Error severity levels."""
    DEBUG = "debug"          # Debug info
    INFO = "info"            # Informational
    WARNING = "warning"      # Warning (non-critical)
    ERROR = "error"          # Error (critical)
    CRITICAL = "critical"    # Critical (fatal)


class ErrorCategory(str, Enum):
    """Error categories for context."""
    COMMAND = "command"          # Command not found
    AGENT = "agent"              # Agent error
    FILE = "file"                # File operation error
    GIT = "git"                  # Git error
    VALIDATION = "validation"    # Validation error
    SYSTEM = "system"            # System error
    NETWORK = "network"          # Network error
    PERMISSION = "permission"    # Permission error


@dataclass
class ErrorSuggestion:
    """
    Error suggestion.

    Attributes:
        text: Suggestion text
        action: Optional action to execute
        icon: Icon for suggestion
    """
    text: str
    action: Optional[Callable] = None
    icon: str = "💡"


@dataclass
class ErrorContext:
    """
    Error context with suggestions.

    Attributes:
        message: Error message
        category: Error category
        severity: Error severity
        exception: Optional exception object
        suggestions: List of suggestions
        code_snippet: Optional code snippet
        traceback_str: Optional traceback string
        metadata: Additional metadata
    """
    message: str
    category: ErrorCategory
    severity: ErrorSeverity = ErrorSeverity.ERROR
    exception: Optional[Exception] = None
    suggestions: List[ErrorSuggestion] = field(default_factory=list)
    code_snippet: Optional[str] = None
    traceback_str: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def add_suggestion(self, text: str, action: Optional[Callable] = None, icon: str = "💡"):
        """Add suggestion to error context."""
        self.suggestions.append(ErrorSuggestion(text, action, icon))


class ErrorSuggester:
    """
    Generates contextual error suggestions.

    Uses fuzzy matching (difflib) to suggest corrections.

    Example:
        suggester = ErrorSuggester(valid_commands=["agents", "help", "status"])
        suggestions = suggester.suggest("agen")  # ["agents"]
    """

    def __init__(
        self,
        valid_commands: Optional[List[str]] = None,
        valid_agents: Optional[List[str]] = None,
        valid_files: Optional[List[str]] = None,
        similarity_threshold: float = 0.6
    ):
        """
        Initialize error suggester.

        Args:
            valid_commands: List of valid command names
            valid_agents: List of valid agent names
            valid_files: List of valid file paths
            similarity_threshold: Minimum similarity ratio (0-1)
        """
        self.valid_commands = valid_commands or []
        self.valid_agents = valid_agents or []
        self.valid_files = valid_files or []
        self.similarity_threshold = similarity_threshold

        logger.debug("ErrorSuggester initialized")

    def suggest(
        self,
        input_text: str,
        candidates: Optional[List[str]] = None,
        max_suggestions: int = 3
    ) -> List[str]:
        """
        Generate "did you mean" suggestions.

        Args:
            input_text: User input
            candidates: Optional list of candidates (uses valid_commands if None)
            max_suggestions: Maximum suggestions to return

        Returns:
            List of suggested strings
        """
        if candidates is None:
            candidates = self.valid_commands

        if not candidates:
            return []

        # Use difflib.get_close_matches (Levenshtein-like)
        matches = difflib.get_close_matches(
            input_text,
            candidates,
            n=max_suggestions,
            cutoff=self.similarity_threshold
        )

        return matches

    def suggest_command(self, command: str, max_suggestions: int = 3) -> List[str]:
        """Suggest command names."""
        return self.suggest(command, self.valid_commands, max_suggestions)

    def suggest_agent(self, agent: str, max_suggestions: int = 3) -> List[str]:
        """Suggest agent names."""
        return self.suggest(agent, self.valid_agents, max_suggestions)

    def suggest_file(self, file_path: str, max_suggestions: int = 3) -> List[str]:
        """Suggest file paths."""
        return self.suggest(file_path, self.valid_files, max_suggestions)


class SmartErrorDisplay:
    """
    Display smart error messages with Rich formatting.

    Example:
        display = SmartErrorDisplay()

        ctx = ErrorContext(
            message="Command 'agen' not found",
            category=ErrorCategory.COMMAND,
            severity=ErrorSeverity.ERROR
        )
        ctx.add_suggestion("Did you mean 'agents'?", icon="")

        display.show(ctx)
    """

    def __init__(self, console: Optional[Console] = None):
        """
        Initialize smart error display.

        Args:
            console: Rich Console instance
        """
        self.console = console or Console()

        # Severity colors
        self.severity_colors = {
            ErrorSeverity.DEBUG: "dim",
            ErrorSeverity.INFO: NEON_PALETTE['info'],
            ErrorSeverity.WARNING: NEON_PALETTE['warning'],
            ErrorSeverity.ERROR: NEON_PALETTE['error'],
            ErrorSeverity.CRITICAL: "bold red"
        }

        # Severity icons
        self.severity_icons = {
            ErrorSeverity.DEBUG: NERD_ICONS.get('debug', '⚙'),
            ErrorSeverity.INFO: NERD_ICONS.get('info', ''),
            ErrorSeverity.WARNING: NERD_ICONS.get('warning', ''),
            ErrorSeverity.ERROR: NERD_ICONS.get('error', ''),
            ErrorSeverity.CRITICAL: NERD_ICONS.get('fire', '')
        }

        logger.info("SmartErrorDisplay initialized")

    def show(self, ctx: ErrorContext, show_traceback: bool = False):
        """
        Display error with context.

        Args:
            ctx: ErrorContext with error details
            show_traceback: Whether to show full traceback
        """
        # Get color and icon
        color = self.severity_colors[ctx.severity]
        icon = self.severity_icons[ctx.severity]

        # Build content
        content = Text()

        # Error message
        content.append(f"{icon} ", style=f"bold {color}")
        content.append(f"{ctx.message}\n", style=f"bold {color}")

        # Category
        if ctx.category:
            content.append(f"Category: ", style="dim")
            content.append(f"{ctx.category.value}\n", style="cyan")

        # Exception type
        if ctx.exception:
            content.append(f"Exception: ", style="dim")
            content.append(f"{type(ctx.exception).__name__}\n", style="yellow")

        # Code snippet
        if ctx.code_snippet:
            content.append("\nCode:\n", style="bold")
            syntax = Syntax(
                ctx.code_snippet,
                "python",
                theme="monokai",
                line_numbers=True
            )
            self.console.print(syntax)

        # Suggestions
        if ctx.suggestions:
            content.append("\nSuggestions:\n", style="bold green")
            for i, suggestion in enumerate(ctx.suggestions, 1):
                content.append(f"  {suggestion.icon} ", style="yellow")
                content.append(f"{suggestion.text}\n", style="white")

        # Metadata
        if ctx.metadata:
            content.append("\nAdditional Info:\n", style="bold dim")
            for key, value in ctx.metadata.items():
                content.append(f"  {key}: ", style="dim")
                content.append(f"{value}\n", style="white")

        # Display panel
        panel = Panel(
            content,
            title=f"[bold]{ctx.severity.value.upper()}[/bold]",
            border_style=color,
            padding=(1, 2)
        )

        self.console.print(panel)

        # Show traceback if requested
        if show_traceback and ctx.traceback_str:
            self.console.print("\n[bold]Traceback:[/bold]", style="dim")
            self.console.print(ctx.traceback_str, style="dim")


class SmartErrorHandler:
    """
    Smart error handler with context-aware suggestions.

    Integrates ErrorSuggester + SmartErrorDisplay.

    Example:
        handler = SmartErrorHandler(
            valid_commands=["agents", "help", "status"]
        )

        try:
            execute_command("agen")
        except CommandNotFound as e:
            handler.handle_command_error(e, "agen")
    """

    def __init__(
        self,
        console: Optional[Console] = None,
        valid_commands: Optional[List[str]] = None,
        valid_agents: Optional[List[str]] = None,
        valid_files: Optional[List[str]] = None
    ):
        """
        Initialize smart error handler.

        Args:
            console: Rich Console instance
            valid_commands: List of valid commands
            valid_agents: List of valid agents
            valid_files: List of valid files
        """
        self.suggester = ErrorSuggester(
            valid_commands=valid_commands,
            valid_agents=valid_agents,
            valid_files=valid_files
        )
        self.display = SmartErrorDisplay(console=console)

        logger.info("SmartErrorHandler initialized")

    def handle_command_error(
        self,
        exception: Exception,
        command: str,
        available_commands: Optional[List[str]] = None
    ):
        """
        Handle command not found error.

        Args:
            exception: Exception object
            command: Command that was not found
            available_commands: Optional list of available commands
        """
        ctx = ErrorContext(
            message=f"Command '{command}' not found",
            category=ErrorCategory.COMMAND,
            severity=ErrorSeverity.ERROR,
            exception=exception
        )

        # Generate suggestions
        candidates = available_commands or self.suggester.valid_commands
        suggestions = self.suggester.suggest(command, candidates)

        if suggestions:
            for suggestion in suggestions:
                ctx.add_suggestion(
                    f"Did you mean '{suggestion}'?",
                    icon=NERD_ICONS.get('light', '💡')
                )
        else:
            ctx.add_suggestion(
                "Run 'help' to see available commands",
                icon=NERD_ICONS.get('info', '')
            )

        self.display.show(ctx)

    def handle_agent_error(
        self,
        exception: Exception,
        agent_name: str
    ):
        """Handle agent not found error."""
        ctx = ErrorContext(
            message=f"Agent '{agent_name}' not found",
            category=ErrorCategory.AGENT,
            severity=ErrorSeverity.ERROR,
            exception=exception
        )

        # Suggest agents
        suggestions = self.suggester.suggest_agent(agent_name)

        if suggestions:
            for suggestion in suggestions:
                ctx.add_suggestion(
                    f"Did you mean '{suggestion}'?",
                    icon=NERD_ICONS.get('agent_sophia', '󰉋')
                )
        else:
            ctx.add_suggestion(
                "Valid agents: sophia, code, test, review, fix, docs, explore",
                icon=NERD_ICONS.get('info', '')
            )

        self.display.show(ctx)

    def handle_file_error(
        self,
        exception: Exception,
        file_path: str
    ):
        """Handle file not found error."""
        ctx = ErrorContext(
            message=f"File not found: {file_path}",
            category=ErrorCategory.FILE,
            severity=ErrorSeverity.ERROR,
            exception=exception,
            metadata={
                "path": file_path,
                "exists": Path(file_path).exists()
            }
        )

        # Suggest files
        suggestions = self.suggester.suggest_file(file_path)

        if suggestions:
            for suggestion in suggestions:
                ctx.add_suggestion(
                    f"Did you mean '{suggestion}'?",
                    icon=NERD_ICONS.get('file', '')
                )
        else:
            ctx.add_suggestion(
                "Check the file path and try again",
                icon=NERD_ICONS.get('warning', '')
            )

        self.display.show(ctx)

    def handle_validation_error(
        self,
        exception: Exception,
        field: str,
        value: Any,
        expected: str
    ):
        """Handle validation error."""
        ctx = ErrorContext(
            message=f"Validation failed for '{field}'",
            category=ErrorCategory.VALIDATION,
            severity=ErrorSeverity.ERROR,
            exception=exception,
            metadata={
                "field": field,
                "value": value,
                "expected": expected
            }
        )

        ctx.add_suggestion(
            f"Expected {expected}, got {type(value).__name__}",
            icon=NERD_ICONS.get('warning', '')
        )

        self.display.show(ctx)

    def handle_generic_error(
        self,
        exception: Exception,
        category: ErrorCategory = ErrorCategory.SYSTEM,
        severity: ErrorSeverity = ErrorSeverity.ERROR,
        suggestions: Optional[List[str]] = None
    ):
        """Handle generic error."""
        ctx = ErrorContext(
            message=str(exception),
            category=category,
            severity=severity,
            exception=exception,
            traceback_str=traceback.format_exc()
        )

        if suggestions:
            for suggestion in suggestions:
                ctx.add_suggestion(suggestion)

        self.display.show(ctx, show_traceback=True)


# Global handler instance
_handler: Optional[SmartErrorHandler] = None


def get_handler() -> SmartErrorHandler:
    """Get global error handler instance."""
    global _handler
    if _handler is None:
        _handler = SmartErrorHandler()
    return _handler


def handle_error(
    exception: Exception,
    category: ErrorCategory = ErrorCategory.SYSTEM,
    severity: ErrorSeverity = ErrorSeverity.ERROR,
    suggestions: Optional[List[str]] = None
):
    """Handle error with global handler."""
    handler = get_handler()
    handler.handle_generic_error(exception, category, severity, suggestions)


# Demo code
if __name__ == "__main__":
    print("=" * 70)
    print("SMART ERROR MESSAGES DEMO")
    print("=" * 70)
    print()

    # Create handler
    handler = SmartErrorHandler(
        valid_commands=["agents", "help", "status", "git", "config"],
        valid_agents=["sophia", "code", "test", "review", "fix"],
        valid_files=["config.json", "settings.yaml", "README.md"]
    )

    # Demo 1: Command not found
    print("1. COMMAND NOT FOUND ERROR:")
    print()
    try:
        raise Exception("Command not found")
    except Exception as e:
        handler.handle_command_error(e, "agen")

    print()
    print("-" * 70)
    print()

    # Demo 2: Agent not found
    print("2. AGENT NOT FOUND ERROR:")
    print()
    try:
        raise Exception("Agent not found")
    except Exception as e:
        handler.handle_agent_error(e, "sofi")

    print()
    print("-" * 70)
    print()

    # Demo 3: File not found
    print("3. FILE NOT FOUND ERROR:")
    print()
    try:
        raise FileNotFoundError("File not found")
    except Exception as e:
        handler.handle_file_error(e, "config.jsn")

    print()
    print("-" * 70)
    print()

    # Demo 4: Validation error
    print("4. VALIDATION ERROR:")
    print()
    try:
        raise ValueError("Invalid type")
    except Exception as e:
        handler.handle_validation_error(e, "timeout", "invalid", "int or float")

    print()
    print("=" * 70)
    print("DEMO COMPLETE")
    print("=" * 70)
