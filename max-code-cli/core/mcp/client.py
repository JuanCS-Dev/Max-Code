"""
MCP Client - Connect to MCP servers and consume resources/tools

Based on official MCP Python SDK client patterns.

Biblical Foundation:
"Porque onde estiverem dois ou três reunidos em meu nome, aí estou eu no meio deles" (Mateus 18:20)
Connection and unity - standardized integration.
"""

import asyncio
import logging
from typing import Any, Dict, List, Optional
from datetime import datetime

from .types import (
    MCPResource,
    MCPTool,
    MCPPrompt,
    MCPServerInfo,
    MCPRequest,
    MCPResponse,
    MCPConfig,
    MCPTransportType,
)

logger = logging.getLogger(__name__)


class MCPClientError(Exception):
    """Base exception for MCP client errors"""
    pass


class MCPConnectionError(MCPClientError):
    """Connection to MCP server failed"""
    pass


class MCPClient:
    """
    MCP Client - Connect to and consume MCP servers.

    Based on official MCP Python SDK client implementation.

    Example:
        client = MCPClient("http://localhost:3000")
        await client.connect()

        # List available tools
        tools = await client.list_tools()

        # Call a tool
        result = await client.call_tool("calculate", {"a": 2, "b": 3})

        await client.disconnect()
    """

    def __init__(
        self,
        server_url: str,
        config: Optional[MCPConfig] = None,
    ):
        """
        Initialize MCP client.

        Args:
            server_url: MCP server URL
            config: Optional configuration
        """
        self.server_url = server_url
        self.config = config or MCPConfig()

        # Connection state
        self._connected = False
        self._server_info: Optional[MCPServerInfo] = None

        # Discovered capabilities
        self._resources: Dict[str, MCPResource] = {}
        self._tools: Dict[str, MCPTool] = {}
        self._prompts: Dict[str, MCPPrompt] = {}

        # Request tracking
        self._request_id_counter = 0

        logger.info(f"MCPClient initialized: {server_url}")

    async def connect(self):
        """
        Connect to MCP server.

        Establishes connection and discovers capabilities.
        """
        if self._connected:
            logger.warning("Already connected")
            return

        try:
            logger.info(f"Connecting to MCP server: {self.server_url}")

            # Initialize connection (mock for now)
            # Real implementation would use HTTP/stdio/SSE transport
            await self._establish_connection()

            # Get server info
            self._server_info = await self._get_server_info()

            # Discover capabilities
            await self._discover_capabilities()

            self._connected = True
            logger.info(
                f"Connected to MCP server: {self._server_info.name} v{self._server_info.version}"
            )

        except Exception as e:
            logger.error(f"Connection failed: {e}", exc_info=True)
            raise MCPConnectionError(f"Failed to connect: {e}") from e

    async def disconnect(self):
        """Disconnect from MCP server"""
        if not self._connected:
            return

        self._connected = False
        logger.info("Disconnected from MCP server")

    def is_connected(self) -> bool:
        """Check if connected"""
        return self._connected

    async def list_resources(self) -> List[MCPResource]:
        """
        List available resources.

        Returns:
            List of MCP resources
        """
        self._check_connected()
        return list(self._resources.values())

    async def read_resource(self, uri: str) -> Any:
        """
        Read resource content.

        Args:
            uri: Resource URI

        Returns:
            Resource content
        """
        self._check_connected()

        request = MCPRequest(
            method="resources/read",
            params={"uri": uri},
            id=self._next_request_id(),
        )

        response = await self._send_request(request)

        if response.error:
            raise MCPClientError(
                f"Failed to read resource: {response.error['message']}"
            )

        return response.result

    async def list_tools(self) -> List[MCPTool]:
        """
        List available tools.

        Returns:
            List of MCP tools
        """
        self._check_connected()
        return list(self._tools.values())

    async def call_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Any:
        """
        Call MCP tool.

        Args:
            tool_name: Tool name
            arguments: Tool arguments

        Returns:
            Tool result
        """
        self._check_connected()

        if tool_name not in self._tools:
            raise MCPClientError(f"Tool not found: {tool_name}")

        request = MCPRequest(
            method="tools/call",
            params={"name": tool_name, "arguments": arguments},
            id=self._next_request_id(),
        )

        response = await self._send_request(request)

        if response.error:
            raise MCPClientError(f"Tool call failed: {response.error['message']}")

        return response.result

    async def list_prompts(self) -> List[MCPPrompt]:
        """
        List available prompts.

        Returns:
            List of MCP prompts
        """
        self._check_connected()
        return list(self._prompts.values())

    async def get_prompt(self, prompt_name: str, arguments: Dict[str, Any]) -> str:
        """
        Get prompt content.

        Args:
            prompt_name: Prompt name
            arguments: Prompt arguments

        Returns:
            Generated prompt text
        """
        self._check_connected()

        if prompt_name not in self._prompts:
            raise MCPClientError(f"Prompt not found: {prompt_name}")

        request = MCPRequest(
            method="prompts/get",
            params={"name": prompt_name, "arguments": arguments},
            id=self._next_request_id(),
        )

        response = await self._send_request(request)

        if response.error:
            raise MCPClientError(f"Get prompt failed: {response.error['message']}")

        return response.result

    def get_server_info(self) -> Optional[MCPServerInfo]:
        """Get server information"""
        return self._server_info

    # Private methods

    def _check_connected(self):
        """Check if connected, raise if not"""
        if not self._connected:
            raise MCPClientError("Not connected to server")

    def _next_request_id(self) -> str:
        """Generate next request ID"""
        self._request_id_counter += 1
        return f"req_{self._request_id_counter}"

    async def _establish_connection(self):
        """Establish connection to server"""
        # Mock implementation
        # Real implementation would use HTTP/stdio/SSE
        await asyncio.sleep(0.1)

    async def _get_server_info(self) -> MCPServerInfo:
        """Get server information"""
        # Mock implementation
        return MCPServerInfo(
            name="Mock MCP Server",
            version="1.0.0",
            protocol_version="2024-11-05",
            capabilities={
                "resources": True,
                "tools": True,
                "prompts": True,
            },
        )

    async def _discover_capabilities(self):
        """Discover server capabilities"""
        # Discover resources
        if self._server_info.capabilities.get("resources"):
            resources_response = await self._send_request(
                MCPRequest(method="resources/list", id=self._next_request_id())
            )
            if resources_response.result:
                for res_data in resources_response.result.get("resources", []):
                    resource = MCPResource(
                        uri=res_data["uri"],
                        name=res_data["name"],
                        description=res_data.get("description"),
                        mime_type=res_data.get("mimeType", "text/plain"),
                    )
                    self._resources[resource.uri] = resource

        # Discover tools
        if self._server_info.capabilities.get("tools"):
            tools_response = await self._send_request(
                MCPRequest(method="tools/list", id=self._next_request_id())
            )
            if tools_response.result:
                for tool_data in tools_response.result.get("tools", []):
                    tool = MCPTool(
                        name=tool_data["name"],
                        description=tool_data["description"],
                        input_schema=tool_data["inputSchema"],
                    )
                    self._tools[tool.name] = tool

        # Discover prompts
        if self._server_info.capabilities.get("prompts"):
            prompts_response = await self._send_request(
                MCPRequest(method="prompts/list", id=self._next_request_id())
            )
            if prompts_response.result:
                for prompt_data in prompts_response.result.get("prompts", []):
                    prompt = MCPPrompt(
                        name=prompt_data["name"],
                        description=prompt_data["description"],
                        arguments=prompt_data.get("arguments", []),
                    )
                    self._prompts[prompt.name] = prompt

        logger.info(
            f"Discovered: {len(self._resources)} resources, "
            f"{len(self._tools)} tools, {len(self._prompts)} prompts"
        )

    async def _send_request(self, request: MCPRequest) -> MCPResponse:
        """
        Send request to server.

        Args:
            request: MCP request

        Returns:
            MCP response
        """
        # Mock implementation
        # Real implementation would use HTTP/stdio/SSE transport

        logger.debug(f"Sending request: {request.method}")

        await asyncio.sleep(0.05)  # Simulate network delay

        # Mock responses based on method
        if request.method == "resources/list":
            return MCPResponse.success({
                "resources": [
                    {
                        "uri": "file://example.txt",
                        "name": "Example File",
                        "description": "An example text file",
                    }
                ]
            })

        elif request.method == "tools/list":
            return MCPResponse.success({
                "tools": [
                    {
                        "name": "calculate",
                        "description": "Add two numbers",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "a": {"type": "number"},
                                "b": {"type": "number"},
                            },
                            "required": ["a", "b"],
                        },
                    }
                ]
            })

        elif request.method == "prompts/list":
            return MCPResponse.success({
                "prompts": [
                    {
                        "name": "greet",
                        "description": "Generate greeting",
                        "arguments": [
                            {"name": "name", "description": "Person to greet"}
                        ],
                    }
                ]
            })

        elif request.method == "tools/call":
            tool_name = request.params.get("name")
            args = request.params.get("arguments", {})
            return MCPResponse.success({
                "content": [{"type": "text", "text": f"Mock result from {tool_name}"}]
            })

        elif request.method == "resources/read":
            uri = request.params.get("uri")
            return MCPResponse.success({
                "contents": [{"uri": uri, "mimeType": "text/plain", "text": "Mock content"}]
            })

        elif request.method == "prompts/get":
            prompt_name = request.params.get("name")
            return MCPResponse.success({
                "messages": [
                    {"role": "user", "content": {"type": "text", "text": f"Mock prompt: {prompt_name}"}}
                ]
            })

        else:
            return MCPResponse.error_response(
                code=-32601, message=f"Method not found: {request.method}"
            )

    def __repr__(self) -> str:
        status = "connected" if self._connected else "disconnected"
        return f"<MCPClient: {self.server_url} ({status})>"
