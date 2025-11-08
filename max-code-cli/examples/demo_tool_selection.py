"""
Demo: Tool Registry & Smart Selection

Demonstrates intelligent tool selection without depending
on full registry initialization.

Run:
    python examples/demo_tool_selection.py

Biblical Foundation:
"Examinai tudo. Retende o bem" (1 Tessalonicenses 5:21)

Soli Deo Gloria
"""

from core.tools.tool_metadata import (
    EnhancedToolMetadata,
    ToolCategory,
    ToolCapabilities,
    ToolRequirements,
)
from core.tools.enhanced_registry import EnhancedToolRegistry
from core.tools.tool_selector import ToolSelector


def create_demo_tools():
    """Create demo tools for demonstration"""
    tools = [
        EnhancedToolMetadata(
            name="file_reader",
            description="Read file contents with line ranges and offsets",
            category=ToolCategory.FILE_OPS,
            capabilities=ToolCapabilities(can_read=True),
            requirements=ToolRequirements(requires_filepath=True),
            tags=["file", "read", "io"],
            parameters=[
                {"name": "path", "type": "string", "description": "File path", "required": True},
                {"name": "offset", "type": "number", "description": "Line offset", "required": False},
            ]
        ),
        EnhancedToolMetadata(
            name="file_writer",
            description="Write content to files with atomic operations",
            category=ToolCategory.FILE_OPS,
            capabilities=ToolCapabilities(can_write=True),
            requirements=ToolRequirements(requires_filepath=True, requires_content=True),
            tags=["file", "write", "create", "io"],
            parameters=[
                {"name": "path", "type": "string", "description": "File path", "required": True},
                {"name": "content", "type": "string", "description": "File content", "required": True},
            ]
        ),
        EnhancedToolMetadata(
            name="file_editor",
            description="Edit files with exact string replacements",
            category=ToolCategory.FILE_OPS,
            capabilities=ToolCapabilities(can_write=True),
            requirements=ToolRequirements(requires_filepath=True, requires_content=True),
            tags=["file", "edit", "modify", "io"],
            parameters=[
                {"name": "path", "type": "string", "description": "File path", "required": True},
                {"name": "old_string", "type": "string", "description": "String to replace", "required": True},
                {"name": "new_string", "type": "string", "description": "Replacement string", "required": True},
            ]
        ),
        EnhancedToolMetadata(
            name="glob_tool",
            description="Find files matching glob patterns",
            category=ToolCategory.SEARCH,
            capabilities=ToolCapabilities(can_search=True),
            requirements=ToolRequirements(requires_pattern=True),
            tags=["search", "find", "pattern", "glob"],
            parameters=[
                {"name": "pattern", "type": "string", "description": "Glob pattern", "required": True},
                {"name": "path", "type": "string", "description": "Search path", "required": False},
            ]
        ),
        EnhancedToolMetadata(
            name="grep_tool",
            description="Search file contents using regex patterns",
            category=ToolCategory.SEARCH,
            capabilities=ToolCapabilities(can_search=True, can_read=True),
            requirements=ToolRequirements(requires_pattern=True),
            tags=["search", "grep", "regex", "content"],
            parameters=[
                {"name": "pattern", "type": "string", "description": "Regex pattern", "required": True},
                {"name": "path", "type": "string", "description": "Search path", "required": False},
            ]
        ),
    ]
    
    return tools


def demo_basic_selection():
    """Demo: Basic tool selection"""
    print("=" * 70)
    print("DEMO 1: Basic Tool Selection")
    print("=" * 70)
    
    # Create registry and register tools
    registry = EnhancedToolRegistry()
    for tool in create_demo_tools():
        registry.register_enhanced(tool)
    
    print(f"\nRegistered {len(registry.enhanced_tools)} tools")
    
    # Test 1: Select read tool
    print("\n--- Test 1: Read task ---")
    tool = registry.select_best_tool(
        "Read the config file",
        {"needs_read": True, "has_filepath": True},
        use_llm=False
    )
    print(f"Selected: {tool.name if tool else 'None'}")
    print(f"Capabilities: read={tool.capabilities.can_read if tool else 'N/A'}")
    
    # Test 2: Select search tool
    print("\n--- Test 2: Search task ---")
    tool = registry.select_best_tool(
        "Find all TODO comments",
        {"needs_search": True, "has_pattern": True},
        use_llm=False
    )
    print(f"Selected: {tool.name if tool else 'None'}")
    print(f"Capabilities: search={tool.capabilities.can_search if tool else 'N/A'}")


def demo_requirement_inference():
    """Demo: Requirement inference from descriptions"""
    print("\n" + "=" * 70)
    print("DEMO 2: Requirement Inference")
    print("=" * 70)
    
    selector = ToolSelector()
    
    # Register demo tools
    registry = EnhancedToolRegistry()
    for tool in create_demo_tools():
        registry.register_enhanced(tool)
    
    test_cases = [
        "Read the config.json file",
        "Create a new file called output.txt",
        'Find all "TODO" comments in src/',
        "Search for function definitions matching pattern",
    ]
    
    for description in test_cases:
        print(f"\nTask: {description}")
        reqs = selector.infer_requirements(description)
        print(f"Inferred requirements:")
        for key, value in reqs.items():
            if value and key != 'tags':
                print(f"  - {key}: {value}")
        if reqs.get('tags'):
            print(f"  - tags: {', '.join(reqs['tags'])}")


def demo_scoring():
    """Demo: Tool scoring"""
    print("\n" + "=" * 70)
    print("DEMO 3: Tool Scoring")
    print("=" * 70)
    
    # Create tools
    tools = create_demo_tools()
    
    # Requirements for reading
    requirements = {
        "needs_read": True,
        "has_filepath": True,
        "tags": ["file", "read"]
    }
    
    print(f"\nRequirements: {requirements}")
    print(f"\nTool Scores:")
    
    for tool in tools:
        score = tool.matches_requirements(requirements)
        print(f"  {tool.name:20s}: {score:.2f}")


def demo_anthropic_schema():
    """Demo: Anthropic schema generation"""
    print("\n" + "=" * 70)
    print("DEMO 4: Anthropic Schema Generation")
    print("=" * 70)
    
    # Get file_reader tool
    tool = create_demo_tools()[0]  # file_reader
    
    print(f"\nTool: {tool.name}")
    print(f"Description: {tool.description}")
    
    schema = tool.to_anthropic_schema()
    
    print(f"\nAnthrop schema:")
    import json
    print(json.dumps(schema, indent=2))


def main():
    """Run all demos"""
    print("\n")
    print("╔" + "=" * 68 + "╗")
    print("║" + " " * 15 + "TOOL REGISTRY & SMART SELECTION" + " " * 22 + "║")
    print("║" + " " * 27 + "DEMONSTRATION" + " " * 28 + "║")
    print("╚" + "=" * 68 + "╝")
    
    demo_basic_selection()
    demo_requirement_inference()
    demo_scoring()
    demo_anthropic_schema()
    
    print("\n" + "=" * 70)
    print("✅ ALL DEMOS COMPLETE")
    print("=" * 70)
    print("\nSoli Deo Gloria 🙏\n")


if __name__ == "__main__":
    main()
