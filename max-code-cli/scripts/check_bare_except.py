#!/usr/bin/env python3
"""
Pre-commit hook: Prevent bare except blocks in production code

Boris Cherny Standard:
"If it doesn't have types, it's not production"
"Bare excepts are lazy exceptions to lazy exception handling"

Usage:
    python scripts/check_bare_except.py <file1.py> <file2.py> ...

Returns:
    Exit 0: All files clean
    Exit 1: Bare excepts found

Biblical Foundation:
"Tudo o que fizerem, façam de todo o coração" (Colossenses 3:23)
"""

import re
import sys
from pathlib import Path
from typing import List, Tuple


def find_bare_excepts(file_path: Path) -> List[Tuple[int, str]]:
    """
    Find bare except blocks in a Python file.

    Args:
        file_path: Path to Python file

    Returns:
        List of (line_number, line_content) tuples
    """
    violations = []

    try:
        content = file_path.read_text(encoding='utf-8')
        lines = content.splitlines()

        for line_num, line in enumerate(lines, start=1):
            # Skip comments and docstrings
            stripped = line.strip()
            if stripped.startswith('#'):
                continue

            # Match bare except (except: or except :)
            if re.match(r'^\s*except\s*:', line):
                violations.append((line_num, line.rstrip()))

    except (OSError, UnicodeDecodeError) as e:
        # Can't read file - let it pass (other tools will catch this)
        print(f"Warning: Could not read {file_path}: {e}", file=sys.stderr)
        return []

    return violations


def check_files(file_paths: List[str]) -> bool:
    """
    Check multiple files for bare excepts.

    Args:
        file_paths: List of file paths to check

    Returns:
        True if all files clean, False if violations found
    """
    all_clean = True
    total_violations = 0

    for file_path_str in file_paths:
        file_path = Path(file_path_str)

        # Skip non-Python files
        if file_path.suffix != '.py':
            continue

        # Skip test files (bare excepts acceptable in cleanup code)
        if 'test' in file_path.parts or file_path.name.startswith('test_'):
            continue

        violations = find_bare_excepts(file_path)

        if violations:
            all_clean = False
            total_violations += len(violations)

            print(f"\n❌ {file_path}:", file=sys.stderr)
            for line_num, line_content in violations:
                print(f"  Line {line_num}: {line_content}", file=sys.stderr)

    if not all_clean:
        print(f"\n{'='*70}", file=sys.stderr)
        print(f"FAILED: Found {total_violations} bare except(s)", file=sys.stderr)
        print(f"{'='*70}", file=sys.stderr)
        print("\nBoris Cherny Standard: Use specific exceptions!", file=sys.stderr)
        print("\nExamples:", file=sys.stderr)
        print("  ❌ except:", file=sys.stderr)
        print("  ✅ except (ValueError, TypeError):", file=sys.stderr)
        print("  ✅ except OSError as e:", file=sys.stderr)
        print("\nSee docs/BARE_EXCEPT_REMEDIATION.md for guidelines.", file=sys.stderr)
        print(f"{'='*70}\n", file=sys.stderr)

    return all_clean


def main() -> int:
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Usage: check_bare_except.py <file1.py> <file2.py> ...", file=sys.stderr)
        return 1

    file_paths = sys.argv[1:]

    if check_files(file_paths):
        # All clean - silent success (pre-commit convention)
        return 0
    else:
        return 1


if __name__ == '__main__':
    sys.exit(main())
