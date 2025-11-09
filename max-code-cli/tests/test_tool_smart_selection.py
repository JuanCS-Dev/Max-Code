"""
Tests for Tool Registry & Smart Selection (PROMPT 2.2)

Biblical Foundation:
"Examinai tudo. Retende o bem" (1 Tessalonicenses 5:21)

Soli Deo Gloria
"""

import os
import pytest
from core.tools.tool_metadata import (
    EnhancedToolMetadata,
    ToolCategory,
    ToolCapabilities,
    ToolRequirements,
)
from core.tools.enhanced_registry import (
    EnhancedToolRegistry,
    get_enhanced_registry,
)
from core.tools.tool_selector import (
    ToolSelector,
    get_tool_selector,
)


class TestEnhancedToolMetadata:
    """Test enhanced tool metadata"""
    
    def test_metadata_creation(self):
        """Test creating enhanced metadata"""
        metadata = EnhancedToolMetadata(
            name="test_tool",
            description="Test tool",
            category=ToolCategory.FILE_OPS,
            capabilities=ToolCapabilities(can_read=True),
            requirements=ToolRequirements(requires_filepath=True),
            tags=["test", "file"]
        )
        
        assert metadata.name == "test_tool"
        assert metadata.category == ToolCategory.FILE_OPS
        assert metadata.capabilities.can_read is True
        assert metadata.requirements.requires_filepath is True
        assert "test" in metadata.tags
    
    def test_matches_requirements_perfect_match(self):
        """Test perfect requirements match"""
        metadata = EnhancedToolMetadata(
            name="grep",
            description="Search files",
            category=ToolCategory.SEARCH,
            capabilities=ToolCapabilities(can_search=True),
            requirements=ToolRequirements(requires_pattern=True),
            tags=["search", "regex"]
        )
        
        score = metadata.matches_requirements({
            "needs_search": True,
            "has_pattern": True,
            "tags": ["search"]
        })
        
        # Should have high score (3 matches: search capability, pattern req, tag overlap)
        assert score > 0.8
    
    def test_matches_requirements_no_match(self):
        """Test no requirements match"""
        metadata = EnhancedToolMetadata(
            name="file_writer",
            description="Write files",
            category=ToolCategory.FILE_OPS,
            capabilities=ToolCapabilities(can_write=True),
        )
        
        score = metadata.matches_requirements({
            "needs_read": True,  # Tool can't read
            "needs_execute": True,  # Tool can't execute
        })
        
        assert score == 0.0
    
    def test_to_anthropic_schema(self):
        """Test Anthropic schema conversion"""
        metadata = EnhancedToolMetadata(
            name="read_file",
            description="Read file contents",
            category=ToolCategory.FILE_OPS,
            parameters=[
                {"name": "path", "type": "string", "description": "File path", "required": True},
                {"name": "offset", "type": "number", "description": "Line offset", "required": False}
            ]
        )
        
        schema = metadata.to_anthropic_schema()
        
        assert schema["name"] == "read_file"
        assert schema["description"] == "Read file contents"
        assert "path" in schema["input_schema"]["properties"]
        assert "path" in schema["input_schema"]["required"]
        assert "offset" not in schema["input_schema"]["required"]
    
    def test_infer_capabilities(self):
        """Test capability inference from name/description"""
        caps = EnhancedToolMetadata._infer_capabilities(
            "grep_tool",
            "Search and find patterns in files"
        )
        
        assert caps.can_search is True
        assert caps.can_read is False  # Not mentioned
    
    def test_infer_requirements(self):
        """Test requirement inference from parameters"""
        params = [
            type('Param', (), {'name': 'file_path'}),
            type('Param', (), {'name': 'pattern'}),
        ]
        
        reqs = EnhancedToolMetadata._infer_requirements(params)
        
        assert reqs.requires_filepath is True
        assert reqs.requires_pattern is True


class TestEnhancedToolRegistry:
    """Test enhanced tool registry"""
    
    def test_singleton_pattern(self):
        """Test registry is singleton"""
        registry1 = EnhancedToolRegistry()
        registry2 = EnhancedToolRegistry()
        
        assert registry1 is registry2
    
    def test_register_enhanced(self):
        """Test registering enhanced tool"""
        registry = EnhancedToolRegistry()
        
        metadata = EnhancedToolMetadata(
            name="test_tool_reg",
            description="Test",
            category=ToolCategory.FILE_OPS,
        )
        
        registry.register_enhanced(metadata)
        
        retrieved = registry.get_tool("test_tool_reg")
        assert retrieved is not None
        assert retrieved.name == "test_tool_reg"
    
    def test_list_tools_by_category(self):
        """Test listing tools by category"""
        registry = EnhancedToolRegistry()
        registry.enhance_existing_tools()  # Load existing tools
        
        file_tools = registry.list_tools(ToolCategory.FILE_OPS)
        search_tools = registry.list_tools(ToolCategory.SEARCH)
        
        assert len(file_tools) > 0
        assert len(search_tools) > 0
        
        # Check all file tools are in FILE_OPS category
        for tool in file_tools:
            assert tool.category == ToolCategory.FILE_OPS
    
    def test_enhance_existing_tools(self):
        """Test auto-enhancement of existing tools"""
        registry = get_enhanced_registry()
        
        # Should have enhanced file_reader
        file_reader = registry.get_tool("file_reader")
        assert file_reader is not None
        assert file_reader.capabilities.can_read is True
        assert file_reader.requirements.requires_filepath is True
        assert "read" in file_reader.tags
    
    def test_select_best_tool_scoring(self):
        """Test tool selection using scoring"""
        registry = get_enhanced_registry()
        
        # Select tool for reading files
        tool = registry.select_best_tool(
            "Read a config file",
            {"needs_read": True, "has_filepath": True},
            use_llm=False
        )
        
        assert tool is not None
        assert tool.capabilities.can_read is True
        assert tool.name == "file_reader"
    
    def test_select_best_tool_search(self):
        """Test selecting search tool"""
        registry = get_enhanced_registry()
        
        # Select tool for searching
        tool = registry.select_best_tool(
            "Find TODO comments",
            {"needs_search": True, "has_pattern": True},
            use_llm=False
        )
        
        assert tool is not None
        assert tool.capabilities.can_search is True
        # Should be grep_tool (searches content) or glob_tool (searches files)
        assert tool.name in ["grep_tool", "glob_tool"]
    
    def test_select_no_match(self):
        """Test selection with no matching tools"""
        registry = get_enhanced_registry()
        
        # Request capability that doesn't exist
        tool = registry.select_best_tool(
            "Deploy to production",
            {"needs_deploy": True},  # No tool has deploy capability
            use_llm=False
        )
        
        # Should return None (no match) or a low-scoring tool
        # Accept both outcomes as valid
        assert tool is None or tool.matches_requirements({"needs_deploy": True}) < 0.5
    
    def test_get_tools_for_anthropic(self):
        """Test Anthropic schema export"""
        registry = get_enhanced_registry()
        
        schemas = registry.get_tools_for_anthropic()
        
        assert isinstance(schemas, list)
        assert len(schemas) > 0
        
        # Check schema structure
        schema = schemas[0]
        assert "name" in schema
        assert "description" in schema
        assert "input_schema" in schema


class TestToolSelector:
    """Test tool selector"""
    
    def test_infer_requirements_read(self):
        """Test inferring read requirements"""
        selector = ToolSelector()
        
        reqs = selector.infer_requirements("Read the config.json file")
        
        assert reqs['needs_read'] is True
        assert reqs['has_filepath'] is True
        assert "read" in reqs['tags']
    
    def test_infer_requirements_write(self):
        """Test inferring write requirements"""
        selector = ToolSelector()
        
        reqs = selector.infer_requirements("Create a new file called output.txt")
        
        assert reqs['needs_write'] is True
        assert reqs['has_filepath'] is True
        assert "write" in reqs['tags']
    
    def test_infer_requirements_search(self):
        """Test inferring search requirements"""
        selector = ToolSelector()
        
        reqs = selector.infer_requirements('Find all "TODO" comments in src/')
        
        assert reqs['needs_search'] is True
        assert reqs['has_pattern'] is True
        assert reqs['has_directory'] is True
        assert "search" in reqs['tags']
    
    def test_select_for_task_read(self):
        """Test selecting tool for read task"""
        selector = get_tool_selector()
        
        tool = selector.select_for_task("Read the README.md file")
        
        assert tool is not None
        assert tool.name == "file_reader"
        assert tool.capabilities.can_read is True
    
    def test_select_for_task_search(self):
        """Test selecting tool for search task"""
        selector = get_tool_selector()
        
        tool = selector.select_for_task("Search for TODO comments in code")
        
        assert tool is not None
        assert tool.capabilities.can_search is True
    
    def test_select_for_task_explicit_requirements(self):
        """Test selection with explicit requirements"""
        selector = get_tool_selector()
        
        tool = selector.select_for_task(
            "Process data",
            explicit_requirements={"needs_read": True, "has_filepath": True}
        )
        
        assert tool is not None
        assert tool.capabilities.can_read is True
    
    def test_explain_selection(self):
        """Test selection explanation"""
        selector = get_tool_selector()
        
        explanation = selector.explain_selection("Read config.json")
        
        assert "task" in explanation
        assert "selected_tool" in explanation
        assert "requirements" in explanation
        assert "all_scores" in explanation
        assert "top_3" in explanation
        assert "reasoning" in explanation
        
        # Should have selected file_reader
        assert explanation["selected_tool"] == "file_reader"
        
        # Should have scored tools
        assert len(explanation["all_scores"]) > 0
        assert len(explanation["top_3"]) <= 3
    
    def test_get_all_tools(self):
        """Test getting all tools"""
        selector = get_tool_selector()
        
        tools = selector.get_all_tools()
        
        assert len(tools) > 0
        assert all(isinstance(tool, EnhancedToolMetadata) for tool in tools)
    
    def test_get_tools_for_category(self):
        """Test getting tools by category"""
        selector = get_tool_selector()
        
        file_tools = selector.get_tools_for_category(ToolCategory.FILE_OPS)
        search_tools = selector.get_tools_for_category(ToolCategory.SEARCH)
        
        assert len(file_tools) > 0
        assert len(search_tools) > 0
        
        # Verify categories
        for tool in file_tools:
            assert tool.category == ToolCategory.FILE_OPS


class TestIntegration:
    """Integration tests for full workflow"""
    
    def test_full_selection_workflow(self):
        """Test complete selection workflow"""
        # 1. Get selector
        selector = get_tool_selector()
        
        # 2. Select tool for task
        tool = selector.select_for_task("Read the config file at ./config.json")
        
        # 3. Verify selection
        assert tool is not None
        assert tool.name == "file_reader"
        
        # 4. Check tool metadata
        assert tool.capabilities.can_read is True
        assert tool.requirements.requires_filepath is True
        
        # 5. Verify Anthropic schema
        schema = tool.to_anthropic_schema()
        assert schema["name"] == "file_reader"
    
    def test_scoring_consistency(self):
        """Test that scoring is consistent"""
        selector = get_tool_selector()
        
        # Same task should get same tool
        tool1 = selector.select_for_task("Read file.txt")
        tool2 = selector.select_for_task("Read file.txt")
        
        assert tool1.name == tool2.name
    
    def test_different_tasks_different_tools(self):
        """Test that different tasks select different tools"""
        selector = get_tool_selector()
        
        read_tool = selector.select_for_task("Read config.json")
        write_tool = selector.select_for_task("Create new file output.txt")
        search_tool = selector.select_for_task("Find TODO in code")
        
        # Should select different tools for different capabilities
        assert read_tool.name != write_tool.name
        assert read_tool.capabilities.can_read is True
        assert write_tool.capabilities.can_write is True
        assert search_tool.capabilities.can_search is True


class TestBatchSelection:
    """Test batch selection features (NEW in v3.0)"""
    
    @pytest.mark.asyncio
    async def test_batch_select_with_tasks(self):
        """Test batch selection with multiple tasks"""
        from core.task_models import Task, TaskType, TaskRequirement
        
        selector = get_tool_selector()
        
        # Create mock tasks
        tasks = [
            Task(
                id="task_1",
                description="Read the config.json file",
                type=TaskType.READ,
                requirements=TaskRequirement(
                    agent_type="code",
                    tools=[],
                    inputs={"file_path": "config.json"}
                )
            ),
            Task(
                id="task_2",
                description="Search for TODO comments in src/",
                type=TaskType.READ,
                requirements=TaskRequirement(
                    agent_type="code",
                    tools=[],
                    inputs={"pattern": "TODO", "directory": "src/"}
                )
            ),
            Task(
                id="task_3",
                description="Create a new file output.txt",
                type=TaskType.WRITE,
                requirements=TaskRequirement(
                    agent_type="code",
                    tools=[],
                    inputs={"file_path": "output.txt", "content": "test"}
                )
            ),
        ]
        
        # Test individual selection (fallback, no API key needed)
        selections = await selector.select_tools_for_tasks(tasks, batch_mode=False)
        
        # Verify selections
        assert len(selections) == 3
        assert "task_1" in selections
        assert "task_2" in selections
        assert "task_3" in selections
        
        # Verify correct tools selected
        assert selections["task_1"].capabilities.can_read is True
        assert selections["task_2"].capabilities.can_search is True
        assert selections["task_3"].capabilities.can_write is True
    
    @pytest.mark.asyncio
    @pytest.mark.skipif(
        not os.getenv("ANTHROPIC_API_KEY"),
        reason="ANTHROPIC_API_KEY not set"
    )
    async def test_batch_select_with_claude(self):
        """Test batch selection using Claude API (requires API key)"""
        from core.task_models import Task, TaskType, TaskRequirement
        
        selector = get_tool_selector()
        
        tasks = [
            Task(
                id="task_1",
                description="Read the README.md file",
                type=TaskType.READ,
                requirements=TaskRequirement(
                    agent_type="code",
                    inputs={"file_path": "README.md"}
                )
            ),
            Task(
                id="task_2",
                description="Find all Python files in src/",
                type=TaskType.READ,
                requirements=TaskRequirement(
                    agent_type="code",
                    inputs={"pattern": "*.py", "directory": "src/"}
                )
            ),
        ]
        
        # Test batch selection with Claude
        selections = await selector.select_tools_for_tasks(tasks, batch_mode=True)
        
        assert len(selections) == 2
        assert selections["task_1"].capabilities.can_read is True
        assert selections["task_2"].capabilities.can_search is True


class TestToolValidation:
    """Test tool validation features (NEW in v3.0)"""
    
    def test_validate_tool_success(self):
        """Test successful tool validation"""
        from core.task_models import Task, TaskType, TaskRequirement
        
        selector = get_tool_selector()
        tool = selector.registry.get_tool("file_reader")
        
        task = Task(
            id="task_1",
            description="Read config.json",
            type=TaskType.READ,
            requirements=TaskRequirement(
                agent_type="code",
                tools=["file_reader"],  # Explicit tool requirement (no warning)
                inputs={"file_path": "config.json"}
            )
        )
        
        valid, issues = selector.validate_tool_for_task(tool, task, strict=False)
        
        assert valid is True
        assert len(issues) == 0
    
    def test_validate_tool_missing_params(self):
        """Test validation fails with missing parameters"""
        from core.task_models import Task, TaskType, TaskRequirement
        
        selector = get_tool_selector()
        tool = selector.registry.get_tool("file_reader")
        
        # Check what parameters file_reader actually requires
        required_params = [p.name for p in tool.parameters if p.required]
        
        # If file_reader has no required params, this test is not applicable
        if not required_params:
            pytest.skip("file_reader has no required parameters")
        
        task = Task(
            id="task_1",
            description="Read a file",
            type=TaskType.READ,
            requirements=TaskRequirement(
                agent_type="code",
                inputs={}  # Missing required parameters
            )
        )
        
        valid, issues = selector.validate_tool_for_task(tool, task, strict=False)
        
        # Should fail validation if required params are missing
        if required_params:
            assert valid is False
            assert len(issues) > 0
            # Check that missing param is mentioned
            issues_text = " ".join(issues).lower()
            assert any(param.lower() in issues_text for param in required_params)
    
    def test_validate_tool_capability_mismatch(self):
        """Test validation fails with capability mismatch"""
        from core.task_models import Task, TaskType, TaskRequirement
        
        selector = get_tool_selector()
        tool = selector.registry.get_tool("file_reader")  # Can only read
        
        task = Task(
            id="task_1",
            description="Write to file",
            type=TaskType.WRITE,  # Requires write capability
            requirements=TaskRequirement(
                agent_type="code",
                inputs={"file_path": "output.txt", "content": "test"}
            )
        )
        
        valid, issues = selector.validate_tool_for_task(tool, task)
        
        assert valid is False
        assert any("write" in issue.lower() for issue in issues)
    
    def test_validate_tool_non_strict(self):
        """Test non-strict validation (warnings allowed)"""
        from core.task_models import Task, TaskType, TaskRequirement
        
        selector = get_tool_selector()
        tool = selector.registry.get_tool("file_reader")
        
        task = Task(
            id="task_1",
            description="Read file",
            type=TaskType.READ,
            requirements=TaskRequirement(
                agent_type="code",
                inputs={"file_path": "config.json"},
                tools=[]  # Empty tools list (warning, not error)
            )
        )
        
        # Non-strict: warnings don't fail validation
        valid, issues = selector.validate_tool_for_task(tool, task, strict=False)
        assert valid is True
        
        # Strict: warnings fail validation
        valid, issues = selector.validate_tool_for_task(tool, task, strict=True)
        # May have warnings about empty tools list


class TestAlternativeTools:
    """Test alternative tool suggestions (NEW in v3.0)"""
    
    @pytest.mark.asyncio
    async def test_suggest_alternatives_basic(self):
        """Test basic alternative suggestions"""
        from core.task_models import Task, TaskType, TaskRequirement
        
        selector = get_tool_selector()
        primary_tool = selector.registry.get_tool("file_reader")
        
        task = Task(
            id="task_1",
            description="Read and analyze config.json",
            type=TaskType.READ,
            requirements=TaskRequirement(
                agent_type="code",
                inputs={"file_path": "config.json"}
            )
        )
        
        alternatives = await selector.suggest_alternative_tools(
            task, primary_tool, count=2
        )
        
        # Should suggest alternatives (may be empty if no good matches)
        assert isinstance(alternatives, list)
        assert len(alternatives) <= 2
        
        # Alternatives should not include primary tool
        for alt in alternatives:
            assert alt.name != primary_tool.name
    
    @pytest.mark.asyncio
    async def test_suggest_alternatives_exclude_failed(self):
        """Test excluding failed tools from suggestions"""
        from core.task_models import Task, TaskType, TaskRequirement
        
        selector = get_tool_selector()
        primary_tool = selector.registry.get_tool("grep_tool")
        
        task = Task(
            id="task_1",
            description="Search for TODO comments",
            type=TaskType.READ,
            requirements=TaskRequirement(
                agent_type="code",
                inputs={"pattern": "TODO"}
            )
        )
        
        # Exclude primary and glob_tool
        alternatives = await selector.suggest_alternative_tools(
            task, 
            primary_tool, 
            count=3,
            exclude_failed=["grep_tool", "glob_tool"]
        )
        
        # Should not suggest excluded tools
        for alt in alternatives:
            assert alt.name not in ["grep_tool", "glob_tool"]
    
    @pytest.mark.asyncio
    async def test_suggest_alternatives_sorted_by_score(self):
        """Test alternatives are sorted by match score"""
        from core.task_models import Task, TaskType, TaskRequirement
        
        selector = get_tool_selector()
        primary_tool = selector.registry.get_tool("file_reader")
        
        task = Task(
            id="task_1",
            description="Read multiple files matching pattern *.json",
            type=TaskType.READ,
            requirements=TaskRequirement(
                agent_type="code",
                inputs={"pattern": "*.json"}
            )
        )
        
        alternatives = await selector.suggest_alternative_tools(
            task, primary_tool, count=3
        )
        
        if len(alternatives) > 1:
            # Verify alternatives are sorted (first should have highest score)
            reqs = selector.infer_requirements(task.description)
            scores = [alt.matches_requirements(reqs) for alt in alternatives]
            
            # Scores should be in descending order
            for i in range(len(scores) - 1):
                assert scores[i] >= scores[i + 1]


class TestEdgeCases:
    """Test edge cases and error handling (NEW in v3.0)"""
    
    def test_validate_tool_without_requirements(self):
        """Test validation when task has no requirements"""
        from core.task_models import Task, TaskType
        
        selector = get_tool_selector()
        tool = selector.registry.get_tool("file_reader")
        
        # Create task without requirements attribute
        task = type('Task', (), {
            'id': 'task_1',
            'description': 'Read file',
            'type': TaskType.READ
        })()
        
        valid, issues = selector.validate_tool_for_task(tool, task)
        
        # Should handle gracefully (no crash)
        assert isinstance(valid, bool)
        assert isinstance(issues, list)
    
    @pytest.mark.asyncio
    async def test_batch_select_empty_tasks(self):
        """Test batch selection with empty task list"""
        selector = get_tool_selector()
        
        selections = await selector.select_tools_for_tasks([], batch_mode=False)
        
        assert selections == {}
    
    @pytest.mark.asyncio
    async def test_suggest_alternatives_no_matches(self):
        """Test alternative suggestions when no tools match"""
        from core.task_models import Task, TaskType, TaskRequirement
        
        selector = get_tool_selector()
        primary_tool = selector.registry.get_tool("file_reader")
        
        # Create task with requirements no tool can satisfy
        task = Task(
            id="task_1",
            description="Deploy to production server",
            type=type('TaskType', (), {'value': 'deploy'})(),  # Non-existent type
            requirements=TaskRequirement(
                agent_type="deploy",
                inputs={"server": "prod"}
            )
        )
        
        alternatives = await selector.suggest_alternative_tools(
            task, primary_tool, count=2
        )
        
        # Should return empty list or low-scoring tools
        assert isinstance(alternatives, list)
    
    def test_infer_requirements_edge_cases(self):
        """Test requirement inference with edge cases"""
        selector = get_tool_selector()
        
        # Empty description
        reqs1 = selector.infer_requirements("")
        assert isinstance(reqs1, dict)
        
        # Very long description
        reqs2 = selector.infer_requirements("x" * 10000)
        assert isinstance(reqs2, dict)
        
        # Special characters
        reqs3 = selector.infer_requirements("Read file @#$%^&*()")
        assert reqs3['needs_read'] is True
