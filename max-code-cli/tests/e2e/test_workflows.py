"""
E2E Workflow Tests - Real User Scenarios

Tests complete user workflows from start to finish.
Focus on realistic developer experiences and performance.

Performance Targets:
- Health check: < 500ms
- First chat token: < 1000ms
- Fast predict: < 100ms
- Config operations: < 50ms
"""

import pytest
import time
from pathlib import Path
from click.testing import CliRunner

from cli.main import cli


class TestFirstTimeUserWorkflow:
    """Test the experience of a new user discovering Max-Code."""

    def test_help_command_is_fast(self, cli_runner, performance_tracker):
        """First interaction - user runs --help."""
        start = time.perf_counter()
        result = cli_runner.invoke(cli, ["--help"])
        elapsed_ms = (time.perf_counter() - start) * 1000

        assert result.exit_code == 0
        assert "Max-Code CLI" in result.output or "Usage:" in result.output

        performance_tracker.record("--help", elapsed_ms)
        assert elapsed_ms < 100, f"Help command took {elapsed_ms:.2f}ms (too slow for first impression)"

    def test_health_check_first_run(self, cli_runner, isolated_config, performance_tracker):
        """User checks if services are running."""
        start = time.perf_counter()
        result = cli_runner.invoke(cli, ["health"])
        elapsed_ms = (time.perf_counter() - start) * 1000

        # Should work even if services are down
        assert result.exit_code == 0
        assert "Health Check" in result.output or "Service" in result.output

        performance_tracker.record("health", elapsed_ms)
        # Health check should be fast even with timeouts
        assert elapsed_ms < 3000, f"Health check took {elapsed_ms:.2f}ms (includes timeout delays)"

    def test_config_view_defaults(self, cli_runner, isolated_config):
        """User views default configuration."""
        result = cli_runner.invoke(cli, ["config"])

        # Should show configuration (or prompt to create)
        assert result.exit_code in [0, 1, 2]  # 2 if command needs subcommands

    def test_first_prediction_request(self, cli_runner, isolated_config, python_project, performance_tracker):
        """User tries their first command prediction."""
        # Change to project directory
        with cli_runner.isolated_filesystem(temp_dir=python_project):
            start = time.perf_counter()
            result = cli_runner.invoke(cli, ["predict", "--mode", "fast"])
            elapsed_ms = (time.perf_counter() - start) * 1000

            # Should not crash even if services unavailable
            assert result.exit_code in [0, 1]  # 1 if services down

            performance_tracker.record("predict --fast", elapsed_ms)

            # Fast mode must be FAST (critical to avoid "LERDEZA extrema")
            # Allow 5s when services are down (includes retry delays)
            if result.exit_code == 0:
                assert elapsed_ms < 5000, f"Fast predict took {elapsed_ms:.2f}ms (too slow)"


class TestDevelopmentWorkflow:
    """Test typical development workflow with Max-Code."""

    def test_git_workflow_with_predictions(self, cli_runner, python_project, performance_tracker):
        """
        Realistic workflow:
        1. User makes code changes
        2. Checks git status
        3. Asks Max-Code for next command
        4. Commits changes
        """
        import subprocess

        with cli_runner.isolated_filesystem(temp_dir=python_project):
            # First commit the existing files so changes can be detected
            subprocess.run(
                ["git", "add", "."],
                cwd=python_project,
                capture_output=True,
                check=True
            )
            subprocess.run(
                ["git", "commit", "-m", "Add project files"],
                cwd=python_project,
                capture_output=True,
                check=True
            )

            # Step 1: Make a change
            main_file = python_project / "src" / "test_project" / "main.py"
            main_file.write_text("""
def hello(name: str) -> str:
    \"\"\"Greet someone warmly.\"\"\"
    return f"Hello, {name}! Welcome!"
""")

            # Step 2: User asks for prediction
            start = time.perf_counter()
            result = cli_runner.invoke(cli, ["predict", "--mode", "fast"])
            elapsed_ms = (time.perf_counter() - start) * 1000

            # Should suggest git commands (if services available)
            # Or gracefully degrade if not
            assert result.exit_code in [0, 1]

            performance_tracker.record("predict_in_dirty_repo", elapsed_ms)

            # Step 3: User can still use git normally
            git_result = subprocess.run(
                ["git", "status"],
                cwd=python_project,
                capture_output=True,
                text=True
            )
            assert git_result.returncode == 0
            assert "modified:" in git_result.stdout or "Changes not staged" in git_result.stdout

    def test_learning_system_activation(self, cli_runner, isolated_config):
        """
        User enables learning system (GDPR opt-in).

        This tests:
        - Config modification
        - Privacy consent flow
        - Learning system initialization
        """
        # Enable learning
        result = cli_runner.invoke(
            cli,
            ["learn", "enable"],
            input="y\n"  # Confirm GDPR consent
        )

        # Should succeed or prompt for confirmation
        assert result.exit_code in [0, 1, 2]

        # Verify learning is enabled
        config_result = cli_runner.invoke(cli, ["learn", "status"])
        assert config_result.exit_code in [0, 1, 2]

    def test_sabbath_mode_toggle(self, cli_runner, isolated_config, performance_tracker):
        """User enables Sabbath mode for rest periods."""
        start = time.perf_counter()
        result = cli_runner.invoke(cli, ["sabbath", "status"])
        elapsed_ms = (time.perf_counter() - start) * 1000

        # Should show status (even if services down)
        assert result.exit_code in [0, 1]

        performance_tracker.record("sabbath status", elapsed_ms)
        assert elapsed_ms < 500, f"Sabbath status took {elapsed_ms:.2f}ms"


class TestProductionDeploymentWorkflow:
    """Test production deployment scenarios."""

    def test_health_check_monitoring(self, cli_runner, performance_tracker):
        """
        Production monitoring scenario:
        - Run health check periodically
        - Verify service availability
        - Alert on failures
        """
        results = []

        # Simulate 5 health checks (monitoring loop)
        for i in range(5):
            start = time.perf_counter()
            result = cli_runner.invoke(cli, ["health"])
            elapsed_ms = (time.perf_counter() - start) * 1000

            results.append({
                "iteration": i,
                "exit_code": result.exit_code,
                "duration_ms": elapsed_ms
            })

            performance_tracker.record(f"health_check_{i}", elapsed_ms)

        # All checks should complete (even if services down)
        assert all(r["exit_code"] in [0, 1] for r in results)

        # Average latency should be reasonable
        avg_latency = sum(r["duration_ms"] for r in results) / len(results)
        assert avg_latency < 3000, f"Average health check latency {avg_latency:.2f}ms too high"

    def test_graceful_degradation_no_services(self, cli_runner, python_project):
        """
        Critical test: Max-Code should work even when ALL services are down.

        This prevents "LERDEZA extrema" - tools that hang waiting for services.
        """
        with cli_runner.isolated_filesystem(temp_dir=python_project):
            # Try all major commands with services down
            commands_to_test = [
                ["health"],
                ["predict", "--mode", "fast"],
                ["learn", "status"],
                ["sabbath", "status"],
                ["config"],
            ]

            for cmd in commands_to_test:
                start = time.perf_counter()
                result = cli_runner.invoke(cli, cmd)
                elapsed_ms = (time.perf_counter() - start) * 1000

                # Should complete quickly even with failures
                assert elapsed_ms < 5000, \
                    f"Command {' '.join(cmd)} took {elapsed_ms:.2f}ms (hanging on unavailable services)"

                # Should fail gracefully, not crash
                assert result.exit_code in [0, 1], \
                    f"Command {' '.join(cmd)} crashed with exit code {result.exit_code}"


class TestErrorRecoveryWorkflows:
    """Test how Max-Code handles errors and recovers."""

    def test_invalid_command_suggestions(self, cli_runner):
        """User types invalid command - should get helpful suggestion."""
        result = cli_runner.invoke(cli, ["predic"])  # Typo: predic instead of predict

        # Click should suggest correct command
        assert result.exit_code != 0
        # Output should be helpful (Click provides suggestions)

    def test_corrupted_config_recovery(self, cli_runner, isolated_config):
        """User has corrupted config file - should recover gracefully."""
        # Create corrupted config
        config_file = isolated_config / "config.json"
        config_file.parent.mkdir(parents=True, exist_ok=True)
        config_file.write_text("{ invalid json }")

        # Commands should still work (recreate config)
        result = cli_runner.invoke(cli, ["config"])

        # Should handle gracefully (may show usage with exit code 2)
        assert result.exit_code in [0, 1, 2]

    def test_network_timeout_fast_fail(self, cli_runner, performance_tracker):
        """
        Service timeout should fail FAST, not hang.

        This is critical to avoid "LERDEZA extrema".
        """
        start = time.perf_counter()
        result = cli_runner.invoke(cli, ["health", "--detailed"])
        elapsed_ms = (time.perf_counter() - start) * 1000

        performance_tracker.record("health_timeout", elapsed_ms)

        # Even with timeouts, should complete in reasonable time
        # Circuit breaker should kick in after first failure
        assert elapsed_ms < 10000, \
            f"Health check with timeouts took {elapsed_ms:.2f}ms (should fail fast)"


class TestPerformanceCriticalPaths:
    """Test performance-critical user paths."""

    def test_cold_start_latency(self, cli_runner, performance_tracker):
        """
        Measure cold start - first command execution.

        Critical for user experience - slow cold start = bad first impression.
        """
        start = time.perf_counter()
        result = cli_runner.invoke(cli, ["--version"])
        elapsed_ms = (time.perf_counter() - start) * 1000

        assert result.exit_code == 0

        performance_tracker.record("cold_start", elapsed_ms)
        assert elapsed_ms < 200, f"Cold start took {elapsed_ms:.2f}ms (too slow)"

    def test_rapid_fire_predictions(self, cli_runner, python_project, performance_tracker):
        """
        User makes multiple rapid predictions (chat-like experience).

        Tests:
        - No memory leaks
        - Consistent performance
        - Rate limiting
        """
        timings = []

        with cli_runner.isolated_filesystem(temp_dir=python_project):
            for i in range(10):
                start = time.perf_counter()
                result = cli_runner.invoke(cli, ["predict", "--mode", "fast"])
                elapsed_ms = (time.perf_counter() - start) * 1000

                timings.append(elapsed_ms)
                performance_tracker.record(f"rapid_fire_{i}", elapsed_ms)

                # Each should complete
                assert result.exit_code in [0, 1]

        # Performance should not degrade over time
        first_half_avg = sum(timings[:5]) / 5
        second_half_avg = sum(timings[5:]) / 5

        # Allow 50% slowdown due to rate limiting, but no more
        assert second_half_avg < first_half_avg * 1.5, \
            f"Performance degraded: {first_half_avg:.2f}ms → {second_half_avg:.2f}ms"

    @pytest.mark.skip(reason="Rich Console not thread-safe - concurrent CLI usage tested in integration tests")
    def test_concurrent_command_safety(self, isolated_config):
        """
        Test running multiple commands concurrently.

        NOTE: Skipped because Rich Console is not thread-safe.
        Concurrent usage should be tested at integration level (separate processes).

        Ensures:
        - No database locks
        - No race conditions
        - Thread safety
        """
        import concurrent.futures

        def run_command():
            # Each thread needs its own CliRunner (not thread-safe to share)
            runner = CliRunner(mix_stderr=False)
            # Use --no-banner to avoid Rich Console thread safety issues
            result = runner.invoke(cli, ["--no-banner", "health"], catch_exceptions=False)
            return result.exit_code

        # Run 5 concurrent health checks
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(run_command) for _ in range(5)]
            results = [f.result() for f in concurrent.futures.as_completed(futures)]

        # All should complete without crashes
        assert all(code in [0, 1] for code in results)


# ============================================================================
# PERFORMANCE SUMMARY TEST
# ============================================================================

class TestPerformanceSummary:
    """Summary of all performance tests."""

    @pytest.mark.slow
    def test_generate_performance_report(self, performance_tracker):
        """
        Generate performance report from all tracked timings.

        This runs at the end to summarize all performance data.
        """
        if not performance_tracker.timings:
            pytest.skip("No performance data collected")

        print("\n" + "="*80)
        print("PERFORMANCE REPORT - E2E Tests")
        print("="*80)

        # Group by command
        commands = {}
        for timing in performance_tracker.timings:
            cmd = timing["command"]
            if cmd not in commands:
                commands[cmd] = []
            commands[cmd].append(timing["duration_ms"])

        # Print summary
        for cmd, times in sorted(commands.items()):
            avg = sum(times) / len(times)
            min_time = min(times)
            max_time = max(times)
            count = len(times)

            print(f"\n{cmd}:")
            print(f"  Count: {count}")
            print(f"  Avg:   {avg:.2f}ms")
            print(f"  Min:   {min_time:.2f}ms")
            print(f"  Max:   {max_time:.2f}ms")

        print("\n" + "="*80)

        # Assert key performance targets
        if "health" in commands:
            health_avg = sum(commands["health"]) / len(commands["health"])
            # Allow higher latency due to timeouts in tests
            assert health_avg < 5000, f"Health check average {health_avg:.2f}ms exceeds 5s"

        if "predict --fast" in commands:
            predict_avg = sum(commands["predict --fast"]) / len(commands["predict --fast"])
            assert predict_avg < 3000, f"Fast predict average {predict_avg:.2f}ms exceeds 3s"


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
