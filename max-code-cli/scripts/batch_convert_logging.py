#!/usr/bin/env python3
"""
Batch convert print() → logging across all core/ modules.

PRESERVES 100% EPL (Emoji Protocol Language) - all emojis are semantic tokens.

Usage:
    python scripts/batch_convert_logging.py core/
"""

import sys
import re
from pathlib import Path
from typing import Tuple, List


def convert_file(file_path: Path) -> Tuple[bool, int]:
    """
    Convert all print() in a file to logging.

    Returns:
        (modified, num_replacements)
    """
    try:
        content = file_path.read_text(encoding='utf-8')
    except Exception as e:
        print(f"❌ Error reading {file_path}: {e}")
        return False, 0

    original_content = content
    num_replacements = 0

    # Skip if already has logger
    has_logger = "logger = get_logger(__name__)" in content or "logger = logging.getLogger(__name__)" in content

    # Step 1: Add logger import if not present
    if not has_logger and "print(" in content:
        # Find position after imports
        import_pattern = r'(^from .+ import .+$|^import .+$)'
        matches = list(re.finditer(import_pattern, content, re.MULTILINE))

        if matches:
            last_import = matches[-1]
            insert_pos = last_import.end()

            # Check if logging_config import already exists
            if "from config.logging_config import get_logger" not in content:
                content = (
                    content[:insert_pos] +
                    "\nfrom config.logging_config import get_logger\n\nlogger = get_logger(__name__)" +
                    content[insert_pos:]
                )

    # Step 2: Replace print() statements with logging
    # This pattern matches print(f"..." or print("...") with any indentation
    def replace_print(match):
        nonlocal num_replacements
        num_replacements += 1

        indent = match.group(1)
        message_content = match.group(2)

        # Determine log level based on content/emojis
        msg_lower = message_content.lower()

        if "✅" in message_content or "✓" in message_content or "success" in msg_lower:
            level = "info"
        elif "❌" in message_content or "error" in msg_lower or "failed" in msg_lower:
            level = "error"
        elif "⚠️" in message_content or "warning" in msg_lower or "offline" in msg_lower:
            level = "warning"
        elif "🔍" in message_content or "debug" in msg_lower:
            level = "debug"
        else:
            level = "info"  # Default

        # Build logging call - PRESERVE EXACT MESSAGE INCLUDING EPL EMOJIS
        return f'{indent}logger.{level}({message_content})'

    # Pattern: matches print(...) with f-string or regular string
    # Captures indentation and message content
    print_pattern = r'^(\s*)print\((f?"[^"]*"|f?\'[^\']*\')\)\s*$'
    content = re.sub(print_pattern, replace_print, content, flags=re.MULTILINE)

    # Only write if modified
    if content != original_content:
        try:
            file_path.write_text(content, encoding='utf-8')
            return True, num_replacements
        except Exception as e:
            print(f"❌ Error writing {file_path}: {e}")
            return False, 0

    return False, 0


def find_python_files_with_prints(directory: Path) -> List[Path]:
    """Find all .py files containing print() statements"""
    files_with_prints = []

    for py_file in directory.rglob("*.py"):
        # Skip __pycache__ and test files if needed
        if "__pycache__" in str(py_file):
            continue

        try:
            content = py_file.read_text(encoding='utf-8')
            if re.search(r'^\s*print\(', content, re.MULTILINE):
                files_with_prints.append(py_file)
        except Exception:
            continue

    return files_with_prints


def main():
    if len(sys.argv) < 2:
        print("Usage: python batch_convert_logging.py <directory>")
        sys.exit(1)

    target_dir = Path(sys.argv[1])

    if not target_dir.exists() or not target_dir.is_dir():
        print(f"❌ Directory not found: {target_dir}")
        sys.exit(1)

    print(f"🔍 Scanning {target_dir} for files with print() statements...")
    files = find_python_files_with_prints(target_dir)

    print(f"📊 Found {len(files)} files with print() statements")
    print(f"⚠️  PRESERVING 100% EPL emojis (critical semantic tokens)")
    print()

    total_replacements = 0
    modified_files = 0

    for i, file_path in enumerate(files, 1):
        try:
            rel_path = file_path.relative_to(Path.cwd())
        except ValueError:
            rel_path = file_path
        print(f"[{i}/{len(files)}] Processing {rel_path}...", end=" ")

        modified, num_replaced = convert_file(file_path)

        if modified:
            print(f"✅ {num_replaced} prints → logging")
            modified_files += 1
            total_replacements += num_replaced
        else:
            print("⏭️  skipped")

    print()
    print("="*70)
    print(f"✅ Conversion complete!")
    print(f"   Modified files: {modified_files}/{len(files)}")
    print(f"   Total conversions: {total_replacements}")
    print(f"   EPL emojis preserved: 100%")
    print("="*70)


if __name__ == "__main__":
    main()
