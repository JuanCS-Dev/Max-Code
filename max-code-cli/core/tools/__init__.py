"""
Tools Framework - Anthropic SDK-style tool management

Biblical Foundation:
"Dá-me entendimento, e guardarei a tua lei" (Salmos 119:34)
Understanding through tools - wisdom in action.

Features:
- @tool decorator (Anthropic SDK pattern)
- Tool registry and discovery
- Type-safe tool schemas
- Automatic validation

File Tools:
- FileReader: Read files with line ranges
- FileWriter: Write files atomically
- FileEditor: Edit files with exact replacements
- GlobTool: Pattern-based file search
- GrepTool: Content search with regex
"""

from .file_reader import (
    FileReader,
    FileReadResult,
    read_file,
)

from .file_writer import (
    FileWriter,
    FileWriteResult,
    write_file,
)

from .file_editor import (
    FileEditor,
    FileEditResult,
    edit_file,
)

from .glob_tool import (
    GlobTool,
    GlobResult,
    glob_files,
)

from .grep_tool import (
    GrepTool,
    GrepResult,
    GrepMatch,
    grep_files,
)

# Tool decorator and framework (FASE 2.1)
from .types import (
    ToolResult,
    ToolContent,
    ToolResultType,
    ToolSchema,
    ToolParameter,
    ToolMetadata,
)

from .registry import (
    ToolRegistry,
    get_registry,
    ToolRegistryError,
    ToolNotFoundError,
    ToolAlreadyRegisteredError,
)

from .decorator import (
    tool,
    beta_tool,
    text_tool,
    file_tool,
    async_tool,
)

# Unified Tool Executor Bridge (FASE 11 - Constitutional integration)
from .executor_bridge import (
    UnifiedToolExecutor,
    get_unified_executor,
    execute_tool_unified,
)

__all__ = [
    # Tool Framework (FASE 2.1)
    'tool',
    'beta_tool',
    'text_tool',
    'file_tool',
    'async_tool',
    'ToolResult',
    'ToolContent',
    'ToolResultType',
    'ToolSchema',
    'ToolParameter',
    'ToolMetadata',
    'ToolRegistry',
    'get_registry',
    'ToolRegistryError',
    'ToolNotFoundError',
    'ToolAlreadyRegisteredError',

    # FileReader
    'FileReader',
    'FileReadResult',
    'read_file',

    # FileWriter
    'FileWriter',
    'FileWriteResult',
    'write_file',

    # FileEditor
    'FileEditor',
    'FileEditResult',
    'edit_file',

    # GlobTool
    'GlobTool',
    'GlobResult',
    'glob_files',

    # GrepTool
    'GrepTool',
    'GrepResult',
    'GrepMatch',
    'grep_files',

    # Unified Executor Bridge (FASE 11)
    'UnifiedToolExecutor',
    'get_unified_executor',
    'execute_tool_unified',
]

__version__ = '2.1.0'  # FASE 11: Unified Tool Executor Bridge
