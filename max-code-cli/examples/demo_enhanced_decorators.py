"""
Demo: Enhanced Tool Decorators v2.0

Demonstrates the new enhanced decorators with rich metadata
for intelligent tool selection.

Run:
    python examples/demo_enhanced_decorators.py

Biblical Foundation:
"O que trabalha com mão remissa empobrece, mas a mão dos diligentes enriquece" (Provérbios 10:4)

Soli Deo Gloria
"""

import asyncio
from core.tools.decorator import (
    enhanced_tool,
    quick_tool,
    search_tool,
    write_tool,
    execute_tool,
)
from core.tools.tool_metadata import ToolCategory
from core.tools.types import ToolResult
from core.tools.enhanced_registry import get_enhanced_registry


# ============================================================================
# Example 1: Basic @enhanced_tool
# ============================================================================

@enhanced_tool(
    name="read_config",
    description="Read configuration file",
    category=ToolCategory.FILE_OPS,
    can_read=True,
    requires_filepath=True,
    safe=True,
    tags=["config", "read", "io"],
    examples=[
        {"input": {"filepath": "config.json"}, "output": "{...config data...}"}
    ]
)
def read_config(filepath: str) -> ToolResult:
    """Read and parse configuration file"""
    try:
        with open(filepath, 'r') as f:
            content = f.read()
        return ToolResult.success(f"Read {len(content)} bytes from {filepath}")
    except FileNotFoundError:
        return ToolResult.error(f"File not found: {filepath}")


# ============================================================================
# Example 2: @quick_tool for simple operations
# ============================================================================

@quick_tool("list_files", "List files in directory")
def list_files(directory: str = ".") -> ToolResult:
    """List all files in a directory"""
    import os
    try:
        files = os.listdir(directory)
        return ToolResult.success(f"Found {len(files)} files in {directory}")
    except Exception as e:
        return ToolResult.error(str(e))


# ============================================================================
# Example 3: @search_tool for search operations
# ============================================================================

@search_tool(
    name="grep_pattern",
    description="Search for pattern in files",
    tags=["grep", "search", "regex"]
)
def grep_pattern(pattern: str, directory: str = ".") -> ToolResult:
    """Search for pattern in files"""
    import os
    import re
    
    matches = []
    try:
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith('.py'):
                    filepath = os.path.join(root, file)
                    try:
                        with open(filepath, 'r') as f:
                            for line_num, line in enumerate(f, 1):
                                if re.search(pattern, line):
                                    matches.append(f"{filepath}:{line_num}: {line.strip()}")
                    except:
                        pass
        
        return ToolResult.success(f"Found {len(matches)} matches")
    except Exception as e:
        return ToolResult.error(str(e))


# ============================================================================
# Example 4: @write_tool for write operations
# ============================================================================

@write_tool(
    name="create_file",
    description="Create new file with content"
)
def create_file(filepath: str, content: str) -> ToolResult:
    """Create a new file"""
    try:
        with open(filepath, 'w') as f:
            f.write(content)
        return ToolResult.success(f"Created {filepath} with {len(content)} bytes")
    except Exception as e:
        return ToolResult.error(str(e))


# ============================================================================
# Example 5: @execute_tool for command execution
# ============================================================================

@execute_tool(
    name="run_command",
    description="Execute shell command"
)
async def run_command(command: str) -> ToolResult:
    """Execute a shell command"""
    import subprocess
    
    try:
        # Security: This is a demo/example tool
        # In production, implement proper command sanitization
        result = subprocess.run(
            command,
            shell=True,  # nosec B602
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode == 0:
            return ToolResult.success(f"Command output:\n{result.stdout}")
        else:
            return ToolResult.error(f"Command failed:\n{result.stderr}")
    except subprocess.TimeoutExpired:
        return ToolResult.error("Command timed out")
    except Exception as e:
        return ToolResult.error(str(e))


# ============================================================================
# Example 6: Complex tool with all features
# ============================================================================

@enhanced_tool(
    name="analyze_code",
    description="Analyze Python code for complexity",
    category=ToolCategory.ANALYSIS,
    can_read=True,
    can_analyze=True,
    requires_filepath=True,
    safe=True,
    expensive=False,
    estimated_time=3,
    tags=["analysis", "code", "complexity", "python"],
    examples=[
        {
            "input": {"filepath": "main.py"},
            "output": "Complexity: 5, Lines: 100, Functions: 8"
        }
    ]
)
def analyze_code(filepath: str) -> ToolResult:
    """Analyze Python code complexity"""
    import os
    
    try:
        with open(filepath, 'r') as f:
            lines = f.readlines()
        
        # Simple analysis
        total_lines = len(lines)
        functions = sum(1 for line in lines if line.strip().startswith('def '))
        classes = sum(1 for line in lines if line.strip().startswith('class '))
        imports = sum(1 for line in lines if 'import ' in line)
        
        analysis = f"""
Analysis of {filepath}:
- Total lines: {total_lines}
- Functions: {functions}
- Classes: {classes}
- Imports: {imports}
- Size: {os.path.getsize(filepath)} bytes
"""
        return ToolResult.success(analysis.strip())
    
    except Exception as e:
        return ToolResult.error(str(e))


# ============================================================================
# Demonstration Functions
# ============================================================================

def demo_basic_usage():
    """Demo: Basic tool usage"""
    print("=" * 70)
    print("DEMO 1: Basic Tool Usage")
    print("=" * 70)
    
    # Test read_config
    print("\n--- Testing read_config ---")
    result = read_config({"filepath": "README.md"})
    print(f"Result: {result.content[0].text}")
    
    # Test list_files
    print("\n--- Testing list_files ---")
    result = list_files({"directory": "examples"})
    print(f"Result: {result.content[0].text}")


def demo_search_tool():
    """Demo: Search tool"""
    print("\n" + "=" * 70)
    print("DEMO 2: Search Tool")
    print("=" * 70)
    
    print("\n--- Searching for 'def ' pattern ---")
    result = grep_pattern({"pattern": "def ", "directory": "core/tools"})
    print(f"Result: {result.content[0].text}")


async def demo_async_tool():
    """Demo: Async tool execution"""
    print("\n" + "=" * 70)
    print("DEMO 3: Async Tool Execution")
    print("=" * 70)
    
    print("\n--- Running command: 'echo Hello World' ---")
    result = await run_command({"command": "echo 'Hello from enhanced tool!'"})
    print(f"Result: {result.content[0].text}")


def demo_registry_integration():
    """Demo: Registry integration"""
    print("\n" + "=" * 70)
    print("DEMO 4: Registry Integration")
    print("=" * 70)
    
    registry = get_enhanced_registry()
    
    print("\n--- Registered Tools ---")
    tools = registry.list_tools()
    
    # Find our decorated tools
    our_tools = [t for t in tools if t.name in [
        'read_config', 'list_files', 'grep_pattern',
        'create_file', 'run_command', 'analyze_code'
    ]]
    
    for tool in our_tools:
        print(f"\n{tool.name}:")
        print(f"  Category: {tool.category.value}")
        print(f"  Capabilities: read={tool.capabilities.can_read}, "
              f"write={tool.capabilities.can_write}, "
              f"search={tool.capabilities.can_search}")
        print(f"  Safe: {tool.performance.safe}")
        print(f"  Tags: {', '.join(tool.tags)}")


def demo_metadata_inspection():
    """Demo: Inspect tool metadata"""
    print("\n" + "=" * 70)
    print("DEMO 5: Metadata Inspection")
    print("=" * 70)
    
    print("\n--- Analyzing 'analyze_code' tool ---")
    metadata = analyze_code._tool_enhanced_metadata
    
    print(f"Name: {metadata.name}")
    print(f"Description: {metadata.description}")
    print(f"Category: {metadata.category.value}")
    print(f"\nCapabilities:")
    print(f"  can_read: {metadata.capabilities.can_read}")
    print(f"  can_analyze: {metadata.capabilities.can_analyze}")
    print(f"\nRequirements:")
    print(f"  requires_filepath: {metadata.requirements.requires_filepath}")
    print(f"\nPerformance:")
    print(f"  safe: {metadata.performance.safe}")
    print(f"  expensive: {metadata.performance.expensive}")
    print(f"  estimated_time: {metadata.performance.estimated_time}s")
    print(f"\nParameters:")
    for param in metadata.parameters:
        print(f"  - {param['name']}: {param['type']} (required: {param['required']})")
    print(f"\nTags: {', '.join(metadata.tags)}")


def demo_smart_selection():
    """Demo: Smart tool selection based on metadata"""
    print("\n" + "=" * 70)
    print("DEMO 6: Smart Tool Selection")
    print("=" * 70)
    
    registry = get_enhanced_registry()
    
    # Select tool for reading
    print("\n--- Task: Read a file ---")
    requirements = {
        'needs_read': True,
        'has_filepath': True
    }
    tool = registry.select_best_tool("Read the config file", requirements)
    if tool:
        print(f"Selected: {tool.name}")
        print(f"  Reason: Can read files, requires filepath")
    
    # Select tool for searching
    print("\n--- Task: Search for pattern ---")
    requirements = {
        'needs_search': True,
        'has_pattern': True
    }
    tool = registry.select_best_tool("Find all TODO comments", requirements)
    if tool:
        print(f"Selected: {tool.name}")
        print(f"  Reason: Can search, requires pattern")


def main():
    """Run all demos"""
    print("\n")
    print("╔" + "=" * 68 + "╗")
    print("║" + " " * 15 + "ENHANCED TOOL DECORATORS v2.0" + " " * 24 + "║")
    print("║" + " " * 22 + "WORLD-CLASS QUALITY" + " " * 27 + "║")
    print("╚" + "=" * 68 + "╝")
    
    demo_basic_usage()
    demo_search_tool()
    asyncio.run(demo_async_tool())
    demo_registry_integration()
    demo_metadata_inspection()
    demo_smart_selection()
    
    print("\n" + "=" * 70)
    print("✅ ALL DEMOS COMPLETE")
    print("=" * 70)
    print("\nKey Features Demonstrated:")
    print("  ✓ @enhanced_tool with rich metadata")
    print("  ✓ @quick_tool for simple operations")
    print("  ✓ @search_tool, @write_tool, @execute_tool specializations")
    print("  ✓ Automatic parameter extraction")
    print("  ✓ Sync and async support")
    print("  ✓ Registry integration")
    print("  ✓ Smart tool selection")
    print("\nSoli Deo Gloria 🙏\n")


if __name__ == "__main__":
    main()
