"""
Pytest fixtures for tool validation tests
Constitutional AI v3.0 - FASE 1
"""

import pytest
import tempfile
import shutil
import os
from pathlib import Path
from typing import Iterator


@pytest.fixture
def temp_dir() -> Iterator[Path]:
    """Create temporary directory for tests"""
    tmp = Path(tempfile.mkdtemp(prefix="max_code_tool_test_"))
    try:
        yield tmp
    finally:
        if tmp.exists():
            shutil.rmtree(tmp)


@pytest.fixture
def temp_file(temp_dir: Path) -> Path:
    """Create temporary file for tests"""
    file = temp_dir / "test.txt"
    file.write_text("Initial content\n")
    return file


@pytest.fixture
def temp_git_repo(temp_dir: Path) -> Iterator[Path]:
    """Create temporary git repository"""
    os.chdir(temp_dir)
    os.system("git init > /dev/null 2>&1")
    os.system("git config user.name 'Test User' > /dev/null 2>&1")
    os.system("git config user.email 'test@example.com' > /dev/null 2>&1")

    # Create initial commit
    readme = temp_dir / "README.md"
    readme.write_text("# Test Repository\n")
    os.system("git add README.md > /dev/null 2>&1")
    os.system("git commit -m 'Initial commit' > /dev/null 2>&1")

    yield temp_dir


@pytest.fixture
def sample_files(temp_dir: Path) -> dict:
    """Create sample files with various encodings and content"""
    files = {}

    # UTF-8 file
    utf8_file = temp_dir / "utf8.txt"
    utf8_file.write_text("Hello World\nLine 2\nLine 3\n", encoding='utf-8')
    files['utf8'] = utf8_file

    # File with special characters
    special_file = temp_dir / "special.txt"
    special_file.write_text("Special: Ñoño 日本語 مرحبا 🎉\n", encoding='utf-8')
    files['special'] = special_file

    # Multiline file
    multiline = temp_dir / "multiline.txt"
    multiline.write_text("\n".join([f"Line {i}" for i in range(1, 101)]) + "\n")
    files['multiline'] = multiline

    # Binary-like file
    binary_file = temp_dir / "binary.dat"
    binary_file.write_bytes(b'\x00\x01\x02\x03\x04\x05')
    files['binary'] = binary_file

    return files


@pytest.fixture
def python_file(temp_dir: Path) -> Path:
    """Create sample Python file"""
    py_file = temp_dir / "sample.py"
    py_file.write_text("""
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

def main():
    print(fibonacci(10))

if __name__ == "__main__":
    main()
""")
    return py_file


@pytest.fixture(autouse=True)
def reset_cwd():
    """Reset working directory after each test"""
    original_cwd = os.getcwd()
    yield
    os.chdir(original_cwd)
