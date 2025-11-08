"""
File Editor Tool - Edit files with exact string replacement

Inspired by Claude Code's Edit tool.

Biblical Foundation:
"Corrige-me, SENHOR, mas com medida" (Jeremias 10:24)
Correction with precision - surgical edits.

Features:
- Exact string replacement
- Replace all occurrences
- Backup before editing
- Validation (old_string must exist)
- Atomic operations
- Diff generation
"""

from typing import Optional, List, Tuple
from dataclasses import dataclass
from pathlib import Path
import difflib
from config.logging_config import get_logger

logger = get_logger(__name__)

# Handle both package and standalone imports
try:
    from .file_reader import FileReader
    from .file_writer import FileWriter
except ImportError:
    from file_reader import FileReader
    from file_writer import FileWriter


@dataclass
class FileEditResult:
    """Result of file edit operation"""
    success: bool
    file_path: str
    old_string: str
    new_string: str
    replacements: int = 0
    backup_path: Optional[str] = None
    diff: Optional[str] = None
    error: Optional[str] = None


class FileEditor:
    """
    File Editor Tool

    Edits files using exact string replacement.
    Inspired by Claude Code's Edit tool.

    Important:
    - old_string must exist in file (exact match)
    - Preserves indentation and formatting
    - Creates backup before editing
    - Atomic operation (all or nothing)
    - Can replace all occurrences or just first
    - **NEW: Interactive confirmation for risky operations**

    Example:
        >>> editor = FileEditor()
        >>> result = editor.edit(
        ...     file_path="/path/to/file.py",
        ...     old_string="def old_function():",
        ...     new_string="def new_function():"
        ... )
    """

    def __init__(self, skip_confirmation: bool = False):
        """
        Initialize FileEditor
        
        Args:
            skip_confirmation: Skip interactive confirmations (use with caution)
        """
        self.reader = FileReader()
        self.writer = FileWriter()
        self.skip_confirmation = skip_confirmation
        
        # Import confirmation components
        from core.risk_classifier import RiskClassifier
        from ui.confirmation import ConfirmationUI, QuietConfirmationUI
        
        self.risk_classifier = RiskClassifier()
        
        if skip_confirmation:
            self.confirmation_ui = QuietConfirmationUI()
        else:
            self.confirmation_ui = ConfirmationUI()

    def edit(
        self,
        file_path: str,
        old_string: str,
        new_string: str,
        replace_all: bool = False,
        generate_diff: bool = True
    ) -> FileEditResult:
        """
        Edit file by replacing old_string with new_string

        Args:
            file_path: Absolute path to file
            old_string: String to replace (must exist exactly)
            new_string: Replacement string (must be different)
            replace_all: Replace all occurrences (default: False = first only)
            generate_diff: Generate diff output (default: True)

        Returns:
            FileEditResult with operation details

        Example:
            >>> editor = FileEditor()
            >>> result = editor.edit(
            ...     "/path/to/file.py",
            ...     old_string="print('hello')",
            ...     new_string="print('goodbye')"
            ... )
        """
        path = Path(file_path)

        # Validate file exists
        if not path.exists():
            return FileEditResult(
                success=False,
                file_path=file_path,
                old_string=old_string,
                new_string=new_string,
                error=f"File not found: {file_path}"
            )

        # Validate old_string != new_string
        if old_string == new_string:
            return FileEditResult(
                success=False,
                file_path=file_path,
                old_string=old_string,
                new_string=new_string,
                error="old_string and new_string must be different"
            )

        # Read current content
        read_result = self.reader.read_all(file_path)
        if not read_result.success:
            return FileEditResult(
                success=False,
                file_path=file_path,
                old_string=old_string,
                new_string=new_string,
                error=f"Failed to read file: {read_result.error}"
            )

        # Extract content (remove line numbers from cat -n format)
        original_content = self._extract_content(read_result.content)

        # Check if old_string exists
        if old_string not in original_content:
            return FileEditResult(
                success=False,
                file_path=file_path,
                old_string=old_string,
                new_string=new_string,
                error=f"old_string not found in file. Make sure it's an exact match."
            )

        # Count occurrences
        occurrences = original_content.count(old_string)

        # Check uniqueness if not replace_all
        if not replace_all and occurrences > 1:
            return FileEditResult(
                success=False,
                file_path=file_path,
                old_string=old_string,
                new_string=new_string,
                error=f"old_string appears {occurrences} times. Either provide a unique string or use replace_all=True."
            )

        # Perform replacement
        if replace_all:
            new_content = original_content.replace(old_string, new_string)
            replacements = occurrences
        else:
            # Replace only first occurrence
            new_content = original_content.replace(old_string, new_string, 1)
            replacements = 1

        # Generate diff
        diff = None
        if generate_diff:
            diff = self._generate_diff(
                original_content,
                new_content,
                str(path)
            )
        
        # NEW: Risk assessment and confirmation
        risk = self.risk_classifier.assess_file_operation(
            operation="edit",
            filepath=file_path,
            file_exists=True,
            content_size=len(new_content)
        )
        
        # Ask for confirmation if needed
        if risk.requires_confirmation:
            confirmed = self.confirmation_ui.confirm_file_operation(
                risk=risk,
                diff=diff,
                old_content=original_content,
                new_content=new_content,
                operation_name="file edit"
            )
            
            if not confirmed:
                return FileEditResult(
                    success=False,
                    file_path=file_path,
                    old_string=old_string,
                    new_string=new_string,
                    error="Operation cancelled by user"
                )

        # Write new content
        write_result = self.writer.write(
            file_path,
            new_content,
            overwrite=True
        )

        if not write_result.success:
            return FileEditResult(
                success=False,
                file_path=file_path,
                old_string=old_string,
                new_string=new_string,
                error=f"Failed to write file: {write_result.error}"
            )

        return FileEditResult(
            success=True,
            file_path=file_path,
            old_string=old_string,
            new_string=new_string,
            replacements=replacements,
            backup_path=write_result.backup_path,
            diff=diff,
        )

    def _extract_content(self, formatted_content: str) -> str:
        """Extract content from cat -n formatted output"""
        if not formatted_content:
            return ""

        lines = formatted_content.split('\n')
        extracted = []

        for line in lines:
            # Format is: "     1→content"
            if '→' in line:
                # Split on → and take everything after
                parts = line.split('→', 1)
                if len(parts) == 2:
                    extracted.append(parts[1])
            else:
                # Line without formatting (shouldn't happen, but handle it)
                extracted.append(line)

        return '\n'.join(extracted)

    def _generate_diff(
        self,
        original: str,
        modified: str,
        filename: str
    ) -> str:
        """Generate unified diff"""
        original_lines = original.splitlines(keepends=True)
        modified_lines = modified.splitlines(keepends=True)

        diff = difflib.unified_diff(
            original_lines,
            modified_lines,
            fromfile=f"{filename} (original)",
            tofile=f"{filename} (modified)",
            lineterm=''
        )

        return ''.join(diff)

    def edit_multiple(
        self,
        file_path: str,
        edits: List[Tuple[str, str]],
        **kwargs
    ) -> FileEditResult:
        """
        Apply multiple edits to same file

        Args:
            file_path: Path to file
            edits: List of (old_string, new_string) tuples
            **kwargs: Additional arguments for edit()

        Returns:
            FileEditResult for all edits combined

        Example:
            >>> editor = FileEditor()
            >>> edits = [
            ...     ("old1", "new1"),
            ...     ("old2", "new2"),
            ... ]
            >>> result = editor.edit_multiple("/path/to/file.py", edits)
        """
        total_replacements = 0
        all_diffs = []

        for old_str, new_str in edits:
            result = self.edit(
                file_path,
                old_str,
                new_str,
                **kwargs
            )

            if not result.success:
                return result

            total_replacements += result.replacements
            if result.diff:
                all_diffs.append(result.diff)

        combined_diff = "\n\n".join(all_diffs) if all_diffs else None

        return FileEditResult(
            success=True,
            file_path=file_path,
            old_string=f"{len(edits)} edits",
            new_string=f"{len(edits)} edits",
            replacements=total_replacements,
            diff=combined_diff,
        )


# ============================================================================
# CONVENIENCE FUNCTIONS
# ============================================================================

def edit_file(
    file_path: str,
    old_string: str,
    new_string: str,
    **kwargs
) -> bool:
    """
    Convenience function to edit file

    Args:
        file_path: Path to file
        old_string: String to replace
        new_string: Replacement string
        **kwargs: Additional arguments for edit()

    Returns:
        True if successful, False otherwise

    Example:
        >>> if edit_file("/path/to/file.py", "old", "new"):
        ...     print("Success!")
    """
    editor = FileEditor()
    result = editor.edit(file_path, old_string, new_string, **kwargs)

    if not result.success:
        logger.error(f"Error: {result.error}")
    return result.success


# ============================================================================
# DEMO
# ============================================================================

if __name__ == "__main__":
    logger.info("✏️  File Editor Demo\n")
    try:
        from .file_writer import FileWriter
    except ImportError:
        from file_writer import FileWriter

    # Setup: Create test file
    test_file = "/tmp/max_code_edit_test.py"
    original_content = """def hello():
    logger.info('Hello, World!')
    return True

def goodbye():
    logger.info('Goodbye, World!')
    return False
"""

    writer = FileWriter()
    writer.write(test_file, original_content)

    editor = FileEditor()

    # Test 1: Simple edit (first occurrence)
    print("=" * 70)
    logger.info("TEST 1: Edit first occurrence")
    print("=" * 70)

    result = editor.edit(
        test_file,
        old_string="print('Hello, World!')",
        new_string="print('Greetings, Universe!')"
    )

    if result.success:
        logger.info(f"✓ Success!")
        logger.info(f"  Replacements: {result.replacements}")
        logger.info(f"  Backup: {result.backup_path}")
        logger.info(f"\nDiff:\n{result.diff}")
    else:
        logger.error(f"✗ Failed: {result.error}")
    # Test 2: Replace all occurrences
    print("\n" + "=" * 70)
    logger.info("TEST 2: Replace all occurrences of 'World'")
    print("=" * 70)

    result = editor.edit(
        test_file,
        old_string="World",
        new_string="Universe",
        replace_all=True
    )

    if result.success:
        logger.info(f"✓ Replaced {result.replacements} occurrences!")
        logger.info(f"\nDiff:\n{result.diff}")
    else:
        logger.error(f"✗ Failed: {result.error}")
    # Test 3: Error - string not found
    print("\n" + "=" * 70)
    logger.error("TEST 3: Error handling - string not found")
    print("=" * 70)

    result = editor.edit(
        test_file,
        old_string="nonexistent string",
        new_string="something"
    )

    if not result.success:
        logger.info(f"✓ Correctly detected error: {result.error}")
    else:
        logger.error(f"✗ Should have failed!")
    # Test 4: Error - non-unique string without replace_all
    print("\n" + "=" * 70)
    logger.error("TEST 4: Error handling - non-unique string")
    print("=" * 70)

    # Reset file
    writer.write(test_file, original_content, overwrite=True)

    result = editor.edit(
        test_file,
        old_string="return",
        new_string="yield",
        replace_all=False
    )

    if not result.success:
        logger.info(f"✓ Correctly detected non-unique string: {result.error}")
    else:
        logger.error(f"✗ Should have failed!")
    # Test 5: Multiple edits
    print("\n" + "=" * 70)
    logger.info("TEST 5: Multiple edits")
    print("=" * 70)

    # Reset file
    writer.write(test_file, original_content, overwrite=True)

    edits = [
        ("def hello():", "def greet():"),
        ("def goodbye():", "def farewell():"),
    ]

    result = editor.edit_multiple(test_file, edits)

    if result.success:
        logger.info(f"✓ Applied {result.replacements} edits!")
        logger.info(f"\nDiff:\n{result.diff}")
    else:
        logger.error(f"✗ Failed: {result.error}")
    # Cleanup
    print("\n" + "=" * 70)
    logger.info("Cleanup")
    print("=" * 70)

    Path(test_file).unlink()
    logger.info(f"  Removed: {test_file}")
    # Remove backups
    import glob
    for backup in glob.glob(f"{test_file}.backup.*"):
        Path(backup).unlink()
        logger.info(f"  Removed backup: {backup}")


# Auto-register tool (PROMPT 2.2 - Zero Duplication)
from .auto_register import register_tool

register_tool(
    name="file_editor",
    description="Edit files with exact string replacements. Safer than full rewrites - changes only specified strings.",
    handler_class=FileEditor,
    handler_method="edit",
    parameters=[
        {"name": "file_path", "type": "string", "description": "Path to file to edit", "required": True},
        {"name": "old_string", "type": "string", "description": "Exact string to find and replace", "required": True},
        {"name": "new_string", "type": "string", "description": "Replacement string", "required": True},
    ],
    tags=["file", "edit", "modify", "io"]
)