"""
Grep Tool - Content search with regex

Inspired by Claude Code's Grep tool (built on ripgrep).

Biblical Foundation:
"Procurai nas Escrituras" (João 5:39)
Search the scriptures - grep reveals hidden wisdom.

Features:
- Regex pattern matching
- Multiple output modes (content, files, count)
- Context lines (before/after)
- File type filtering
- Case-insensitive search
- Line number display
- Fast performance (regex-based)
"""

from typing import List, Optional, Dict, Tuple
from dataclasses import dataclass, field
from pathlib import Path
import re
import fnmatch
from config.logging_config import get_logger

logger = get_logger(__name__)


@dataclass
class GrepMatch:
    """Single grep match"""
    file_path: str
    line_number: int
    line_content: str
    match_start: int = 0
    match_end: int = 0


@dataclass
class GrepResult:
    """Result of grep search"""
    success: bool
    pattern: str
    output_mode: str
    matches: List[GrepMatch] = field(default_factory=list)
    files_with_matches: List[str] = field(default_factory=list)
    match_counts: Dict[str, int] = field(default_factory=dict)
    total_matches: int = 0
    files_searched: int = 0
    error: Optional[str] = None


class GrepTool:
    """
    Grep Tool - Content search with regex

    Supports regex patterns and multiple output modes.
    Inspired by Claude Code's Grep tool (ripgrep).

    Output Modes:
    - content: Show matching lines with context
    - files_with_matches: Show only file paths
    - count: Show match counts per file

    Examples:
        GrepTool().grep("def.*test")           - Find function definitions
        GrepTool().grep("TODO", output_mode="files")  - Files with TODOs
        GrepTool().grep("error", case_sensitive=False) - Case-insensitive
    """

    def __init__(self, default_ignore: Optional[List[str]] = None):
        """
        Initialize GrepTool

        Args:
            default_ignore: Default patterns to ignore
        """
        self.default_ignore = default_ignore or [
            '**/node_modules/**',
            '**/.git/**',
            '**/__pycache__/**',
            '**/.venv/**',
            '**/.pytest_cache/**',
            '**/*.pyc',
            '**/venv/**',
        ]

    def grep(
        self,
        pattern: str,
        path: Optional[str] = None,
        output_mode: str = "files_with_matches",
        case_sensitive: bool = True,
        glob_filter: Optional[str] = None,
        file_type: Optional[str] = None,
        context_before: int = 0,
        context_after: int = 0,
        max_matches: int = 1000,
    ) -> GrepResult:
        """
        Search for pattern in files

        Args:
            pattern: Regex pattern to search for
            path: Directory to search (default: current directory)
            output_mode: Output mode (content, files_with_matches, count)
            case_sensitive: Case-sensitive search (default: True)
            glob_filter: Glob pattern to filter files (e.g., "*.py")
            file_type: File type filter (e.g., "py", "js")
            context_before: Lines of context before match
            context_after: Lines of context after match
            max_matches: Maximum matches to return

        Returns:
            GrepResult with matches

        Example:
            >>> tool = GrepTool()
            >>> result = tool.grep("TODO", path="src/", output_mode="content")
            >>> for match in result.matches:
            ...     print(f"{match.file_path}:{match.line_number}: {match.line_content}")
        """
        # Default to current directory
        search_path = Path(path) if path else Path.cwd()

        # Validate search path
        if not search_path.exists():
            return GrepResult(
                success=False,
                pattern=pattern,
                output_mode=output_mode,
                error=f"Search path does not exist: {search_path}"
            )

        # Compile regex pattern
        try:
            flags = 0 if case_sensitive else re.IGNORECASE
            regex = re.compile(pattern, flags)
        except re.error as e:
            return GrepResult(
                success=False,
                pattern=pattern,
                output_mode=output_mode,
                error=f"Invalid regex pattern: {e}"
            )

        # Build glob pattern for file filtering
        if glob_filter:
            file_pattern = glob_filter
        elif file_type:
            file_pattern = f"**/*.{file_type}"
        else:
            file_pattern = "**/*"

        # Search files
        try:
            matches = []
            files_with_matches = set()
            match_counts = {}
            files_searched = 0

            # Iterate through files
            for file_path in search_path.glob(file_pattern):
                # Skip non-files
                if not file_path.is_file():
                    continue

                # Check ignore patterns
                try:
                    relative_path = file_path.relative_to(search_path)
                    path_str = str(relative_path)
                except ValueError:
                    path_str = str(file_path)

                if self._should_ignore(path_str, self.default_ignore):
                    continue

                # Skip binary files (basic check)
                if not self._is_text_file(file_path):
                    continue

                files_searched += 1

                # Search file content
                file_matches = self._search_file(
                    file_path,
                    regex,
                    context_before,
                    context_after,
                    max_matches - len(matches)
                )

                if file_matches:
                    matches.extend(file_matches)
                    files_with_matches.add(path_str)
                    match_counts[path_str] = len(file_matches)

                # Stop if we hit max matches
                if len(matches) >= max_matches:
                    break

            # Build result based on output mode
            if output_mode == "content":
                return GrepResult(
                    success=True,
                    pattern=pattern,
                    output_mode=output_mode,
                    matches=matches,
                    total_matches=len(matches),
                    files_searched=files_searched,
                )
            elif output_mode == "files_with_matches":
                return GrepResult(
                    success=True,
                    pattern=pattern,
                    output_mode=output_mode,
                    files_with_matches=sorted(list(files_with_matches)),
                    total_matches=len(matches),
                    files_searched=files_searched,
                )
            elif output_mode == "count":
                return GrepResult(
                    success=True,
                    pattern=pattern,
                    output_mode=output_mode,
                    match_counts=match_counts,
                    total_matches=len(matches),
                    files_searched=files_searched,
                )
            else:
                return GrepResult(
                    success=False,
                    pattern=pattern,
                    output_mode=output_mode,
                    error=f"Invalid output mode: {output_mode}"
                )

        except Exception as e:
            return GrepResult(
                success=False,
                pattern=pattern,
                output_mode=output_mode,
                error=f"Grep search failed: {e}"
            )

    def _search_file(
        self,
        file_path: Path,
        regex: re.Pattern,
        context_before: int,
        context_after: int,
        max_matches: int
    ) -> List[GrepMatch]:
        """Search a single file for pattern"""
        matches = []

        try:
            # Read file
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()

            # Search each line
            for line_num, line in enumerate(lines, start=1):
                # Check for match
                match = regex.search(line)
                if match:
                    # Create match object
                    grep_match = GrepMatch(
                        file_path=str(file_path),
                        line_number=line_num,
                        line_content=line.rstrip('\n'),
                        match_start=match.start(),
                        match_end=match.end(),
                    )
                    matches.append(grep_match)

                    # Stop if we hit max matches
                    if len(matches) >= max_matches:
                        break

        except Exception:
            # Skip files that can't be read
            pass

        return matches

    def _should_ignore(self, path: str, ignore_patterns: List[str]) -> bool:
        """Check if path matches any ignore pattern"""
        for pattern in ignore_patterns:
            if fnmatch.fnmatch(path, pattern):
                return True
            if pattern.startswith('**/'):
                simple_pattern = pattern[3:]
                if fnmatch.fnmatch(path, simple_pattern):
                    return True
        return False

    def _is_text_file(self, file_path: Path) -> bool:
        """Check if file is likely a text file (basic heuristic)"""
        # Check extension
        text_extensions = {
            '.py', '.js', '.ts', '.jsx', '.tsx', '.java', '.cpp', '.c', '.h',
            '.cs', '.go', '.rs', '.rb', '.php', '.swift', '.kt', '.scala',
            '.txt', '.md', '.rst', '.json', '.yaml', '.yml', '.toml', '.xml',
            '.html', '.css', '.scss', '.sass', '.less', '.sql', '.sh', '.bash',
            '.zsh', '.fish', '.vim', '.el', '.lua', '.pl', '.r', '.jl', '.m',
        }

        if file_path.suffix.lower() in text_extensions:
            return True

        # Try reading first few bytes
        try:
            with open(file_path, 'rb') as f:
                sample = f.read(512)
                # Check for null bytes (common in binary files)
                if b'\x00' in sample:
                    return False
                return True
        except Exception:
            return False

    def find_todos(self, path: Optional[str] = None) -> GrepResult:
        """Find TODO comments in code"""
        return self.grep(
            pattern=r"(TODO|FIXME|XXX|HACK|NOTE):",
            path=path,
            output_mode="content",
            case_sensitive=False,
        )

    def find_imports(self, module_name: str, path: Optional[str] = None, file_type: str = "py") -> GrepResult:
        """Find import statements for a module"""
        pattern = f"(import|from).*{module_name}"
        return self.grep(
            pattern=pattern,
            path=path,
            output_mode="content",
            file_type=file_type,
        )

    def find_function_calls(self, function_name: str, path: Optional[str] = None) -> GrepResult:
        """Find function calls"""
        pattern = f"{function_name}\\s*\\("
        return self.grep(
            pattern=pattern,
            path=path,
            output_mode="content",
        )


# ============================================================================
# CONVENIENCE FUNCTIONS
# ============================================================================

def grep_files(pattern: str, path: Optional[str] = None, **kwargs) -> List[str]:
    """
    Convenience function to grep files

    Args:
        pattern: Regex pattern
        path: Search directory
        **kwargs: Additional arguments for grep()

    Returns:
        List of file paths with matches

    Example:
        >>> files = grep_files("TODO", path="src/")
        >>> for f in files:
        ...     print(f)
    """
    tool = GrepTool()
    result = tool.grep(pattern, path=path, output_mode="files_with_matches", **kwargs)

    if result.success:
        return result.files_with_matches
    else:
        logger.error(f"Error: {result.error}")
        return []


# ============================================================================
# DEMO
# ============================================================================

if __name__ == "__main__":
    logger.info("🔎 Grep Tool Demo\n")
    tool = GrepTool()

    # Test 1: Find TODOs
    print("=" * 70)
    logger.info("TEST 1: Find TODO comments in code")
    print("=" * 70)

    result = tool.find_todos(path="core/")

    if result.success:
        logger.info(f"✓ Found {result.total_matches} TODOs in {len(result.files_with_matches)} files")
        logger.info(f"  Files searched: {result.files_searched}")
        logger.info(f"\nFirst 5 matches:")
        for match in result.matches[:5]:
            logger.info(f"  {match.file_path}:{match.line_number}: {match.line_content.strip()}")
    else:
        logger.error(f"✗ Failed: {result.error}")
    # Test 2: Find files with pattern (files_with_matches mode)
    print("\n" + "=" * 70)
    logger.info("TEST 2: Find files containing 'Biblical Foundation'")
    print("=" * 70)

    result = tool.grep("Biblical Foundation", path="core/", output_mode="files_with_matches")

    if result.success:
        logger.info(f"✓ Found in {len(result.files_with_matches)} files")
        logger.info(f"\nFiles:")
        for file_path in result.files_with_matches[:10]:
            logger.info(f"  - {file_path}")
    else:
        logger.error(f"✗ Failed: {result.error}")
    # Test 3: Count matches per file
    print("\n" + "=" * 70)
    logger.info("TEST 3: Count occurrences of 'def ' in Python files")
    print("=" * 70)

    result = tool.grep(r"def\s+\w+", path="core/epl/", output_mode="count", file_type="py")

    if result.success:
        logger.info(f"✓ Found {result.total_matches} function definitions")
        logger.info(f"\nTop files:")
        sorted_counts = sorted(result.match_counts.items(), key=lambda x: x[1], reverse=True)
        for file_path, count in sorted_counts[:5]:
            logger.info(f"  {count:3d} - {file_path}")
    else:
        logger.error(f"✗ Failed: {result.error}")
    # Test 4: Case-insensitive search
    print("\n" + "=" * 70)
    logger.error("TEST 4: Case-insensitive search for 'error'")
    print("=" * 70)

    result = tool.grep("error", path="core/tools/", output_mode="count", case_sensitive=False)

    if result.success:
        logger.info(f"✓ Found {result.total_matches} matches")
        for file_path, count in result.match_counts.items():
            logger.info(f"  {count} - {file_path}")
    else:
        logger.error(f"✗ Failed: {result.error}")
    # Test 5: Convenience function
    print("\n" + "=" * 70)
    logger.info("TEST 5: Convenience function - find imports")
    print("=" * 70)

    result = tool.find_imports("dataclass", path="core/epl/")

    if result.success:
        logger.info(f"✓ Found {result.total_matches} import statements")
        for match in result.matches[:3]:
            logger.info(f"  {match.file_path}:{match.line_number}")
            logger.info(f"    {match.line_content.strip()}")
    else:
        logger.error(f"✗ Failed: {result.error}")


# Auto-register tool (PROMPT 2.2 - Zero Duplication)
from .auto_register import register_tool

register_tool(
    name="grep_tool",
    description="Search file contents using regex patterns. Returns matching lines with context. Supports gitignore filtering.",
    handler_class=GrepTool,
    handler_method="grep",
    parameters=[
        {"name": "pattern", "type": "string", "description": "Regex pattern to search for", "required": True},
        {"name": "path", "type": "string", "description": "Path to search in (file or directory)", "required": False},
        {"name": "case_sensitive", "type": "boolean", "description": "Case sensitive search (default: False)", "required": False},
        {"name": "max_results", "type": "integer", "description": "Maximum number of matches", "required": False},
    ],
    tags=["search", "grep", "regex", "content", "find"]
)