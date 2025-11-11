"""
Tool Selector - World-Class Unified Tool Selection API

Provides comprehensive interface for intelligent tool selection:
- Natural language descriptions → tools
- Task objects → tools
- Batch selection for multiple tasks
- Validation and alternatives
- Sync and async support

Integrates:
- EnhancedToolRegistry (enhanced_registry.py)
- Task requirement inference
- Claude-powered batch selection
- Fallback strategies

Biblical Foundation:
"A sabedoria do prudente é entender o seu caminho" (Provérbios 14:8)

Soli Deo Gloria
"""

from typing import Dict, List, Any, Optional, Tuple
import logging
import re
import json
import os
import asyncio

from .enhanced_registry import get_enhanced_registry, EnhancedToolRegistry
from .tool_metadata import EnhancedToolMetadata, ToolCategory
from .types import ToolResult

logger = logging.getLogger(__name__)

# Lazy import for Task models and Anthropic (avoid import errors if not installed)
_Task = None
_TaskRequirement = None
_Anthropic = None
_AsyncAnthropic = None

def _get_task_models():
    """Lazy import task models"""
    global _Task, _TaskRequirement
    if _Task is None:
        try:
            from core.task_models import Task, TaskRequirement
            _Task = Task
            _TaskRequirement = TaskRequirement
        except ImportError:
            logger.debug("Task models not available (optional dependency)")
    return _Task, _TaskRequirement

def _get_anthropic_clients():
    """Lazy import Anthropic SDK"""
    global _Anthropic, _AsyncAnthropic
    if _Anthropic is None:
        try:
            from anthropic import Anthropic, AsyncAnthropic
            _Anthropic = Anthropic
            _AsyncAnthropic = AsyncAnthropic
        except ImportError:
            logger.debug("Anthropic SDK not available (optional for LLM-powered batch selection)")
    return _Anthropic, _AsyncAnthropic


class ToolSelector:
    """
    High-level tool selector for agents
    
    Provides simple API:
    1. Infer requirements from task description
    2. Select best tool using enhanced registry
    3. Execute tool with parameters
    
    Examples:
        >>> selector = ToolSelector()
        >>> 
        >>> # Simple selection
        >>> tool = selector.select_for_task("Read the config file")
        >>> print(tool.name)  # "file_reader"
        >>> 
        >>> # Select and execute
        >>> result = selector.select_and_execute(
        ...     "Read the config file",
        ...     {"file_path": "config.json"}
        ... )
    """
    
    def __init__(self, use_llm_selection: bool = False):
        """
        Initialize tool selector
        
        Args:
            use_llm_selection: Use Claude for final tool selection
        """
        self.registry: EnhancedToolRegistry = get_enhanced_registry()
        self.use_llm = use_llm_selection
    
    def infer_requirements(self, task_description: str) -> Dict[str, Any]:
        """
        Infer task requirements from natural language description
        
        Uses keyword matching and pattern detection to identify:
        - Capability needs (read, write, search, etc.)
        - Context availability (filepath, pattern, etc.)
        - Intent tags
        
        Args:
            task_description: Natural language task description
        
        Returns:
            Requirements dict for tool matching
        
        Examples:
            >>> selector = ToolSelector()
            >>> reqs = selector.infer_requirements("Find all TODO comments in src/")
            >>> print(reqs)
            {
                'needs_search': True,
                'has_pattern': True,
                'has_directory': True,
                'tags': ['search', 'find']
            }
        """
        text = task_description.lower()
        requirements = {}
        
        # Infer capability needs
        read_keywords = [r"\bread\b", r"\bget\b", r"\bshow\b", r"\bdisplay\b", r"\bview\b", r"\bcheck\b", r"\binspect\b"]
        write_keywords = [r"\bwrite\b", r"\bcreate\b", r"\bmake\b", r"\bgenerate\b", r"\badd\b", r"\binsert\b", r"\bupdate\b", r"\bmodify\b", r"\bedit\b", r"\bchange\b", r"\breplace\b"]
        search_keywords = [r"\bfind\b", r"\bsearch\b", r"\bgrep\b", r"look for", r"\blocate\b", r"\bmatch\b"]
        execute_keywords = [r"\brun\b", r"\bexecute\b", r"\bbash\b", r"\bcommand\b", r"\bshell\b"]
        
        requirements['needs_read'] = any(re.search(kw, text) for kw in read_keywords)
        requirements['needs_write'] = any(re.search(kw, text) for kw in write_keywords)
        requirements['needs_search'] = any(re.search(kw, text) for kw in search_keywords)
        requirements['needs_execute'] = any(re.search(kw, text) for kw in execute_keywords)
        
        # Infer context availability
        # File path patterns: /path/to/file, ./file, ../file, file.ext, word.ext (anywhere)
        has_filepath = bool(
            re.search(r'[./][\w/.-]+\.\w+', text) or  # ./path/file.ext
            re.search(r'\bfile\b.*\b\w+\.\w+\b', text) or  # file config.json
            re.search(r'\b[\w-]+\.\w{2,4}\b', text)  # filename.ext (2-4 char extension)
        )
        requirements['has_filepath'] = has_filepath
        
        # Directory patterns: in src/, from dir/, directory name
        has_directory = bool(
            re.search(r'\bin\s+[\w/-]+/', text) or
            re.search(r'\bdir(?:ectory)?\b', text) or
            re.search(r'\bfolder\b', text)
        )
        requirements['has_directory'] = has_directory
        
        # Pattern indicators: "TODO", regex, pattern, match
        has_pattern = bool(
            re.search(r'"[^"]+"', text) or  # Quoted strings
            re.search(r'\bpattern\b', text) or
            re.search(r'\bregex\b', text) or
            re.search(r'\bmatch', text)
        )
        requirements['has_pattern'] = has_pattern
        
        # Content indicators: "text content", data, content
        has_content = bool(
            re.search(r'\bcontent\b', text) or
            re.search(r'\btext\b', text) or
            re.search(r'\bdata\b', text)
        )
        requirements['has_content'] = has_content
        
        # Extract tags from keywords
        tags = []
        if requirements['needs_search']:
            tags.extend(['search', 'find'])
        if requirements['needs_read']:
            tags.append('read')
        if requirements['needs_write']:
            tags.extend(['write', 'modify'])
        if has_filepath:
            tags.append('file')
        if has_pattern:
            tags.append('pattern')
        
        # Specific tool hints (for disambiguation)
        if re.search(r'\bedit\b.*\breplac', text) or re.search(r'\breplac.*\bedit\b', text):
            # "edit replacing" suggests file_editor
            tags.append('edit')
            requirements['prefers_editor'] = True
        
        if re.search(r'(TODO|FIXME|comments?|content)', text, re.IGNORECASE):
            # Searching for content suggests grep (not glob)
            tags.append('content')
            requirements['prefers_grep'] = True
        
        if re.search(r'\*\.\w+|glob', text):
            # Glob pattern syntax suggests glob_tool
            tags.append('glob')
            requirements['prefers_glob'] = True
        
        requirements['tags'] = tags
        
        return requirements
    
    def select_for_task(
        self,
        task_description: str,
        explicit_requirements: Optional[Dict[str, Any]] = None
    ) -> Optional[EnhancedToolMetadata]:
        """
        Select best tool for task
        
        Args:
            task_description: Natural language task description
            explicit_requirements: Optional explicit requirements (overrides inference)
        
        Returns:
            Best matching tool or None
        
        Examples:
            >>> selector = ToolSelector()
            >>> tool = selector.select_for_task("Read config.json")
            >>> print(tool.name)  # "file_reader"
        """
        # Infer or use explicit requirements
        if explicit_requirements:
            requirements = explicit_requirements
        else:
            requirements = self.infer_requirements(task_description)
        
        logger.info(f"Task: {task_description}")
        logger.debug(f"Requirements: {requirements}")
        
        # Select tool
        tool = self.registry.select_best_tool(
            task_description,
            requirements,
            use_llm=self.use_llm
        )
        
        if tool:
            logger.info(f"Selected tool: {tool.name}")
        else:
            logger.warning("No suitable tool found")
        
        return tool
    
    def select_and_execute(
        self,
        task_description: str,
        parameters: Dict[str, Any],
        explicit_requirements: Optional[Dict[str, Any]] = None
    ) -> ToolResult:
        """
        Select and execute tool for task
        
        Args:
            task_description: Natural language task description
            parameters: Tool parameters (e.g., {"file_path": "config.json"})
            explicit_requirements: Optional explicit requirements
        
        Returns:
            ToolResult from execution
        
        Examples:
            >>> selector = ToolSelector()
            >>> result = selector.select_and_execute(
            ...     "Read the config file",
            ...     {"file_path": "config.json"}
            ... )
            >>> print(result.content[0].text)
        """
        # Select tool
        tool = self.select_for_task(task_description, explicit_requirements)
        
        if not tool:
            return ToolResult.error(f"No suitable tool found for: {task_description}")
        
        # Execute tool
        try:
            result = self.registry.execute_tool(tool.name, **parameters)
            return result
        except Exception as e:
            logger.error(f"Tool execution failed: {e}")
            return ToolResult.error(f"Tool execution failed: {str(e)}")
    
    def get_tools_for_category(self, category: ToolCategory) -> List[EnhancedToolMetadata]:
        """
        Get all tools in category
        
        Args:
            category: Tool category
        
        Returns:
            List of tools in category
        """
        return self.registry.list_tools(category)
    
    def get_all_tools(self) -> List[EnhancedToolMetadata]:
        """Get all available tools"""
        return self.registry.list_tools()
    
    def explain_selection(
        self,
        task_description: str,
        explicit_requirements: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Explain tool selection decision
        
        Returns detailed information about how tool was selected
        
        Args:
            task_description: Task description
            explicit_requirements: Optional explicit requirements
        
        Returns:
            Dict with:
                - selected_tool: Tool name
                - requirements: Inferred requirements
                - scores: All tool scores
                - reasoning: Selection reasoning
        """
        # Infer requirements
        if explicit_requirements:
            requirements = explicit_requirements
        else:
            requirements = self.infer_requirements(task_description)
        
        # Score all tools
        scores = []
        for tool in self.registry.list_tools():
            score = tool.matches_requirements(requirements)
            scores.append({
                "tool": tool.name,
                "score": score,
                "category": tool.category.value,
                "capabilities": {
                    "read": tool.capabilities.can_read,
                    "write": tool.capabilities.can_write,
                    "search": tool.capabilities.can_search,
                },
            })
        
        # Sort by score
        scores.sort(key=lambda x: x["score"], reverse=True)
        
        # Select best
        selected = self.registry.select_best_tool(
            task_description,
            requirements,
            use_llm=self.use_llm
        )
        
        return {
            "task": task_description,
            "selected_tool": selected.name if selected else None,
            "requirements": requirements,
            "all_scores": scores,
            "top_3": scores[:3],
            "reasoning": self._generate_reasoning(requirements, selected, scores[:3])
        }
    
    def _generate_reasoning(
        self,
        requirements: Dict[str, Any],
        selected: Optional[EnhancedToolMetadata],
        top_scores: List[Dict[str, Any]]
    ) -> str:
        """Generate human-readable reasoning for selection"""
        if not selected:
            return "No tool matched the requirements"
        
        reasoning = f"Selected '{selected.name}' because:\n"
        
        # Explain requirements match
        matched_reqs = []
        if requirements.get('needs_read') and selected.capabilities.can_read:
            matched_reqs.append("can read files")
        if requirements.get('needs_write') and selected.capabilities.can_write:
            matched_reqs.append("can write/modify files")
        if requirements.get('needs_search') and selected.capabilities.can_search:
            matched_reqs.append("can search content")
        
        if matched_reqs:
            reasoning += f"- Capabilities: {', '.join(matched_reqs)}\n"
        
        # Show score comparison
        if len(top_scores) > 1:
            reasoning += f"- Score: {top_scores[0]['score']:.2f} (highest)\n"
            reasoning += f"- Competitors: {', '.join([s['tool'] for s in top_scores[1:]])}\n"
        
        return reasoning
    
    async def select_tools_for_tasks(
        self,
        tasks: List[Any],
        batch_mode: bool = True,
        api_key: Optional[str] = None
    ) -> Dict[str, EnhancedToolMetadata]:
        """
        Select tools for multiple tasks (async batch processing)
        
        Uses single Claude API call for efficient batch selection when batch_mode=True.
        Falls back to individual selection if batch fails or batch_mode=False.
        
        Args:
            tasks: List of Task objects (from core.task_models)
            batch_mode: Use single Claude call for all tasks (more efficient)
            api_key: Optional Anthropic API key (uses ANTHROPIC_API_KEY env var if not provided)
        
        Returns:
            Dict mapping task_id -> selected tool
        
        Examples:
            >>> selector = ToolSelector()
            >>> tasks = [task1, task2, task3]
            >>> selections = await selector.select_tools_for_tasks(tasks)
            >>> print(selections)
            {
                "task_1_id": EnhancedToolMetadata(name="file_reader", ...),
                "task_2_id": EnhancedToolMetadata(name="file_editor", ...),
                ...
            }
        
        Notes:
            - Requires Anthropic SDK installed
            - Batch mode is significantly faster for >3 tasks
            - Automatically falls back to individual selection on errors
        """
        if batch_mode:
            try:
                return await self._batch_select_with_claude(tasks, api_key)
            except Exception as e:
                logger.warning(f"Batch selection failed ({e}), falling back to individual selection")
                return await self._individual_select_async(tasks)
        else:
            return await self._individual_select_async(tasks)
    
    async def _batch_select_with_claude(
        self,
        tasks: List[Any],
        api_key: Optional[str] = None
    ) -> Dict[str, EnhancedToolMetadata]:
        """
        Batch select tools using single Claude API call
        
        More token-efficient for multiple tasks (single request vs N requests).
        Uses structured JSON output for deterministic parsing.
        """
        # Get Anthropic client
        Anthropic, AsyncAnthropic = _get_anthropic_clients()
        if AsyncAnthropic is None:
            raise ImportError("Anthropic SDK required for batch selection. Install: pip install anthropic")
        
        # Initialize async client
        api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY required for LLM-powered batch selection")
        
        client = AsyncAnthropic(api_key=api_key)
        
        # Get available tools
        available_tools = self.registry.list_tools()
        tools_summary = self._build_tools_summary(available_tools)
        
        # Build task descriptions
        task_descriptions = []
        task_id_map = {}
        
        for i, task in enumerate(tasks):
            task_id = getattr(task, 'id', f"task_{i}")
            task_id_map[task_id] = task
            
            task_desc = getattr(task, 'description', str(task))
            task_type = getattr(task, 'type', 'unknown')
            
            # Extract requirements if available
            requirements = {}
            if hasattr(task, 'requirements'):
                req = task.requirements
                requirements = {
                    'agent_type': getattr(req, 'agent_type', 'unknown'),
                    'tools': getattr(req, 'tools', []),
                    'inputs': getattr(req, 'inputs', {})
                }
            
            task_descriptions.append(f"""
Task {i+1} (ID: {task_id}):
  Description: {task_desc}
  Type: {task_type}
  Requirements: {json.dumps(requirements, indent=2)}
""")
        
        # Build prompt with structured output instructions
        prompt = f"""You are an expert tool selector. Select the BEST tool for each task.

AVAILABLE TOOLS:
{tools_summary}

TASKS TO ANALYZE:
{''.join(task_descriptions)}

SELECTION CRITERIA:
1. Match tool capabilities to task requirements
2. Prefer specialized tools over generic ones
3. Consider input parameters available
4. Prioritize tools with exact capability match

RESPONSE FORMAT (JSON only):
{{
  "task_id_1": "tool_name",
  "task_id_2": "tool_name",
  ...
}}

IMPORTANT: Respond with ONLY valid JSON. No markdown, no explanations."""
        
        try:
            # Call Claude with structured output
            response = await client.messages.create(
                model="claude-3-5-haiku-20241022",
                max_tokens=2048,
                temperature=0,  # Deterministic selection
                messages=[{"role": "user", "content": prompt}]
            )
            
            # Extract and parse response
            response_text = response.content[0].text.strip()
            
            # Handle markdown code blocks if present
            if "```json" in response_text:
                json_text = response_text.split("```json")[1].split("```")[0].strip()
            elif "```" in response_text:
                json_text = response_text.split("```")[1].split("```")[0].strip()
            else:
                json_text = response_text
            
            # Parse JSON
            selections_json = json.loads(json_text)
            
            # Map to ToolMetadata objects
            selections = {}
            for task_id, tool_name in selections_json.items():
                tool = self.registry.get_tool(tool_name)
                if tool:
                    selections[task_id] = tool
                else:
                    logger.warning(f"Tool '{tool_name}' not found for task '{task_id}'")
            
            logger.info(f"Batch selected {len(selections)}/{len(tasks)} tools via Claude")
            return selections
            
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse Claude response as JSON: {e}")
            raise
        except Exception as e:
            logger.error(f"Claude API call failed: {e}")
            raise
    
    async def _individual_select_async(self, tasks: List[Any]) -> Dict[str, EnhancedToolMetadata]:
        """
        Select tools individually (fallback)
        
        Less efficient but more robust. Used when batch selection unavailable or fails.
        """
        selections = {}
        
        for i, task in enumerate(tasks):
            task_id = getattr(task, 'id', f"task_{i}")
            task_desc = getattr(task, 'description', str(task))
            
            # Use synchronous selection
            tool = self.select_for_task(task_desc)
            if tool:
                selections[task_id] = tool
            else:
                logger.warning(f"No tool selected for task '{task_id}'")
        
        return selections
    
    def _build_tools_summary(self, tools: List[EnhancedToolMetadata]) -> str:
        """Build concise summary of available tools for LLM prompt"""
        summary_lines = []
        
        for tool in tools:
            caps = []
            if tool.capabilities.can_read:
                caps.append("read")
            if tool.capabilities.can_write:
                caps.append("write")
            if tool.capabilities.can_search:
                caps.append("search")
            if tool.capabilities.can_execute:
                caps.append("execute")
            
            summary_lines.append(
                f"- {tool.name}: {tool.description} | Capabilities: {', '.join(caps)}"
            )
        
        return "\n".join(summary_lines)
    
    def validate_tool_for_task(
        self,
        tool: EnhancedToolMetadata,
        task: Any,
        strict: bool = True
    ) -> Tuple[bool, List[str]]:
        """
        Validate if tool can execute task
        
        Checks:
        1. Required parameters are available
        2. Tool capabilities match task type
        3. Input types are compatible
        
        Args:
            tool: Tool to validate
            task: Task to execute (Task object from core.task_models)
            strict: Strict validation (fail on warnings)
        
        Returns:
            (is_valid, issues_list)
        
        Examples:
            >>> selector = ToolSelector()
            >>> tool = selector.registry.get_tool("file_reader")
            >>> valid, issues = selector.validate_tool_for_task(tool, task)
            >>> if not valid:
            ...     print(f"Validation failed: {issues}")
        """
        issues = []
        warnings = []
        
        # Extract task information
        task_type = getattr(task, 'type', None)
        task_requirements = getattr(task, 'requirements', None)
        
        # Check 1: Required parameters
        if task_requirements and tool.parameters:
            # Handle both dict and object parameter formats
            required_params = set()
            for p in tool.parameters:
                if isinstance(p, dict):
                    if p.get('required', False):
                        required_params.add(p['name'])
                else:
                    # Object with attributes
                    if getattr(p, 'required', False):
                        required_params.add(p.name)
            
            provided_params = set(task_requirements.inputs.keys())
            
            missing = required_params - provided_params
            if missing:
                issues.append(f"Missing required parameters: {missing}")
        
        # Check 2: Capability matching
        if task_type:
            task_type_value = getattr(task_type, 'value', str(task_type))
            
            if task_type_value == 'read' and not tool.capabilities.can_read:
                issues.append("Tool cannot read but task requires reading")
            
            if task_type_value == 'write' and not tool.capabilities.can_write:
                issues.append("Tool cannot write but task requires writing")
            
            if task_type_value == 'execute' and not tool.capabilities.can_execute:
                issues.append("Tool cannot execute but task requires execution")
        
        # Check 3: Tool-specific validation
        if hasattr(tool, 'validate_parameters'):
            try:
                params = task_requirements.inputs if task_requirements else {}
                valid, tool_issues = tool.validate_parameters(params)
                if not valid:
                    issues.extend(tool_issues)
            except Exception as e:
                warnings.append(f"Tool validation raised exception: {e}")
        
        # Warnings (non-critical)
        if task_requirements and not task_requirements.tools:
            warnings.append("Task has no explicit tool requirements")
        
        # Combine issues
        all_issues = issues + (warnings if strict else [])
        
        return (len(issues) == 0, all_issues)
    
    async def suggest_alternative_tools(
        self,
        task: Any,
        primary_tool: EnhancedToolMetadata,
        count: int = 2,
        exclude_failed: List[str] = None
    ) -> List[EnhancedToolMetadata]:
        """
        Suggest alternative tools if primary fails
        
        Uses requirement matching to find next-best tools.
        Excludes tools that already failed (avoid retry loops).
        
        Args:
            task: The task to execute
            primary_tool: Primary tool that failed/is unavailable
            count: Number of alternatives to suggest (default: 2)
            exclude_failed: List of tool names that already failed
        
        Returns:
            List of alternative tools, sorted by match score
        
        Examples:
            >>> selector = ToolSelector()
            >>> primary = selector.registry.get_tool("file_editor")
            >>> alternatives = await selector.suggest_alternative_tools(
            ...     task, primary, count=2, exclude_failed=["file_editor"]
            ... )
            >>> for alt in alternatives:
            ...     print(f"Try {alt.name} instead")
        
        Notes:
            - Returns empty list if no suitable alternatives
            - Alternatives are sorted by match score (best first)
            - Considers task requirements and capabilities
        """
        exclude_failed = exclude_failed or []
        exclude_names = set(exclude_failed + [primary_tool.name])
        
        # Extract task description and requirements
        task_desc = getattr(task, 'description', str(task))
        requirements = self.infer_requirements(task_desc)
        
        # Get all matching tools
        candidates = []
        for tool in self.registry.list_tools():
            if tool.name in exclude_names:
                continue  # Skip primary and failed tools
            
            score = tool.matches_requirements(requirements)
            if score > 0:
                candidates.append((score, tool))
        
        # Sort by score (descending)
        candidates.sort(reverse=True, key=lambda x: x[0])
        
        # Take top N
        alternatives = [tool for _, tool in candidates[:count]]
        
        logger.info(f"Found {len(alternatives)} alternatives for {primary_tool.name}")
        return alternatives


# Global selector instance
_selector: Optional[ToolSelector] = None


def get_tool_selector(use_llm: bool = False) -> ToolSelector:
    """
    Get global tool selector instance
    
    Args:
        use_llm: Use Claude for tool selection
    
    Returns:
        Singleton ToolSelector
    """
    global _selector
    if _selector is None:
        _selector = ToolSelector(use_llm_selection=use_llm)
    return _selector
