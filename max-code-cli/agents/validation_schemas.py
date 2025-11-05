"""
Agent Task Parameter Validation Schemas

Pydantic v2 schemas for validating agent task parameters.
Ensures type safety and input validation following 2025 best practices.

Biblical Foundation:
"Examinai tudo. Retende o bem" (1 Tessalonicenses 5:21)
Validate all inputs - ensure data integrity before processing.
"""

from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field, field_validator, ConfigDict
from enum import Enum


# =============================================================================
# Base Validation Models
# =============================================================================

class TaskParametersBase(BaseModel):
    """Base model for all task parameters with common validation"""
    model_config = ConfigDict(
        str_strip_whitespace=True,
        validate_assignment=True,
        extra='allow'  # Allow extra fields for extensibility
    )


# =============================================================================
# Code Agent Parameters
# =============================================================================

class CodeAgentParameters(TaskParametersBase):
    """
    Parameters for Code Generation Agent.

    All fields optional - description comes from AgentTask.description
    """
    language: Optional[str] = Field(
        default="python",
        pattern="^(python|javascript|typescript|java|go|rust)$",
        description="Target programming language"
    )
    style: Optional[str] = Field(
        default="clean",
        description="Code style (clean, functional, oop, etc.)"
    )
    max_lines: Optional[int] = Field(
        default=100,
        ge=1,
        le=1000,
        description="Maximum number of lines"
    )
    context: Optional[str] = Field(
        default=None,
        description="Additional context for code generation"
    )
    requirements: Optional[List[str]] = Field(
        default_factory=list,
        description="List of specific requirements"
    )


# =============================================================================
# Review Agent Parameters
# =============================================================================

class ReviewAgentParameters(TaskParametersBase):
    """
    Parameters for Code Review Agent.

    Required: code
    Optional: context, review_type
    """
    code: str = Field(
        ...,  # Required
        min_length=1,
        max_length=100000,  # 100KB max
        description="Code to review"
    )
    context: Optional[Dict[str, Any]] = Field(
        default_factory=dict,
        description="Review context (author, PR number, etc.)"
    )
    review_type: Optional[str] = Field(
        default="full",
        pattern="^(full|security|style|performance)$",
        description="Type of review to perform"
    )

    @field_validator('code')
    @classmethod
    def code_not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Code cannot be empty")
        return v


# =============================================================================
# Test Agent Parameters
# =============================================================================

class TestAgentParameters(TaskParametersBase):
    """
    Parameters for Test Generation Agent.

    Required: function_code
    Optional: test_framework, coverage_threshold
    """
    function_code: str = Field(
        ...,  # Required
        min_length=1,
        max_length=50000,  # 50KB max
        description="Function code to test"
    )
    test_framework: Optional[str] = Field(
        default="pytest",
        pattern="^(pytest|unittest|nose2|doctest)$",
        description="Test framework to use"
    )
    coverage_threshold: Optional[float] = Field(
        default=0.80,
        ge=0.0,
        le=1.0,
        description="Target code coverage (0.0-1.0)"
    )

    @field_validator('function_code')
    @classmethod
    def function_code_not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Function code cannot be empty")
        return v


# =============================================================================
# Fix Agent Parameters
# =============================================================================

class FixAgentParameters(TaskParametersBase):
    """
    Parameters for Bug Fix Agent.

    Required: code, error
    Optional: context
    """
    code: str = Field(
        ...,  # Required
        min_length=1,
        max_length=100000,
        description="Broken code to fix"
    )
    error: str = Field(
        ...,  # Required
        min_length=1,
        max_length=10000,
        description="Error message or trace"
    )
    context: Optional[Dict[str, Any]] = Field(
        default_factory=dict,
        description="Additional debugging context"
    )

    @field_validator('code', 'error')
    @classmethod
    def not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Field cannot be empty")
        return v


# =============================================================================
# Docs Agent Parameters
# =============================================================================

class CodeChange(BaseModel):
    """Represents a code change for documentation"""
    file_path: str = Field(..., min_length=1)
    change_type: str = Field(..., pattern="^(added|modified|deleted|renamed)$")
    description: str = Field(..., min_length=1)
    lines_changed: Optional[int] = Field(default=0, ge=0)


class DocsAgentParameters(TaskParametersBase):
    """
    Parameters for Documentation Agent.

    Required: changes or code
    Optional: doc_type, style
    """
    changes: Optional[List[CodeChange]] = Field(
        default_factory=list,
        description="List of code changes to document"
    )
    code: Optional[str] = Field(
        default=None,
        description="Code to document (alternative to changes)"
    )
    doc_type: Optional[str] = Field(
        default="standard",
        pattern="^(standard|narrative|api|tutorial)$",
        description="Type of documentation"
    )
    style: Optional[str] = Field(
        default="technical",
        description="Documentation style"
    )
    context: Optional[Dict[str, Any]] = Field(
        default_factory=dict,
        description="Additional context"
    )

    @field_validator('changes', mode='after')
    @classmethod
    def changes_or_code_required(cls, v: List[CodeChange], info) -> List[CodeChange]:
        """Ensure either changes or code is provided"""
        if not v and not info.data.get('code'):
            raise ValueError("Either 'changes' or 'code' must be provided")
        return v


# =============================================================================
# Architect Agent Parameters
# =============================================================================

class ArchitectAgentParameters(TaskParametersBase):
    """
    Parameters for System Architect Agent.

    Required: requirements
    Optional: constraints, architecture_style
    """
    requirements: List[str] = Field(
        ...,  # Required
        min_length=1,
        description="System requirements"
    )
    constraints: Optional[List[str]] = Field(
        default_factory=list,
        description="System constraints"
    )
    architecture_style: Optional[str] = Field(
        default="microservices",
        pattern="^(monolith|microservices|serverless|event-driven)$",
        description="Architecture style"
    )

    @field_validator('requirements')
    @classmethod
    def requirements_not_empty(cls, v: List[str]) -> List[str]:
        if not v or all(not req.strip() for req in v):
            raise ValueError("Requirements cannot be empty")
        return [req.strip() for req in v if req.strip()]


# =============================================================================
# Plan Agent Parameters
# =============================================================================

class PlanAgentParameters(TaskParametersBase):
    """
    Parameters for Planning Agent.

    Required: goal
    Optional: constraints, timeline
    """
    goal: str = Field(
        ...,  # Required
        min_length=10,
        max_length=1000,
        description="Planning goal"
    )
    constraints: Optional[List[str]] = Field(
        default_factory=list,
        description="Planning constraints"
    )
    timeline: Optional[str] = Field(
        default=None,
        description="Target timeline (e.g., '2 weeks')"
    )

    @field_validator('goal')
    @classmethod
    def goal_not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Goal cannot be empty")
        return v


# =============================================================================
# Explore Agent Parameters
# =============================================================================

class ExploreAgentParameters(TaskParametersBase):
    """
    Parameters for Codebase Exploration Agent.

    Required: query or target
    Optional: scope, depth
    """
    query: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=500,
        description="Exploration query"
    )
    target: Optional[str] = Field(
        default=None,
        description="Target file/directory to explore"
    )
    scope: Optional[str] = Field(
        default="full",
        pattern="^(full|quick|deep)$",
        description="Exploration scope"
    )
    depth: Optional[int] = Field(
        default=3,
        ge=1,
        le=10,
        description="Directory depth to explore"
    )

    @field_validator('query', mode='after')
    @classmethod
    def query_or_target_required(cls, v: Optional[str], info) -> Optional[str]:
        """Ensure either query or target is provided"""
        if not v and not info.data.get('target'):
            raise ValueError("Either 'query' or 'target' must be provided")
        return v


# =============================================================================
# Sleep Agent Parameters
# =============================================================================

class SleepAgentParameters(TaskParametersBase):
    """
    Parameters for End-of-Day Sleep Agent.

    All fields optional - uses defaults
    """
    include_maximus: Optional[bool] = Field(
        default=True,
        description="Include MAXIMUS session summary"
    )
    create_snapshot: Optional[bool] = Field(
        default=True,
        description="Create session snapshot"
    )
    run_cleanup: Optional[bool] = Field(
        default=True,
        description="Run cleanup tasks"
    )


# =============================================================================
# Validation Helper Functions
# =============================================================================

def validate_task_parameters(agent_type: str, parameters: Dict[str, Any]) -> BaseModel:
    """
    Validate task parameters based on agent type.

    Args:
        agent_type: Type of agent (code, review, test, fix, docs, architect, plan, explore, sleep)
        parameters: Raw parameters dictionary

    Returns:
        Validated Pydantic model

    Raises:
        ValueError: If agent_type is unknown
        pydantic.ValidationError: If parameters are invalid
    """
    schema_map = {
        'code': CodeAgentParameters,
        'code_agent': CodeAgentParameters,
        'review': ReviewAgentParameters,
        'review_agent': ReviewAgentParameters,
        'test': TestAgentParameters,
        'test_agent': TestAgentParameters,
        'fix': FixAgentParameters,
        'fix_agent': FixAgentParameters,
        'docs': DocsAgentParameters,
        'docs_agent': DocsAgentParameters,
        'architect': ArchitectAgentParameters,
        'architect_agent': ArchitectAgentParameters,
        'plan': PlanAgentParameters,
        'plan_agent': PlanAgentParameters,
        'explore': ExploreAgentParameters,
        'explore_agent': ExploreAgentParameters,
        'sleep': SleepAgentParameters,
        'sleep_agent': SleepAgentParameters,
    }

    agent_key = agent_type.lower().replace('-', '_')
    if agent_key not in schema_map:
        raise ValueError(f"Unknown agent type: {agent_type}. Valid types: {list(set(schema_map.keys()))}")

    schema = schema_map[agent_key]
    return schema(**parameters)


def get_schema_for_agent(agent_type: str) -> type[BaseModel]:
    """
    Get Pydantic schema class for agent type.

    Args:
        agent_type: Type of agent

    Returns:
        Pydantic schema class
    """
    schema_map = {
        'code': CodeAgentParameters,
        'review': ReviewAgentParameters,
        'test': TestAgentParameters,
        'fix': FixAgentParameters,
        'docs': DocsAgentParameters,
        'architect': ArchitectAgentParameters,
        'plan': PlanAgentParameters,
        'explore': ExploreAgentParameters,
        'sleep': SleepAgentParameters,
    }

    agent_key = agent_type.lower().replace('-', '_').replace('_agent', '')
    return schema_map.get(agent_key, TaskParametersBase)


__all__ = [
    'TaskParametersBase',
    'CodeAgentParameters',
    'ReviewAgentParameters',
    'TestAgentParameters',
    'FixAgentParameters',
    'DocsAgentParameters',
    'ArchitectAgentParameters',
    'PlanAgentParameters',
    'ExploreAgentParameters',
    'SleepAgentParameters',
    'CodeChange',
    'validate_task_parameters',
    'get_schema_for_agent',
]
