"""
MCP Types - Model Context Protocol type definitions

Based on official MCP Python SDK specification (2025).
Anthropic's open standard for AI context integration.

Biblical Foundation:
"Porque ninguém pode pôr outro fundamento além do que já está posto, o qual é Jesus Cristo" (1 Coríntios 3:11)
Solid foundation - standardized protocol for integration.
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Literal, Callable
from datetime import datetime
from enum import Enum


class MCPPrimitiveType(str, Enum):
    """
    MCP core primitives.

    Based on official MCP specification.
    """
    RESOURCE = "resource"  # Read-only data (like GET endpoints)
    TOOL = "tool"  # Executable functions (like POST endpoints)
    PROMPT = "prompt"  # Interaction templates


class MCPTransportType(str, Enum):
    """
    MCP transport protocols.

    Supported by official MCP Python SDK.
    """
    STDIO = "stdio"  # Standard I/O (direct process communication)
    SSE = "sse"  # Server-Sent Events (streaming)
    HTTP = "http"  # Streamable HTTP


@dataclass
class MCPResource:
    """
    MCP Resource - Read-only data exposed via URI.

    Similar to GET endpoints in REST APIs.

    Example:
        @mcp.resource("file://documents/{name}")
        def read_document(name: str) -> str:
            return f"Content of {name}"
    """
    uri: str  # Resource URI pattern (e.g., "file://documents/{name}")
    name: str  # Resource name
    description: Optional[str] = None
    mime_type: Optional[str] = "text/plain"
    handler: Optional[Callable] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to MCP protocol format"""
        return {
            "uri": self.uri,
            "name": self.name,
            "description": self.description,
            "mimeType": self.mime_type,
        }


@dataclass
class MCPTool:
    """
    MCP Tool - Executable function with side effects.

    Similar to POST endpoints in REST APIs.

    Example:
        @mcp.tool()
        def calculate(a: int, b: int) -> int:
            '''Add two numbers together.'''
            return a + b
    """
    name: str  # Tool name
    description: str  # Tool description
    input_schema: Dict[str, Any]  # JSON schema for parameters
    handler: Optional[Callable] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to MCP protocol format"""
        return {
            "name": self.name,
            "description": self.description,
            "inputSchema": self.input_schema,
        }


@dataclass
class MCPPrompt:
    """
    MCP Prompt - Reusable interaction template.

    Defines templated prompts for LLM conversations.

    Example:
        @mcp.prompt()
        def greet_user(name: str, style: str = "friendly") -> str:
            '''Generate a greeting prompt'''
            return f"Please write a {style} greeting for {name}."
    """
    name: str  # Prompt name
    description: str  # Prompt description
    arguments: List[Dict[str, Any]] = field(default_factory=list)
    handler: Optional[Callable] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to MCP protocol format"""
        return {
            "name": self.name,
            "description": self.description,
            "arguments": self.arguments,
        }


@dataclass
class MCPServerInfo:
    """
    MCP Server information.

    Metadata about MCP server capabilities.
    """
    name: str  # Server name
    version: str = "1.0.0"  # Server version
    protocol_version: str = "2024-11-05"  # MCP protocol version
    capabilities: Dict[str, bool] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to MCP protocol format"""
        return {
            "name": self.name,
            "version": self.version,
            "protocolVersion": self.protocol_version,
            "capabilities": self.capabilities,
        }


@dataclass
class MCPRequest:
    """
    MCP protocol request.

    Standardized request format.
    """
    method: str  # Request method (e.g., "tools/list", "resources/read")
    params: Dict[str, Any] = field(default_factory=dict)
    id: Optional[str] = None
    timestamp: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to MCP protocol format"""
        result = {
            "method": self.method,
            "params": self.params,
        }
        if self.id:
            result["id"] = self.id
        return result


@dataclass
class MCPResponse:
    """
    MCP protocol response.

    Standardized response format.
    """
    result: Optional[Any] = None
    error: Optional[Dict[str, Any]] = None
    id: Optional[str] = None

    @classmethod
    def success(cls, result: Any, id: Optional[str] = None) -> "MCPResponse":
        """Create success response"""
        return cls(result=result, id=id)

    @classmethod
    def error_response(
        cls, code: int, message: str, id: Optional[str] = None
    ) -> "MCPResponse":
        """Create error response"""
        return cls(
            error={"code": code, "message": message},
            id=id,
        )

    def to_dict(self) -> Dict[str, Any]:
        """Convert to MCP protocol format"""
        result = {}
        if self.result is not None:
            result["result"] = self.result
        if self.error is not None:
            result["error"] = self.error
        if self.id:
            result["id"] = self.id
        return result


@dataclass
class MCPContext:
    """
    MCP request context.

    Provides access to request-specific data.

    Example:
        @mcp.tool()
        async def task(ctx: MCPContext) -> str:
            await ctx.info("Starting task")
            await ctx.report_progress(0.5, 1.0)
            return "Done"
    """
    request_id: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    async def info(self, message: str):
        """Log info message"""
        # Implementation depends on server
        pass

    async def report_progress(self, progress: float, total: float = 1.0):
        """Report progress"""
        # Implementation depends on server
        pass


@dataclass
class MCPConfig:
    """
    MCP configuration.

    Settings for MCP server/client.
    """
    server_name: str = "max-code-mcp"
    version: str = "1.0.0"
    transport: MCPTransportType = MCPTransportType.STDIO

    # Server settings
    host: str = "localhost"
    port: int = 3000

    # Capabilities
    supports_resources: bool = True
    supports_tools: bool = True
    supports_prompts: bool = True

    # Timeouts
    request_timeout: float = 30.0
    connect_timeout: float = 10.0

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "server_name": self.server_name,
            "version": self.version,
            "transport": self.transport,
            "host": self.host,
            "port": self.port,
            "capabilities": {
                "resources": self.supports_resources,
                "tools": self.supports_tools,
                "prompts": self.supports_prompts,
            },
        }
