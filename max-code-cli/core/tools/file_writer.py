"""
File Writer Tool - Write files to filesystem

Inspired by Claude Code's Write tool.

Biblical Foundation:
"Escreve a visão e torna-a bem legível" (Habacuque 2:2)
Write the vision clearly - persistent truth.

Features:
- Atomic writes (write to temp, then rename)
- Automatic backup creation
- Directory creation
- Encoding support
- Overwrite protection
- Dry-run mode
"""

from typing import Optional
from dataclasses import dataclass
from pathlib import Path
import os
import shutil
import tempfile
from datetime import datetime


@dataclass
class FileWriteResult:
    """Result of file write operation"""
    success: bool
    file_path: str
    bytes_written: int = 0
    backup_path: Optional[str] = None
    created_dirs: bool = False
    overwritten: bool = False
    error: Optional[str] = None


class FileWriter:
    """
    File Writer Tool

    Writes files to filesystem with:
    - Atomic writes (via temp file)
    - Automatic backups
    - Directory creation
    - Overwrite protection

    Inspired by Claude Code's Write tool.
    """

    def __init__(
        self,
        create_backup: bool = True,
        create_dirs: bool = True,
        encoding: str = "utf-8"
    ):
        """
        Initialize FileWriter

        Args:
            create_backup: Create backup before overwriting (default: True)
            create_dirs: Create parent directories if missing (default: True)
            encoding: Character encoding (default: utf-8)
        """
        self.create_backup = create_backup
        self.create_dirs = create_dirs
        self.encoding = encoding

    def write(
        self,
        file_path: str,
        content: str,
        overwrite: bool = True,
        dry_run: bool = False
    ) -> FileWriteResult:
        """
        Write content to file

        Args:
            file_path: Absolute path to file
            content: Content to write
            overwrite: Allow overwriting existing file (default: True)
            dry_run: Don't actually write, just validate (default: False)

        Returns:
            FileWriteResult with operation details

        Example:
            >>> writer = FileWriter()
            >>> result = writer.write("/path/to/file.py", "print('hello')")
            >>> if result.success:
            ...     print(f"Wrote {result.bytes_written} bytes")
        """
        path = Path(file_path)

        # Check if file exists
        file_exists = path.exists()

        # Check overwrite protection
        if file_exists and not overwrite:
            return FileWriteResult(
                success=False,
                file_path=file_path,
                error=f"File exists and overwrite=False: {file_path}"
            )

        # Dry run - just validate
        if dry_run:
            return FileWriteResult(
                success=True,
                file_path=file_path,
                bytes_written=len(content.encode(self.encoding)),
                overwritten=file_exists,
            )

        # Create parent directories if needed
        created_dirs = False
        if self.create_dirs:
            parent = path.parent
            if not parent.exists():
                try:
                    parent.mkdir(parents=True, exist_ok=True)
                    created_dirs = True
                except Exception as e:
                    return FileWriteResult(
                        success=False,
                        file_path=file_path,
                        error=f"Failed to create directories: {e}"
                    )

        # Create backup if file exists
        backup_path = None
        if file_exists and self.create_backup:
            try:
                backup_path = self._create_backup(path)
            except Exception as e:
                return FileWriteResult(
                    success=False,
                    file_path=file_path,
                    error=f"Failed to create backup: {e}"
                )

        # Write file atomically
        try:
            # Write to temporary file first
            temp_fd, temp_path = tempfile.mkstemp(
                dir=path.parent,
                prefix=f".{path.name}.",
                suffix=".tmp"
            )

            try:
                # Write content to temp file
                with os.fdopen(temp_fd, 'w', encoding=self.encoding) as f:
                    f.write(content)

                # Atomic rename (overwrites destination)
                os.replace(temp_path, path)

                bytes_written = len(content.encode(self.encoding))

                return FileWriteResult(
                    success=True,
                    file_path=file_path,
                    bytes_written=bytes_written,
                    backup_path=backup_path,
                    created_dirs=created_dirs,
                    overwritten=file_exists,
                )

            except Exception as e:
                # Clean up temp file on error
                try:
                    os.unlink(temp_path)
                except (OSError, FileNotFoundError):
                    pass
                raise e

        except Exception as e:
            return FileWriteResult(
                success=False,
                file_path=file_path,
                error=f"Failed to write file: {e}"
            )

    def _create_backup(self, path: Path) -> str:
        """Create backup of existing file"""
        # Generate backup filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = path.parent / f"{path.name}.backup.{timestamp}"

        # Copy file to backup
        shutil.copy2(path, backup_path)

        return str(backup_path)

    def write_lines(
        self,
        file_path: str,
        lines: list,
        **kwargs
    ) -> FileWriteResult:
        """
        Write list of lines to file

        Args:
            file_path: Path to file
            lines: List of lines (will be joined with \\n)
            **kwargs: Additional arguments for write()

        Returns:
            FileWriteResult

        Example:
            >>> writer = FileWriter()
            >>> lines = ["line 1", "line 2", "line 3"]
            >>> writer.write_lines("/path/to/file.txt", lines)
        """
        content = "\n".join(lines)
        if lines and not lines[-1].endswith('\n'):
            content += '\n'  # Add trailing newline

        return self.write(file_path, content, **kwargs)

    def append(
        self,
        file_path: str,
        content: str
    ) -> FileWriteResult:
        """
        Append content to existing file

        Args:
            file_path: Path to file
            content: Content to append

        Returns:
            FileWriteResult

        Example:
            >>> writer = FileWriter()
            >>> writer.append("/path/to/log.txt", "New log entry\\n")
        """
        path = Path(file_path)

        # Read existing content
        existing_content = ""
        if path.exists():
            try:
                with open(path, 'r', encoding=self.encoding) as f:
                    existing_content = f.read()
            except Exception as e:
                return FileWriteResult(
                    success=False,
                    file_path=file_path,
                    error=f"Failed to read existing file: {e}"
                )

        # Append new content
        new_content = existing_content + content

        # Write combined content
        return self.write(file_path, new_content, overwrite=True)


# ============================================================================
# CONVENIENCE FUNCTIONS
# ============================================================================

def write_file(file_path: str, content: str, **kwargs) -> bool:
    """
    Convenience function to write file

    Args:
        file_path: Path to file
        content: Content to write
        **kwargs: Additional arguments for write()

    Returns:
        True if successful, False otherwise

    Example:
        >>> if write_file("/path/to/file.py", "print('hello')"):
        ...     print("Success!")
    """
    writer = FileWriter()
    result = writer.write(file_path, content, **kwargs)

    if not result.success:
        print(f"Error: {result.error}")

    return result.success


# ============================================================================
# DEMO
# ============================================================================

if __name__ == "__main__":
    print("✍️  File Writer Demo\n")

    writer = FileWriter()

    # Test 1: Write new file
    print("=" * 70)
    print("TEST 1: Write new file")
    print("=" * 70)

    test_file = "/tmp/max_code_test.txt"
    content = """Hello, World!
This is a test file created by FileWriter.

Biblical Foundation:
"Escreve a visão e torna-a bem legível" (Habacuque 2:2)
"""

    result = writer.write(test_file, content)

    if result.success:
        print(f"✓ Success!")
        print(f"  File: {result.file_path}")
        print(f"  Bytes written: {result.bytes_written}")
        print(f"  Created dirs: {result.created_dirs}")
        print(f"  Overwritten: {result.overwritten}")
    else:
        print(f"✗ Failed: {result.error}")

    # Test 2: Overwrite file (with backup)
    print("\n" + "=" * 70)
    print("TEST 2: Overwrite file (with backup)")
    print("=" * 70)

    new_content = "This is the updated content.\n"
    result = writer.write(test_file, new_content, overwrite=True)

    if result.success:
        print(f"✓ Overwritten!")
        print(f"  Bytes written: {result.bytes_written}")
        print(f"  Backup created: {result.backup_path}")
    else:
        print(f"✗ Failed: {result.error}")

    # Test 3: Write with directory creation
    print("\n" + "=" * 70)
    print("TEST 3: Write with directory creation")
    print("=" * 70)

    nested_file = "/tmp/max_code/nested/dir/test.txt"
    result = writer.write(nested_file, "Nested file content\n")

    if result.success:
        print(f"✓ Created nested file!")
        print(f"  File: {result.file_path}")
        print(f"  Created dirs: {result.created_dirs}")
    else:
        print(f"✗ Failed: {result.error}")

    # Test 4: Write lines
    print("\n" + "=" * 70)
    print("TEST 4: Write lines")
    print("=" * 70)

    lines = [
        "Line 1",
        "Line 2",
        "Line 3",
    ]

    result = writer.write_lines("/tmp/lines.txt", lines)

    if result.success:
        print(f"✓ Wrote {len(lines)} lines!")
        print(f"  Bytes: {result.bytes_written}")
    else:
        print(f"✗ Failed: {result.error}")

    # Test 5: Append
    print("\n" + "=" * 70)
    print("TEST 5: Append to file")
    print("=" * 70)

    result = writer.append("/tmp/lines.txt", "Line 4\n")

    if result.success:
        print(f"✓ Appended content!")
        print(f"  Total bytes: {result.bytes_written}")
    else:
        print(f"✗ Failed: {result.error}")

    # Test 6: Dry run
    print("\n" + "=" * 70)
    print("TEST 6: Dry run")
    print("=" * 70)

    result = writer.write("/tmp/dryrun.txt", "This won't be written", dry_run=True)

    if result.success:
        print(f"✓ Dry run validated!")
        print(f"  Would write: {result.bytes_written} bytes")
        print(f"  File exists: {Path('/tmp/dryrun.txt').exists()}")
    else:
        print(f"✗ Failed: {result.error}")

    # Cleanup
    print("\n" + "=" * 70)
    print("Cleanup")
    print("=" * 70)

    import shutil
    for path in ["/tmp/max_code_test.txt", "/tmp/max_code", "/tmp/lines.txt"]:
        try:
            p = Path(path)
            if p.is_file():
                p.unlink()
                print(f"  Removed: {path}")
            elif p.is_dir():
                shutil.rmtree(p)
                print(f"  Removed dir: {path}")
        except (OSError, FileNotFoundError, PermissionError):
            pass
