"""
Model Context Protocol (MCP) - Anthropic's open standard for AI integration

Based on official MCP Python SDK specification (2025).
Standardized way to connect AI models to external systems.

Biblical Foundation:
"Porque ninguém pode pôr outro fundamento além do que já está posto, o qual é Jesus Cristo" (1 Coríntios 3:11)
Solid foundation - standardized protocol for integration.

Features:
- ✅ MCP Client (connect to MCP servers)
- ✅ MCP Server (expose resources, tools, prompts)
- ✅ Resource primitive (read-only data like GET)
- ✅ Tool primitive (executable functions like POST)
- ✅ Prompt primitive (interaction templates)
- ✅ Protocol-compliant request/response
- ✅ Transport abstraction (stdio, SSE, HTTP)

Example (Server):
    >>> from core.mcp import MCPServer
    >>>
    >>> server = MCPServer("My Server")
    >>>
    >>> @server.resource("file://{path}")
    >>> def read_file(path: str) -> str:
    ...     return f"Content of {path}"
    >>>
    >>> @server.tool()
    >>> def calculate(a: int, b: int) -> int:
    ...     '''Add two numbers'''
    ...     return a + b
    >>>
    >>> @server.prompt()
    >>> def greet(name: str) -> str:
    ...     return f"Please greet {name}"
    >>>
    >>> await server.serve()

Example (Client):
    >>> from core.mcp import MCPClient
    >>>
    >>> client = MCPClient("http://localhost:3000")
    >>> await client.connect()
    >>>
    >>> # List tools
    >>> tools = await client.list_tools()
    >>>
    >>> # Call tool
    >>> result = await client.call_tool("calculate", {"a": 2, "b": 3})
    >>>
    >>> await client.disconnect()
"""

from .types import (
    MCPPrimitiveType,
    MCPTransportType,
    MCPResource,
    MCPTool,
    MCPPrompt,
    MCPServerInfo,
    MCPRequest,
    MCPResponse,
    MCPContext,
    MCPConfig,
)

from .client import (
    MCPClient,
    MCPClientError,
    MCPConnectionError,
)

from .server import (
    MCPServer,
)

__all__ = [
    # Types
    'MCPPrimitiveType',
    'MCPTransportType',
    'MCPResource',
    'MCPTool',
    'MCPPrompt',
    'MCPServerInfo',
    'MCPRequest',
    'MCPResponse',
    'MCPContext',
    'MCPConfig',

    # Client
    'MCPClient',
    'MCPClientError',
    'MCPConnectionError',

    # Server
    'MCPServer',
]

__version__ = '2.0.0'  # FASE 2.5: MCP Integration
