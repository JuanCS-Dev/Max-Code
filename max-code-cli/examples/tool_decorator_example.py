"""
Example: @tool Decorator Pattern

Demonstrates Anthropic SDK-style tool decoration following FASE 2.1 implementation.

Run: python examples/tool_decorator_example.py
"""

import asyncio
import sys
sys.path.insert(0, '.')

from core.tools import (
    tool,
    async_tool,
    file_tool,
    ToolResult,
    get_registry,
)


# ============================================================================
# EXAMPLE 1: Simple synchronous tool
# ============================================================================

@tool(name="greet", description="Greet a user", schema={"name": str})
def greet_user(args):
    """Greet user by name"""
    name = args.get("name", "World")
    return ToolResult.success(f"Hello, {name}!")


# ============================================================================
# EXAMPLE 2: Async tool with automatic schema extraction
# ============================================================================

@tool(
    name="fetch_weather",
    description="Fetch weather for a location",
    schema={"location": str, "units": str}
)
async def fetch_weather(args):
    """Fetch weather for a location"""
    location: str = args.get("location", "Unknown")
    units: str = args.get("units", "celsius")

    # Simulate API call
    await asyncio.sleep(0.1)

    return ToolResult.success(
        f"Weather in {location}: 22°{units[0].upper()}, Sunny"
    )


# ============================================================================
# EXAMPLE 3: File tool with custom tags
# ============================================================================

@file_tool(
    name="count_lines",
    description="Count lines in a file",
    schema={"filepath": str},
    tags=["file", "analysis"],
)
def count_lines(args):
    """Count lines in a file"""
    filepath = args["filepath"]

    try:
        with open(filepath, "r") as f:
            lines = len(f.readlines())
        return ToolResult.success(f"File has {lines} lines")
    except FileNotFoundError:
        return ToolResult.error(f"File not found: {filepath}")
    except Exception as e:
        return ToolResult.error(f"Error reading file: {e}")


# ============================================================================
# EXAMPLE 4: Tool with complex schema
# ============================================================================

@tool(
    name="calculate",
    description="Perform arithmetic operations",
    schema={
        "operation": str,  # add, subtract, multiply, divide
        "a": float,
        "b": float,
    },
    version="2.0.0",
)
def calculate(args):
    """Perform arithmetic calculation"""
    operation = args["operation"]
    a = args["a"]
    b = args["b"]

    operations = {
        "add": lambda x, y: x + y,
        "subtract": lambda x, y: x - y,
        "multiply": lambda x, y: x * y,
        "divide": lambda x, y: x / y if y != 0 else None,
    }

    if operation not in operations:
        return ToolResult.error(f"Unknown operation: {operation}")

    result = operations[operation](a, b)

    if result is None:
        return ToolResult.error("Division by zero")

    return ToolResult.success(f"{operation}({a}, {b}) = {result}")


# ============================================================================
# EXAMPLE 5: Tool returning dict (auto-converted to ToolResult)
# ============================================================================

@tool
def get_system_info(args):
    """Get system information"""
    import platform

    return {
        "system": platform.system(),
        "release": platform.release(),
        "python_version": platform.python_version(),
    }


# ============================================================================
# MAIN: Demonstrate tool usage
# ============================================================================

async def main():
    print("=" * 70)
    print("TOOL DECORATOR EXAMPLES - FASE 2.1")
    print("=" * 70)
    print()

    registry = get_registry()

    # List all registered tools
    print(f"📋 Registered Tools: {registry.get_tool_count()}")
    for tool_meta in registry.list_tools():
        print(f"  - {tool_meta.name}: {tool_meta.description}")
    print()

    # ========================================================================
    # Test 1: Simple greeting
    # ========================================================================
    print("[1/5] Simple Tool (greet)")
    result = await registry.execute("greet", {"name": "Claude"})
    print(f"  Result: {result.content[0].text}")
    print()

    # ========================================================================
    # Test 2: Async weather tool
    # ========================================================================
    print("[2/5] Async Tool (fetch_weather)")
    result = await registry.execute("fetch_weather", {
        "location": "San Francisco",
        "units": "fahrenheit"
    })
    print(f"  Result: {result.content[0].text}")
    print()

    # ========================================================================
    # Test 3: File tool
    # ========================================================================
    print("[3/5] File Tool (count_lines)")
    result = await registry.execute("count_lines", {
        "filepath": "examples/tool_decorator_example.py"
    })
    print(f"  Result: {result.content[0].text}")
    print()

    # ========================================================================
    # Test 4: Calculator
    # ========================================================================
    print("[4/5] Complex Schema Tool (calculate)")
    result = await registry.execute("calculate", {
        "operation": "multiply",
        "a": 7,
        "b": 6
    })
    print(f"  Result: {result.content[0].text}")
    print()

    # ========================================================================
    # Test 5: Dict return (auto-conversion)
    # ========================================================================
    print("[5/5] Dict Return Tool (get_system_info)")
    result = await registry.execute("get_system_info", {})
    print(f"  Result: {result.content[0].text}")
    print()

    # ========================================================================
    # Export schemas
    # ========================================================================
    print("=" * 70)
    print("TOOL SCHEMAS (for API documentation)")
    print("=" * 70)
    import json
    schemas = registry.export_schemas()
    print(json.dumps(schemas, indent=2))


if __name__ == "__main__":
    asyncio.run(main())
