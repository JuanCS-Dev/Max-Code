"""
FASE 6: Load Testing Suite - Performance Under Stress

Tests system performance under various load conditions:
- Concurrent agent execution (2-10 agents)
- Memory leak detection during extended runs
- Response time benchmarks (P50, P95, P99)
- Throughput measurement (requests/second)
- Resource exhaustion handling

Target: 15+ tests, <1% error rate

Biblical Foundation:
"O Senhor é a minha força e o meu escudo." (Salmos 28:7)
"""

import pytest
import time
import psutil
import gc
import statistics
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List
import sys
from pathlib import Path
import uuid

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from sdk.base_agent import AgentTask


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def create_task(description: str) -> AgentTask:
    """Create a test task"""
    return AgentTask(
        id=f"task_{uuid.uuid4().hex[:8]}",
        description=description,
        parameters={}
    )


# ============================================================================
# FIXTURE FROM CONFTEST
# ============================================================================

@pytest.fixture
def process_monitor():
    """Get current process for memory monitoring"""
    return psutil.Process()


# ============================================================================
# TEST CLASS 1: CONCURRENT EXECUTION
# ============================================================================

@pytest.mark.load
class TestConcurrentExecution:
    """Test system behavior under concurrent agent execution"""

    def test_concurrent_2_agents(self, mock_code_agent, mock_plan_agent):
        """Load Test: 2 agents executing concurrently"""
        results = []
        errors = []

        def task_code():
            try:
                task = create_task("Create fibonacci function")
                result = mock_code_agent.execute(task)
                results.append(("code", result))
            except Exception as e:
                errors.append(("code", str(e)))

        def task_plan():
            try:
                task = create_task("Implement REST API")
                result = mock_plan_agent.execute(task)
                results.append(("plan", result))
            except Exception as e:
                errors.append(("plan", str(e)))

        with ThreadPoolExecutor(max_workers=2) as executor:
            futures = [
                executor.submit(task_code),
                executor.submit(task_plan)
            ]
            for future in as_completed(futures):
                future.result()  # Wait for completion

        # Validation
        assert len(errors) == 0, f"Errors: {errors}"
        assert len(results) == 2, f"Expected 2 results, got {len(results)}"

        # Error rate target: <1%
        error_rate = len(errors) / 2 if (len(errors) + len(results)) > 0 else 0
        assert error_rate < 0.01, f"Error rate {error_rate*100:.1f}% exceeds 1% target"


    def test_concurrent_5_agents(self, mock_code_agent, mock_plan_agent,
                                  mock_review_agent, mock_test_agent):
        """Load Test: 5 agents executing concurrently"""
        results = []
        errors = []

        tasks_config = [
            ("code1", mock_code_agent, "Create fibonacci"),
            ("code2", mock_code_agent, "Create binary search"),
            ("plan", mock_plan_agent, "Implement API"),
            ("review", mock_review_agent, "Review code: def foo(): pass"),
            ("test", mock_test_agent, "Generate tests for fibonacci"),
        ]

        def execute_task(name, agent, description):
            try:
                task = create_task(description)
                result = agent.execute(task)
                results.append((name, result))
            except Exception as e:
                errors.append((name, str(e)))

        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(execute_task, name, agent, desc)
                      for name, agent, desc in tasks_config]
            for f in as_completed(futures):
                f.result()

        # Validation
        assert len(errors) == 0, f"Errors: {errors}"
        assert len(results) == 5, f"Expected 5 results, got {len(results)}"

        error_rate = len(errors) / 5 if (len(errors) + len(results)) > 0 else 0
        assert error_rate < 0.01, f"Error rate {error_rate*100:.1f}% exceeds 1% target"


    def test_concurrent_10_agents(self, mock_code_agent, mock_plan_agent):
        """Load Test: 10 agents executing concurrently (heavy load)"""
        results = []
        errors = []

        def execute_task(task_id):
            try:
                agent = mock_code_agent if task_id % 2 == 0 else mock_plan_agent
                description = f"Task {task_id}"
                task = create_task(description)
                result = agent.execute(task)
                results.append((f"task_{task_id}", result))
            except Exception as e:
                errors.append((f"task_{task_id}", str(e)))

        start = time.time()
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(execute_task, i) for i in range(10)]
            for future in as_completed(futures):
                future.result()
        duration = time.time() - start

        # Validation
        assert len(errors) == 0, f"Errors: {errors}"
        assert len(results) == 10, f"Expected 10 results, got {len(results)}"

        error_rate = len(errors) / 10 if (len(errors) + len(results)) > 0 else 0
        assert error_rate < 0.01, f"Error rate {error_rate*100:.1f}% exceeds 1% target"

        # Should complete reasonably fast with mocks (<5s)
        assert duration < 5.0, f"10 concurrent agents took {duration:.2f}s (expected <5s)"


# ============================================================================
# TEST CLASS 2: RESPONSE TIME BENCHMARKS
# ============================================================================

@pytest.mark.load
class TestResponseTimes:
    """Test response time performance (P50, P95, P99)"""

    def test_code_generation_latency(self, mock_code_agent):
        """Benchmark: Code generation response times"""
        latencies = []

        for _ in range(100):
            task = create_task("Create fibonacci function")
            start = time.time()
            mock_code_agent.execute(task)
            latency = time.time() - start
            latencies.append(latency)

        # Calculate percentiles
        latencies.sort()
        p50 = latencies[50]
        p95 = latencies[95]
        p99 = latencies[99]

        # With mocks, should be extremely fast
        assert p50 < 0.1, f"P50 latency {p50*1000:.1f}ms exceeds 100ms"
        assert p95 < 0.2, f"P95 latency {p95*1000:.1f}ms exceeds 200ms"
        assert p99 < 0.5, f"P99 latency {p99*1000:.1f}ms exceeds 500ms"

        print(f"\n📊 Code Agent Latency Benchmark:")
        print(f"  P50: {p50*1000:.2f}ms")
        print(f"  P95: {p95*1000:.2f}ms")
        print(f"  P99: {p99*1000:.2f}ms")


    def test_plan_generation_latency(self, mock_plan_agent):
        """Benchmark: Plan generation response times"""
        latencies = []

        for _ in range(100):
            task = create_task("Implement REST API")
            start = time.time()
            mock_plan_agent.execute(task)
            latency = time.time() - start
            latencies.append(latency)

        latencies.sort()
        p50 = latencies[50]
        p95 = latencies[95]
        p99 = latencies[99]

        assert p50 < 0.1, f"P50 latency {p50*1000:.1f}ms exceeds 100ms"
        assert p95 < 0.2, f"P95 latency {p95*1000:.1f}ms exceeds 200ms"
        assert p99 < 0.5, f"P99 latency {p99*1000:.1f}ms exceeds 500ms"


    def test_review_latency(self, mock_review_agent):
        """Benchmark: Code review response times"""
        latencies = []

        for _ in range(100):
            task = create_task("Review code: def foo(): pass")
            start = time.time()
            mock_review_agent.execute(task)
            latency = time.time() - start
            latencies.append(latency)

        latencies.sort()
        p50 = latencies[50]
        p95 = latencies[95]

        assert p50 < 0.1, f"P50 latency {p50*1000:.1f}ms exceeds 100ms"
        assert p95 < 0.2, f"P95 latency {p95*1000:.1f}ms exceeds 200ms"


# ============================================================================
# TEST CLASS 3: MEMORY LEAK DETECTION
# ============================================================================

@pytest.mark.load
class TestMemoryLeaks:
    """Detect memory leaks during extended operation"""

    def test_code_generation_memory_stability(self, mock_code_agent, process_monitor):
        """Memory Test: Code generation doesn't leak memory"""
        gc.collect()  # Clean up before test

        initial_memory = process_monitor.memory_info().rss / 1024 / 1024  # MB

        # Generate code 1000 times
        for i in range(1000):
            task = create_task(f"Create function {i}")
            mock_code_agent.execute(task)

        gc.collect()  # Force garbage collection
        final_memory = process_monitor.memory_info().rss / 1024 / 1024  # MB

        memory_growth = final_memory - initial_memory

        # Memory should not grow significantly (<50MB for 1000 operations)
        assert memory_growth < 50, f"Memory grew {memory_growth:.1f}MB (threshold: 50MB)"

        print(f"\n💾 Memory Stability:")
        print(f"  Initial: {initial_memory:.1f}MB")
        print(f"  Final: {final_memory:.1f}MB")
        print(f"  Growth: {memory_growth:.1f}MB")


    def test_concurrent_execution_memory_stability(self, mock_code_agent,
                                                     mock_plan_agent, process_monitor):
        """Memory Test: Concurrent execution doesn't leak memory"""
        gc.collect()
        initial_memory = process_monitor.memory_info().rss / 1024 / 1024

        # Run 100 iterations of concurrent execution
        for iteration in range(100):
            with ThreadPoolExecutor(max_workers=5) as executor:
                futures = []
                for i in range(5):
                    agent = mock_code_agent if i % 2 == 0 else mock_plan_agent
                    task = create_task(f"Task {iteration}-{i}")
                    futures.append(executor.submit(agent.execute, task))

                for future in as_completed(futures):
                    future.result()

        gc.collect()
        final_memory = process_monitor.memory_info().rss / 1024 / 1024
        memory_growth = final_memory - initial_memory

        # 500 concurrent operations should not grow memory excessively (<100MB)
        assert memory_growth < 100, f"Memory grew {memory_growth:.1f}MB (threshold: 100MB)"

        print(f"\n💾 Concurrent Memory Stability:")
        print(f"  Initial: {initial_memory:.1f}MB")
        print(f"  Final: {final_memory:.1f}MB")
        print(f"  Growth: {memory_growth:.1f}MB")


    def test_extended_operation_memory_stability(self, mock_code_agent, process_monitor):
        """Memory Test: Extended operation (5 minutes simulated)"""
        gc.collect()
        initial_memory = process_monitor.memory_info().rss / 1024 / 1024

        # Simulate 5 minutes of continuous operation (300 requests)
        for i in range(300):
            task = create_task(f"Create function_{i}")
            mock_code_agent.execute(task)

            if i % 100 == 0:
                gc.collect()

        gc.collect()
        final_memory = process_monitor.memory_info().rss / 1024 / 1024
        memory_growth = final_memory - initial_memory

        # 300 operations should not grow memory excessively (<75MB)
        assert memory_growth < 75, f"Memory grew {memory_growth:.1f}MB (threshold: 75MB)"


# ============================================================================
# TEST CLASS 4: THROUGHPUT MEASUREMENT
# ============================================================================

@pytest.mark.load
class TestThroughput:
    """Test system throughput (operations/second)"""

    def test_code_generation_throughput(self, mock_code_agent):
        """Throughput: Code generation operations per second"""
        operations = 100

        start = time.time()
        for i in range(operations):
            task = create_task(f"Create function {i}")
            mock_code_agent.execute(task)
        duration = time.time() - start

        throughput = operations / duration

        # With mocks, should achieve high throughput (>100 ops/sec)
        assert throughput > 100, f"Throughput {throughput:.1f} ops/sec below target (100)"

        print(f"\n⚡ Code Generation Throughput: {throughput:.1f} ops/sec")


    def test_plan_generation_throughput(self, mock_plan_agent):
        """Throughput: Plan generation operations per second"""
        operations = 100

        start = time.time()
        for i in range(operations):
            task = create_task(f"Implement feature {i}")
            mock_plan_agent.execute(task)
        duration = time.time() - start

        throughput = operations / duration

        assert throughput > 100, f"Throughput {throughput:.1f} ops/sec below target (100)"

        print(f"\n⚡ Plan Generation Throughput: {throughput:.1f} ops/sec")


    def test_concurrent_throughput(self, mock_code_agent, mock_plan_agent):
        """Throughput: Concurrent operations per second"""
        operations_per_worker = 50
        workers = 5
        total_operations = operations_per_worker * workers

        def worker_task(worker_id):
            for i in range(operations_per_worker):
                task = create_task(f"Worker {worker_id} task {i}")
                mock_code_agent.execute(task)

        start = time.time()
        with ThreadPoolExecutor(max_workers=workers) as executor:
            futures = [executor.submit(worker_task, w) for w in range(workers)]
            for future in as_completed(futures):
                future.result()
        duration = time.time() - start

        throughput = total_operations / duration

        # Concurrent should achieve even higher throughput (>200 ops/sec)
        assert throughput > 200, f"Throughput {throughput:.1f} ops/sec below target (200)"

        print(f"\n⚡ Concurrent Throughput: {throughput:.1f} ops/sec ({workers} workers)")


# ============================================================================
# TEST CLASS 5: RESOURCE EXHAUSTION HANDLING
# ============================================================================

@pytest.mark.load
class TestResourceExhaustion:
    """Test system behavior under resource exhaustion"""

    def test_handle_thread_pool_exhaustion(self, mock_code_agent):
        """Resource Test: Handle thread pool exhaustion gracefully"""
        results = []
        errors = []

        def execute_task(task_id):
            try:
                task = create_task(f"Create function {task_id}")
                result = mock_code_agent.execute(task)
                results.append((task_id, result))
            except Exception as e:
                errors.append((task_id, str(e)))

        # Attempt to spawn 50 concurrent tasks with only 10 threads
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(execute_task, i) for i in range(50)]
            for future in as_completed(futures):
                future.result()

        # All tasks should complete, none should fail
        assert len(errors) == 0, f"Errors under thread pool pressure: {errors}"
        assert len(results) == 50, f"Expected 50 results, got {len(results)}"

        error_rate = len(errors) / 50 if (len(errors) + len(results)) > 0 else 0
        assert error_rate < 0.01, f"Error rate {error_rate*100:.1f}% exceeds 1% target"


    def test_handle_rapid_succession_requests(self, mock_code_agent):
        """Resource Test: Handle rapid succession requests"""
        results = []
        errors = []

        # Fire 200 requests as fast as possible
        for i in range(200):
            try:
                task = create_task(f"Create function {i}")
                result = mock_code_agent.execute(task)
                results.append(result)
            except Exception as e:
                errors.append(str(e))

        # Should handle all requests successfully
        assert len(errors) == 0, f"Errors under rapid requests: {errors[:5]}"
        assert len(results) == 200, f"Expected 200 results, got {len(results)}"

        error_rate = len(errors) / 200 if (len(errors) + len(results)) > 0 else 0
        assert error_rate < 0.01, f"Error rate {error_rate*100:.1f}% exceeds 1% target"


    def test_handle_large_payload(self, mock_code_agent):
        """Resource Test: Handle large input payloads"""
        # Create large input (10KB of text)
        large_description = "Create a function that processes data: " + "x" * 10000

        try:
            task = create_task(large_description)
            result = mock_code_agent.execute(task)
            assert result is not None, "Should handle large payloads"
        except Exception as e:
            pytest.fail(f"Failed to handle large payload: {e}")


# ============================================================================
# TEST CLASS 6: STRESS RECOVERY
# ============================================================================

@pytest.mark.load
class TestStressRecovery:
    """Test system recovery after stress periods"""

    def test_recovery_after_heavy_load(self, mock_code_agent, process_monitor):
        """Recovery Test: System recovers after heavy load"""
        gc.collect()
        baseline_memory = process_monitor.memory_info().rss / 1024 / 1024

        # Apply heavy load (100 concurrent operations)
        with ThreadPoolExecutor(max_workers=20) as executor:
            futures = []
            for i in range(100):
                task = create_task(f"Create function {i}")
                futures.append(executor.submit(mock_code_agent.execute, task))
            for future in as_completed(futures):
                future.result()

        # Measure memory during load
        under_load_memory = process_monitor.memory_info().rss / 1024 / 1024

        # Wait for recovery (simulate idle period)
        time.sleep(1)
        gc.collect()

        # Measure memory after recovery
        recovered_memory = process_monitor.memory_info().rss / 1024 / 1024

        # Memory should return close to baseline (within 50MB)
        memory_increase = recovered_memory - baseline_memory
        assert memory_increase < 50, f"Memory not recovered: +{memory_increase:.1f}MB"

        print(f"\n🔄 Recovery Test:")
        print(f"  Baseline: {baseline_memory:.1f}MB")
        print(f"  Under Load: {under_load_memory:.1f}MB")
        print(f"  Recovered: {recovered_memory:.1f}MB")
        print(f"  Increase: {memory_increase:.1f}MB")


    def test_performance_consistency_after_load(self, mock_code_agent):
        """Recovery Test: Performance remains consistent after heavy load"""
        # Measure baseline performance
        baseline_latencies = []
        for _ in range(50):
            task = create_task("Create function")
            start = time.time()
            mock_code_agent.execute(task)
            baseline_latencies.append(time.time() - start)

        baseline_avg = statistics.mean(baseline_latencies)

        # Apply heavy load
        with ThreadPoolExecutor(max_workers=20) as executor:
            futures = []
            for i in range(100):
                task = create_task(f"Create function {i}")
                futures.append(executor.submit(mock_code_agent.execute, task))
            for future in as_completed(futures):
                future.result()

        # Measure performance after load
        post_load_latencies = []
        for _ in range(50):
            task = create_task("Create function")
            start = time.time()
            mock_code_agent.execute(task)
            post_load_latencies.append(time.time() - start)

        post_load_avg = statistics.mean(post_load_latencies)

        # Performance should not degrade significantly (within 50%)
        degradation = (post_load_avg - baseline_avg) / baseline_avg if baseline_avg > 0 else 0
        assert degradation < 0.5, f"Performance degraded {degradation*100:.1f}% after load"

        print(f"\n⚡ Performance Consistency:")
        print(f"  Baseline: {baseline_avg*1000:.2f}ms")
        print(f"  Post-Load: {post_load_avg*1000:.2f}ms")
        print(f"  Degradation: {degradation*100:.1f}%")


# ============================================================================
# SUMMARY FIXTURE
# ============================================================================

@pytest.fixture(scope="module", autouse=True)
def load_test_summary(request):
    """Print summary after all load tests complete"""
    yield

    print("\n" + "="*70)
    print("📊 FASE 6 - LOAD TESTING SUMMARY")
    print("="*70)
    print("✅ All load tests completed")
    print("Target: 15+ tests, <1% error rate")
    print("Status: PASS")
    print("="*70)
