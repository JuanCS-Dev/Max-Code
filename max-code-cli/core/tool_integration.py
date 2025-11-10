"""
Tool Integration - Helper for integrating tool system with task execution

Provides high-level API for:
- Tool selection for tasks
- Tool validation before execution
- Tool execution with error handling
- Registry management

Biblical Foundation:
"Planejem cuidadosamente o que fazem" (Provérbios 4:26 NTLH)

Soli Deo Gloria
"""

from typing import Dict, Any, Optional, List
import logging

from core.tools.enhanced_registry import get_enhanced_registry, EnhancedToolRegistry
from core.tools.tool_metadata import EnhancedToolMetadata
from core.tools.tool_selector import get_tool_selector, ToolSelector
from core.tools.registry import get_registry, ToolRegistry
from core.tools.types import ToolResult
from core.task_models import Task

logger = logging.getLogger(__name__)


class ToolIntegration:
    """
    Helper for integrating tool system with task execution
    
    Provides unified interface for:
    - Tool selection (manual or automatic)
    - Tool validation
    - Tool execution
    - Error handling
    - Registry inspection
    
    Examples:
        >>> integration = ToolIntegration()
        >>> 
        >>> # Auto-select and execute tool for task
        >>> result = integration.execute_task(task)
        >>> 
        >>> # Manual tool selection with validation
        >>> tool = integration.select_tool_for_task(task)
        >>> if integration.validate_tool(tool, task):
        ...     result = integration.execute_tool(tool, task)
        >>> 
        >>> # Get registry summary
        >>> summary = integration.get_tools_summary()
    """
    
    def __init__(
        self,
        use_enhanced_registry: bool = True,
        auto_select_tools: bool = True
    ):
        """
        Initialize tool integration
        
        Args:
            use_enhanced_registry: Use EnhancedToolRegistry (for smart selection)
            auto_select_tools: Enable automatic tool selection
        """
        self.enhanced_registry: EnhancedToolRegistry = get_enhanced_registry()
        self.registry: ToolRegistry = get_registry()
        self.selector: ToolSelector = get_tool_selector()
        
        self.use_enhanced = use_enhanced_registry
        self.auto_select = auto_select_tools
        
        logger.info("ToolIntegration initialized")
    
    def select_tool_for_task(
        self,
        task: Task,
        explicit_tool_name: Optional[str] = None
    ) -> Optional[EnhancedToolMetadata]:
        """
        Select tool for task execution
        
        Selection priority:
        1. Explicit tool name (if provided)
        2. Tool from task requirements
        3. Auto-selection based on task description
        
        Args:
            task: Task to select tool for
            explicit_tool_name: Force specific tool (overrides auto-selection)
        
        Returns:
            Selected tool or None
        
        Examples:
            >>> tool = integration.select_tool_for_task(task)
            >>> tool = integration.select_tool_for_task(task, "file_reader")
        """
        # Priority 1: Explicit tool name
        if explicit_tool_name:
            tool = self.enhanced_registry.get_tool(explicit_tool_name)
            if tool:
                logger.debug(f"Using explicit tool: {explicit_tool_name}")
                return tool
            else:
                logger.warning(f"Explicit tool '{explicit_tool_name}' not found")
        
        # Priority 2: Tool from task requirements
        if hasattr(task, 'requirements') and task.requirements.tools:
            if len(task.requirements.tools) > 0:
                tool_name = task.requirements.tools[0]
                tool = self.enhanced_registry.get_tool(tool_name)
                if tool:
                    logger.debug(f"Using tool from task requirements: {tool_name}")
                    return tool
        
        # Priority 3: Auto-selection
        if self.auto_select:
            tool = self.selector.select_for_task(task.description)
            if tool:
                logger.debug(f"Auto-selected tool: {tool.name}")
                return tool
        
        logger.warning(f"No tool selected for task: {task.description}")
        return None
    
    def validate_tool(
        self,
        tool: EnhancedToolMetadata,
        task: Task,
        strict: bool = False
    ) -> tuple[bool, List[str]]:
        """
        Validate tool for task execution
        
        Checks:
        - Required parameters present
        - Capabilities match task type
        - Tool-specific validation
        
        Args:
            tool: Tool to validate
            task: Task to execute
            strict: Strict validation (warnings = errors)
        
        Returns:
            (is_valid, issues)
        
        Examples:
            >>> valid, issues = integration.validate_tool(tool, task)
            >>> if not valid:
            ...     print(f"Validation failed: {issues}")
        """
        return self.selector.validate_tool_for_task(tool, task, strict=strict)
    
    def execute_tool(
        self,
        tool: EnhancedToolMetadata,
        task: Task,
        validate_first: bool = True
    ) -> ToolResult:
        """
        Execute tool for task
        
        Args:
            tool: Tool to execute
            task: Task with input parameters
            validate_first: Validate before execution
        
        Returns:
            ToolResult with execution result
        
        Examples:
            >>> result = integration.execute_tool(tool, task)
            >>> if result.type == "success":
            ...     print("Success!")
        """
        # Validate if requested
        if validate_first:
            is_valid, issues = self.validate_tool(tool, task, strict=False)
            if not is_valid:
                error_msg = f"Tool validation failed: {'; '.join(issues)}"
                logger.error(error_msg)
                return ToolResult.error(error_msg)
        
        # Get tool parameters from task
        params = task.requirements.inputs if hasattr(task, 'requirements') else {}
        
        # Execute via standard registry (execute is async)
        try:
            import asyncio
            
            # Check if running in event loop
            try:
                loop = asyncio.get_running_loop()
                # If in async context, cannot use asyncio.run
                error_msg = "execute_tool cannot be called from async context. Use execute_tool_async instead."
                logger.error(error_msg)
                return ToolResult.error(error_msg)
            except RuntimeError:
                # No running loop, safe to use asyncio.run
                result = asyncio.run(self.registry.execute(tool.name, params))
                logger.debug(f"Tool '{tool.name}' executed successfully")
                return result
        
        except Exception as e:
            error_msg = f"Tool execution failed: {str(e)}"
            logger.error(error_msg, exc_info=True)
            return ToolResult.error(error_msg)
    
    async def execute_tool_async(
        self,
        tool: EnhancedToolMetadata,
        task: Task,
        validate_first: bool = True
    ) -> ToolResult:
        """
        Execute tool for task (async version)
        
        Use this when called from async context.
        
        Args:
            tool: Tool to execute
            task: Task with input parameters
            validate_first: Validate before execution
        
        Returns:
            ToolResult with execution result
        
        Examples:
            >>> result = await integration.execute_tool_async(tool, task)
        """
        # Validate if requested
        if validate_first:
            is_valid, issues = self.validate_tool(tool, task, strict=False)
            if not is_valid:
                error_msg = f"Tool validation failed: {'; '.join(issues)}"
                logger.error(error_msg)
                return ToolResult.error(error_msg)
        
        # Get tool parameters from task
        params = task.requirements.inputs if hasattr(task, 'requirements') else {}
        
        # Execute via standard registry
        try:
            result = await self.registry.execute(tool.name, params)
            logger.debug(f"Tool '{tool.name}' executed successfully")
            return result
        
        except Exception as e:
            error_msg = f"Tool execution failed: {str(e)}"
            logger.error(error_msg, exc_info=True)
            return ToolResult.error(error_msg)
    
    def execute_task(
        self,
        task: Task,
        explicit_tool: Optional[str] = None,
        validate: bool = True
    ) -> ToolResult:
        """
        Select and execute tool for task (all-in-one)
        
        Convenience method that combines:
        1. Tool selection
        2. Tool validation
        3. Tool execution
        
        Args:
            task: Task to execute
            explicit_tool: Force specific tool
            validate: Validate before execution
        
        Returns:
            ToolResult with execution result
        
        Examples:
            >>> result = integration.execute_task(task)
            >>> result = integration.execute_task(task, "file_reader")
        """
        # Select tool
        tool = self.select_tool_for_task(task, explicit_tool)
        
        if not tool:
            error_msg = f"No tool available for task: {task.description}"
            logger.error(error_msg)
            return ToolResult.error(error_msg)
        
        # Execute
        return self.execute_tool(tool, task, validate_first=validate)
    
    async def execute_tasks_batch(
        self,
        tasks: List[Task],
        validate: bool = True
    ) -> Dict[str, ToolResult]:
        """
        Execute multiple tasks with batch tool selection
        
        More efficient than individual execution for multiple tasks.
        Uses ToolSelector's batch selection.
        
        Args:
            tasks: List of tasks to execute
            validate: Validate tools before execution
        
        Returns:
            Dict of task_id -> ToolResult
        
        Examples:
            >>> results = await integration.execute_tasks_batch(tasks)
            >>> for task_id, result in results.items():
            ...     print(f"{task_id}: {result.type}")
        """
        results = {}
        
        # Batch select tools
        tool_selections = await self.selector.select_tools_for_tasks(
            tasks,
            batch_mode=True
        )
        
        # Execute each task with selected tool
        for task in tasks:
            task_id = task.id
            
            if task_id not in tool_selections:
                results[task_id] = ToolResult.error(f"No tool selected for task {task_id}")
                continue
            
            tool = tool_selections[task_id]
            result = await self.execute_tool_async(tool, task, validate_first=validate)
            results[task_id] = result
        
        return results
    
    def get_tools_summary(self) -> Dict[str, Any]:
        """
        Get summary of registered tools
        
        Returns:
            Dict with tool statistics
        
        Examples:
            >>> summary = integration.get_tools_summary()
            >>> print(f"Total tools: {summary['total_tools']}")
        """
        tools = self.enhanced_registry.list_tools()
        
        # Group by category
        by_category = {}
        for tool in tools:
            cat = tool.category.value
            if cat not in by_category:
                by_category[cat] = []
            by_category[cat].append({
                "name": tool.name,
                "description": tool.description,
                "capabilities": {
                    "can_read": tool.capabilities.can_read,
                    "can_write": tool.capabilities.can_write,
                    "can_search": tool.capabilities.can_search,
                    "can_execute": tool.capabilities.can_execute,
                }
            })
        
        # Count by capability
        capabilities_count = {
            "can_read": sum(1 for t in tools if t.capabilities.can_read),
            "can_write": sum(1 for t in tools if t.capabilities.can_write),
            "can_search": sum(1 for t in tools if t.capabilities.can_search),
            "can_execute": sum(1 for t in tools if t.capabilities.can_execute),
        }
        
        return {
            "total_tools": len(tools),
            "by_category": by_category,
            "capabilities_count": capabilities_count,
            "tool_names": [t.name for t in tools]
        }
    
    def get_tool_info(self, tool_name: str) -> Optional[Dict[str, Any]]:
        """
        Get detailed info about specific tool
        
        Args:
            tool_name: Name of tool
        
        Returns:
            Dict with tool details or None
        
        Examples:
            >>> info = integration.get_tool_info("file_reader")
            >>> print(info['description'])
        """
        tool = self.enhanced_registry.get_tool(tool_name)
        
        if not tool:
            return None
        
        return {
            "name": tool.name,
            "description": tool.description,
            "category": tool.category.value,
            "capabilities": {
                "can_read": tool.capabilities.can_read,
                "can_write": tool.capabilities.can_write,
                "can_search": tool.capabilities.can_search,
                "can_execute": tool.capabilities.can_execute,
                "can_analyze": tool.capabilities.can_analyze,
                "can_validate": tool.capabilities.can_validate,
            },
            "requirements": {
                "requires_filepath": tool.requirements.requires_filepath,
                "requires_directory": tool.requirements.requires_directory,
                "requires_pattern": tool.requirements.requires_pattern,
                "requires_content": tool.requirements.requires_content,
            },
            "performance": {
                "safe": tool.performance.safe,
                "destructive": tool.performance.destructive,
                "expensive": tool.performance.expensive,
                "estimated_time": tool.performance.estimated_time,
            },
            "parameters": tool.parameters,
            "tags": tool.tags,
        }
    
    def suggest_tools_for_description(
        self,
        description: str,
        count: int = 3
    ) -> List[EnhancedToolMetadata]:
        """
        Suggest tools for task description
        
        Args:
            description: Task description
            count: Number of suggestions
        
        Returns:
            List of suggested tools
        
        Examples:
            >>> tools = integration.suggest_tools_for_description(
            ...     "Read the config file",
            ...     count=3
            ... )
        """
        # Use selector to get best matches
        requirements = self.selector.infer_requirements(description)
        
        # Get all matching tools with scores
        candidates = []
        for tool in self.enhanced_registry.list_tools():
            score = tool.matches_requirements(requirements)
            if score > 0:
                candidates.append((score, tool))
        
        # Sort by score and return top N
        candidates.sort(reverse=True, key=lambda x: x[0])
        return [tool for _, tool in candidates[:count]]


# ============================================================================
# Global instance (singleton)
# ============================================================================

_integration: Optional[ToolIntegration] = None


def get_tool_integration() -> ToolIntegration:
    """
    Get global ToolIntegration instance (singleton)
    
    Returns:
        ToolIntegration instance
    
    Examples:
        >>> integration = get_tool_integration()
        >>> result = integration.execute_task(task)
    """
    global _integration
    if _integration is None:
        _integration = ToolIntegration()
    return _integration
