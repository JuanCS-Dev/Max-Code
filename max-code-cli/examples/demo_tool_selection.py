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


def demo_batch_selection():
    """Demo: Batch tool selection (NEW in v3.0)"""
    print("\n" + "=" * 70)
    print("DEMO 5: Batch Tool Selection (NEW)")
    print("=" * 70)
    
    try:
        from core.task_models import Task, TaskType, TaskRequirement
        import asyncio
        
        selector = ToolSelector()
        
        # Register demo tools
        registry = EnhancedToolRegistry()
        for tool in create_demo_tools():
            registry.register_enhanced(tool)
        
        # Create multiple tasks
        tasks = [
            Task(
                id="task_1",
                description="Read the config.json file",
                type=TaskType.READ,
                requirements=TaskRequirement(
                    agent_type="code",
                    inputs={"file_path": "config.json"}
                )
            ),
            Task(
                id="task_2",
                description="Search for TODO comments in src/",
                type=TaskType.READ,
                requirements=TaskRequirement(
                    agent_type="code",
                    inputs={"pattern": "TODO", "directory": "src/"}
                )
            ),
            Task(
                id="task_3",
                description="Create output.txt file",
                type=TaskType.WRITE,
                requirements=TaskRequirement(
                    agent_type="code",
                    inputs={"file_path": "output.txt", "content": "test"}
                )
            ),
        ]
        
        print(f"\nSelecting tools for {len(tasks)} tasks...")
        
        # Run async batch selection (fallback mode, no API key needed)
        async def run_batch():
            return await selector.select_tools_for_tasks(tasks, batch_mode=False)
        
        selections = asyncio.run(run_batch())
        
        print(f"\nSelected {len(selections)} tools:")
        for task_id, tool in selections.items():
            print(f"  {task_id}: {tool.name} ({tool.category.value})")
    
    except ImportError:
        print("\n⚠️  Task models not available. Skipping batch selection demo.")


def demo_tool_validation():
    """Demo: Tool validation (NEW in v3.0)"""
    print("\n" + "=" * 70)
    print("DEMO 6: Tool Validation (NEW)")
    print("=" * 70)
    
    try:
        from core.task_models import Task, TaskType, TaskRequirement
        
        selector = ToolSelector()
        
        # Register demo tools
        registry = EnhancedToolRegistry()
        for tool in create_demo_tools():
            registry.register_enhanced(tool)
        
        # Create task
        task = Task(
            id="task_1",
            description="Read config.json",
            type=TaskType.READ,
            requirements=TaskRequirement(
                agent_type="code",
                tools=["file_reader"],
                inputs={"path": "config.json"}  # Using 'path' parameter
            )
        )
        
        # Get tool
        tool = registry.get_tool("file_reader")
        
        print(f"\nValidating tool '{tool.name}' for task...")
        
        # Validate
        valid, issues = selector.validate_tool_for_task(tool, task, strict=False)
        
        if valid:
            print("✅ Validation PASSED")
        else:
            print("❌ Validation FAILED")
            for issue in issues:
                print(f"   - {issue}")
    
    except ImportError:
        print("\n⚠️  Task models not available. Skipping validation demo.")


def demo_alternative_suggestions():
    """Demo: Alternative tool suggestions (NEW in v3.0)"""
    print("\n" + "=" * 70)
    print("DEMO 7: Alternative Tool Suggestions (NEW)")
    print("=" * 70)
    
    try:
        from core.task_models import Task, TaskType, TaskRequirement
        import asyncio
        
        selector = ToolSelector()
        
        # Register demo tools
        registry = EnhancedToolRegistry()
        for tool in create_demo_tools():
            registry.register_enhanced(tool)
        
        # Create task
        task = Task(
            id="task_1",
            description="Search for patterns in files",
            type=TaskType.READ,
            requirements=TaskRequirement(
                agent_type="code",
                inputs={"pattern": "TODO"}
            )
        )
        
        # Primary tool (pretend it failed)
        primary_tool = registry.get_tool("grep_tool")
        
        print(f"\nPrimary tool '{primary_tool.name}' failed.")
        print(f"Suggesting alternatives...")
        
        # Get alternatives
        async def run_suggest():
            return await selector.suggest_alternative_tools(
                task, primary_tool, count=2
            )
        
        alternatives = asyncio.run(run_suggest())
        
        if alternatives:
            print(f"\n✅ Found {len(alternatives)} alternatives:")
            for i, alt in enumerate(alternatives, 1):
                print(f"   {i}. {alt.name} - {alt.description}")
        else:
            print("\n⚠️  No suitable alternatives found.")
    
    except ImportError:
        print("\n⚠️  Task models not available. Skipping alternatives demo.")


def main():
    """Run all demos"""
    print("\n")
    print("╔" + "=" * 68 + "╗")
    print("║" + " " * 15 + "TOOL REGISTRY & SMART SELECTION" + " " * 22 + "║")
    print("║" + " " * 27 + "DEMONSTRATION" + " " * 28 + "║")
    print("║" + " " * 25 + "v3.0 - World Class" + " " * 24 + "║")
    print("╚" + "=" * 68 + "╝")
    
    demo_basic_selection()
    demo_requirement_inference()
    demo_scoring()
    demo_anthropic_schema()
    demo_batch_selection()
    demo_tool_validation()
    demo_alternative_suggestions()
    
    print("\n" + "=" * 70)
    print("✅ ALL DEMOS COMPLETE")
    print("=" * 70)
    print("\nSoli Deo Gloria 🙏\n")


if __name__ == "__main__":
    main()
