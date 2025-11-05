"""
Example: Model Context Protocol (MCP) - Anthropic's Open Standard

Demonstrates MCP integration following official MCP Python SDK patterns.

Features:
- MCP Server (expose resources, tools, prompts)
- MCP Client (connect and consume)
- Resource primitive (read-only data)
- Tool primitive (executable functions)
- Prompt primitive (interaction templates)

Run: python examples/mcp_example.py
"""

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, '.')

from core.mcp import (
    MCPServer,
    MCPClient,
    MCPConfig,
    MCPRequest,
    MCPResponse,
)


# ============================================================================
# EXAMPLE 1: Create MCP Server
# ============================================================================

def example_create_server():
    """Create MCP server with resources, tools, and prompts"""
    print("=" * 70)
    print("EXAMPLE 1: Create MCP Server")
    print("=" * 70)

    server = MCPServer("Example Server", version="1.0.0")

    # Register resource
    @server.resource("file://example.txt")
    def read_example():
        """Read example file"""
        return "This is example file content"

    # Register tool
    @server.tool()
    def calculate(a: int, b: int) -> int:
        """Add two numbers together"""
        return a + b

    # Register prompt
    @server.prompt()
    def greet(name: str, style: str = "friendly") -> str:
        """Generate a greeting prompt"""
        return f"Please write a {style} greeting for {name}."

    print(f"✅ MCP Server created: {server.name} v{server.version}")
    print(f"   - Resources: {len(server._resources)}")
    print(f"   - Tools: {len(server._tools)}")
    print(f"   - Prompts: {len(server._prompts)}")
    print()

    return server


# ============================================================================
# EXAMPLE 2: Server capabilities
# ============================================================================

async def example_server_capabilities(server: MCPServer):
    """Demonstrate server capabilities"""
    print("=" * 70)
    print("EXAMPLE 2: Server Capabilities")
    print("=" * 70)

    # List resources
    request = MCPRequest(method="resources/list", id="1")
    response = await server.handle_request(request)
    print(f"📁 Resources:")
    for res in response.result["resources"]:
        print(f"   - {res['uri']}: {res['description']}")

    # List tools
    request = MCPRequest(method="tools/list", id="2")
    response = await server.handle_request(request)
    print(f"\n🔧 Tools:")
    for tool in response.result["tools"]:
        print(f"   - {tool['name']}: {tool['description']}")

    # List prompts
    request = MCPRequest(method="prompts/list", id="3")
    response = await server.handle_request(request)
    print(f"\n💬 Prompts:")
    for prompt in response.result["prompts"]:
        print(f"   - {prompt['name']}: {prompt['description']}")

    print()


# ============================================================================
# EXAMPLE 3: Call tool
# ============================================================================

async def example_call_tool(server: MCPServer):
    """Call MCP tool"""
    print("=" * 70)
    print("EXAMPLE 3: Call Tool")
    print("=" * 70)

    request = MCPRequest(
        method="tools/call",
        params={"name": "calculate", "arguments": {"a": 5, "b": 3}},
        id="4",
    )

    response = await server.handle_request(request)

    if response.error:
        print(f"❌ Error: {response.error['message']}")
    else:
        result = response.result["content"][0]["text"]
        print(f"✅ Tool result: {result}")

    print()


# ============================================================================
# EXAMPLE 4: Read resource
# ============================================================================

async def example_read_resource(server: MCPServer):
    """Read MCP resource"""
    print("=" * 70)
    print("EXAMPLE 4: Read Resource")
    print("=" * 70)

    request = MCPRequest(
        method="resources/read",
        params={"uri": "file://example.txt"},
        id="5",
    )

    response = await server.handle_request(request)

    if response.error:
        print(f"❌ Error: {response.error['message']}")
    else:
        content = response.result["contents"][0]["text"]
        print(f"✅ Resource content: {content}")

    print()


# ============================================================================
# EXAMPLE 5: Get prompt
# ============================================================================

async def example_get_prompt(server: MCPServer):
    """Get MCP prompt"""
    print("=" * 70)
    print("EXAMPLE 5: Get Prompt")
    print("=" * 70)

    request = MCPRequest(
        method="prompts/get",
        params={"name": "greet", "arguments": {"name": "Alice", "style": "formal"}},
        id="6",
    )

    response = await server.handle_request(request)

    if response.error:
        print(f"❌ Error: {response.error['message']}")
    else:
        prompt_text = response.result["messages"][0]["content"]["text"]
        print(f"✅ Generated prompt: {prompt_text}")

    print()


# ============================================================================
# EXAMPLE 6: MCP Client
# ============================================================================

async def example_mcp_client():
    """Demonstrate MCP client"""
    print("=" * 70)
    print("EXAMPLE 6: MCP Client")
    print("=" * 70)

    client = MCPClient("http://localhost:3000")

    print("Connecting to MCP server...")
    await client.connect()

    print(f"✅ Connected to: {client.get_server_info().name}")
    print()

    # List resources
    resources = await client.list_resources()
    print(f"📁 Discovered resources: {len(resources)}")
    for res in resources:
        print(f"   - {res.uri}: {res.description}")

    # List tools
    tools = await client.list_tools()
    print(f"\n🔧 Discovered tools: {len(tools)}")
    for tool in tools:
        print(f"   - {tool.name}: {tool.description}")

    # List prompts
    prompts = await client.list_prompts()
    print(f"\n💬 Discovered prompts: {len(prompts)}")
    for prompt in prompts:
        print(f"   - {prompt.name}: {prompt.description}")

    await client.disconnect()
    print("\n✅ Disconnected")
    print()


# ============================================================================
# EXAMPLE 7: Client call tool
# ============================================================================

async def example_client_call_tool():
    """Client calls server tool"""
    print("=" * 70)
    print("EXAMPLE 7: Client Call Tool")
    print("=" * 70)

    client = MCPClient("http://localhost:3000")
    await client.connect()

    # Call tool
    result = await client.call_tool("calculate", {"a": 10, "b": 5})

    print(f"✅ Tool result: {result}")

    await client.disconnect()
    print()


# ============================================================================
# EXAMPLE 8: Client read resource
# ============================================================================

async def example_client_read_resource():
    """Client reads server resource"""
    print("=" * 70)
    print("EXAMPLE 8: Client Read Resource")
    print("=" * 70)

    client = MCPClient("http://localhost:3000")
    await client.connect()

    # Read resource
    content = await client.read_resource("file://example.txt")

    print(f"✅ Resource content:")
    print(f"   {content}")

    await client.disconnect()
    print()


# ============================================================================
# EXAMPLE 9: Multiple tools server
# ============================================================================

def example_multiple_tools():
    """Server with multiple tools"""
    print("=" * 70)
    print("EXAMPLE 9: Multiple Tools Server")
    print("=" * 70)

    server = MCPServer("Multi-Tool Server")

    @server.tool()
    def add(a: int, b: int) -> int:
        """Add two numbers"""
        return a + b

    @server.tool()
    def multiply(a: int, b: int) -> int:
        """Multiply two numbers"""
        return a * b

    @server.tool()
    def greet(name: str) -> str:
        """Greet someone"""
        return f"Hello, {name}!"

    @server.tool()
    def get_time() -> str:
        """Get current time"""
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    print(f"✅ Created server with {len(server._tools)} tools:")
    for tool_name in server._tools:
        print(f"   - {tool_name}")

    print()

    return server


# ============================================================================
# EXAMPLE 10: Server info and initialization
# ============================================================================

async def example_server_initialization():
    """Server initialization and info"""
    print("=" * 70)
    print("EXAMPLE 10: Server Initialization")
    print("=" * 70)

    server = MCPServer("Init Server", version="2.0.0")

    # Initialize request
    request = MCPRequest(method="initialize", id="init")
    response = await server.handle_request(request)

    info = response.result

    print(f"✅ Server Info:")
    print(f"   - Name: {info['name']}")
    print(f"   - Version: {info['version']}")
    print(f"   - Protocol: {info['protocolVersion']}")
    print(f"   - Capabilities:")
    for cap, enabled in info['capabilities'].items():
        status = "✅" if enabled else "❌"
        print(f"     {status} {cap}: {enabled}")

    print()


# ============================================================================
# MAIN: Run all examples
# ============================================================================

async def main():
    print("\n")
    print("╔" + "=" * 68 + "╗")
    print("║" + " " * 20 + "MCP EXAMPLES - FASE 2.5" + " " * 25 + "║")
    print("║" + " " * 10 + "Model Context Protocol - Anthropic Open Standard" + " " * 11 + "║")
    print("╚" + "=" * 68 + "╝")
    print("\n")

    # Run examples
    server = example_create_server()
    await example_server_capabilities(server)
    await example_call_tool(server)
    await example_read_resource(server)
    await example_get_prompt(server)
    await example_mcp_client()
    await example_client_call_tool()
    await example_client_read_resource()
    multi_server = example_multiple_tools()
    await example_server_initialization()

    print("=" * 70)
    print("✅ All examples completed successfully!")
    print("=" * 70)
    print()

    print("📊 SUMMARY:")
    print("   - MCP Server: Expose resources, tools, prompts")
    print("   - MCP Client: Connect and consume MCP servers")
    print("   - 3 Primitives: Resources, Tools, Prompts")
    print("   - Protocol-compliant: Official MCP spec (2024-11-05)")
    print("   - Transport-ready: stdio, SSE, HTTP support")
    print()

    print("🌐 Model Context Protocol:")
    print("   - Open standard by Anthropic (2024)")
    print("   - Adopted by OpenAI (March 2025)")
    print("   - Adopted by Google DeepMind (April 2025)")
    print("   - Industry-standard AI integration protocol")
    print()


if __name__ == "__main__":
    asyncio.run(main())
