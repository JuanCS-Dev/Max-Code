"""
Tool Selector - High-level API for intelligent tool selection

Provides simple interface for agents to select and execute tools
based on natural language task descriptions.

Integrates:
- EnhancedToolRegistry (enhanced_registry.py)
- Task requirement inference from description
- Automatic tool selection and execution

Biblical Foundation:
"A sabedoria do prudente é entender o seu caminho" (Provérbios 14:8)

Soli Deo Gloria
"""

from typing import Dict, List, Any, Optional
import logging
import re

from .enhanced_registry import get_enhanced_registry, EnhancedToolRegistry
from .tool_metadata import EnhancedToolMetadata, ToolCategory
from .types import ToolResult

logger = logging.getLogger(__name__)


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
        # File path patterns: /path/to/file, ./file, ../file, file.ext
        has_filepath = bool(
            re.search(r'[./][\w/.-]+\.\w+', text) or  # ./path/file.ext
            re.search(r'\bfile\b.*\b\w+\.\w+\b', text)  # file config.json
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
