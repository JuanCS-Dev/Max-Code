"""
Max-Code CLI UI Validation

Input validation utilities for UI components.
Ensures data integrity and provides helpful error messages.

Usage:
    from ui.validation import validate_items, validate_score, validate_percentage

    validate_items(items, min_items=1)
    validate_score(8.5)
"""

from typing import Any, List, Optional
from ui.exceptions import InvalidInputError, EmptyDataError


def validate_items(
    items: List[Any],
    min_items: int = 1,
    max_items: Optional[int] = None,
    item_name: str = "items"
) -> None:
    """
    Validate list of items.

    Args:
        items: List to validate
        min_items: Minimum number of items required
        max_items: Maximum number of items allowed
        item_name: Name for error messages

    Raises:
        EmptyDataError: If items list is empty
        InvalidInputError: If constraints not met
    """
    if not items:
        raise EmptyDataError(
            f"{item_name.capitalize()} list is empty",
            suggestion=f"Provide at least {min_items} {item_name}"
        )

    if len(items) < min_items:
        raise InvalidInputError(
            f"Too few {item_name}: {len(items)} (minimum: {min_items})",
            suggestion=f"Provide at least {min_items} {item_name}"
        )

    if max_items and len(items) > max_items:
        raise InvalidInputError(
            f"Too many {item_name}: {len(items)} (maximum: {max_items})",
            suggestion=f"Reduce to {max_items} {item_name} or fewer"
        )


def validate_score(score: float, min_score: float = 0.0, max_score: float = 10.0) -> None:
    """
    Validate score is within range.

    Args:
        score: Score to validate
        min_score: Minimum allowed score
        max_score: Maximum allowed score

    Raises:
        InvalidInputError: If score out of range
    """
    if not isinstance(score, (int, float)):
        raise InvalidInputError(
            f"Score must be a number, got {type(score).__name__}",
            suggestion=f"Use a float between {min_score} and {max_score}"
        )

    if score < min_score or score > max_score:
        raise InvalidInputError(
            f"Score {score} out of range [{min_score}, {max_score}]",
            suggestion=f"Use a value between {min_score} and {max_score}"
        )


def validate_percentage(percentage: float) -> None:
    """
    Validate percentage is 0-100.

    Args:
        percentage: Percentage to validate

    Raises:
        InvalidInputError: If not valid percentage
    """
    validate_score(percentage, min_score=0.0, max_score=100.0)


def validate_string(
    text: str,
    min_length: int = 1,
    max_length: Optional[int] = None,
    field_name: str = "text"
) -> None:
    """
    Validate string constraints.

    Args:
        text: String to validate
        min_length: Minimum length
        max_length: Maximum length
        field_name: Name for error messages

    Raises:
        InvalidInputError: If constraints not met
    """
    if not isinstance(text, str):
        raise InvalidInputError(
            f"{field_name.capitalize()} must be a string, got {type(text).__name__}",
            suggestion="Provide a text string"
        )

    if len(text) < min_length:
        raise InvalidInputError(
            f"{field_name.capitalize()} too short: {len(text)} chars (minimum: {min_length})",
            suggestion=f"Provide at least {min_length} characters"
        )

    if max_length and len(text) > max_length:
        raise InvalidInputError(
            f"{field_name.capitalize()} too long: {len(text)} chars (maximum: {max_length})",
            suggestion=f"Reduce to {max_length} characters or fewer"
        )


def validate_positive_int(
    value: int,
    field_name: str = "value",
    allow_zero: bool = False
) -> None:
    """
    Validate positive integer.

    Args:
        value: Integer to validate
        field_name: Name for error messages
        allow_zero: Whether to allow zero

    Raises:
        InvalidInputError: If not positive integer
    """
    if not isinstance(value, int):
        raise InvalidInputError(
            f"{field_name.capitalize()} must be an integer, got {type(value).__name__}",
            suggestion="Provide an integer value"
        )

    min_value = 0 if allow_zero else 1
    if value < min_value:
        raise InvalidInputError(
            f"{field_name.capitalize()} must be >= {min_value}, got {value}",
            suggestion=f"Use a value >= {min_value}"
        )


def validate_choice(
    value: Any,
    choices: List[Any],
    field_name: str = "value"
) -> None:
    """
    Validate value is in allowed choices.

    Args:
        value: Value to validate
        choices: List of allowed choices
        field_name: Name for error messages

    Raises:
        InvalidInputError: If value not in choices
    """
    if value not in choices:
        choices_str = ", ".join(str(c) for c in choices)
        raise InvalidInputError(
            f"Invalid {field_name}: {value}",
            suggestion=f"Choose from: {choices_str}"
        )


def validate_type(
    value: Any,
    expected_type: type,
    field_name: str = "value"
) -> None:
    """
    Validate value type.

    Args:
        value: Value to validate
        expected_type: Expected type
        field_name: Name for error messages

    Raises:
        InvalidInputError: If wrong type
    """
    if not isinstance(value, expected_type):
        raise InvalidInputError(
            f"{field_name.capitalize()} must be {expected_type.__name__}, got {type(value).__name__}",
            suggestion=f"Provide a {expected_type.__name__} value"
        )


__all__ = [
    'validate_items',
    'validate_score',
    'validate_percentage',
    'validate_string',
    'validate_positive_int',
    'validate_choice',
    'validate_type',
]
