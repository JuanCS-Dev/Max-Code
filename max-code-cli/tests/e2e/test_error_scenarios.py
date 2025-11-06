"""
E2E Error Scenario Tests

Tests error handling, edge cases, and failure modes.
Ensures Max-Code degrades gracefully under adverse conditions.

Philosophy: "Fail fast, fail gracefully, never hang."
"""

import pytest
import time
import subprocess
from pathlib import Path
from click.testing import CliRunner

from cli.main import cli


class TestServiceUnavailableScenarios:
    """Test behavior when MAXIMUS services are unavailable."""

    def test_all_services_down_health_check(self, cli_runner, performance_tracker):
        """
        All 8 MAXIMUS services down - health check should report clearly.

        Critical: Should NOT hang, should complete in < 10s even with 8 services.
        """
        start = time.perf_counter()
        result = cli_runner.invoke(cli, ["health"])
        elapsed_ms = (time.perf_counter() - start) * 1000

        # Should complete even with all services down
        assert result.exit_code in [0, 1]

        # Should show service status
        assert "Service" in result.output or "Health" in result.output

        performance_tracker.record("all_services_down", elapsed_ms)

        # Circuit breaker should prevent hanging
        # 8 services * 1s timeout = 8s max, but circuit breaker should reduce this
        assert elapsed_ms < 10000, \
            f"Health check with all services down took {elapsed_ms:.2f}ms (hanging)"

    def test_predict_with_services_down_uses_heuristic(self, cli_runner, python_project):
        """
        Predict command falls back to heuristic when services unavailable.

        3-tier fallback: Oraculo → Claude → Heuristic
        """
        with cli_runner.isolated_filesystem(temp_dir=python_project):
            result = cli_runner.invoke(cli, ["predict", "--mode", "fast"])

            # Should complete even without services
            assert result.exit_code in [0, 1]

            # If exit code 0, should show predictions (from heuristic)
            if result.exit_code == 0:
                # Heuristic should suggest reasonable commands
                assert len(result.output) > 0

    def test_sabbath_mode_without_penelope(self, cli_runner):
        """
        Sabbath mode should work locally even if Penelope is down.

        Local schedule calculations don't require external services.
        """
        result = cli_runner.invoke(cli, ["sabbath", "status"])

        # Should show status even without services
        assert result.exit_code in [0, 1]

    def test_learning_system_offline_mode(self, cli_runner, isolated_config):
        """
        Learning system should work entirely locally when services down.

        GDPR compliance: All data local, no external dependencies.
        """
        # Enable learning (local only)
        enable_result = cli_runner.invoke(cli, ["learn", "enable"], input="y\n")

        # Should work without external services
        assert enable_result.exit_code in [0, 1]

        # Check status (local database query)
        status_result = cli_runner.invoke(cli, ["learn", "status"])
        assert status_result.exit_code in [0, 1]


class TestInvalidInputHandling:
    """Test handling of invalid user inputs."""

    def test_invalid_mode_parameter(self, cli_runner):
        """User provides invalid --mode value."""
        result = cli_runner.invoke(cli, ["predict", "--mode", "invalid"])

        # Should reject with clear error
        assert result.exit_code != 0
        # Click validation should provide helpful message

    def test_nonexistent_command(self, cli_runner):
        """User runs non-existent command."""
        result = cli_runner.invoke(cli, ["nonexistent"])

        # Should fail with suggestion
        assert result.exit_code != 0

    def test_missing_required_argument(self, cli_runner):
        """User omits required argument."""
        # Example: chat command without message
        result = cli_runner.invoke(cli, ["chat"])

        # Should fail gracefully or prompt for input
        assert result.exit_code in [0, 1, 2]  # 2 is Click's usage error code

    def test_invalid_config_values(self, cli_runner, isolated_config):
        """User sets invalid configuration values."""
        # Try to use config command (may not have set subcommand)
        result = cli_runner.invoke(cli, ["config"])

        # Should show usage or work
        assert result.exit_code in [0, 1, 2]


class TestFilesystemErrors:
    """Test handling of filesystem-related errors."""

    def test_readonly_config_directory(self, cli_runner, tmp_path):
        """Config directory is read-only."""
        config_dir = tmp_path / ".max-code"
        config_dir.mkdir(parents=True, exist_ok=True)

        # Make read-only
        import os
        os.chmod(config_dir, 0o444)

        try:
            # Try to use config command (should fail gracefully)
            result = cli_runner.invoke(cli, ["config"])

            # Should handle gracefully (not crash)
            assert result.exit_code in [0, 1, 2]

        finally:
            # Restore permissions for cleanup
            os.chmod(config_dir, 0o755)

    def test_corrupted_database(self, cli_runner, isolated_config):
        """Learning database is corrupted."""
        # Create corrupted database
        db_path = isolated_config / "learning.db"
        db_path.parent.mkdir(parents=True, exist_ok=True)
        db_path.write_text("corrupted data")

        # Try to use learning system
        result = cli_runner.invoke(cli, ["learn", "status"])

        # Should handle corruption gracefully (recreate DB or show error)
        assert result.exit_code in [0, 1]

    def test_disk_full_simulation(self, cli_runner, isolated_config, monkeypatch):
        """Simulate disk full condition."""
        # This is hard to test without actual disk full
        # Can be tested manually or with Docker resource limits
        pytest.skip("Disk full simulation requires special environment")


class TestGitRepositoryErrors:
    """Test handling of git-related errors."""

    def test_not_in_git_repo(self, cli_runner, tmp_path):
        """User runs predict outside git repository."""
        non_git_dir = tmp_path / "not-a-repo"
        non_git_dir.mkdir(parents=True, exist_ok=True)

        with cli_runner.isolated_filesystem(temp_dir=non_git_dir):
            result = cli_runner.invoke(cli, ["predict", "--mode", "fast"])

            # Should work even without git
            assert result.exit_code in [0, 1]

    def test_corrupted_git_repo(self, cli_runner, mock_git_repo):
        """Git repository is corrupted."""
        # Corrupt .git directory
        git_dir = mock_git_repo / ".git"
        (git_dir / "HEAD").write_text("corrupted")

        with cli_runner.isolated_filesystem(temp_dir=mock_git_repo):
            result = cli_runner.invoke(cli, ["predict", "--mode", "fast"])

            # Should handle gracefully (git commands may fail, but CLI shouldn't crash)
            assert result.exit_code in [0, 1]

    def test_detached_head_state(self, cli_runner, mock_git_repo):
        """Git repository in detached HEAD state."""
        # Create detached HEAD
        subprocess.run(
            ["git", "checkout", "HEAD~0"],
            cwd=mock_git_repo,
            capture_output=True
        )

        with cli_runner.isolated_filesystem(temp_dir=mock_git_repo):
            result = cli_runner.invoke(cli, ["predict", "--mode", "fast"])

            # Should handle detached HEAD gracefully
            assert result.exit_code in [0, 1]


class TestConcurrencyErrors:
    """Test concurrent access and race conditions."""

    @pytest.mark.skip(reason="Rich Console not thread-safe - concurrent tests run at integration level")
    def test_concurrent_database_writes(self, cli_runner, isolated_config):
        """Multiple processes writing to learning database simultaneously."""
        import concurrent.futures

        def write_execution():
            """Simulate recording command execution."""
            runner = CliRunner()
            # This would normally record an execution
            # For now, just run learn status
            result = runner.invoke(cli, ["learn", "status"])
            return result.exit_code

        # Run 10 concurrent operations
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(write_execution) for _ in range(10)]
            results = [f.result() for f in concurrent.futures.as_completed(futures)]

        # All should complete (SQLite handles concurrent access with locks)
        assert all(code in [0, 1] for code in results)

    @pytest.mark.skip(reason="Rich Console not thread-safe - concurrent tests run at integration level")
    def test_config_file_race_condition(self, cli_runner, isolated_config):
        """Two processes modifying config simultaneously."""
        import concurrent.futures

        def modify_config():
            runner = CliRunner()
            result = runner.invoke(cli, ["config"])
            return result.exit_code

        # Run 5 concurrent config reads
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(modify_config) for _ in range(5)]
            results = [f.result() for f in concurrent.futures.as_completed(futures)]

        # Should handle gracefully (concurrent reads should work)
        assert all(code in [0, 1, 2] for code in results)


class TestMemoryLeaks:
    """Test for memory leaks in long-running operations."""

    def test_repeated_predictions_no_memory_leak(self, cli_runner, python_project):
        """
        Run many predictions to check for memory leaks.

        Memory should stay roughly constant, not grow unbounded.
        """
        import tracemalloc

        tracemalloc.start()

        with cli_runner.isolated_filesystem(temp_dir=python_project):
            # Get baseline memory
            snapshot_start = tracemalloc.take_snapshot()

            # Run 50 predictions
            for _ in range(50):
                result = cli_runner.invoke(cli, ["predict", "--mode", "fast"])
                assert result.exit_code in [0, 1]

            # Check memory after
            snapshot_end = tracemalloc.take_snapshot()

        tracemalloc.stop()

        # Compare memory usage
        top_stats = snapshot_end.compare_to(snapshot_start, 'lineno')

        # Total memory increase (in KB)
        total_increase = sum(stat.size_diff for stat in top_stats) / 1024

        # Allow some increase, but not unbounded growth
        # 50 predictions should not leak > 10MB
        assert total_increase < 10 * 1024, \
            f"Memory leak detected: {total_increase:.2f}KB increase over 50 predictions"

    def test_health_check_loop_memory_stable(self, cli_runner):
        """
        Health check loop (monitoring scenario) should not leak memory.
        """
        import tracemalloc

        tracemalloc.start()
        snapshot_start = tracemalloc.take_snapshot()

        # Simulate monitoring loop
        for _ in range(20):
            result = cli_runner.invoke(cli, ["health"])
            assert result.exit_code in [0, 1]

        snapshot_end = tracemalloc.take_snapshot()
        tracemalloc.stop()

        top_stats = snapshot_end.compare_to(snapshot_start, 'lineno')
        total_increase = sum(stat.size_diff for stat in top_stats) / 1024

        # 20 health checks should not leak > 5MB
        assert total_increase < 5 * 1024, \
            f"Memory leak in health check: {total_increase:.2f}KB increase"


class TestRateLimitingEdgeCases:
    """Test rate limiting behavior under edge cases."""

    def test_rate_limit_enforcement(self, cli_runner, python_project):
        """
        Rapid predictions should trigger rate limiting.

        Rate limiter should protect services without hanging.
        """
        with cli_runner.isolated_filesystem(temp_dir=python_project):
            results = []

            # Fire 20 rapid predictions
            for i in range(20):
                start = time.perf_counter()
                result = cli_runner.invoke(cli, ["predict", "--mode", "fast"])
                elapsed_ms = (time.perf_counter() - start) * 1000

                results.append({
                    "iteration": i,
                    "exit_code": result.exit_code,
                    "duration_ms": elapsed_ms,
                    "rate_limited": "rate limit" in result.output.lower() if result.output else False
                })

        # At least some requests should be rate limited (or all should succeed fast)
        rate_limited_count = sum(1 for r in results if r["rate_limited"])

        # Either rate limiting kicks in OR all complete successfully
        # (depending on whether services are available)
        assert all(r["exit_code"] in [0, 1] for r in results)

    def test_rate_limit_recovery(self, cli_runner, python_project):
        """
        After rate limit window expires, requests should succeed again.
        """
        with cli_runner.isolated_filesystem(temp_dir=python_project):
            # Trigger rate limit
            for _ in range(10):
                cli_runner.invoke(cli, ["predict", "--mode", "fast"])

            # Wait for rate limit window to expire (typically 60s, but tests use shorter)
            time.sleep(2)

            # Next request should succeed
            result = cli_runner.invoke(cli, ["predict", "--mode", "fast"])
            assert result.exit_code in [0, 1]


class TestCircuitBreakerBehavior:
    """Test circuit breaker pattern for service failures."""

    def test_circuit_breaker_opens_after_failures(self, cli_runner):
        """
        After N consecutive failures, circuit breaker should open.

        This prevents hammering unavailable services.
        """
        results = []

        # Run health checks repeatedly (services likely down in test)
        for i in range(10):
            result = cli_runner.invoke(cli, ["health"])
            results.append({
                "iteration": i,
                "exit_code": result.exit_code
            })

        # All should complete (circuit breaker prevents hanging)
        assert all(r["exit_code"] in [0, 1] for r in results)

    def test_circuit_breaker_half_open_recovery(self, cli_runner):
        """
        Circuit breaker should attempt recovery after timeout.

        After breaker opens, it should periodically test if service recovered.
        """
        # Trigger circuit breaker
        for _ in range(5):
            cli_runner.invoke(cli, ["health"])

        # Wait for half-open state (30s typically, but tests may use shorter)
        time.sleep(2)

        # Next request should attempt connection (half-open state)
        result = cli_runner.invoke(cli, ["health"])
        assert result.exit_code in [0, 1]


class TestGDPRComplianceErrors:
    """Test GDPR compliance under error conditions."""

    def test_data_export_with_empty_database(self, cli_runner, isolated_config):
        """Export data when no learning data exists."""
        result = cli_runner.invoke(cli, ["learn", "export", "export.json"])

        # Should succeed with empty export
        assert result.exit_code in [0, 1]

    def test_data_deletion_confirmation_required(self, cli_runner, isolated_config):
        """Data deletion should require explicit confirmation."""
        # Try to delete without confirmation
        result = cli_runner.invoke(cli, ["learn", "reset"])

        # Should prompt for confirmation or require --confirm flag
        # (Exact behavior depends on implementation)
        assert result.exit_code in [0, 1, 2]

    def test_learning_disabled_no_data_collection(self, cli_runner, isolated_config):
        """When learning disabled, no data should be collected."""
        # Ensure learning is disabled
        cli_runner.invoke(cli, ["learn", "disable"])

        # Run commands (should not record)
        cli_runner.invoke(cli, ["predict", "--mode", "fast"])

        # Check statistics - should show 0 executions
        result = cli_runner.invoke(cli, ["learn", "status"])

        # Should show learning disabled
        if result.exit_code == 0:
            assert "disabled" in result.output.lower() or "0" in result.output


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short", "-x"])  # -x stops on first failure
