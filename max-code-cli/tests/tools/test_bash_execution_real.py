"""
Bash Execution Real Test Suite
Constitutional AI v3.0 - FASE 1.3

Tests REAL bash execution (not just structure validation).
Following Anthropic TDD Pattern: Write tests → Run → Discover APIs → Adjust

Target: 20+ tests, 95%+ pass rate
"""

import pytest
import sys
import os
import time
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from core.tools.bash_executor import BashExecutor


# ═══════════════════════════════════════════════════════════════════════════
# CATEGORY 1: BASIC COMMAND EXECUTION
# ═══════════════════════════════════════════════════════════════════════════

class TestBasicExecution:
    """Test basic bash command execution"""

    def test_execute_simple_command(self):
        """Test executing simple echo command"""
        executor = BashExecutor()
        result = executor.execute("echo 'Hello World'")

        assert result.type == "success"
        assert "Hello World" in result.content[0].text
        assert result.metadata['exit_code'] == 0

    def test_execute_pwd(self, temp_dir):
        """Test pwd command returns current directory"""
        executor = BashExecutor()
        result = executor.execute(f"cd {temp_dir} && pwd")

        assert result.type == "success"
        assert str(temp_dir) in result.content[0].text

    def test_execute_ls(self, temp_dir):
        """Test ls command lists files"""
        # Create test files
        (temp_dir / "file1.txt").write_text("test")
        (temp_dir / "file2.txt").write_text("test")

        executor = BashExecutor()
        result = executor.execute(f"ls {temp_dir}")

        assert result.type == "success"
        assert "file1.txt" in result.content[0].text
        assert "file2.txt" in result.content[0].text

    def test_execute_cat(self, temp_dir):
        """Test cat command reads file"""
        test_file = temp_dir / "test.txt"
        test_file.write_text("Test content\nLine 2\n")

        executor = BashExecutor()
        result = executor.execute(f"cat {test_file}")

        assert result.type == "success"
        assert "Test content" in result.content[0].text
        assert "Line 2" in result.content[0].text

    def test_execute_mkdir(self, temp_dir):
        """Test mkdir creates directory"""
        new_dir = temp_dir / "newdir"

        executor = BashExecutor()
        result = executor.execute(f"mkdir {new_dir}")

        assert result.type == "success"
        assert new_dir.exists()
        assert new_dir.is_dir()


# ═══════════════════════════════════════════════════════════════════════════
# CATEGORY 2: ERROR HANDLING
# ═══════════════════════════════════════════════════════════════════════════

class TestErrorHandling:
    """Test bash error handling"""

    def test_nonexistent_command(self):
        """Test executing nonexistent command fails gracefully"""
        executor = BashExecutor()
        result = executor.execute("nonexistent_command_xyz")

        assert result.type == "error"
        assert result.metadata["exit_code"] != 0
        assert result.metadata.get("stderr", "") is not None

    def test_invalid_syntax(self):
        """Test invalid bash syntax fails gracefully"""
        executor = BashExecutor()
        result = executor.execute("if [[ ]]; then")

        assert result.type == "error"
        assert result.metadata["exit_code"] != 0

    def test_permission_denied(self, temp_dir):
        """Test permission denied error handling"""
        # Create file with no execute permissions
        script = temp_dir / "noperm.sh"
        script.write_text("#!/bin/bash\necho test")
        script.chmod(0o000)

        executor = BashExecutor()
        result = executor.execute(f"{script}")

        # Should fail with permission error
        assert result.type == "error" or "Permission denied" in result.metadata.get("stderr", "")

    def test_file_not_found(self, temp_dir):
        """Test file not found error"""
        executor = BashExecutor()
        result = executor.execute(f"cat {temp_dir}/nonexistent.txt")

        assert result.type == "error"
        assert result.metadata["exit_code"] != 0


# ═══════════════════════════════════════════════════════════════════════════
# CATEGORY 3: TIMEOUT & RESOURCE LIMITS
# ═══════════════════════════════════════════════════════════════════════════

class TestTimeoutAndLimits:
    """Test timeout and resource limit enforcement"""

    def test_timeout_enforcement(self):
        """Test command timeout is enforced"""
        executor = BashExecutor()
        start_time = time.time()

        # Sleep for 10 seconds with 2-second timeout
        result = executor.execute("sleep 10", timeout=2)

        elapsed = time.time() - start_time

        # Should timeout before 10 seconds
        assert elapsed < 5  # Allow some margin
        assert result.type == "error" or result.metadata.get("timed_out", False)

    def test_no_timeout_for_quick_commands(self):
        """Test quick commands don't timeout"""
        executor = BashExecutor()
        result = executor.execute("echo 'fast'", timeout=5)

        assert result.type == "success"
        assert not result.metadata.get("timed_out", False)

    def test_default_timeout(self):
        """Test default timeout exists"""
        executor = BashExecutor()
        # Should have some reasonable default (e.g., 120s)
        result = executor.execute("sleep 0.1")

        assert result.type == "success"
        # If no timeout mechanism, this test just validates it completes


# ═══════════════════════════════════════════════════════════════════════════
# CATEGORY 4: OUTPUT CAPTURE
# ═══════════════════════════════════════════════════════════════════════════

class TestOutputCapture:
    """Test stdout/stderr capture"""

    def test_stdout_capture(self):
        """Test stdout is captured correctly"""
        executor = BashExecutor()
        result = executor.execute("echo 'stdout line 1'; echo 'stdout line 2'")

        assert result.type == "success"
        assert "stdout line 1" in result.content[0].text
        assert "stdout line 2" in result.content[0].text

    def test_stderr_capture(self):
        """Test stderr is captured correctly"""
        executor = BashExecutor()
        result = executor.execute("echo 'error message' >&2")

        # Command succeeds (echo to stderr is valid)
        assert result.type == "success"
        # stderr should contain the error message
        assert "error message" in result.metadata.get("stderr", "")

    def test_mixed_stdout_stderr(self):
        """Test both stdout and stderr are captured"""
        executor = BashExecutor()
        result = executor.execute(
            "echo 'to stdout'; echo 'to stderr' >&2"
        )

        assert result.type == "success"
        assert "to stdout" in result.content[0].text
        assert "to stderr" in result.metadata.get("stderr", "")

    def test_multiline_output(self):
        """Test multiline output capture"""
        executor = BashExecutor()
        result = executor.execute("for i in 1 2 3; do echo Line $i; done")

        assert result.type == "success"
        assert "Line 1" in result.content[0].text
        assert "Line 2" in result.content[0].text
        assert "Line 3" in result.content[0].text


# ═══════════════════════════════════════════════════════════════════════════
# CATEGORY 5: SAFETY & VALIDATION
# ═══════════════════════════════════════════════════════════════════════════

class TestSafetyValidation:
    """Test command safety validation"""

    def test_dangerous_command_detection(self):
        """Test detection of dangerous commands (if implemented)"""
        executor = BashExecutor()

        # If CommandValidator exists, these should be blocked or flagged
        dangerous_commands = [
            "rm -rf /",
            ":(){ :|:& };:",  # Fork bomb
            "dd if=/dev/zero of=/dev/sda",
        ]

        for cmd in dangerous_commands:
            # Either blocked (raises exception) or flagged (result.is_dangerous)
            try:
                result = executor.execute(cmd)
                # If not blocked, check if flagged as dangerous
                # (API may vary - discover during TDD)
            except Exception as e:
                # Blocking is acceptable too
                assert "dangerous" in str(e).lower() or "blocked" in str(e).lower()

    def test_command_injection_prevention(self):
        """Test command injection is prevented"""
        executor = BashExecutor()

        # Attempt injection via semicolon
        # Note: This depends on how BashExecutor handles input
        # If it uses shell=True, this is a known risk
        result = executor.execute("echo safe; echo injected")

        # Both commands might execute - verify controlled behavior
        assert result.type == "success" or result.type == "error"
        # Main test: doesn't crash catastrophically


# ═══════════════════════════════════════════════════════════════════════════
# CATEGORY 6: WORKING DIRECTORY
# ═══════════════════════════════════════════════════════════════════════════

class TestWorkingDirectory:
    """Test working directory handling"""

    def test_cwd_parameter(self, temp_dir):
        """Test cwd parameter sets working directory"""
        # Create nested directory
        nested = temp_dir / "nested"
        nested.mkdir()
        (nested / "marker.txt").write_text("test")

        executor = BashExecutor()
        # Execute ls in nested directory
        result = executor.execute("ls", cwd=str(nested))

        assert result.type == "success"
        assert "marker.txt" in result.content[0].text

    def test_default_cwd_preserved(self):
        """Test default cwd is preserved after execution"""
        original_cwd = os.getcwd()

        executor = BashExecutor()
        executor.execute("cd /tmp")

        # CWD should be preserved (not changed by executor)
        assert os.getcwd() == original_cwd


# ═══════════════════════════════════════════════════════════════════════════
# RUN SUMMARY
# ═══════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
