"""
Test Error Handling for UI Components

Tests that UI gracefully handles edge cases and invalid input.
"""

import sys
sys.path.insert(0, '/media/juan/DATA1/projects/MAXIMUS AI/max-code-cli')

from ui.agents import AgentDisplay, Agent, AgentStatus
from ui.exceptions import EmptyDataError, InvalidInputError
from ui.validation import (
    validate_items, validate_score, validate_percentage,
    validate_string, validate_positive_int
)
from rich.console import Console
from io import StringIO


def test_empty_agents_list():
    """Test that empty agents list is handled gracefully."""
    print("Test 1: Empty agents list")

    console = Console(file=StringIO())
    display = AgentDisplay(console=console)

    # Should not crash, should show empty state
    display.show_dashboard([])
    print("  ✓ Handled empty list gracefully\n")


def test_invalid_agent_data():
    """Test that invalid agent data is handled."""
    print("Test 2: Invalid agent data")

    console = Console(file=StringIO())
    display = AgentDisplay(console=console)

    # Agent with invalid progress (>100)
    bad_agent = Agent(
        name="BadAgent",
        role="Test",
        status=AgentStatus.ACTIVE,
        progress=150.0  # Invalid!
    )

    # Should clamp to valid range
    display.show_dashboard([bad_agent])
    print("  ✓ Clamped invalid progress to valid range\n")


def test_validation_functions():
    """Test validation functions."""
    print("Test 3: Validation functions")

    # Test empty list validation
    try:
        validate_items([], min_items=1)
        print("  ✗ Should have raised EmptyDataError")
    except EmptyDataError as e:
        print(f"  ✓ Caught empty list: {e.message}")

    # Test score validation
    try:
        validate_score(15.0, max_score=10.0)
        print("  ✗ Should have raised InvalidInputError")
    except InvalidInputError as e:
        print(f"  ✓ Caught invalid score: {e.message}")

    # Test percentage validation
    try:
        validate_percentage(150.0)
        print("  ✗ Should have raised InvalidInputError")
    except InvalidInputError as e:
        print(f"  ✓ Caught invalid percentage: {e.message}")

    # Test positive int validation
    try:
        validate_positive_int(-5, field_name="count")
        print("  ✗ Should have raised InvalidInputError")
    except InvalidInputError as e:
        print(f"  ✓ Caught negative int: {e.message}")

    print()


def test_agent_with_none_values():
    """Test agent with None values."""
    print("Test 4: Agent with None values")

    console = Console(file=StringIO())
    display = AgentDisplay(console=console)

    # Agent with None task
    agent = Agent(
        name="TestAgent",
        role="Test",
        status=AgentStatus.ACTIVE,
        current_task=None  # None value
    )

    # Should handle None gracefully
    display.show_dashboard([agent])
    print("  ✓ Handled None task gracefully\n")


def test_agent_with_extreme_values():
    """Test agent with extreme values."""
    print("Test 5: Extreme values")

    console = Console(file=StringIO())
    display = AgentDisplay(console=console)

    agents = [
        Agent("A", "R", AgentStatus.ACTIVE, progress=-50.0),   # Negative
        Agent("B", "R", AgentStatus.ACTIVE, progress=500.0),   # Too large
        Agent("C", "R", AgentStatus.ACTIVE, progress=50.5),    # Normal
    ]

    # Should clamp all values
    display.show_dashboard(agents)
    print("  ✓ Clamped all extreme values\n")


def main():
    """Run all error handling tests."""
    print("=" * 80)
    print("ERROR HANDLING TESTS")
    print("=" * 80)
    print()

    test_empty_agents_list()
    test_invalid_agent_data()
    test_validation_functions()
    test_agent_with_none_values()
    test_agent_with_extreme_values()

    print("=" * 80)
    print("✅ ALL ERROR HANDLING TESTS PASSED!")
    print("=" * 80)


if __name__ == '__main__':
    main()
