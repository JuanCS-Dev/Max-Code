"""
Tool Executor Bridge - Unifica /core/tools/ com ToolExecutor

Problema identificado:
- /core/tools/ tem @tool decorator + ToolRegistry (interface limpa)
- /core/deter_agent/execution/tool_executor.py tem Constitutional validation + self-correction
- São incompatíveis!

Solução:
- Este bridge faz tools do /core/tools/ usarem ToolExecutor internamente
- Mantém interface limpa do @tool decorator
- Adiciona Constitutional validation + audit + self-correction automaticamente

Biblical Foundation:
"Dois são melhor que um... se caírem, um levanta ao companheiro" (Eclesiastes 4:9-10)
Unificação através da colaboração.
"""

from typing import Dict, Any, Optional
from pathlib import Path
import sys

# Import both systems
from .types import ToolResult as NewToolResult
from .registry import get_registry

# Import ToolExecutor (old system)
deter_path = Path(__file__).parent.parent / "deter_agent" / "execution"
if str(deter_path) not in sys.path:
    sys.path.insert(0, str(deter_path))

from core.deter_agent.execution.tool_executor import (
    ToolExecutor,
    Tool as OldTool,
    ToolType,
    ToolResult as OldToolResult,
    ToolStatus
)

from config.logging_config import get_logger

logger = get_logger(__name__)


class UnifiedToolExecutor:
    """
    Executor unificado que combina:
    - Interface do /core/tools/ (@tool decorator)
    - Constitutional validation do ToolExecutor

    Fluxo:
    1. Tool registrada via @tool decorator
    2. UnifiedToolExecutor converte para OldTool
    3. Executa via ToolExecutor (Constitutional + self-correction)
    4. Converte resultado de volta para NewToolResult
    """

    def __init__(self, safe_mode: bool = True, enable_self_correction: bool = True):
        """
        Initialize unified executor

        Args:
            safe_mode: Enable Constitutional validation (P2, P5)
            enable_self_correction: Enable self-correction loops (P5)
        """
        self.tool_executor = ToolExecutor(
            safe_mode=safe_mode,
            enable_self_correction=enable_self_correction
        )
        self.registry = get_registry()

        logger.info("🔗 Unified Tool Executor initialized (bridge active)")

    def execute_tool(
        self,
        tool_name: str,
        args: Dict[str, Any],
        validate: bool = True
    ) -> NewToolResult:
        """
        Execute tool with Constitutional validation

        Args:
            tool_name: Name of tool to execute
            args: Tool arguments
            validate: Enable Constitutional validation (default: True)

        Returns:
            NewToolResult with execution result

        Process:
            1. Get tool from new registry
            2. Convert to old Tool format
            3. Execute via ToolExecutor (Constitutional validation)
            4. Convert result back to NewToolResult
        """
        # Get tool from new registry
        tool_metadata = self.registry.get(tool_name)

        if not tool_metadata:
            return NewToolResult.error(f"Tool '{tool_name}' not found in registry")

        # Convert to old Tool format for ToolExecutor
        old_tool = self._convert_to_old_tool(tool_metadata, args)

        # Register with ToolExecutor if not already registered
        if tool_name not in self.tool_executor.registered_tools:
            self.tool_executor.register_tool(old_tool)

        # Execute via ToolExecutor (gets Constitutional validation + audit)
        old_result = self.tool_executor.execute(tool_name, parameters=args)

        # Convert result back to new format
        new_result = self._convert_to_new_result(old_result)

        return new_result

    def _convert_to_old_tool(self, tool_metadata, args: Dict[str, Any]) -> OldTool:
        """
        Convert new tool metadata to old Tool format

        Maps:
            - name → name
            - description → description
            - args → parameters
            - Infer ToolType from name/tags
        """
        # Infer ToolType from tool name or tags
        tool_type = self._infer_tool_type(tool_metadata)

        return OldTool(
            name=tool_metadata.name,
            type=tool_type,
            description=tool_metadata.description,
            parameters=args,
            requires_validation=True,  # Always validate (Constitutional AI)
            safe_mode=True,  # Always safe mode (P5)
            timeout=30.0  # Default timeout
        )

    def _infer_tool_type(self, tool_metadata) -> ToolType:
        """
        Infer ToolType from tool name or tags

        Mapping:
            - bash/shell → BASH
            - read/file_read → FILE_READ
            - write/file_write → FILE_WRITE
            - edit/file_edit → FILE_EDIT
            - glob/pattern → GLOB
            - grep/search → GREP
            - api/http/web → API_CALL
            - default → SEARCH (generic)
        """
        name_lower = tool_metadata.name.lower()
        tags_lower = [t.lower() for t in tool_metadata.tags]

        # Check name
        if "bash" in name_lower or "shell" in name_lower:
            return ToolType.BASH
        if "read" in name_lower and "file" in name_lower:
            return ToolType.FILE_READ
        if "write" in name_lower and "file" in name_lower:
            return ToolType.FILE_WRITE
        if "edit" in name_lower and "file" in name_lower:
            return ToolType.FILE_EDIT
        if "glob" in name_lower or "pattern" in name_lower:
            return ToolType.GLOB
        if "grep" in name_lower:
            return ToolType.GREP
        if "api" in name_lower or "http" in name_lower or "web" in name_lower:
            return ToolType.API_CALL

        # Check tags
        if "bash" in tags_lower or "shell" in tags_lower or "execution" in tags_lower:
            return ToolType.BASH
        if "file_operations" in tags_lower:
            if "read" in name_lower:
                return ToolType.FILE_READ
            if "write" in name_lower:
                return ToolType.FILE_WRITE
            if "edit" in name_lower:
                return ToolType.FILE_EDIT
        if "web" in tags_lower or "http" in tags_lower:
            return ToolType.API_CALL

        # Default
        return ToolType.SEARCH

    def _convert_to_new_result(self, old_result: OldToolResult) -> NewToolResult:
        """
        Convert old ToolResult to new ToolResult

        Maps:
            - SUCCESS → success type
            - FAILURE/TIMEOUT/BLOCKED → error type
            - output → content
            - error → error field
        """
        if old_result.status == ToolStatus.SUCCESS:
            return NewToolResult.success(
                content=str(old_result.output) if old_result.output else ""
            )
        else:
            error_msg = old_result.error or f"Execution failed with status: {old_result.status.value}"
            return NewToolResult.error(error_msg)

    def get_execution_history(self):
        """Get execution history from ToolExecutor (audit trail - P4)"""
        return self.tool_executor.execution_history

    def get_stats(self):
        """Get execution stats from ToolExecutor"""
        return self.tool_executor.stats


# ============================================================================
# GLOBAL INSTANCE
# ============================================================================

_unified_executor = None


def get_unified_executor(
    safe_mode: bool = True,
    enable_self_correction: bool = True
) -> UnifiedToolExecutor:
    """
    Get global unified executor instance (singleton)

    Args:
        safe_mode: Enable Constitutional validation
        enable_self_correction: Enable self-correction loops

    Returns:
        UnifiedToolExecutor instance
    """
    global _unified_executor

    if _unified_executor is None:
        _unified_executor = UnifiedToolExecutor(
            safe_mode=safe_mode,
            enable_self_correction=enable_self_correction
        )

    return _unified_executor


# ============================================================================
# CONVENIENCE FUNCTION FOR TOOL EXECUTION
# ============================================================================

async def execute_tool_unified(
    tool_name: str,
    args: Dict[str, Any],
    validate: bool = True
) -> NewToolResult:
    """
    Execute tool with Constitutional validation

    This is the main entry point for executing tools in the unified system.

    Args:
        tool_name: Name of tool to execute
        args: Tool arguments
        validate: Enable Constitutional validation (default: True)

    Returns:
        NewToolResult with execution result

    Example:
        >>> result = await execute_tool_unified(
        ...     "bash",
        ...     {"command": "ls -la"}
        ... )
        >>> if result.is_success:
        ...     print(result.content)
    """
    executor = get_unified_executor()
    return executor.execute_tool(tool_name, args, validate=validate)
