"""E2E Tests for 'max-code heal' command"""
import pytest


class TestHealE2E:
    @pytest.mark.e2e
    def test_heal_help(self, invoke_command):
        result = invoke_command("heal", ["--help"])
        assert result.exit_code == 0
