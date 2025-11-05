#!/usr/bin/env python3
"""
Script to convert print() → logging calls while preserving 100% of EPL emojis.

CRITICAL: EPL (Emoji Protocol Language) is a semantic communication protocol
that achieves 60-80% token compression. Emojis MUST be preserved.

Usage:
    python scripts/convert_prints_to_logging.py agents/plan_agent.py
    python scripts/convert_prints_to_logging.py agents/architect_agent.py
    python scripts/convert_prints_to_logging.py agents/sleep_agent.py
"""

import sys
import re
from pathlib import Path


def convert_prints_to_logging(file_path: Path) -> tuple[str, int]:
    """
    Convert all print() statements to logging calls.

    Returns:
        (modified_content, num_replacements)
    """
    content = file_path.read_text()
    num_replacements = 0

    # Step 1: Add logger import if not present
    if "from config.logging_config import get_logger" not in content:
        # Find the last import line
        import_pattern = r'(^from .+ import .+$|^import .+$)'
        matches = list(re.finditer(import_pattern, content, re.MULTILINE))
        if matches:
            last_import = matches[-1]
            insert_pos = last_import.end()
            content = (
                content[:insert_pos] +
                "\nfrom config.logging_config import get_logger\n\nlogger = get_logger(__name__)" +
                content[insert_pos:]
            )

    # Step 2: Update version docstring
    content = re.sub(
        r'(v\d+\.\d+: [^\n]+)(\n""")',
        r'\1\nv2.2: Replaced print() with logging (FASE 3.4)\2',
        content,
        count=1
    )

    # Step 3: Replace print() statements
    # Pattern matches: print(f"...") or print("...")
    def replace_print(match):
        nonlocal num_replacements
        num_replacements += 1

        full_match = match.group(0)
        indent = match.group(1)
        message = match.group(2)

        # Determine log level based on emoji/content
        if "✅" in message or "✓" in message:
            level = "info"
        elif "❌" in message or "error" in message.lower():
            level = "error"
        elif "⚠️" in message or "warning" in message.lower() or "offline" in message.lower():
            level = "warning"
        elif "🔍" in message or "debug" in message.lower():
            level = "debug"
        else:
            level = "info"  # Default

        # Extract f-string or regular string
        if message.startswith('f"') or message.startswith("f'"):
            # f-string
            msg_content = message[2:-1]  # Remove f" and "
            return f'{indent}logger.{level}(f"{msg_content}", extra={{"task_id": task.id}})'
        else:
            # Regular string
            msg_content = message[1:-1]  # Remove " and "
            return f'{indent}logger.{level}("{msg_content}", extra={{"task_id": task.id}})'

    # Match print statements (handles indentation)
    print_pattern = r'^(\s*)print\((f?"[^"]*"|f?\'[^\']*\')\)$'
    content = re.sub(print_pattern, replace_print, content, flags=re.MULTILINE)

    return content, num_replacements


def main():
    if len(sys.argv) < 2:
        print("Usage: python convert_prints_to_logging.py <file_path>")
        sys.exit(1)

    file_path = Path(sys.argv[1])

    if not file_path.exists():
        print(f"❌ File not found: {file_path}")
        sys.exit(1)

    print(f"🔄 Converting {file_path}...")
    print(f"   Preserving 100% of EPL emojis (🌳, 🧠, 🏥, etc)")

    # Backup original
    backup_path = file_path.with_suffix(file_path.suffix + ".backup")
    backup_path.write_text(file_path.read_text())
    print(f"   💾 Backup created: {backup_path}")

    # Convert
    modified_content, num_replacements = convert_prints_to_logging(file_path)

    # Write back
    file_path.write_text(modified_content)

    print(f"   ✅ Converted {num_replacements} print() statements")
    print(f"   📝 File updated: {file_path}")
    print()


if __name__ == "__main__":
    main()
