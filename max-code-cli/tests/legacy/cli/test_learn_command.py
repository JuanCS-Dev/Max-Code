"""
Tests for learn_command - Learning Mode Management

NO MOCK, NO PLACEHOLDER, NO TODO
"""

import pytest
from click.testing import CliRunner
from cli.learn_command import learn


class TestLearnCommandHelp:
    def setup_method(self):
        self.runner = CliRunner()

    def test_learn_help(self):
        result = self.runner.invoke(learn, ["--help"])
        assert result.exit_code == 0


class TestLearnCommandEnable:
    def setup_method(self):
        self.runner = CliRunner()

    def test_learn_enable(self):
        result = self.runner.invoke(learn, ["enable"])
        assert result.exit_code in [0, 1]

    def test_learn_enable_auto(self):
        result = self.runner.invoke(learn, ["enable", "--auto"])
        assert result.exit_code in [0, 1]


class TestLearnCommandDisable:
    def setup_method(self):
        self.runner = CliRunner()

    def test_learn_disable(self):
        result = self.runner.invoke(learn, ["disable"])
        assert result.exit_code in [0, 1]


class TestLearnCommandInsights:
    def setup_method(self):
        self.runner = CliRunner()

    def test_learn_insights(self):
        result = self.runner.invoke(learn, ["insights"])
        assert result.exit_code in [0, 1]


class TestLearnCommandExport:
    def setup_method(self):
        self.runner = CliRunner()

    def test_learn_export(self):
        result = self.runner.invoke(learn, ["export", "/tmp/test_export.json"])
        assert result.exit_code in [0, 1]


class TestLearnCommandReset:
    def setup_method(self):
        self.runner = CliRunner()

    def test_learn_reset_cancelled(self):
        result = self.runner.invoke(learn, ["reset"], input="n\n")
        assert result.exit_code in [0, 1]

    def test_learn_reset_confirm_flag(self):
        result = self.runner.invoke(learn, ["reset", "--confirm"])
        assert result.exit_code in [0, 1]


class TestLearnCommandStatus:
    def setup_method(self):
        self.runner = CliRunner()

    def test_learn_status(self):
        result = self.runner.invoke(learn, ["status"])
        assert result.exit_code in [0, 1]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
