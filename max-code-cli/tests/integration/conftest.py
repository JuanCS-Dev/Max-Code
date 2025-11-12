"""
Pytest fixtures for integration tests
Constitutional AI v3.0 - FASE 2
"""

import pytest
import tempfile
import shutil
from pathlib import Path
from typing import Iterator


@pytest.fixture
def temp_dir() -> Iterator[Path]:
    """Create temporary directory for tests"""
    tmp = Path(tempfile.mkdtemp(prefix="max_code_integration_test_"))
    try:
        yield tmp
    finally:
        if tmp.exists():
            shutil.rmtree(tmp)
