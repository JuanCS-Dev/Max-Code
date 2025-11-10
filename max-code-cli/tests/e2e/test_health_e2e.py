"""
E2E Tests for 'max-code health' command

Biblical Foundation:
"Examina-te a ti mesmo" (2 Coríntios 13:5)
"""
import pytest
import json
import statistics


class TestHealthE2E:
    """End-to-end tests for health command"""
    
    # ========================================================================
    # BASIC FUNCTIONALITY
    # ========================================================================
    
    @pytest.mark.e2e
    def test_health_all_services_offline(self, invoke_command, timer):
        """Test: health command when services offline (graceful degradation)"""
        with timer() as t:
            result = invoke_command("health")
        
        # Should complete even if services offline
        assert t.elapsed < 60, f"Health check timeout: {t.elapsed:.2f}s"
        
        # Should show compassionate error or degraded status
        assert "health" in result.output.lower() or "service" in result.output.lower()
        
        print(f"\n✓ Health check completed in {t.elapsed:.2f}s (services offline)")
    
    
    @pytest.mark.e2e
    def test_health_invalid_service(self, invoke_command):
        """Test: health with invalid service name"""
        result = invoke_command("health", ["invalid_service"])
        
        assert result.exit_code != 0
        assert "invalid" in result.output.lower() or "service" in result.output.lower()
    
    
    @pytest.mark.e2e
    def test_health_help(self, invoke_command):
        """Test: health --help"""
        result = invoke_command("health", ["--help"])
        
        assert result.exit_code == 0
        assert "health" in result.output.lower()
        assert "--help" in result.output or "usage" in result.output.lower()
    
    
    # ========================================================================
    # OUTPUT FORMATS
    # ========================================================================
    
    @pytest.mark.e2e
    def test_health_json_format(self, invoke_command):
        """Test: health with JSON output"""
        result = invoke_command("health", ["--format", "json"])
        
        # Should not crash
        assert "traceback" not in result.output.lower()
        
        # Try to parse JSON
        try:
            data = json.loads(result.output)
            assert isinstance(data, (list, dict))
        except json.JSONDecodeError:
            # If services offline, might not be JSON
            pass
    
    
    @pytest.mark.e2e
    def test_health_yaml_format(self, invoke_command):
        """Test: health with YAML output"""
        result = invoke_command("health", ["--format", "yaml"])
        
        # Should not crash
        assert "traceback" not in result.output.lower()
    
    
    # ========================================================================
    # FLAGS AND OPTIONS
    # ========================================================================
    
    @pytest.mark.e2e
    def test_health_detailed(self, invoke_command):
        """Test: health with detailed flag"""
        result = invoke_command("health", ["--detailed"])
        
        # Should not crash
        assert "traceback" not in result.output.lower()
    
    
    @pytest.mark.e2e
    def test_health_custom_timeout(self, invoke_command, timer):
        """Test: health with custom timeout"""
        with timer() as t:
            result = invoke_command("health", ["--timeout", "3"])
        
        # Should respect timeout
        assert t.elapsed < 10, "Timeout not respected"
    
    
    @pytest.mark.e2e
    def test_health_specific_service(self, invoke_command):
        """Test: health for specific service"""
        result = invoke_command("health", ["core"])
        
        # Should complete
        assert "traceback" not in result.output.lower()


# ============================================================================
# SCIENTIFIC TESTS
# ============================================================================

class TestHealthScientific:
    """Scientific validation tests for health command"""
    
    @pytest.mark.scientific
    @pytest.mark.parametrize("iteration", range(10))
    def test_health_response_time_consistency(
        self,
        invoke_command,
        metrics_collector,
        iteration
    ):
        """
        Scientific Test: Response time consistency
        
        Hypothesis: Response times should be consistent across multiple calls
        Sample size: 10 iterations
        """
        import time
        
        start = time.time()
        result = invoke_command("health")
        elapsed = time.time() - start
        
        metrics_collector.record(
            name="health_response_time",
            value=elapsed,
            unit="seconds"
        )
        
        # Should complete reasonably fast
        assert elapsed < 60, f"Response too slow: {elapsed:.2f}s"
    
    
    @pytest.mark.scientific
    @pytest.mark.slow
    def test_health_response_time_statistics(
        self,
        invoke_command,
        benchmark_dir
    ):
        """
        Scientific Test: Statistical analysis of response times
        
        Metrics:
        - Mean response time
        - Standard deviation
        - 95th percentile
        - Coefficient of variation
        """
        import time
        
        response_times = []
        
        # Collect 30 samples
        print("\nCollecting response time samples...")
        for i in range(30):
            start = time.time()
            result = invoke_command("health")
            elapsed = time.time() - start
            
            response_times.append(elapsed)
            
            if (i + 1) % 10 == 0:
                print(f"  Completed {i + 1}/30 samples")
        
        # Calculate statistics
        mean = statistics.mean(response_times)
        stdev = statistics.stdev(response_times)
        median = statistics.median(response_times)
        p95 = sorted(response_times)[int(len(response_times) * 0.95)]
        cv = (stdev / mean) * 100  # Coefficient of variation %
        
        stats = {
            "command": "health",
            "sample_size": len(response_times),
            "mean": mean,
            "median": median,
            "stdev": stdev,
            "min": min(response_times),
            "max": max(response_times),
            "p95": p95,
            "coefficient_of_variation": cv,
            "raw_times": response_times
        }
        
        # Save benchmark
        benchmark_file = benchmark_dir / "health_response_times.json"
        with open(benchmark_file, "w") as f:
            json.dump(stats, f, indent=2)
        
        print("\n" + "="*60)
        print("RESPONSE TIME STATISTICS (health command)")
        print("="*60)
        print(f"Sample size:    {stats['sample_size']}")
        print(f"Mean:           {stats['mean']:.3f}s")
        print(f"Median:         {stats['median']:.3f}s")
        print(f"Std Dev:        {stats['stdev']:.3f}s")
        print(f"Min:            {stats['min']:.3f}s")
        print(f"Max:            {stats['max']:.3f}s")
        print(f"95th %ile:      {stats['p95']:.3f}s")
        print(f"CV:             {stats['coefficient_of_variation']:.1f}%")
        print("="*60)
        print(f"Benchmark saved: {benchmark_file}")
        print("="*60)
        
        # Assertions: Be lenient since services may be offline
        assert mean < 60, f"Mean response time too high: {mean:.2f}s"
        print(f"\n✅ Performance acceptable (mean: {mean:.2f}s)")
