"""
MCP Server - Expose resources, tools, and prompts

Based on official MCP Python SDK FastMCP pattern.

Biblical Foundation:
"Cada um administre aos outros o dom como o recebeu" (1 Pedro 4:10)
Serve others - expose capabilities for shared benefit.
"""

import logging
import inspect
from typing import Any, Dict, List, Optional, Callable
from datetime import datetime

from .types import (
    MCPResource,
    MCPTool,
    MCPPrompt,
    MCPServerInfo,
    MCPRequest,
    MCPResponse,
    MCPConfig,
    MCPContext,
)

logger = logging.getLogger(__name__)


class MCPServer:
    """
    MCP Server - Expose resources, tools, and prompts.

    Based on official MCP Python SDK FastMCP implementation.

    Example:
        server = MCPServer("My Server")

        @server.resource("file://{path}")
        def read_file(path: str) -> str:
            return f"Content of {path}"

        @server.tool()
        def calculate(a: int, b: int) -> int:
            '''Add two numbers'''
            return a + b

        @server.prompt()
        def greet(name: str) -> str:
            return f"Please greet {name}"

        await server.serve()
    """

    def __init__(
        self,
        name: str,
        version: str = "1.0.0",
        config: Optional[MCPConfig] = None,
    ):
        """
        Initialize MCP server.

        Args:
            name: Server name
            version: Server version
            config: Optional configuration
        """
        self.name = name
        self.version = version
        self.config = config or MCPConfig()

        # Server info
        self.info = MCPServerInfo(
            name=name,
            version=version,
            capabilities={
                "resources": True,
                "tools": True,
                "prompts": True,
            },
        )

        # Registered capabilities
        self._resources: Dict[str, MCPResource] = {}
        self._tools: Dict[str, MCPTool] = {}
        self._prompts: Dict[str, MCPPrompt] = {}

        # Server state
        self._running = False

        logger.info(f"MCPServer initialized: {name} v{version}")

    def resource(self, uri: str, description: Optional[str] = None):
        """
        Register resource decorator.

        Example:
            @server.resource("file://{path}")
            def read_file(path: str) -> str:
                return f"Content of {path}"

        Args:
            uri: Resource URI pattern
            description: Resource description
        """

        def decorator(func: Callable) -> Callable:
            # Extract function metadata
            func_name = func.__name__
            func_doc = description or func.__doc__ or f"Resource: {func_name}"

            # Create resource
            resource = MCPResource(
                uri=uri,
                name=func_name,
                description=func_doc,
                handler=func,
            )

            self._resources[uri] = resource
            logger.debug(f"Registered resource: {uri}")

            return func

        return decorator

    def tool(self, description: Optional[str] = None):
        """
        Register tool decorator.

        Example:
            @server.tool()
            def calculate(a: int, b: int) -> int:
                '''Add two numbers together.'''
                return a + b

        Args:
            description: Tool description
        """

        def decorator(func: Callable) -> Callable:
            # Extract function metadata
            func_name = func.__name__
            func_doc = description or func.__doc__ or f"Tool: {func_name}"

            # Build input schema from function signature
            input_schema = self._build_input_schema(func)

            # Create tool
            tool = MCPTool(
                name=func_name,
                description=func_doc,
                input_schema=input_schema,
                handler=func,
            )

            self._tools[func_name] = tool
            logger.debug(f"Registered tool: {func_name}")

            return func

        return decorator

    def prompt(self, description: Optional[str] = None):
        """
        Register prompt decorator.

        Example:
            @server.prompt()
            def greet_user(name: str, style: str = "friendly") -> str:
                '''Generate a greeting prompt'''
                return f"Please write a {style} greeting for {name}."

        Args:
            description: Prompt description
        """

        def decorator(func: Callable) -> Callable:
            # Extract function metadata
            func_name = func.__name__
            func_doc = description or func.__doc__ or f"Prompt: {func_name}"

            # Build arguments from function signature
            arguments = self._build_prompt_arguments(func)

            # Create prompt
            prompt = MCPPrompt(
                name=func_name,
                description=func_doc,
                arguments=arguments,
                handler=func,
            )

            self._prompts[func_name] = prompt
            logger.debug(f"Registered prompt: {func_name}")

            return func

        return decorator

    async def handle_request(self, request: MCPRequest) -> MCPResponse:
        """
        Handle MCP request.

        Args:
            request: MCP request

        Returns:
            MCP response
        """
        logger.debug(f"Handling request: {request.method}")

        try:
            # Route based on method
            if request.method == "initialize":
                return self._handle_initialize(request)

            elif request.method == "resources/list":
                return self._handle_list_resources(request)

            elif request.method == "resources/read":
                return await self._handle_read_resource(request)

            elif request.method == "tools/list":
                return self._handle_list_tools(request)

            elif request.method == "tools/call":
                return await self._handle_call_tool(request)

            elif request.method == "prompts/list":
                return self._handle_list_prompts(request)

            elif request.method == "prompts/get":
                return await self._handle_get_prompt(request)

            else:
                return MCPResponse.error_response(
                    code=-32601,
                    message=f"Method not found: {request.method}",
                    id=request.id,
                )

        except Exception as e:
            logger.error(f"Request handler error: {e}", exc_info=True)
            return MCPResponse.error_response(
                code=-32603, message=str(e), id=request.id
            )

    async def serve(self, port: Optional[int] = None):
        """
        Start MCP server.

        Args:
            port: Optional port (default from config)
        """
        port = port or self.config.port

        self._running = True
        logger.info(f"MCP server started: {self.name} on port {port}")

        # Mock serve implementation
        # Real implementation would use HTTP/stdio/SSE transport
        logger.info("Server ready to handle requests")

    def stop(self):
        """Stop MCP server"""
        self._running = False
        logger.info("MCP server stopped")

    def is_running(self) -> bool:
        """Check if server is running"""
        return self._running

    # Request handlers

    def _handle_initialize(self, request: MCPRequest) -> MCPResponse:
        """Handle initialize request"""
        return MCPResponse.success(
            result=self.info.to_dict(),
            id=request.id,
        )

    def _handle_list_resources(self, request: MCPRequest) -> MCPResponse:
        """Handle list resources request"""
        resources = [res.to_dict() for res in self._resources.values()]
        return MCPResponse.success(
            result={"resources": resources},
            id=request.id,
        )

    async def _handle_read_resource(self, request: MCPRequest) -> MCPResponse:
        """Handle read resource request"""
        uri = request.params.get("uri")

        if uri not in self._resources:
            return MCPResponse.error_response(
                code=-32602,
                message=f"Resource not found: {uri}",
                id=request.id,
            )

        resource = self._resources[uri]

        # Call handler
        try:
            # Extract path parameters from URI
            # Simplified: real implementation would parse URI pattern
            content = resource.handler()

            return MCPResponse.success(
                result={
                    "contents": [
                        {
                            "uri": uri,
                            "mimeType": resource.mime_type,
                            "text": content,
                        }
                    ]
                },
                id=request.id,
            )

        except Exception as e:
            logger.error(f"Resource handler error: {e}", exc_info=True)
            return MCPResponse.error_response(
                code=-32603, message=str(e), id=request.id
            )

    def _handle_list_tools(self, request: MCPRequest) -> MCPResponse:
        """Handle list tools request"""
        tools = [tool.to_dict() for tool in self._tools.values()]
        return MCPResponse.success(
            result={"tools": tools},
            id=request.id,
        )

    async def _handle_call_tool(self, request: MCPRequest) -> MCPResponse:
        """Handle call tool request"""
        tool_name = request.params.get("name")
        arguments = request.params.get("arguments", {})

        if tool_name not in self._tools:
            return MCPResponse.error_response(
                code=-32602,
                message=f"Tool not found: {tool_name}",
                id=request.id,
            )

        tool = self._tools[tool_name]

        # Call handler
        try:
            if inspect.iscoroutinefunction(tool.handler):
                result = await tool.handler(**arguments)
            else:
                result = tool.handler(**arguments)

            return MCPResponse.success(
                result={
                    "content": [
                        {"type": "text", "text": str(result)}
                    ]
                },
                id=request.id,
            )

        except Exception as e:
            logger.error(f"Tool handler error: {e}", exc_info=True)
            return MCPResponse.error_response(
                code=-32603, message=str(e), id=request.id
            )

    def _handle_list_prompts(self, request: MCPRequest) -> MCPResponse:
        """Handle list prompts request"""
        prompts = [prompt.to_dict() for prompt in self._prompts.values()]
        return MCPResponse.success(
            result={"prompts": prompts},
            id=request.id,
        )

    async def _handle_get_prompt(self, request: MCPRequest) -> MCPResponse:
        """Handle get prompt request"""
        prompt_name = request.params.get("name")
        arguments = request.params.get("arguments", {})

        if prompt_name not in self._prompts:
            return MCPResponse.error_response(
                code=-32602,
                message=f"Prompt not found: {prompt_name}",
                id=request.id,
            )

        prompt = self._prompts[prompt_name]

        # Call handler
        try:
            if inspect.iscoroutinefunction(prompt.handler):
                result = await prompt.handler(**arguments)
            else:
                result = prompt.handler(**arguments)

            return MCPResponse.success(
                result={
                    "messages": [
                        {
                            "role": "user",
                            "content": {"type": "text", "text": result},
                        }
                    ]
                },
                id=request.id,
            )

        except Exception as e:
            logger.error(f"Prompt handler error: {e}", exc_info=True)
            return MCPResponse.error_response(
                code=-32603, message=str(e), id=request.id
            )

    # Helper methods

    def _build_input_schema(self, func: Callable) -> Dict[str, Any]:
        """
        Build JSON schema from function signature.

        Args:
            func: Function to analyze

        Returns:
            JSON schema for parameters
        """
        sig = inspect.signature(func)
        properties = {}
        required = []

        for param_name, param in sig.parameters.items():
            # Skip context parameter
            if param_name == "ctx":
                continue

            # Get type annotation
            param_type = param.annotation
            if param_type == inspect.Parameter.empty:
                param_type = str

            # Map Python type to JSON schema type
            json_type = self._python_type_to_json_type(param_type)

            properties[param_name] = {"type": json_type}

            # Check if required (no default value)
            if param.default == inspect.Parameter.empty:
                required.append(param_name)

        return {
            "type": "object",
            "properties": properties,
            "required": required,
        }

    def _build_prompt_arguments(self, func: Callable) -> List[Dict[str, Any]]:
        """
        Build prompt arguments from function signature.

        Args:
            func: Function to analyze

        Returns:
            List of argument definitions
        """
        sig = inspect.signature(func)
        arguments = []

        for param_name, param in sig.parameters.items():
            argument = {
                "name": param_name,
                "description": f"Parameter: {param_name}",
                "required": param.default == inspect.Parameter.empty,
            }
            arguments.append(argument)

        return arguments

    def _python_type_to_json_type(self, python_type: type) -> str:
        """Map Python type to JSON schema type"""
        type_mapping = {
            int: "number",
            float: "number",
            str: "string",
            bool: "boolean",
            list: "array",
            dict: "object",
        }

        return type_mapping.get(python_type, "string")

    def __repr__(self) -> str:
        status = "running" if self._running else "stopped"
        return (
            f"<MCPServer: {self.name} v{self.version} ({status}), "
            f"{len(self._resources)} resources, {len(self._tools)} tools, "
            f"{len(self._prompts)} prompts>"
        )
