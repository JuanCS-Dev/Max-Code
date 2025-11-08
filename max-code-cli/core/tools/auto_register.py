"""
Auto-Registration Helper for Tools (PROMPT 2.2)

Eliminates code duplication in tool registration.
Each tool calls register_tool() at module level.

Biblical Foundation:
"Não te multipliques em palavras" (Eclesiastes 5:2)
DRY principle - Don't Repeat Yourself

Soli Deo Gloria
"""

from typing import Dict, List, Callable, Any, Optional
from config.logging_config import get_logger

logger = get_logger(__name__)


def register_tool(
    name: str,
    description: str,
    handler_class: type,
    handler_method: str,
    parameters: List[Dict[str, Any]],
    tags: List[str],
    version: str = "1.0.0",
    init_kwargs: Optional[Dict[str, Any]] = None
):
    """
    Register tool with ToolRegistry (auto-called on import)
    
    Args:
        name: Tool name
        description: Tool description
        handler_class: Tool class (e.g., FileReader)
        handler_method: Method name to call (e.g., "read")
        parameters: List of parameter dicts with name, type, description, required
        tags: Tool tags
        version: Tool version
        init_kwargs: Optional kwargs for handler_class.__init__()
    
    Examples:
        >>> register_tool(
        ...     name="file_reader",
        ...     description="Read files",
        ...     handler_class=FileReader,
        ...     handler_method="read",
        ...     parameters=[
        ...         {"name": "file_path", "type": "string", "description": "Path", "required": True}
        ...     ],
        ...     tags=["file", "read"]
        ... )
    """
    try:
        from .registry import get_registry
        from .types import ToolSchema, ToolParameter, ToolMetadata, ToolResult
        
        # Build schema
        schema_params = [
            ToolParameter(
                name=p["name"],
                type=p["type"],
                description=p["description"],
                required=p.get("required", False),
                default=p.get("default")
            )
            for p in parameters
        ]
        
        schema = ToolSchema(parameters=schema_params)
        
        # Create handler wrapper
        def handler_wrapper(args: Dict) -> ToolResult:
            """Generated handler wrapper"""
            # Instantiate handler class
            init_args = init_kwargs or {}
            handler_instance = handler_class(**init_args)
            
            # Call method
            method = getattr(handler_instance, handler_method)
            result = method(**args)
            
            # Convert to ToolResult
            # Check if result has success/error attributes (our Result pattern)
            if hasattr(result, 'success') and hasattr(result, 'error'):
                if result.success:
                    content = getattr(result, 'content', str(result))
                    metadata = {}
                    
                    # Extract metadata from result
                    for attr in dir(result):
                        if not attr.startswith('_') and attr not in ['success', 'error', 'content']:
                            value = getattr(result, attr)
                            if not callable(value):
                                metadata[attr] = value
                    
                    return ToolResult.success(content, **metadata)
                else:
                    return ToolResult.error(result.error or "Unknown error")
            else:
                # Plain return value
                return ToolResult.success(str(result))
        
        # Register with registry
        registry = get_registry()
        registry.register(
            name=name,
            description=description,
            schema=schema,
            handler=handler_wrapper,
            tags=tags,
            version=version
        )
        
        logger.debug(f"✓ {name} registered with ToolRegistry")
        
    except Exception as e:
        # Fail silently (import-time errors are hard to debug)
        logger.debug(f"Could not auto-register {name}: {e}")


def register_tool_function(
    name: str,
    description: str,
    function: Callable,
    parameters: List[Dict[str, Any]],
    tags: List[str],
    version: str = "1.0.0"
):
    """
    Register standalone function as tool
    
    Args:
        name: Tool name
        description: Tool description
        function: Function to call
        parameters: Parameter specifications
        tags: Tool tags
        version: Tool version
    """
    try:
        from .registry import get_registry
        from .types import ToolSchema, ToolParameter, ToolResult
        
        # Build schema
        schema_params = [
            ToolParameter(
                name=p["name"],
                type=p["type"],
                description=p["description"],
                required=p.get("required", False),
                default=p.get("default")
            )
            for p in parameters
        ]
        
        schema = ToolSchema(parameters=schema_params)
        
        # Create handler wrapper
        def handler_wrapper(args: Dict) -> ToolResult:
            """Generated function wrapper"""
            result = function(**args)
            
            # Handle different return types
            if isinstance(result, ToolResult):
                return result
            elif isinstance(result, str):
                return ToolResult.success(result)
            elif hasattr(result, 'success'):
                if result.success:
                    content = getattr(result, 'content', str(result))
                    return ToolResult.success(content)
                else:
                    return ToolResult.error(result.error or "Unknown error")
            else:
                return ToolResult.success(str(result))
        
        # Register
        registry = get_registry()
        registry.register(
            name=name,
            description=description,
            schema=schema,
            handler=handler_wrapper,
            tags=tags,
            version=version
        )
        
        logger.debug(f"✓ {name} function registered")
        
    except Exception as e:
        logger.debug(f"Could not auto-register {name} function: {e}")
