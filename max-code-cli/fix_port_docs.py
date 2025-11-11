#!/usr/bin/env python3
"""
Fix Port Documentation Discrepancy

Corrects 91 occurrences where Penelope/MABA ports are documented incorrectly.

TRUTH:
- Penelope: 8154
- MABA: 8151
- Orchestrator: 8154 (shares with Penelope logically separate)

PROBLEM:
- Docs often swap 8151/8154 between services
"""

import re
from pathlib import Path
from typing import List, Tuple

# Directories to search
SEARCH_DIRS = [
    "docs/",
    "papers/",
    "RELATORIOS/",
    ".",  # Root for FOUNDATION.md files
]

# Files to exclude
EXCLUDE_PATTERNS = [
    "__pycache__",
    ".git",
    "node_modules",
    ".venv",
    "venv",
    "htmlcov",
]

def should_process(file_path: Path) -> bool:
    """Check if file should be processed"""
    if not file_path.suffix in [".md", ".txt", ".yml", ".yaml"]:
        return False

    for pattern in EXCLUDE_PATTERNS:
        if pattern in str(file_path):
            return False

    return True

def fix_port_references(content: str) -> Tuple[str, int]:
    """
    Fix port references in content.

    Strategy: Look for patterns like "Penelope.*8151" and fix to 8154
    """
    fixes = 0
    original = content

    # Pattern 1: "Penelope (Port 8151)" -> "Penelope (Port 8154)"
    content, n1 = re.subn(
        r'(Penelope[^\n]*?)(\bPort\s*)8151\b',
        r'\g<1>\g<2>8154',
        content,
        flags=re.IGNORECASE
    )
    fixes += n1

    # Pattern 2: "Penelope: 8151" -> "Penelope: 8154"
    content, n2 = re.subn(
        r'(Penelope[^\n]*?:\s*)8151\b',
        r'\g<1>8154',
        content
    )
    fixes += n2

    # Pattern 3: "MABA (Port 8154)" -> "MABA (Port 8151)"
    content, n3 = re.subn(
        r'(MABA[^\n]*?)(\bPort\s*)8154\b',
        r'\g<1>\g<2>8151',
        content,
        flags=re.IGNORECASE
    )
    fixes += n3

    # Pattern 4: "MABA: 8154" -> "MABA: 8151"
    content, n4 = re.subn(
        r'(MABA[^\n]*?:\s*)8154\b',
        r'\g<1>8151',
        content
    )
    fixes += n4

    # Pattern 5: "8151.*Penelope" (reverse order)
    content, n5 = re.subn(
        r'\b8151(\s*[-–:]\s*Penelope)',
        r'8154\g<1>',
        content
    )
    fixes += n5

    # Pattern 6: "8154.*MABA" (reverse order)
    content, n6 = re.subn(
        r'\b8154(\s*[-–:]\s*MABA)',
        r'8151\g<1>',
        content
    )
    fixes += n6

    return content, fixes

def main():
    """Main execution"""
    print("🔧 Port Documentation Fix Utility")
    print("=" * 50)
    print("Correcting Penelope/MABA port references...")
    print()

    total_files_processed = 0
    total_fixes = 0
    files_modified: List[Path] = []

    for search_dir in SEARCH_DIRS:
        base_path = Path(search_dir)
        if not base_path.exists():
            continue

        if base_path.is_file():
            files = [base_path]
        else:
            files = list(base_path.rglob("*"))

        for file_path in files:
            if not file_path.is_file() or not should_process(file_path):
                continue

            try:
                content = file_path.read_text(encoding='utf-8')
                new_content, fixes = fix_port_references(content)

                if fixes > 0:
                    file_path.write_text(new_content, encoding='utf-8')
                    files_modified.append(file_path)
                    total_fixes += fixes
                    print(f"✅ {file_path}: {fixes} fix(es)")

                total_files_processed += 1

            except Exception as e:
                print(f"⚠️  {file_path}: {e}")

    print()
    print("=" * 50)
    print(f"📊 Summary:")
    print(f"   Files processed: {total_files_processed}")
    print(f"   Files modified:  {len(files_modified)}")
    print(f"   Total fixes:     {total_fixes}")
    print()

    if files_modified:
        print("Modified files:")
        for f in files_modified:
            print(f"   - {f}")

if __name__ == "__main__":
    main()
