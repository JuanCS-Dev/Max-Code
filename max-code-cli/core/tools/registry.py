"""
Tool Registry - Central tool registration and discovery

Based on Anthropic SDK patterns for tool management.
Provides singleton registry for all @tool decorated functions.

Biblical Foundation:
"Cada qual segundo a sua obra" (Apocalipse 20:13)
"""

import logging
import asyncio
from typing import Dict, List, Optional, Any, Callable
from datetime import datetime

from .types import (
    ToolMetadata,
    ToolResult,
    ToolSchema,
    ToolHandler,
    AsyncToolHandler,
)

logger = logging.getLogger(__name__)


class ToolRegistryError(Exception):
    """Base exception for tool registry errors"""
    pass


class ToolNotFoundError(ToolRegistryError):
    """Tool not found in registry"""
    pass


class ToolAlreadyRegisteredError(ToolRegistryError):
    """Tool name already registered"""
    pass


class ToolRegistry:
    """
    Singleton registry for all tools.

    Manages tool registration, discovery, and execution.
    Thread-safe for concurrent access.
    """

    _instance: Optional["ToolRegistry"] = None
    _lock = asyncio.Lock()

    def __new__(cls):
        """Singleton pattern"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        """Initialize registry (only once due to singleton)"""
        if self._initialized:
            return

        self._tools: Dict[str, ToolMetadata] = {}
        self._tags_index: Dict[str, List[str]] = {}
        self._initialized = True
        logger.info("ToolRegistry initialized")

    def register(
        self,
        name: str,
        description: str,
        schema: ToolSchema,
        handler: Callable,
        async_handler: bool = False,
        tags: Optional[List[str]] = None,
        version: str = "1.0.0",
        force: bool = False,
    ) -> ToolMetadata:
        """
        Register a tool in the registry.

        Args:
            name: Unique tool name
            description: Tool description
            schema: Tool parameter schema
            handler: Tool handler function
            async_handler: Whether handler is async
            tags: Optional tags for categorization
            version: Tool version
            force: If True, overwrite existing tool

        Returns:
            ToolMetadata: Registered tool metadata

        Raises:
            ToolAlreadyRegisteredError: If tool name already exists and force=False
        """
        if name in self._tools and not force:
            raise ToolAlreadyRegisteredError(
                f"Tool '{name}' is already registered. Use force=True to overwrite."
            )

        metadata = ToolMetadata(
            name=name,
            description=description,
            schema=schema,
            handler=handler,
            async_handler=async_handler,
            tags=tags or [],
            version=version,
            created_at=datetime.now(),
        )

        self._tools[name] = metadata

        # Update tags index
        for tag in metadata.tags:
            if tag not in self._tags_index:
                self._tags_index[tag] = []
            if name not in self._tags_index[tag]:
                self._tags_index[tag].append(name)

        logger.info(f"Tool '{name}' registered successfully (version {version})")
        return metadata

    def unregister(self, name: str) -> bool:
        """
        Unregister a tool.

        Args:
            name: Tool name to unregister

        Returns:
            bool: True if tool was removed, False if not found
        """
        if name not in self._tools:
            return False

        metadata = self._tools[name]

        # Remove from tags index
        for tag in metadata.tags:
            if tag in self._tags_index and name in self._tags_index[tag]:
                self._tags_index[tag].remove(name)
                if not self._tags_index[tag]:
                    del self._tags_index[tag]

        del self._tools[name]
        logger.info(f"Tool '{name}' unregistered")
        return True

    def get(self, name: str) -> Optional[ToolMetadata]:
        """
        Get tool metadata by name.

        Args:
            name: Tool name

        Returns:
            ToolMetadata if found, None otherwise
        """
        return self._tools.get(name)

    def exists(self, name: str) -> bool:
        """Check if tool exists in registry"""
        return name in self._tools

    def list_tools(self, tag: Optional[str] = None) -> List[ToolMetadata]:
        """
        List all registered tools.

        Args:
            tag: Optional tag filter

        Returns:
            List of ToolMetadata
        """
        if tag is None:
            return list(self._tools.values())

        if tag not in self._tags_index:
            return []

        return [self._tools[name] for name in self._tags_index[tag]]

    def list_tool_names(self, tag: Optional[str] = None) -> List[str]:
        """
        List tool names.

        Args:
            tag: Optional tag filter

        Returns:
            List of tool names
        """
        if tag is None:
            return list(self._tools.keys())

        return self._tags_index.get(tag, [])

    def get_tool_count(self) -> int:
        """Get total number of registered tools"""
        return len(self._tools)

    async def execute(
        self,
        name: str,
        args: Dict[str, Any],
        validate: bool = True,
    ) -> ToolResult:
        """
        Execute a tool by name.

        Args:
            name: Tool name
            args: Tool arguments
            validate: Whether to validate args against schema

        Returns:
            ToolResult from tool execution

        Raises:
            ToolNotFoundError: If tool not found
            ValueError: If argument validation fails
        """
        metadata = self.get(name)
        if metadata is None:
            raise ToolNotFoundError(f"Tool '{name}' not found in registry")

        try:
            # Validate arguments
            if validate:
                validated_args = metadata.schema.validate(args)
            else:
                validated_args = args

            # Execute handler
            if metadata.async_handler:
                result = await metadata.handler(validated_args)
            else:
                result = metadata.handler(validated_args)

            # Ensure result is ToolResult
            if not isinstance(result, ToolResult):
                # Convert dict to ToolResult
                if isinstance(result, dict):
                    if "content" in result:
                        return ToolResult(**result)
                    else:
                        return ToolResult.success(str(result))
                else:
                    return ToolResult.success(str(result))

            return result

        except Exception as e:
            logger.error(f"Tool '{name}' execution failed: {e}")
            return ToolResult.error(f"Tool execution failed: {str(e)}")

    def export_schemas(self) -> Dict[str, Any]:
        """
        Export all tool schemas for API documentation.

        Returns:
            Dict mapping tool names to their schemas
        """
        return {
            name: metadata.to_dict()
            for name, metadata in self._tools.items()
        }

    def clear(self):
        """Clear all registered tools (useful for testing)"""
        self._tools.clear()
        self._tags_index.clear()
        logger.warning("ToolRegistry cleared")

    def __repr__(self) -> str:
        return f"<ToolRegistry: {len(self._tools)} tools registered>"

    def __str__(self) -> str:
        tools_list = ", ".join(self._tools.keys()) if self._tools else "none"
        return f"ToolRegistry({len(self._tools)} tools: {tools_list})"


# Global singleton instance
_registry = ToolRegistry()


def get_registry() -> ToolRegistry:
    """Get the global tool registry instance"""
    return _registry
