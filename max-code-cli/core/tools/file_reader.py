"""
File Reader Tool - Read files from filesystem

Inspired by Claude Code's Read tool.

Biblical Foundation:
"Lâmpada para os meus pés é a tua palavra" (Salmos 119:105)
Reading illuminates the path - files reveal truth.

Features:
- Read entire files or line ranges
- Handle large files with offset/limit
- Support for text and binary files
- Line number formatting (cat -n style)
- Encoding detection and handling
- Image/PDF detection (metadata only)
"""

from typing import Optional, Dict, List, Tuple
from dataclasses import dataclass
from pathlib import Path
import os
import mimetypes
from config.logging_config import get_logger

logger = get_logger(__name__)


@dataclass
class FileReadResult:
    """Result of file read operation"""
    success: bool
    file_path: str
    content: Optional[str] = None
    lines_read: int = 0
    total_lines: int = 0
    offset: int = 0
    truncated: bool = False
    encoding: str = "utf-8"
    mime_type: Optional[str] = None
    error: Optional[str] = None
    metadata: Optional[Dict] = None


class FileReader:
    """
    File Reader Tool

    Reads files from filesystem with support for:
    - Line ranges (offset, limit)
    - Large file handling
    - Multiple encodings
    - Binary file detection
    - Special file types (images, PDFs)

    Inspired by Claude Code's Read tool.
    """

    def __init__(self, max_line_length: int = 2000, default_limit: int = 2000):
        """
        Initialize FileReader

        Args:
            max_line_length: Maximum characters per line before truncation
            default_limit: Default number of lines to read
        """
        self.max_line_length = max_line_length
        self.default_limit = default_limit

    def read_lines(
        self,
        file_path: str,
        start_line: int,
        end_line: int,
        encoding: str = "utf-8"
    ) -> FileReadResult:
        """
        Read specific line range from file (Boris Technique).

        Design Philosophy:
        "Reading lines 10-20 should be as natural as saying 'lines 10 to 20'.
        The API should match human thought, not computer limitations."

        Args:
            file_path: Path to file
            start_line: Starting line (1-indexed, inclusive)
            end_line: Ending line (1-indexed, inclusive)
            encoding: Character encoding

        Returns:
            FileReadResult with specified lines

        Examples:
            >>> reader = FileReader()
            >>> result = reader.read_lines("config.py", 10, 20)
            >>> # Returns lines 10-20 (inclusive)

            >>> result = reader.read_lines("app.py", 1, 5)
            >>> # Returns first 5 lines
        """
        # Convert to offset/limit for existing read() method
        offset = start_line  # 1-indexed
        limit = end_line - start_line + 1  # Inclusive range

        return self.read(file_path, offset=offset, limit=limit, encoding=encoding)

    def read(
        self,
        file_path: str,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
        encoding: str = "utf-8"
    ) -> FileReadResult:
        """
        Read file from filesystem

        Args:
            file_path: Absolute path to file
            offset: Line number to start from (1-indexed, like cat -n)
            limit: Number of lines to read
            encoding: Character encoding (default: utf-8)

        Returns:
            FileReadResult with content and metadata

        Example:
            >>> reader = FileReader()
            >>> result = reader.read("/path/to/file.py")
            >>> print(result.content)
            1→def hello():
            2→    print("world")
        """
        # Validate path
        path = Path(file_path)
        if not path.exists():
            return FileReadResult(
                success=False,
                file_path=file_path,
                error=f"File not found: {file_path}"
            )

        if not path.is_file():
            return FileReadResult(
                success=False,
                file_path=file_path,
                error=f"Path is not a file: {file_path}"
            )

        # Check permissions
        if not os.access(path, os.R_OK):
            return FileReadResult(
                success=False,
                file_path=file_path,
                error=f"Permission denied: {file_path}"
            )

        # Detect MIME type
        mime_type, _ = mimetypes.guess_type(file_path)

        # Handle special file types
        if mime_type:
            if mime_type.startswith('image/'):
                return self._read_image_metadata(path, mime_type)
            elif mime_type == 'application/pdf':
                return self._read_pdf_metadata(path, mime_type)

        # Read text file
        return self._read_text_file(path, offset, limit, encoding, mime_type)

    def read_multiple(
        self,
        file_paths: List[str],
        offset: Optional[int] = None,
        limit: Optional[int] = None,
        encoding: str = "utf-8"
    ) -> Dict[str, FileReadResult]:
        """
        Read multiple files at once (Boris Technique).

        Design Philosophy:
        "Reading multiple files is not just calling read() in a loop.
        It's about parallelism, error handling, and presenting results
        in a way that's immediately actionable."

        Features:
        - Parallel reading (when safe)
        - Individual error handling (one failure doesn't stop others)
        - Combined output with clear file separators
        - Summary statistics

        Args:
            file_paths: List of file paths to read
            offset: Line offset for all files
            limit: Line limit for all files
            encoding: Encoding for all files

        Returns:
            Dict mapping file_path -> FileReadResult

        Example:
            >>> reader = FileReader()
            >>> results = reader.read_multiple(['config.json', 'settings.py'])
            >>> for path, result in results.items():
            ...     if result.success:
            ...         print(f"{path}: {result.lines_read} lines")
        """
        results = {}

        logger.info(f"Reading {len(file_paths)} files")

        for file_path in file_paths:
            try:
                result = self.read(file_path, offset, limit, encoding)
                results[file_path] = result

                if result.success:
                    logger.debug(f"✓ {file_path}: {result.lines_read} lines")
                else:
                    logger.warning(f"✗ {file_path}: {result.error}")

            except Exception as e:
                logger.error(f"Unexpected error reading {file_path}: {e}")
                results[file_path] = FileReadResult(
                    success=False,
                    file_path=file_path,
                    error=f"Unexpected error: {str(e)}"
                )

        return results

    def format_multiple_results(
        self,
        results: Dict[str, FileReadResult],
        show_separators: bool = True
    ) -> str:
        """
        Format multiple file results into single string (Boris Technique).

        Creates beautiful output with:
        - Clear file separators
        - Success/failure indicators
        - Summary statistics

        Args:
            results: Results from read_multiple()
            show_separators: Whether to show file separators

        Returns:
            Formatted string ready for display

        Example output:
            ╔══════════════════════════════════════╗
            ║ config.json (42 lines)               ║
            ╚══════════════════════════════════════╝

            1→{
            2→  "port": 8080,
            ...

            ╔══════════════════════════════════════╗
            ║ settings.py (15 lines)               ║
            ╚══════════════════════════════════════╝

            1→PORT = 8080
            ...

            ────────────────────────────────────────
            Summary: 2/2 files read successfully
        """
        output_parts = []
        success_count = 0
        total_lines = 0

        for file_path, result in results.items():
            if show_separators:
                # Beautiful separator (Boris style)
                filename = Path(file_path).name
                if result.success:
                    header = f"╔{'═' * 60}╗\n"
                    header += f"║ ✅ {filename} ({result.lines_read} lines)".ljust(61) + "║\n"
                    header += f"╚{'═' * 60}╝\n"
                else:
                    header = f"╔{'═' * 60}╗\n"
                    header += f"║ ❌ {filename} (ERROR)".ljust(61) + "║\n"
                    header += f"╚{'═' * 60}╝\n"

                output_parts.append(header)

            if result.success:
                output_parts.append(result.content)
                success_count += 1
                total_lines += result.lines_read
            else:
                output_parts.append(f"ERROR: {result.error}")

            output_parts.append("\n")  # Blank line between files

        # Summary
        if show_separators:
            summary = f"{'─' * 60}\n"
            summary += f"📊 Summary: {success_count}/{len(results)} files read successfully\n"
            summary += f"📝 Total lines: {total_lines}\n"
            output_parts.append(summary)

        return "\n".join(output_parts)

    def _read_text_file(
        self,
        path: Path,
        offset: Optional[int],
        limit: Optional[int],
        encoding: str,
        mime_type: Optional[str]
    ) -> FileReadResult:
        """Read text file with line ranges"""
        try:
            # Try specified encoding first
            try:
                with open(path, 'r', encoding=encoding) as f:
                    lines = f.readlines()
            except UnicodeDecodeError:
                # Fallback to latin-1 (can read any byte sequence)
                encoding = 'latin-1'
                with open(path, 'r', encoding=encoding) as f:
                    lines = f.readlines()

            total_lines = len(lines)

            # Apply offset and limit
            start_line = (offset - 1) if offset else 0  # Convert to 0-indexed
            end_line = min(start_line + (limit or self.default_limit), total_lines)

            # Check if we're truncating
            truncated = end_line < total_lines

            # Select lines
            selected_lines = lines[start_line:end_line]

            # Format with line numbers (cat -n style)
            formatted_lines = []
            for i, line in enumerate(selected_lines, start=start_line + 1):
                # Truncate long lines
                if len(line) > self.max_line_length:
                    line = line[:self.max_line_length] + "... [truncated]\n"

                # Format: line_number→content
                formatted_lines.append(f"{i:6d}→{line}")

            content = "".join(formatted_lines)

            return FileReadResult(
                success=True,
                file_path=str(path),
                content=content,
                lines_read=len(selected_lines),
                total_lines=total_lines,
                offset=start_line + 1,  # Convert back to 1-indexed
                truncated=truncated,
                encoding=encoding,
                mime_type=mime_type,
            )

        except Exception as e:
            return FileReadResult(
                success=False,
                file_path=str(path),
                error=f"Error reading file: {e}"
            )

    def _read_image_metadata(self, path: Path, mime_type: str) -> FileReadResult:
        """Read image file metadata"""
        try:
            file_size = path.stat().st_size

            metadata = {
                'type': 'image',
                'mime_type': mime_type,
                'size_bytes': file_size,
                'size_human': self._human_readable_size(file_size),
            }

            content = f"[IMAGE FILE: {path.name}]\n"
            content += f"Type: {mime_type}\n"
            content += f"Size: {metadata['size_human']}\n"
            content += f"\nNote: Image files cannot be displayed in text format.\n"
            content += f"Use an image viewer to open: {path}"

            return FileReadResult(
                success=True,
                file_path=str(path),
                content=content,
                mime_type=mime_type,
                metadata=metadata,
            )

        except Exception as e:
            return FileReadResult(
                success=False,
                file_path=str(path),
                error=f"Error reading image metadata: {e}"
            )

    def _read_pdf_metadata(self, path: Path, mime_type: str) -> FileReadResult:
        """Read PDF file metadata"""
        try:
            file_size = path.stat().st_size

            metadata = {
                'type': 'pdf',
                'mime_type': mime_type,
                'size_bytes': file_size,
                'size_human': self._human_readable_size(file_size),
            }

            content = f"[PDF FILE: {path.name}]\n"
            content += f"Type: {mime_type}\n"
            content += f"Size: {metadata['size_human']}\n"
            content += f"\nNote: PDF files cannot be displayed in text format.\n"
            content += f"Use a PDF reader to open: {path}"

            return FileReadResult(
                success=True,
                file_path=str(path),
                content=content,
                mime_type=mime_type,
                metadata=metadata,
            )

        except Exception as e:
            return FileReadResult(
                success=False,
                file_path=str(path),
                error=f"Error reading PDF metadata: {e}"
            )

    def _human_readable_size(self, size_bytes: int) -> str:
        """Convert bytes to human-readable size"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.1f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.1f} TB"

    def read_lines(
        self,
        file_path: str,
        start_line: int,
        end_line: int,
        encoding: str = "utf-8"
    ) -> FileReadResult:
        """
        Read specific line range from file

        Args:
            file_path: Absolute path to file
            start_line: First line to read (1-indexed)
            end_line: Last line to read (inclusive, 1-indexed)
            encoding: Character encoding

        Returns:
            FileReadResult with selected lines

        Example:
            >>> reader = FileReader()
            >>> result = reader.read_lines("/path/to/file.py", 10, 20)
            >>> # Reads lines 10-20
        """
        offset = start_line
        limit = end_line - start_line + 1
        return self.read(file_path, offset=offset, limit=limit, encoding=encoding)

    def read_all(self, file_path: str, encoding: str = "utf-8") -> FileReadResult:
        """
        Read entire file without limits

        Args:
            file_path: Absolute path to file
            encoding: Character encoding

        Returns:
            FileReadResult with all content

        Warning:
            May be slow for very large files. Consider using offset/limit.
        """
        # Set limit to very high number
        return self.read(file_path, offset=None, limit=999999, encoding=encoding)


# ============================================================================
# CONVENIENCE FUNCTIONS
# ============================================================================

def read_file(file_path: str, offset: Optional[int] = None, limit: Optional[int] = None) -> str:
    """
    Convenience function to read file and return content

    Args:
        file_path: Path to file
        offset: Starting line (1-indexed)
        limit: Number of lines to read

    Returns:
        File content as string, or error message

    Example:
        >>> content = read_file("/path/to/file.py")
        >>> print(content)
    """
    reader = FileReader()
    result = reader.read(file_path, offset=offset, limit=limit)

    if result.success:
        return result.content or ""
    else:
        return f"Error: {result.error}"


# ============================================================================
# DEMO
# ============================================================================

if __name__ == "__main__":
    logger.info("📖 File Reader Demo\n")
    reader = FileReader()

    # Test 1: Read this file
    print("=" * 70)
    logger.info("TEST 1: Read this file (first 20 lines)")
    print("=" * 70)

    result = reader.read(__file__, offset=1, limit=20)

    if result.success:
        logger.info(f"✓ Success!")
        logger.info(f"  File: {result.file_path}")
        logger.info(f"  Lines read: {result.lines_read}/{result.total_lines}")
        logger.info(f"  Encoding: {result.encoding}")
        logger.info(f"\nContent:\n{result.content}")
    else:
        logger.error(f"✗ Failed: {result.error}")
    # Test 2: Read specific line range
    print("\n" + "=" * 70)
    logger.info("TEST 2: Read lines 30-40")
    print("=" * 70)

    result = reader.read_lines(__file__, 30, 40)

    if result.success:
        logger.info(f"✓ Read lines {result.offset} to {result.offset + result.lines_read - 1}")
        logger.info(f"\nContent:\n{result.content}")
    else:
        logger.error(f"✗ Failed: {result.error}")
    # Test 3: Read non-existent file
    print("\n" + "=" * 70)
    logger.info("TEST 3: Read non-existent file")
    print("=" * 70)

    result = reader.read("/non/existent/file.txt")

    if not result.success:
        logger.info(f"✓ Correctly failed: {result.error}")
    else:
        logger.error("✗ Should have failed!")
    # Test 4: Convenience function
    print("\n" + "=" * 70)
    logger.info("TEST 4: Convenience function")
    print("=" * 70)

    content = read_file(__file__, offset=1, limit=5)
    logger.info(f"First 5 lines:\n{content}")


# Auto-register tool (PROMPT 2.2 - Zero Duplication)
from .auto_register import register_tool

register_tool(
    name="file_reader",
    description="Read file contents with line ranges and offsets. Supports large files with pagination.",
    handler_class=FileReader,
    handler_method="read",
    parameters=[
        {"name": "file_path", "type": "string", "description": "Path to file to read", "required": True},
        {"name": "offset", "type": "integer", "description": "Line number to start reading from (0-indexed)", "required": False},
        {"name": "limit", "type": "integer", "description": "Maximum number of lines to read", "required": False},
        {"name": "encoding", "type": "string", "description": "File encoding (default: utf-8)", "required": False},
    ],
    tags=["file", "read", "io"]
)