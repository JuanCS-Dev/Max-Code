"""
@tool Decorator - Anthropic SDK-style tool decorator

Provides clean Pythonic API for tool registration:

@tool(name="read_file", description="Read file contents", schema={"path": str})
async def read_file(args):
    return ToolResult.success(...)

Biblical Foundation:
"O que trabalha com mão remissa empobrece, mas a mão dos diligentes enriquece" (Provérbios 10:4)
"""

import logging
import asyncio
import functools
from typing import Dict, Any, Optional, Callable, Union, List

from .types import (
    ToolResult,
    ToolSchema,
    ToolParameter,
)
from .registry import get_registry, ToolRegistry

logger = logging.getLogger(__name__)


def tool(
    _func: Optional[Callable] = None,
    *,
    name: Optional[str] = None,
    description: Optional[str] = None,
    schema: Optional[Union[Dict[str, type], ToolSchema]] = None,
    tags: Optional[List[str]] = None,
    version: str = "1.0.0",
    auto_register: bool = True,
    registry: Optional[ToolRegistry] = None,
):
    """
    Decorator to register a function as a tool.

    Based on Anthropic SDK patterns:
    - @beta_tool for simple functions
    - @tool for Agent SDK

    Can be used with or without parentheses:
        @tool
        @tool()
        @tool(name="custom_name")

    Args:
        name: Tool name (defaults to function name)
        description: Tool description (defaults to docstring)
        schema: Parameter schema (dict or ToolSchema)
        tags: Optional tags for categorization
        version: Tool version
        auto_register: If True, register immediately on decoration
        registry: Custom registry (defaults to global)

    Returns:
        Decorated function that returns ToolResult

    Examples:
        >>> @tool(name="greet", description="Greet user", schema={"name": str})
        >>> async def greet_user(args):
        ...     return ToolResult.success(f"Hello, {args['name']}!")

        >>> @tool  # Uses function name and docstring
        >>> def calculate_sum(args):
        ...     '''Calculate sum of two numbers'''
        ...     a = args.get("a", 0)
        ...     b = args.get("b", 0)
        ...     return ToolResult.success(f"Sum: {a + b}")
    """

    def decorator(func: Callable) -> Callable:
        # Extract metadata
        tool_name = name or func.__name__
        tool_description = description or func.__doc__ or f"Tool: {tool_name}"

        # Build schema
        if schema is None:
            # Extract from function signature
            tool_schema = ToolSchema.from_function(func)
        elif isinstance(schema, dict):
            # Convert dict to ToolSchema
            tool_schema = ToolSchema.from_dict(schema)
        elif isinstance(schema, ToolSchema):
            tool_schema = schema
        else:
            raise ValueError(f"Invalid schema type: {type(schema)}")

        # Detect if function is async
        is_async = asyncio.iscoroutinefunction(func)

        # Wrap function to ensure ToolResult return
        if is_async:
            @functools.wraps(func)
            async def async_wrapper(args: Dict[str, Any]) -> ToolResult:
                try:
                    result = await func(args)
                    return _ensure_tool_result(result, tool_name)
                except Exception as e:
                    logger.error(f"Tool '{tool_name}' failed: {e}", exc_info=True)
                    return ToolResult.error(f"Tool execution failed: {str(e)}")

            handler = async_wrapper
        else:
            @functools.wraps(func)
            def sync_wrapper(args: Dict[str, Any]) -> ToolResult:
                try:
                    result = func(args)
                    return _ensure_tool_result(result, tool_name)
                except Exception as e:
                    logger.error(f"Tool '{tool_name}' failed: {e}", exc_info=True)
                    return ToolResult.error(f"Tool execution failed: {str(e)}")

            handler = sync_wrapper

        # Attach metadata to function
        handler._tool_name = tool_name
        handler._tool_description = tool_description
        handler._tool_schema = tool_schema
        handler._tool_tags = tags or []
        handler._tool_version = version
        handler._tool_is_async = is_async
        handler._tool_registered = False

        # Auto-register if requested
        if auto_register:
            reg = registry or get_registry()
            try:
                reg.register(
                    name=tool_name,
                    description=tool_description,
                    schema=tool_schema,
                    handler=handler,
                    async_handler=is_async,
                    tags=tags or [],
                    version=version,
                )
                handler._tool_registered = True
                logger.debug(f"Tool '{tool_name}' auto-registered")
            except Exception as e:
                logger.warning(f"Failed to auto-register tool '{tool_name}': {e}")

        return handler

    # Support using decorator without parentheses: @tool
    if _func is not None:
        return decorator(_func)

    # Support using decorator with parentheses: @tool()
    return decorator


def _ensure_tool_result(result: Any, tool_name: str) -> ToolResult:
    """
    Ensure result is a ToolResult.

    Converts various return types to ToolResult:
    - ToolResult: Pass through
    - Dict with "content": Convert to ToolResult
    - Dict without "content": Wrap in success result
    - String: Wrap in success result
    - Other: Convert to string and wrap
    """
    if isinstance(result, ToolResult):
        return result

    if isinstance(result, dict):
        if "content" in result:
            try:
                return ToolResult(**result)
            except Exception as e:
                logger.warning(f"Failed to convert dict to ToolResult for '{tool_name}': {e}")
                return ToolResult.success(str(result))
        else:
            # Dict without "content" - treat as success with JSON
            import json
            return ToolResult.success(json.dumps(result, indent=2))

    if isinstance(result, str):
        return ToolResult.success(result)

    # Convert other types to string
    return ToolResult.success(str(result))


# Convenience functions for common use cases

def text_tool(
    name: Optional[str] = None,
    description: Optional[str] = None,
    schema: Optional[Union[Dict[str, type], ToolSchema]] = None,
    **kwargs
):
    """
    Decorator for tools that return simple text.

    Automatically wraps return value in ToolResult.text()
    """
    return tool(name=name, description=description, schema=schema, **kwargs)


def file_tool(
    name: Optional[str] = None,
    description: Optional[str] = None,
    **kwargs
):
    """
    Decorator for file operation tools.

    Adds "file_operations" tag automatically.
    """
    tags = kwargs.get("tags", [])
    tags.append("file_operations")
    kwargs["tags"] = tags
    return tool(name=name, description=description, **kwargs)


def async_tool(
    name: Optional[str] = None,
    description: Optional[str] = None,
    schema: Optional[Union[Dict[str, type], ToolSchema]] = None,
    **kwargs
):
    """
    Decorator explicitly for async tools.

    Validates that decorated function is async.
    """
    def decorator(func: Callable) -> Callable:
        if not asyncio.iscoroutinefunction(func):
            raise ValueError(f"@async_tool can only decorate async functions, but '{func.__name__}' is not async")
        return tool(name=name, description=description, schema=schema, **kwargs)(func)
    return decorator


# Alias for compatibility with Anthropic SDK naming
beta_tool = tool
