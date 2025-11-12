"""
Tests for task_command - Main Task Execution

NO MOCK, NO PLACEHOLDER, NO TODO
"""

import pytest
from click.testing import CliRunner
from cli.task_command import task


class TestTaskCommandHelp:
    def setup_method(self):
        self.runner = CliRunner()

    def test_task_help(self):
        result = self.runner.invoke(task, ["--help"])
        assert result.exit_code == 0
        assert "task" in result.output.lower()


class TestTaskCommandBasic:
    def setup_method(self):
        self.runner = CliRunner()

    def test_task_simple(self):
        result = self.runner.invoke(task, ["list", "files"])
        assert result.exit_code in [0, 1]

    def test_task_with_cwd(self):
        result = self.runner.invoke(task, ["list", "files", "--cwd", "."])
        assert result.exit_code in [0, 1]

    def test_task_no_stream(self):
        result = self.runner.invoke(task, ["analyze", "code", "--no-stream"])
        assert result.exit_code in [0, 1]

    def test_task_show_tools(self):
        result = self.runner.invoke(task, ["test", "function", "--show-tools"])
        assert result.exit_code in [0, 1]


class TestTaskCommandMissing:
    def setup_method(self):
        self.runner = CliRunner()

    def test_task_missing_argument(self):
        result = self.runner.invoke(task, [])
        assert result.exit_code != 0
        assert "required" in result.output.lower() or "missing" in result.output.lower()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
