"""
Enhanced Tool Metadata for Smart Selection

Extends existing ToolMetadata (types.py) with capabilities,
requirements, and scoring for intelligent tool selection.

Biblical Foundation:
"Quem é sábio? Aquele que aprende de todos" (Pirkei Avot 4:1)

Soli Deo Gloria
"""

from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional
from enum import Enum

from .types import ToolMetadata as BaseToolMetadata, ToolParameter as BaseToolParameter


class ToolCategory(Enum):
    """Tool categories for organization"""
    FILE_OPS = "file_operations"
    CODE_GEN = "code_generation"
    SEARCH = "search"
    EXECUTION = "execution"
    VALIDATION = "validation"
    ANALYSIS = "analysis"


@dataclass
class ToolCapabilities:
    """
    Tool capability flags for smart selection
    
    Used by ToolSelector to match task requirements
    """
    can_read: bool = False
    can_write: bool = False
    can_execute: bool = False
    can_search: bool = False
    can_analyze: bool = False
    can_validate: bool = False


@dataclass
class ToolRequirements:
    """
    Context requirements for tool execution
    
    Defines what inputs the tool expects
    """
    requires_filepath: bool = False
    requires_directory: bool = False
    requires_pattern: bool = False
    requires_command: bool = False
    requires_content: bool = False
    requires_offset: bool = False


@dataclass
class ToolPerformance:
    """
    Performance characteristics
    
    Used for optimization and user expectations
    """
    estimated_time: int = 5  # seconds
    safe: bool = True  # Can run without confirmation
    destructive: bool = False  # Modifies files/data
    expensive: bool = False  # High resource usage


@dataclass
class EnhancedToolMetadata:
    """
    Enhanced tool metadata for smart selection
    
    Extends base ToolMetadata with capabilities, requirements,
    and scoring capabilities for intelligent tool selection.
    
    Examples:
        >>> metadata = EnhancedToolMetadata(
        ...     name="file_reader",
        ...     description="Read file contents",
        ...     category=ToolCategory.FILE_OPS,
        ...     capabilities=ToolCapabilities(can_read=True),
        ...     requirements=ToolRequirements(requires_filepath=True)
        ... )
        >>> score = metadata.matches_requirements({"needs_read": True})
        >>> print(score)  # 1.0 (perfect match)
    """
    
    # Basic metadata (compatible with BaseToolMetadata)
    name: str
    description: str
    category: ToolCategory
    
    # Enhanced metadata
    capabilities: ToolCapabilities = field(default_factory=ToolCapabilities)
    requirements: ToolRequirements = field(default_factory=ToolRequirements)
    performance: ToolPerformance = field(default_factory=ToolPerformance)
    
    # Parameters (compatible with Anthropic schema)
    parameters: List[Dict[str, Any]] = field(default_factory=list)
    
    # Examples and tags
    examples: List[Dict[str, Any]] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)
    
    # Version info
    version: str = "1.0.0"
    
    def to_anthropic_schema(self) -> Dict[str, Any]:
        """
        Convert to Anthropic tool schema format
        
        Returns:
            Dict compatible with Anthropic API tool use
        """
        properties = {}
        required = []
        
        for param in self.parameters:
            param_name = param.get("name")
            properties[param_name] = {
                "type": param.get("type", "string"),
                "description": param.get("description", "")
            }
            
            if param.get("enum"):
                properties[param_name]["enum"] = param["enum"]
            
            if param.get("required", False):
                required.append(param_name)
        
        return {
            "name": self.name,
            "description": self.description,
            "input_schema": {
                "type": "object",
                "properties": properties,
                "required": required
            }
        }
    
    def matches_requirements(self, requirements: Dict[str, Any]) -> float:
        """
        Calculate match score for task requirements
        
        Args:
            requirements: Task requirements dict with keys like:
                - needs_read: bool
                - needs_write: bool
                - needs_execute: bool
                - needs_search: bool
                - has_filepath: bool
                - has_pattern: bool
                - tags: List[str]
        
        Returns:
            Match score from 0.0 (no match) to 1.0 (perfect match)
        
        Examples:
            >>> metadata = EnhancedToolMetadata(
            ...     name="grep",
            ...     description="Search in files",
            ...     category=ToolCategory.SEARCH,
            ...     capabilities=ToolCapabilities(can_search=True),
            ...     requirements=ToolRequirements(requires_pattern=True),
            ...     tags=["search", "regex"]
            ... )
            >>> score = metadata.matches_requirements({
            ...     "needs_search": True,
            ...     "has_pattern": True,
            ...     "tags": ["search"]
            ... })
            >>> print(score)  # High score (3 matches)
        """
        score = 0.0
        checks = 0
        
        # Check capability requirements
        capability_checks = [
            ('needs_read', self.capabilities.can_read),
            ('needs_write', self.capabilities.can_write),
            ('needs_execute', self.capabilities.can_execute),
            ('needs_search', self.capabilities.can_search),
            ('needs_analyze', self.capabilities.can_analyze),
            ('needs_validate', self.capabilities.can_validate),
        ]
        
        for req_key, has_capability in capability_checks:
            if requirements.get(req_key):
                checks += 1
                if has_capability:
                    score += 1.0
        
        # Check context requirements
        context_checks = [
            ('has_filepath', self.requirements.requires_filepath),
            ('has_directory', self.requirements.requires_directory),
            ('has_pattern', self.requirements.requires_pattern),
            ('has_command', self.requirements.requires_command),
            ('has_content', self.requirements.requires_content),
        ]
        
        for req_key, needs_context in context_checks:
            if requirements.get(req_key):
                checks += 1
                if needs_context:
                    score += 1.0
        
        # Check tags overlap
        if 'tags' in requirements and requirements['tags']:
            req_tags = set(requirements['tags'])
            tool_tags = set(self.tags)
            overlap = req_tags & tool_tags
            if overlap:
                checks += 1
                # Score based on percentage of requested tags matched
                score += len(overlap) / len(req_tags)
        
        # Return normalized score
        return score / checks if checks > 0 else 0.0
    
    @classmethod
    def from_base_metadata(
        cls,
        base: BaseToolMetadata,
        category: ToolCategory,
        capabilities: Optional[ToolCapabilities] = None,
        requirements: Optional[ToolRequirements] = None,
        **kwargs
    ) -> "EnhancedToolMetadata":
        """
        Create enhanced metadata from existing base metadata
        
        Args:
            base: Base ToolMetadata from types.py
            category: Tool category
            capabilities: Tool capabilities (auto-inferred if None)
            requirements: Tool requirements (auto-inferred if None)
            **kwargs: Additional enhanced metadata fields
        
        Returns:
            EnhancedToolMetadata instance
        """
        # Auto-infer capabilities from tool name if not provided
        if capabilities is None:
            capabilities = cls._infer_capabilities(base.name, base.description)
        
        # Auto-infer requirements from parameters if not provided
        if requirements is None:
            requirements = cls._infer_requirements(base.schema.parameters if hasattr(base, 'schema') else [])
        
        # Extract tags from base (avoiding duplicate)
        base_tags = base.tags if hasattr(base, 'tags') else []
        provided_tags = kwargs.pop('tags', [])
        merged_tags = list(set(base_tags + provided_tags))
        
        return cls(
            name=base.name,
            description=base.description,
            category=category,
            capabilities=capabilities,
            requirements=requirements,
            tags=merged_tags,
            version=base.version if hasattr(base, 'version') else "1.0.0",
            **kwargs
        )
    
    @staticmethod
    def _infer_capabilities(name: str, description: str) -> ToolCapabilities:
        """
        Infer capabilities from tool name and description
        
        Args:
            name: Tool name
            description: Tool description
        
        Returns:
            ToolCapabilities inferred from metadata
        """
        text = (name + " " + description).lower()
        
        return ToolCapabilities(
            can_read="read" in text or "get" in text or "fetch" in text,
            can_write="write" in text or "create" in text or "edit" in text or "update" in text,
            can_execute="execute" in text or "run" in text or "bash" in text,
            can_search="search" in text or "find" in text or "grep" in text or "glob" in text,
            can_analyze="analyze" in text or "inspect" in text or "parse" in text,
            can_validate="validate" in text or "check" in text or "test" in text,
        )
    
    @staticmethod
    def _infer_requirements(parameters: List[Any]) -> ToolRequirements:
        """
        Infer requirements from parameter list
        
        Args:
            parameters: List of tool parameters
        
        Returns:
            ToolRequirements inferred from parameters
        """
        param_names = [
            p.name if hasattr(p, 'name') else str(p)
            for p in parameters
        ]
        param_text = " ".join(param_names).lower()
        
        return ToolRequirements(
            requires_filepath="path" in param_text or "file" in param_text,
            requires_directory="dir" in param_text or "folder" in param_text,
            requires_pattern="pattern" in param_text or "regex" in param_text,
            requires_command="command" in param_text or "cmd" in param_text,
            requires_content="content" in param_text or "text" in param_text or "data" in param_text,
            requires_offset="offset" in param_text or "limit" in param_text,
        )
