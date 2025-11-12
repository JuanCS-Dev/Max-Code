"""
End-to-End Flow Test Suite
Constitutional AI v3.0 - FASE 2.3

Tests REAL end-to-end workflows combining multiple components.
Following Anthropic TDD: Write tests → Run → Discover APIs → Adjust

Target: 6+ tests, 90%+ pass rate
"""

import pytest
import sys
import subprocess
import time
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from core.tools.file_writer import FileWriter
from core.tools.file_reader import FileReader
from core.tools.bash_executor import BashExecutor


# ═══════════════════════════════════════════════════════════════════════════
# CATEGORY 1: FILE MANIPULATION E2E
# ═══════════════════════════════════════════════════════════════════════════

class TestFileManipulationE2E:
    """Test complete file manipulation workflows"""

    def test_create_edit_read_workflow(self, temp_dir):
        """Test create → edit → read workflow"""
        file_path = temp_dir / "workflow_test.txt"

        # Step 1: Create file
        writer = FileWriter()
        writer.write(str(file_path), "Original content\n")

        assert file_path.exists()

        # Step 2: Edit file (via reading and rewriting)
        reader = FileReader()
        read_result = reader.read(str(file_path))
        assert read_result.success

        modified = read_result.content.replace("Original", "Modified")
        writer.write(str(file_path), modified)

        # Step 3: Verify changes
        final_result = reader.read(str(file_path))
        assert "Modified" in final_result.content
        assert "Original" not in final_result.content

    def test_bash_creates_file_then_read(self, temp_dir):
        """Test bash creates file → then read it"""
        executor = BashExecutor()
        reader = FileReader()

        output_file = temp_dir / "bash_created.txt"

        # Bash creates file
        bash_result = executor.execute(f"echo 'Bash created this' > {output_file}")
        assert bash_result.type == "success"

        # Read file created by bash
        read_result = reader.read(str(output_file))
        assert read_result.success
        assert "Bash created this" in read_result.content


# ═══════════════════════════════════════════════════════════════════════════
# CATEGORY 2: CLI END-TO-END WORKFLOWS
# ═══════════════════════════════════════════════════════════════════════════

class TestCLIWorkflows:
    """Test complete CLI workflows"""

    def test_cli_health_then_predict_workflow(self):
        """Test health check → then predict"""
        # Step 1: Health check
        health_result = subprocess.run(
            ["python", "-m", "cli.main", "health"],
            capture_output=True,
            text=True,
            timeout=60
        )

        # Health executes (services may be down)
        assert health_result.returncode in [0, 1]

        # Step 2: Run predict
        predict_result = subprocess.run(
            ["python", "-m", "cli.main", "predict"],
            capture_output=True,
            text=True,
            timeout=10
        )

        # Predict shows suggestions
        assert predict_result.returncode == 0
        assert len(predict_result.stdout) > 0

    def test_cli_multiple_commands_in_sequence(self):
        """Test running multiple CLI commands sequentially"""
        commands = [
            ["python", "-m", "cli.main", "--help"],
            ["python", "-m", "cli.main", "predict", "--help"],
            ["python", "-m", "cli.main", "health", "--help"],
        ]

        for cmd in commands:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=10
            )
            # All help commands should succeed
            assert result.returncode == 0


# ═══════════════════════════════════════════════════════════════════════════
# CATEGORY 3: TOOL COMPOSITION E2E
# ═══════════════════════════════════════════════════════════════════════════

class TestToolCompositionE2E:
    """Test complex tool composition"""

    def test_multi_tool_pipeline(self, temp_dir):
        """Test pipeline: bash → file read → file write → bash verify"""
        executor = BashExecutor()
        reader = FileReader()
        writer = FileWriter()

        # Step 1: Create file via bash
        source = temp_dir / "source.txt"
        executor.execute(f"echo 'Source data' > {source}")

        # Step 2: Read source
        content = reader.read(str(source))
        assert content.success

        # Step 3: Transform and write to destination
        transformed = content.content.upper()
        dest = temp_dir / "dest.txt"
        writer.write(str(dest), transformed)

        # Step 4: Verify via bash
        verify_result = executor.execute(f"cat {dest}")
        assert "SOURCE DATA" in verify_result.content[0].text

    def test_concurrent_tool_usage(self, temp_dir):
        """Test multiple tools can be used concurrently"""
        import threading

        results = []

        def read_task():
            reader = FileReader()
            file = temp_dir / "concurrent1.txt"
            file.write_text("Concurrent 1")
            results.append(reader.read(str(file)))

        def write_task():
            writer = FileWriter()
            file = temp_dir / "concurrent2.txt"
            writer.write(str(file), "Concurrent 2")
            results.append(file.exists())

        def bash_task():
            executor = BashExecutor()
            result = executor.execute("echo 'concurrent bash'")
            results.append(result.type == "success")

        # Run tasks in parallel
        threads = [
            threading.Thread(target=read_task),
            threading.Thread(target=write_task),
            threading.Thread(target=bash_task),
        ]

        for t in threads:
            t.start()

        for t in threads:
            t.join(timeout=10)

        # All tasks should complete successfully
        assert len(results) == 3
        assert all(results)


# ═══════════════════════════════════════════════════════════════════════════
# CATEGORY 4: ERROR RECOVERY E2E
# ═══════════════════════════════════════════════════════════════════════════

class TestErrorRecoveryE2E:
    """Test error handling and recovery in workflows"""

    def test_recover_from_file_not_found(self, temp_dir):
        """Test workflow recovers from file not found error"""
        reader = FileReader()
        writer = FileWriter()

        missing_file = temp_dir / "missing.txt"

        # Try to read missing file
        result = reader.read(str(missing_file))
        assert not result.success

        # Recover: create the file
        writer.write(str(missing_file), "Now it exists")

        # Retry reading
        retry_result = reader.read(str(missing_file))
        assert retry_result.success
        assert "Now it exists" in retry_result.content


# ═══════════════════════════════════════════════════════════════════════════
# RUN SUMMARY
# ═══════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
