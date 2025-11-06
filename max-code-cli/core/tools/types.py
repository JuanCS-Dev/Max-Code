"""
Tool Types - Type definitions for @tool decorator pattern

Based on Anthropic SDK 2025 patterns:
- ToolResult: Standardized return type
- ToolSchema: Tool parameter schema
- ToolMetadata: Tool registration metadata

Biblical Foundation:
"Tudo tem o seu tempo determinado" (Eclesiastes 3:1)
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Callable, Union
from enum import Enum
from datetime import datetime
import inspect


class ToolResultType(str, Enum):
    """Types of tool result content"""
    TEXT = "text"
    IMAGE = "image"
    ERROR = "error"
    SUCCESS = "success"


@dataclass
class ToolContent:
    """
    Single content block in tool result.

    Matches Anthropic SDK format:
    {"type": "text", "text": "..."}
    """
    type: ToolResultType
    text: Optional[str] = None
    data: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        result = {"type": self.type}
        if self.text is not None:
            result["text"] = self.text
        if self.data is not None:
            result["data"] = self.data
        return result


@dataclass
class ToolResult:
    """
    Standardized tool result format.

    Compatible with Anthropic SDK:
    {
        "content": [
            {"type": "text", "text": "Result message"}
        ]
    }
    """
    content: List[ToolContent] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def success(cls, text: str, **metadata) -> "ToolResult":
        """Create success result with text"""
        return cls(
            content=[ToolContent(type=ToolResultType.SUCCESS, text=text)],
            metadata=metadata
        )

    @classmethod
    def error(cls, error_message: str, **metadata) -> "ToolResult":
        """Create error result"""
        return cls(
            content=[ToolContent(type=ToolResultType.ERROR, text=error_message)],
            metadata=metadata
        )

    @classmethod
    def text(cls, text: str, **metadata) -> "ToolResult":
        """Create text result"""
        return cls(
            content=[ToolContent(type=ToolResultType.TEXT, text=text)],
            metadata=metadata
        )

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        return {
            "content": [c.to_dict() for c in self.content],
            "metadata": self.metadata
        }

    @property
    def type(self) -> str:
        """
        Get result type as string (for compatibility with task_command.py)

        Returns "success" if first content block is SUCCESS type, "error" otherwise
        """
        if not self.content:
            return "error"
        first_type = self.content[0].type
        if first_type == ToolResultType.SUCCESS:
            return "success"
        elif first_type == ToolResultType.ERROR:
            return "error"
        else:
            return "success"  # TEXT/IMAGE treated as success

    @property
    def error_text(self) -> Optional[str]:
        """Get error message if result is an error (for compatibility)"""
        if not self.content:
            return None
        first_content = self.content[0]
        if first_content.type == ToolResultType.ERROR:
            return first_content.text
        return None


@dataclass
class ToolParameter:
    """
    Tool parameter definition.

    Supports both simple types (str, int, bool) and Pydantic models.
    """
    name: str
    type: type
    description: Optional[str] = None
    required: bool = True
    default: Any = None

    def validate(self, value: Any) -> Any:
        """Validate and coerce value to correct type"""
        if value is None:
            if self.required and self.default is None:
                raise ValueError(f"Parameter '{self.name}' is required")
            return self.default

        # Try to coerce to correct type
        try:
            if self.type == bool and isinstance(value, str):
                return value.lower() in ('true', '1', 'yes')
            return self.type(value)
        except (ValueError, TypeError) as e:
            raise ValueError(f"Parameter '{self.name}' must be {self.type.__name__}: {e}")


@dataclass
class ToolSchema:
    """
    Tool schema definition.

    Defines parameters, validation, and type hints for a tool.
    """
    parameters: Dict[str, ToolParameter] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, schema: Dict[str, type]) -> "ToolSchema":
        """
        Create schema from simple dict.

        Example:
            {"name": str, "age": int, "active": bool}
        """
        parameters = {}
        for name, param_type in schema.items():
            parameters[name] = ToolParameter(
                name=name,
                type=param_type,
                required=True
            )
        return cls(parameters=parameters)

    @classmethod
    def from_function(cls, func: Callable) -> "ToolSchema":
        """
        Extract schema from function signature.

        Uses type hints to determine parameter types.
        """
        sig = inspect.signature(func)
        parameters = {}

        for param_name, param in sig.parameters.items():
            if param_name in ('self', 'cls', 'args', 'kwargs'):
                continue

            param_type = param.annotation if param.annotation != inspect.Parameter.empty else str
            has_default = param.default != inspect.Parameter.empty

            parameters[param_name] = ToolParameter(
                name=param_name,
                type=param_type,
                required=not has_default,
                default=param.default if has_default else None
            )

        return cls(parameters=parameters)

    def validate(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate arguments against schema.

        Returns validated and coerced arguments.
        """
        validated = {}

        for param_name, param in self.parameters.items():
            value = args.get(param_name)
            validated[param_name] = param.validate(value)

        # Check for unexpected arguments
        unexpected = set(args.keys()) - set(self.parameters.keys())
        if unexpected:
            raise ValueError(f"Unexpected arguments: {', '.join(unexpected)}")

        return validated


@dataclass
class ToolMetadata:
    """
    Tool registration metadata.

    Stores information about registered tools for discovery and execution.
    """
    name: str
    description: str
    schema: ToolSchema
    handler: Callable
    async_handler: bool = False
    tags: List[str] = field(default_factory=list)
    version: str = "1.0.0"
    created_at: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        return {
            "name": self.name,
            "description": self.description,
            "parameters": {
                name: {
                    "type": param.type.__name__,
                    "description": param.description,
                    "required": param.required,
                    "default": param.default
                }
                for name, param in self.schema.parameters.items()
            },
            "tags": self.tags,
            "version": self.version,
            "async": self.async_handler,
        }


# Type aliases for convenience
ToolHandler = Callable[[Dict[str, Any]], Union[ToolResult, Dict[str, Any]]]
AsyncToolHandler = Callable[[Dict[str, Any]], Union[ToolResult, Dict[str, Any]]]
