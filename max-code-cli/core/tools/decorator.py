"""
@tool Decorator - Anthropic SDK-style tool decorator

Provides clean Pythonic API for tool registration:

@tool(name="read_file", description="Read file contents", schema={"path": str})
async def read_file(args):
    return ToolResult.success(...)

v2.0: Enhanced with EnhancedToolMetadata integration for smart selection

Biblical Foundation:
"O que trabalha com mão remissa empobrece, mas a mão dos diligentes enriquece" (Provérbios 10:4)
"""

import logging
import asyncio
import functools
import inspect
from typing import Dict, Any, Optional, Callable, Union, List

from .types import (
    ToolResult,
    ToolSchema,
    ToolParameter,
)
from .registry import get_registry, ToolRegistry
from .tool_metadata import (
    EnhancedToolMetadata,
    ToolCategory,
    ToolCapabilities,
    ToolRequirements,
    ToolPerformance,
)
from .enhanced_registry import get_enhanced_registry

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


# ============================================================================
# ENHANCED DECORATORS (v2.0) - World-Class Quality
# ============================================================================


def enhanced_tool(
    name: Optional[str] = None,
    description: Optional[str] = None,
    category: ToolCategory = ToolCategory.FILE_OPS,
    can_read: bool = False,
    can_write: bool = False,
    can_execute: bool = False,
    can_search: bool = False,
    can_analyze: bool = False,
    can_validate: bool = False,
    requires_filepath: bool = False,
    requires_directory: bool = False,
    requires_pattern: bool = False,
    requires_content: bool = False,
    safe: bool = True,
    destructive: bool = False,
    expensive: bool = False,
    estimated_time: int = 5,
    tags: Optional[List[str]] = None,
    examples: Optional[List[dict]] = None,
    auto_register: bool = True,
):
    """
    Enhanced decorator with rich metadata for smart tool selection
    
    Combines features of @tool with EnhancedToolMetadata for intelligent
    tool selection via ToolSelector. Automatically registers with both
    standard and enhanced registries.
    
    Args:
        name: Tool name (defaults to function name)
        description: Tool description (defaults to docstring)
        category: Tool category for organization
        can_read: Tool can read files/data
        can_write: Tool can write/modify files/data
        can_execute: Tool can execute commands/scripts
        can_search: Tool can search/find patterns
        can_analyze: Tool can analyze/inspect code/data
        can_validate: Tool can validate/check correctness
        requires_filepath: Requires file path input
        requires_directory: Requires directory path input
        requires_pattern: Requires search pattern input
        requires_content: Requires content/text input
        safe: Safe to run without confirmation
        destructive: Modifies files/data (use with caution)
        expensive: High resource usage (CPU/memory/time)
        estimated_time: Estimated execution time (seconds)
        tags: Optional tags for categorization
        examples: Optional usage examples
        auto_register: Auto-register with registries
    
    Returns:
        Decorated function with rich metadata
    
    Examples:
        >>> @enhanced_tool(
        ...     name="grep_files",
        ...     description="Search for pattern in files",
        ...     category=ToolCategory.SEARCH,
        ...     can_read=True,
        ...     can_search=True,
        ...     requires_pattern=True,
        ...     tags=["search", "grep", "regex"]
        ... )
        ... async def grep_files(pattern: str, path: str = ".") -> ToolResult:
        ...     # Implementation
        ...     results = search_files(pattern, path)
        ...     return ToolResult.success(results)
        
        >>> @enhanced_tool(
        ...     name="write_file",
        ...     description="Write content to file",
        ...     category=ToolCategory.FILE_OPS,
        ...     can_write=True,
        ...     requires_filepath=True,
        ...     requires_content=True,
        ...     destructive=True,
        ...     tags=["file", "write", "io"]
        ... )
        ... def write_file(filepath: str, content: str) -> ToolResult:
        ...     with open(filepath, 'w') as f:
        ...         f.write(content)
        ...     return ToolResult.success(f"Wrote {len(content)} bytes")
    
    Notes:
        - Automatically extracts parameter types from function signature
        - Registers with both ToolRegistry and EnhancedToolRegistry
        - Compatible with sync and async functions
        - Returns ToolResult (same as @tool)
    """
    def decorator(func: Callable) -> Callable:
        # Extract metadata
        tool_name = name or func.__name__
        tool_description = description or func.__doc__ or f"Tool: {tool_name}"
        
        # Extract parameters from function signature
        sig = inspect.signature(func)
        parameters = []
        
        for param_name, param in sig.parameters.items():
            if param_name in ('self', 'args', 'kwargs'):
                continue
            
            # Infer type from annotation
            param_type = "string"  # default
            if param.annotation != inspect.Parameter.empty:
                if param.annotation in (int, 'int'):
                    param_type = "number"
                elif param.annotation in (bool, 'bool'):
                    param_type = "boolean"
                elif param.annotation in (list, List):
                    param_type = "array"
                elif param.annotation in (dict, Dict):
                    param_type = "object"
                elif hasattr(param.annotation, '__origin__'):
                    # Handle typing generics (List[str], Dict[str, Any], etc.)
                    origin = param.annotation.__origin__
                    if origin in (list, List):
                        param_type = "array"
                    elif origin in (dict, Dict):
                        param_type = "object"
            
            parameters.append({
                "name": param_name,
                "type": param_type,
                "description": f"Parameter {param_name}",
                "required": param.default == inspect.Parameter.empty
            })
        
        # Create enhanced metadata
        enhanced_metadata = EnhancedToolMetadata(
            name=tool_name,
            description=tool_description,
            category=category,
            capabilities=ToolCapabilities(
                can_read=can_read,
                can_write=can_write,
                can_execute=can_execute,
                can_search=can_search,
                can_analyze=can_analyze,
                can_validate=can_validate,
            ),
            requirements=ToolRequirements(
                requires_filepath=requires_filepath,
                requires_directory=requires_directory,
                requires_pattern=requires_pattern,
                requires_content=requires_content,
            ),
            performance=ToolPerformance(
                estimated_time=estimated_time,
                safe=safe,
                destructive=destructive,
                expensive=expensive,
            ),
            parameters=parameters,
            tags=tags or [],
            examples=examples or [],
        )
        
        # Detect if async
        is_async = asyncio.iscoroutinefunction(func)
        
        # Create wrapper with ToolResult guarantee
        if is_async:
            @functools.wraps(func)
            async def async_wrapper(args: Dict[str, Any]) -> ToolResult:
                try:
                    result = await func(**args) if isinstance(args, dict) else await func(args)
                    return _ensure_tool_result(result, tool_name)
                except Exception as e:
                    logger.error(f"Enhanced tool '{tool_name}' failed: {e}", exc_info=True)
                    return ToolResult.error(f"Tool execution failed: {str(e)}")
            
            handler = async_wrapper
        else:
            @functools.wraps(func)
            def sync_wrapper(args: Dict[str, Any]) -> ToolResult:
                try:
                    result = func(**args) if isinstance(args, dict) else func(args)
                    return _ensure_tool_result(result, tool_name)
                except Exception as e:
                    logger.error(f"Enhanced tool '{tool_name}' failed: {e}", exc_info=True)
                    return ToolResult.error(f"Tool execution failed: {str(e)}")
            
            handler = sync_wrapper
        
        # Attach metadata
        handler._tool_name = tool_name
        handler._tool_description = tool_description
        handler._tool_enhanced_metadata = enhanced_metadata
        handler._tool_is_async = is_async
        handler._tool_registered = False
        
        # Auto-register with both registries
        if auto_register:
            # Register with standard registry
            try:
                registry = get_registry()
                schema = ToolSchema(
                    type="object",
                    properties={p["name"]: {"type": p["type"], "description": p["description"]} 
                               for p in parameters},
                    required=[p["name"] for p in parameters if p["required"]]
                )
                
                registry.register(
                    name=tool_name,
                    description=tool_description,
                    schema=schema,
                    handler=handler,
                    async_handler=is_async,
                    tags=tags or [],
                    version="1.0.0",
                )
                logger.debug(f"Enhanced tool '{tool_name}' registered with ToolRegistry")
            except Exception as e:
                logger.warning(f"Failed to register '{tool_name}' with ToolRegistry: {e}")
            
            # Register with enhanced registry
            try:
                enhanced_registry = get_enhanced_registry()
                enhanced_registry.register_enhanced(enhanced_metadata)
                handler._tool_registered = True
                logger.debug(f"Enhanced tool '{tool_name}' registered with EnhancedToolRegistry")
            except Exception as e:
                logger.warning(f"Failed to register '{tool_name}' with EnhancedToolRegistry: {e}")
        
        return handler
    
    return decorator


def quick_tool(
    name: Optional[str] = None,
    description: Optional[str] = None,
    category: ToolCategory = ToolCategory.FILE_OPS,
    **kwargs
):
    """
    Quick decorator for simple tools with minimal configuration
    
    Convenience wrapper around @enhanced_tool with sensible defaults
    for common file operations. Automatically sets can_read=True.
    
    Args:
        name: Tool name (defaults to function name)
        description: Tool description (defaults to docstring)
        category: Tool category (defaults to FILE_OPS)
        **kwargs: Additional arguments passed to @enhanced_tool
    
    Returns:
        Decorated function with basic metadata
    
    Examples:
        >>> @quick_tool("read_file", "Read a file")
        ... def read_file(filepath: str) -> ToolResult:
        ...     with open(filepath) as f:
        ...         return ToolResult.success(f.read())
        
        >>> @quick_tool()  # Uses function name and docstring
        ... async def fetch_data(url: str) -> ToolResult:
        ...     '''Fetch data from URL'''
        ...     data = await http_get(url)
        ...     return ToolResult.success(data)
    
    Notes:
        - Sets can_read=True by default
        - Sets safe=True by default
        - Ideal for simple read-only operations
        - Use @enhanced_tool for more control
    """
    # Set defaults for quick tools
    kwargs.setdefault('can_read', True)
    kwargs.setdefault('safe', True)
    
    return enhanced_tool(
        name=name,
        description=description,
        category=category,
        **kwargs
    )


def search_tool(
    name: Optional[str] = None,
    description: Optional[str] = None,
    **kwargs
):
    """
    Decorator for search/grep tools
    
    Convenience wrapper with search-specific defaults.
    
    Args:
        name: Tool name
        description: Tool description
        **kwargs: Additional arguments
    
    Examples:
        >>> @search_tool("grep_files", "Search for pattern in files")
        ... def grep_files(pattern: str, path: str = ".") -> ToolResult:
        ...     results = search(pattern, path)
        ...     return ToolResult.success(results)
    """
    kwargs.setdefault('category', ToolCategory.SEARCH)
    kwargs.setdefault('can_read', True)
    kwargs.setdefault('can_search', True)
    kwargs.setdefault('requires_pattern', True)
    kwargs.setdefault('safe', True)
    
    return enhanced_tool(name=name, description=description, **kwargs)


def write_tool(
    name: Optional[str] = None,
    description: Optional[str] = None,
    **kwargs
):
    """
    Decorator for write/modify tools
    
    Convenience wrapper with write-specific defaults.
    Sets destructive=True as warning.
    
    Args:
        name: Tool name
        description: Tool description
        **kwargs: Additional arguments
    
    Examples:
        >>> @write_tool("create_file", "Create new file")
        ... def create_file(filepath: str, content: str) -> ToolResult:
        ...     with open(filepath, 'w') as f:
        ...         f.write(content)
        ...     return ToolResult.success("File created")
    """
    kwargs.setdefault('category', ToolCategory.FILE_OPS)
    kwargs.setdefault('can_write', True)
    kwargs.setdefault('requires_filepath', True)
    kwargs.setdefault('requires_content', True)
    kwargs.setdefault('destructive', True)
    kwargs.setdefault('safe', False)  # Requires confirmation
    
    return enhanced_tool(name=name, description=description, **kwargs)


def execute_tool(
    name: Optional[str] = None,
    description: Optional[str] = None,
    **kwargs
):
    """
    Decorator for execution/command tools
    
    Convenience wrapper for tools that execute commands.
    Sets can_execute=True and appropriate safety flags.
    
    Args:
        name: Tool name
        description: Tool description
        **kwargs: Additional arguments
    
    Examples:
        >>> @execute_tool("run_command", "Execute shell command")
        ... async def run_command(command: str) -> ToolResult:
        ...     result = await shell_exec(command)
        ...     return ToolResult.success(result)
    """
    kwargs.setdefault('category', ToolCategory.EXECUTION)
    kwargs.setdefault('can_execute', True)
    kwargs.setdefault('destructive', True)
    kwargs.setdefault('safe', False)
    kwargs.setdefault('expensive', True)
    
    return enhanced_tool(name=name, description=description, **kwargs)
