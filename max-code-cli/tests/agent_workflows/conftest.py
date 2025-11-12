"""
Pytest fixtures for agent workflow tests
"""

import pytest
import sys
import tempfile
import shutil
import warnings
from pathlib import Path
from typing import Iterator

# Ensure project root is in path (needed for agent imports)
project_root = Path(__file__).parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

# Suppress ResourceWarning for unclosed client sessions
# (These are managed singletons that close on program exit)
warnings.filterwarnings("ignore", category=ResourceWarning, message="unclosed.*client_session")


@pytest.fixture
def temp_workspace() -> Iterator[Path]:
    """Create temporary workspace for agent execution"""
    tmp = Path(tempfile.mkdtemp(prefix="agent_workspace_"))
    try:
        yield tmp
    finally:
        if tmp.exists():
            shutil.rmtree(tmp)


@pytest.fixture
def sample_code_files(temp_workspace: Path) -> dict:
    """Create sample code files for testing"""
    files = {}

    # Simple function
    simple_py = temp_workspace / "simple.py"
    simple_py.write_text("""def add(a, b):
    return a + b
""")
    files['simple'] = simple_py

    # Function with bug
    buggy_py = temp_workspace / "buggy.py"
    buggy_py.write_text("""def divide(a, b):
    return a / b  # Bug: no zero division check
""")
    files['buggy'] = buggy_py

    # Complex function needing refactor
    complex_py = temp_workspace / "complex.py"
    complex_py.write_text("""def process_data(data):
    result = []
    for item in data:
        if item > 0:
            result.append(item * 2)
        elif item < 0:
            result.append(abs(item))
        else:
            result.append(0)
    return result
""")
    files['complex'] = complex_py

    return files
