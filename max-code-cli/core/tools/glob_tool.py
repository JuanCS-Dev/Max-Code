"""
Glob Tool - Pattern-based file searching

Inspired by Claude Code's Glob tool.

Biblical Foundation:
"Buscai e achareis" (Mateus 7:7)
Seek and you shall find - glob reveals patterns.

Features:
- Glob pattern matching (**, *, ?, [])
- Recursive directory search
- File type filtering
- Sort by modification time
- Ignore patterns (.gitignore style)
- Fast performance (uses pathlib)
"""

from typing import List, Optional, Set
from dataclasses import dataclass
from pathlib import Path
import fnmatch
import os
from datetime import datetime


@dataclass
class GlobResult:
    """Result of glob search"""
    success: bool
    pattern: str
    matches: List[str] = None
    total_matches: int = 0
    search_path: str = "."
    ignored_count: int = 0
    error: Optional[str] = None

    def __post_init__(self):
        if self.matches is None:
            self.matches = []


class GlobTool:
    """
    Glob Tool - Pattern-based file searching

    Supports glob patterns:
    - ** : Match any number of directories
    - *  : Match any characters except /
    - ?  : Match single character
    - [] : Match character ranges

    Inspired by Claude Code's Glob tool.

    Examples:
        **/*.py          - All Python files recursively
        src/**/*.ts      - All TypeScript files in src/
        *.{js,ts}        - All JS or TS files in current dir
        test_*.py        - All test files starting with test_
    """

    def __init__(self, default_ignore: Optional[List[str]] = None):
        """
        Initialize GlobTool

        Args:
            default_ignore: Default patterns to ignore (like .gitignore)
        """
        self.default_ignore = default_ignore or [
            '**/node_modules/**',
            '**/.git/**',
            '**/__pycache__/**',
            '**/.venv/**',
            '**/.pytest_cache/**',
            '**/*.pyc',
            '**/.DS_Store',
            '**/venv/**',
            '**/.env',
        ]

    def glob(
        self,
        pattern: str,
        path: Optional[str] = None,
        ignore_patterns: Optional[List[str]] = None,
        sort_by_mtime: bool = True,
        max_results: int = 1000
    ) -> GlobResult:
        """
        Search for files matching pattern

        Args:
            pattern: Glob pattern (e.g., "**/*.py", "src/**/*.ts")
            path: Search directory (default: current directory)
            ignore_patterns: Additional patterns to ignore
            sort_by_mtime: Sort results by modification time (newest first)
            max_results: Maximum number of results to return

        Returns:
            GlobResult with matching file paths

        Example:
            >>> tool = GlobTool()
            >>> result = tool.glob("**/*.py", path="/my/project")
            >>> for file_path in result.matches:
            ...     print(file_path)
        """
        # Default to current directory
        search_path = Path(path) if path else Path.cwd()

        # Validate search path
        if not search_path.exists():
            return GlobResult(
                success=False,
                pattern=pattern,
                search_path=str(search_path),
                error=f"Search path does not exist: {search_path}"
            )

        if not search_path.is_dir():
            return GlobResult(
                success=False,
                pattern=pattern,
                search_path=str(search_path),
                error=f"Search path is not a directory: {search_path}"
            )

        # Combine ignore patterns
        all_ignore = self.default_ignore.copy()
        if ignore_patterns:
            all_ignore.extend(ignore_patterns)

        try:
            # Perform glob search
            matches = []
            ignored_count = 0

            # Use pathlib's glob (supports **)
            for match in search_path.glob(pattern):
                # Skip directories (only return files)
                if not match.is_file():
                    continue

                # Convert to relative path if possible
                try:
                    relative_path = match.relative_to(search_path)
                    path_str = str(relative_path)
                except ValueError:
                    # If relative path fails, use absolute
                    path_str = str(match)

                # Check ignore patterns
                if self._should_ignore(path_str, all_ignore):
                    ignored_count += 1
                    continue

                matches.append(path_str)

                # Stop if we hit max results
                if len(matches) >= max_results:
                    break

            # Sort by modification time if requested
            if sort_by_mtime and matches:
                matches = self._sort_by_mtime(matches, search_path)

            return GlobResult(
                success=True,
                pattern=pattern,
                matches=matches,
                total_matches=len(matches),
                search_path=str(search_path),
                ignored_count=ignored_count,
            )

        except Exception as e:
            return GlobResult(
                success=False,
                pattern=pattern,
                search_path=str(search_path),
                error=f"Glob search failed: {e}"
            )

    def _should_ignore(self, path: str, ignore_patterns: List[str]) -> bool:
        """Check if path matches any ignore pattern"""
        for pattern in ignore_patterns:
            # Use fnmatch for pattern matching
            if fnmatch.fnmatch(path, pattern):
                return True
            # Also check with leading **/ removed (for patterns like **/node_modules/**)
            if pattern.startswith('**/'):
                simple_pattern = pattern[3:]
                if fnmatch.fnmatch(path, simple_pattern):
                    return True
        return False

    def _sort_by_mtime(self, matches: List[str], base_path: Path) -> List[str]:
        """Sort matches by modification time (newest first)"""
        try:
            # Get modification times
            matches_with_mtime = []
            for match in matches:
                full_path = base_path / match
                if full_path.exists():
                    mtime = full_path.stat().st_mtime
                    matches_with_mtime.append((match, mtime))

            # Sort by mtime (descending)
            matches_with_mtime.sort(key=lambda x: x[1], reverse=True)

            # Return sorted paths
            return [path for path, _ in matches_with_mtime]

        except Exception:
            # If sorting fails, return unsorted
            return matches

    def find_by_extension(
        self,
        extension: str,
        path: Optional[str] = None,
        recursive: bool = True,
        **kwargs
    ) -> GlobResult:
        """
        Find files by extension

        Args:
            extension: File extension (e.g., "py", ".py", "ts")
            path: Search directory
            recursive: Search recursively
            **kwargs: Additional arguments for glob()

        Returns:
            GlobResult with matching files

        Example:
            >>> tool = GlobTool()
            >>> result = tool.find_by_extension("py", path="/my/project")
        """
        # Normalize extension
        if not extension.startswith('.'):
            extension = f".{extension}"

        # Build pattern
        if recursive:
            pattern = f"**/*{extension}"
        else:
            pattern = f"*{extension}"

        return self.glob(pattern, path=path, **kwargs)

    def find_by_name(
        self,
        name_pattern: str,
        path: Optional[str] = None,
        recursive: bool = True,
        **kwargs
    ) -> GlobResult:
        """
        Find files by name pattern

        Args:
            name_pattern: Name pattern (e.g., "test_*", "*_config.py")
            path: Search directory
            recursive: Search recursively
            **kwargs: Additional arguments for glob()

        Returns:
            GlobResult with matching files

        Example:
            >>> tool = GlobTool()
            >>> result = tool.find_by_name("test_*.py", path="/my/project")
        """
        # Build pattern
        if recursive:
            pattern = f"**/{name_pattern}"
        else:
            pattern = name_pattern

        return self.glob(pattern, path=path, **kwargs)


# ============================================================================
# CONVENIENCE FUNCTIONS
# ============================================================================

def glob_files(pattern: str, path: Optional[str] = None) -> List[str]:
    """
    Convenience function to glob files and return matches

    Args:
        pattern: Glob pattern
        path: Search directory (default: current directory)

    Returns:
        List of matching file paths

    Example:
        >>> files = glob_files("**/*.py")
        >>> for f in files:
        ...     print(f)
    """
    tool = GlobTool()
    result = tool.glob(pattern, path=path)

    if result.success:
        return result.matches
    else:
        print(f"Error: {result.error}")
        return []


# ============================================================================
# DEMO
# ============================================================================

if __name__ == "__main__":
    print("🔍 Glob Tool Demo\n")

    tool = GlobTool()

    # Test 1: Find all Python files in current project
    print("=" * 70)
    print("TEST 1: Find all Python files in core/tools/")
    print("=" * 70)

    result = tool.glob("*.py", path="core/tools/")

    if result.success:
        print(f"✓ Found {result.total_matches} files")
        print(f"  Ignored: {result.ignored_count}")
        print(f"\nMatches:")
        for i, match in enumerate(result.matches[:10], 1):
            print(f"  {i}. {match}")
        if result.total_matches > 10:
            print(f"  ... and {result.total_matches - 10} more")
    else:
        print(f"✗ Failed: {result.error}")

    # Test 2: Recursive search
    print("\n" + "=" * 70)
    print("TEST 2: Find all Python files recursively in core/")
    print("=" * 70)

    result = tool.glob("**/*.py", path="core/")

    if result.success:
        print(f"✓ Found {result.total_matches} files")
        print(f"\nFirst 10 matches:")
        for i, match in enumerate(result.matches[:10], 1):
            print(f"  {i}. {match}")
    else:
        print(f"✗ Failed: {result.error}")

    # Test 3: Find by extension
    print("\n" + "=" * 70)
    print("TEST 3: Find by extension (.py)")
    print("=" * 70)

    result = tool.find_by_extension("py", path="core/epl/", recursive=False)

    if result.success:
        print(f"✓ Found {result.total_matches} Python files in core/epl/")
        print(f"\nMatches:")
        for match in result.matches:
            print(f"  - {match}")
    else:
        print(f"✗ Failed: {result.error}")

    # Test 4: Find by name pattern
    print("\n" + "=" * 70)
    print("TEST 4: Find test files (test_*.py)")
    print("=" * 70)

    result = tool.find_by_name("test_*.py", path=".")

    if result.success:
        print(f"✓ Found {result.total_matches} test files")
        print(f"\nMatches:")
        for match in result.matches[:5]:
            print(f"  - {match}")
    else:
        print(f"✗ Failed: {result.error}")

    # Test 5: Convenience function
    print("\n" + "=" * 70)
    print("TEST 5: Convenience function")
    print("=" * 70)

    files = glob_files("core/epl/*.py")
    print(f"✓ Found {len(files)} files in core/epl/")
    for f in files[:3]:
        print(f"  - {f}")
