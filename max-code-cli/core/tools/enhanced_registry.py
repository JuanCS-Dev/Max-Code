"""
Enhanced Tool Registry with Smart Selection

Extends existing ToolRegistry with intelligent tool selection
using scoring + optional LLM-based selection.

Integrates with:
- Existing ToolRegistry (registry.py)
- UnifiedToolExecutor (executor_bridge.py)
- EnhancedToolMetadata (tool_metadata.py)

Biblical Foundation:
"O sábio escolhe o caminho certo" (Provérbios 16:9)

Soli Deo Gloria
"""

from typing import Dict, List, Optional, Any, Tuple
import logging
from pathlib import Path

from .tool_metadata import (
    EnhancedToolMetadata,
    ToolCategory,
    ToolCapabilities,
    ToolRequirements,
)
from .registry import get_registry, ToolRegistry
from .types import ToolMetadata as BaseToolMetadata

logger = logging.getLogger(__name__)


class EnhancedToolRegistry:
    """
    Enhanced tool registry with smart selection capabilities
    
    Wraps existing ToolRegistry and adds:
    - Enhanced metadata (capabilities, requirements)
    - Scoring-based tool selection
    - Optional LLM-based final selection
    - Auto-discovery from existing tools
    
    Examples:
        >>> registry = EnhancedToolRegistry()
        >>> registry.enhance_existing_tools()
        >>> 
        >>> # Smart selection
        >>> tool = registry.select_best_tool(
        ...     task_description="Find all TODO comments in code",
        ...     requirements={"needs_search": True, "has_pattern": True}
        ... )
        >>> print(tool.name)  # "grep_tool"
    """
    
    _instance: Optional["EnhancedToolRegistry"] = None
    
    def __new__(cls):
        """Singleton pattern"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        """Initialize enhanced registry"""
        if self._initialized:
            return
        
        self.base_registry: ToolRegistry = get_registry()
        self.enhanced_tools: Dict[str, EnhancedToolMetadata] = {}
        self.by_category: Dict[ToolCategory, List[str]] = {
            cat: [] for cat in ToolCategory
        }
        self._initialized = True
        
        logger.info("EnhancedToolRegistry initialized")
    
    def register_enhanced(self, metadata: EnhancedToolMetadata):
        """
        Register tool with enhanced metadata
        
        Args:
            metadata: EnhancedToolMetadata instance
        """
        self.enhanced_tools[metadata.name] = metadata
        self.by_category[metadata.category].append(metadata.name)
        
        logger.debug(f"Registered enhanced tool: {metadata.name}")
    
    def enhance_existing_tool(
        self,
        tool_name: str,
        category: ToolCategory,
        capabilities: Optional[ToolCapabilities] = None,
        requirements: Optional[ToolRequirements] = None,
        **kwargs
    ):
        """
        Enhance existing tool from base registry
        
        Args:
            tool_name: Name of tool in base registry
            category: Tool category
            capabilities: Tool capabilities (auto-inferred if None)
            requirements: Tool requirements (auto-inferred if None)
            **kwargs: Additional enhanced metadata
        """
        # Access internal _tools dict (base registry doesn't have get_tool method)
        base_tool = self.base_registry._tools.get(tool_name)
        if not base_tool:
            logger.warning(f"Tool '{tool_name}' not found in base registry")
            return
        
        enhanced = EnhancedToolMetadata.from_base_metadata(
            base_tool,
            category=category,
            capabilities=capabilities,
            requirements=requirements,
            **kwargs
        )
        
        self.register_enhanced(enhanced)
    
    def enhance_existing_tools(self):
        """
        Auto-enhance all existing tools from base registry
        
        Maps known tools to categories and infers metadata
        """
        # Map of tool names to categories (known tools)
        tool_categories = {
            "file_reader": ToolCategory.FILE_OPS,
            "file_writer": ToolCategory.FILE_OPS,
            "file_editor": ToolCategory.FILE_OPS,
            "glob_tool": ToolCategory.SEARCH,
            "grep_tool": ToolCategory.SEARCH,
        }
        
        # Enhanced metadata for known tools
        known_enhancements = {
            "file_reader": {
                "capabilities": ToolCapabilities(can_read=True),
                "requirements": ToolRequirements(requires_filepath=True),
                "tags": ["file", "read", "io"],
            },
            "file_writer": {
                "capabilities": ToolCapabilities(can_write=True),
                "requirements": ToolRequirements(requires_filepath=True, requires_content=True),
                "tags": ["file", "write", "create", "io"],
            },
            "file_editor": {
                "capabilities": ToolCapabilities(can_write=True),
                "requirements": ToolRequirements(requires_filepath=True, requires_content=True),
                "tags": ["file", "edit", "modify", "io"],
            },
            "glob_tool": {
                "capabilities": ToolCapabilities(can_search=True),
                "requirements": ToolRequirements(requires_pattern=True),
                "tags": ["search", "find", "pattern", "glob"],
            },
            "grep_tool": {
                "capabilities": ToolCapabilities(can_search=True),
                "requirements": ToolRequirements(requires_pattern=True),
                "tags": ["search", "grep", "regex", "content"],
            },
        }
        
        # Enhance each known tool
        for tool_name, category in tool_categories.items():
            enhancements = known_enhancements.get(tool_name, {})
            self.enhance_existing_tool(
                tool_name,
                category,
                capabilities=enhancements.get("capabilities"),
                requirements=enhancements.get("requirements"),
                tags=enhancements.get("tags", []),
            )
        
        logger.info(f"Enhanced {len(self.enhanced_tools)} existing tools")
    
    def get_tool(self, name: str) -> Optional[EnhancedToolMetadata]:
        """Get enhanced tool by name"""
        return self.enhanced_tools.get(name)
    
    def list_tools(
        self,
        category: Optional[ToolCategory] = None
    ) -> List[EnhancedToolMetadata]:
        """
        List all tools, optionally filtered by category
        
        Args:
            category: Optional category filter
        
        Returns:
            List of EnhancedToolMetadata
        """
        if category:
            tool_names = self.by_category.get(category, [])
            return [self.enhanced_tools[name] for name in tool_names]
        return list(self.enhanced_tools.values())
    
    def select_best_tool(
        self,
        task_description: str,
        requirements: Dict[str, Any],
        use_llm: bool = False,
        top_n: int = 3
    ) -> Optional[EnhancedToolMetadata]:
        """
        Select best tool for task using scoring + optionally LLM
        
        Algorithm:
        1. Score all tools against requirements
        2. Filter tools with score > 0
        3. Sort by score (descending)
        4. If use_llm and multiple candidates: use Claude for final selection
        5. Return top tool
        
        Args:
            task_description: Description of what to do
            requirements: Task requirements dict with keys:
                - needs_read: bool
                - needs_write: bool
                - needs_execute: bool
                - needs_search: bool
                - has_filepath: bool
                - has_pattern: bool
                - tags: List[str]
            use_llm: Use Claude for final selection among top candidates
            top_n: Number of top candidates to consider for LLM selection
        
        Returns:
            Best matching tool or None if no match
        
        Examples:
            >>> registry = EnhancedToolRegistry()
            >>> registry.enhance_existing_tools()
            >>> 
            >>> tool = registry.select_best_tool(
            ...     "Find all TODO comments",
            ...     {"needs_search": True, "has_pattern": True}
            ... )
            >>> print(tool.name)  # "grep_tool"
        """
        if not self.enhanced_tools:
            logger.warning("No enhanced tools available for selection")
            return None
        
        # Step 1: Score all tools
        scores: List[Tuple[float, EnhancedToolMetadata]] = []
        for tool in self.enhanced_tools.values():
            score = tool.matches_requirements(requirements)
            if score > 0:
                scores.append((score, tool))
        
        if not scores:
            logger.info("No tools matched requirements")
            return None
        
        # Step 2: Sort by score
        scores.sort(reverse=True, key=lambda x: x[0])
        
        # Apply preference boosts
        if requirements.get('prefers_editor') and any(s[1].name == 'file_editor' for s in scores):
            # Boost file_editor if preferred
            for i, (score, tool) in enumerate(scores):
                if tool.name == 'file_editor':
                    scores[i] = (score + 0.5, tool)
        
        if requirements.get('prefers_grep') and any(s[1].name == 'grep_tool' for s in scores):
            # Boost grep_tool if preferred
            for i, (score, tool) in enumerate(scores):
                if tool.name == 'grep_tool':
                    scores[i] = (score + 0.5, tool)
        
        if requirements.get('prefers_glob') and any(s[1].name == 'glob_tool' for s in scores):
            # Boost glob_tool if preferred
            for i, (score, tool) in enumerate(scores):
                if tool.name == 'glob_tool':
                    scores[i] = (score + 0.5, tool)
        
        # Re-sort after boosts
        scores.sort(reverse=True, key=lambda x: x[0])
        
        logger.info(f"Found {len(scores)} matching tools")
        for score, tool in scores[:top_n]:
            logger.debug(f"  {tool.name}: {score:.2f}")
        
        # Step 3: If not using LLM or only one candidate, return top scorer
        if not use_llm or len(scores) == 1:
            best_tool = scores[0][1]
            logger.info(f"Selected tool: {best_tool.name} (score: {scores[0][0]:.2f})")
            return best_tool
        
        # Step 4: Use Claude to select from top N candidates
        top_candidates = scores[:top_n]
        selected = self._llm_select(task_description, top_candidates)
        logger.info(f"LLM selected tool: {selected.name}")
        return selected
    
    def _llm_select(
        self,
        task_description: str,
        candidates: List[Tuple[float, EnhancedToolMetadata]]
    ) -> EnhancedToolMetadata:
        """
        Use Claude to select best tool from candidates
        
        Args:
            task_description: Task description
            candidates: List of (score, tool) tuples
        
        Returns:
            Selected tool (fallback to top scorer if LLM fails)
        """
        try:
            from anthropic import Anthropic
            import os
            
            client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
            
            # Build prompt
            tool_descriptions = []
            for i, (score, tool) in enumerate(candidates, 1):
                caps = tool.capabilities
                reqs = tool.requirements
                
                tool_descriptions.append(f"""
{i}. **{tool.name}** (score: {score:.2f})
   Description: {tool.description}
   Category: {tool.category.value}
   Capabilities: read={caps.can_read}, write={caps.can_write}, execute={caps.can_execute}, search={caps.can_search}
   Requirements: filepath={reqs.requires_filepath}, pattern={reqs.requires_pattern}, content={reqs.requires_content}
   Tags: {', '.join(tool.tags)}
""")
            
            prompt = f"""Given this task: "{task_description}"

Select the BEST tool from these candidates:

{''.join(tool_descriptions)}

Respond with ONLY the number (1, 2, or 3) of the best tool for this specific task.
"""
            
            response = client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=10,
                messages=[{"role": "user", "content": prompt}]
            )
            
            # Parse response
            selection_text = response.content[0].text.strip()
            selection = int(selection_text)
            
            if 1 <= selection <= len(candidates):
                return candidates[selection - 1][1]
            
        except Exception as e:
            logger.warning(f"LLM selection failed: {e}, falling back to top scorer")
        
        # Fallback to top scorer
        return candidates[0][1]
    
    def get_tools_for_anthropic(
        self,
        category: Optional[ToolCategory] = None
    ) -> List[Dict[str, Any]]:
        """
        Get tools in Anthropic API format
        
        Args:
            category: Optional category filter
        
        Returns:
            List of tool schemas for Anthropic API
        """
        tools = self.list_tools(category)
        return [tool.to_anthropic_schema() for tool in tools]
    
    def execute_tool(
        self,
        tool_name: str,
        **kwargs
    ) -> Any:
        """
        Execute tool through UnifiedToolExecutor
        
        Args:
            tool_name: Name of tool to execute
            **kwargs: Tool parameters
        
        Returns:
            Tool result
        """
        from .executor_bridge import UnifiedToolExecutor
        
        executor = UnifiedToolExecutor()
        return executor.execute_tool(tool_name, kwargs)


# Global enhanced registry instance
_enhanced_registry: Optional[EnhancedToolRegistry] = None


def get_enhanced_registry() -> EnhancedToolRegistry:
    """
    Get global enhanced registry instance
    
    Returns:
        Singleton EnhancedToolRegistry
    """
    global _enhanced_registry
    if _enhanced_registry is None:
        _enhanced_registry = EnhancedToolRegistry()
        _enhanced_registry.enhance_existing_tools()
    return _enhanced_registry
