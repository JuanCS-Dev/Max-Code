"""
File Tools - Complete file operation suite

Biblical Foundation:
"Dá-me entendimento, e guardarei a tua lei" (Salmos 119:34)
Understanding through tools - wisdom in action.

Tools:
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

__all__ = [
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
]

__version__ = '1.0.0'
