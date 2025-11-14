"""Performance Benchmarks for PENELOPE Integration.

Day 5: Benchmark tests for PENELOPE performance characteristics.

Measures response times, throughput, and resource usage.

Author: Vértice Platform Team
License: Proprietary
"""
import asyncio
import time
from unittest.mock import AsyncMock, MagicMock

import pytest

from penelope_integration import PageAnalyzer, PenelopeClient, AutoHealer


class TestPageAnalyzerPerformance:
    """Performance benchmarks for PageAnalyzer."""

    @pytest.mark.benchmark
    @pytest.mark.asyncio
    async def test_screenshot_analysis_performance(self, benchmark):
        """Benchmark screenshot analysis performance."""
        analyzer = PageAnalyzer(api_key="test-key")
        analyzer.client = AsyncMock()

        # Mock fast Claude response
        mock_response = MagicMock()
        mock_response.content = [MagicMock(text="Login page with email and password fields")]

        async def fast_create(*args, **kwargs):
            await asyncio.sleep(0.01)  # Simulate 10ms API call
            return mock_response

        analyzer.client.messages.create = fast_create

        screenshot_b64 = "base64_encoded_image_data" * 100  # Realistic size

        # Benchmark the analysis
        async def run_analysis():
            return await analyzer.analyze_screenshot(
                screenshot_b64=screenshot_b64,
                url="https://example.com/login"
            )

        # Run benchmark
        result = benchmark.pedantic(
            lambda: asyncio.run(run_analysis()),
            rounds=10,
            iterations=1
        )

        assert "analysis" in result

        await analyzer.close()

    @pytest.mark.benchmark
    @pytest.mark.asyncio
    async def test_html_truncation_performance(self, benchmark):
        """Benchmark HTML truncation performance with large documents."""
        from penelope_integration.analyzer import _safe_truncate_html

        # Create large HTML document (1MB)
        large_html = "<div>" + ("x" * 1000 + "</div><div>") * 1000 + "</div>"

        # Benchmark truncation
        result = benchmark(_safe_truncate_html, large_html, 50000)

        assert len(result) <= 50000

    @pytest.mark.benchmark
    @pytest.mark.asyncio
    async def test_selector_suggestion_performance(self, benchmark):
        """Benchmark CSS selector suggestion performance."""
        analyzer = PageAnalyzer(api_key="test-key")
        analyzer.client = AsyncMock()

        mock_response = MagicMock()
        mock_response.content = [MagicMock(text="button.submit\nbutton[type='submit']\n#submit-btn")]

        async def fast_create(*args, **kwargs):
            await asyncio.sleep(0.015)  # Simulate 15ms API call
            return mock_response

        analyzer.client.messages.create = fast_create

        html = "<button class='submit' type='submit' id='submit-btn'>Submit</button>" * 100

        async def run_suggestion():
            return await analyzer.suggest_selectors(
                html=html,
                element_description="submit button"
            )

        result = benchmark.pedantic(
            lambda: asyncio.run(run_suggestion()),
            rounds=10,
            iterations=1
        )

        assert len(result) == 3

        await analyzer.close()

    @pytest.mark.benchmark
    @pytest.mark.asyncio
    async def test_json_extraction_performance(self, benchmark):
        """Benchmark LLM data extraction performance."""
        analyzer = PageAnalyzer(api_key="test-key")
        analyzer.client = AsyncMock()

        mock_response = MagicMock()
        mock_response.content = [MagicMock(text='{"title": "Product", "price": "$99", "stock": "Available"}')]

        async def fast_create(*args, **kwargs):
            await asyncio.sleep(0.02)  # Simulate 20ms API call
            return mock_response

        analyzer.client.messages.create = fast_create

        html = """
        <div class="product">
            <h1>Product</h1>
            <span class="price">$99</span>
            <div class="stock">Available</div>
        </div>
        """ * 50

        schema = {"title": "Title", "price": "Price", "stock": "Stock"}

        async def run_extraction():
            return await analyzer.extract_with_llm(html=html, schema=schema)

        result = benchmark.pedantic(
            lambda: asyncio.run(run_extraction()),
            rounds=10,
            iterations=1
        )

        assert result["title"] == "Product"

        await analyzer.close()


class TestAutoHealerPerformance:
    """Performance benchmarks for AutoHealer."""

    @pytest.mark.benchmark
    @pytest.mark.asyncio
    async def test_healing_performance(self, benchmark):
        """Benchmark auto-healing performance."""
        analyzer = AsyncMock()
        mock_response = MagicMock()
        mock_response.content = [MagicMock(text="button.alt\nbutton[type='submit']")]

        async def fast_suggest(*args, **kwargs):
            await asyncio.sleep(0.01)
            return ["button.alt", "button[type='submit']"]

        analyzer.suggest_selectors = fast_suggest
        analyzer.close = AsyncMock()

        healer = AutoHealer(analyzer=analyzer)

        failed_action = {"action": "click", "selector": "button.missing"}
        html = "<button class='alt' type='submit'>Submit</button>"

        async def run_healing():
            return await healer.heal_failed_action(
                failed_action=failed_action,
                error_message="Element not found",
                page_html=html
            )

        result = benchmark.pedantic(
            lambda: asyncio.run(run_healing()),
            rounds=10,
            iterations=1
        )

        assert result is not None

    @pytest.mark.benchmark
    def test_healing_history_performance(self, benchmark):
        """Benchmark healing history management performance."""
        healer = AutoHealer(max_history_size=100)

        # Benchmark adding entries to history
        def add_history_entry():
            healer.healing_history.append({
                "failed_action": {"action": "click", "selector": "button"},
                "error": "not found",
                "healed_action": {"action": "click", "selector": "button.alt"},
                "attempt": 1,
                "success": True
            })

            # Trigger trimming if needed
            if len(healer.healing_history) > healer.max_history_size:
                healer.healing_history = healer.healing_history[-healer.max_history_size:]

        benchmark(add_history_entry)

    @pytest.mark.benchmark
    def test_healing_stats_calculation(self, benchmark):
        """Benchmark healing statistics calculation."""
        healer = AutoHealer()

        # Add 100 history entries
        for i in range(100):
            healer.healing_history.append({
                "failed_action": {"action": "click", "selector": f"button{i}"},
                "error": "not found",
                "healed_action": {"selector": f"button{i}_healed"} if i % 2 == 0 else None,
                "attempt": 1,
                "success": i % 2 == 0
            })

        # Benchmark stats calculation
        result = benchmark(healer.get_healing_stats)

        assert result["total_attempts"] == 100
        assert result["successful"] == 50
        assert result["success_rate"] == 0.5


class TestPenelopeClientPerformance:
    """Performance benchmarks for PenelopeClient."""

    @pytest.mark.benchmark
    @pytest.mark.asyncio
    async def test_suggest_action_performance(self, benchmark):
        """Benchmark action suggestion performance."""
        client = PenelopeClient()
        client.client = AsyncMock()

        mock_response = MagicMock()
        mock_response.json.return_value = {
            "action": "click",
            "selector": "button.login",
            "reasoning": "Click login button",
            "confidence": 0.95
        }

        async def fast_post(*args, **kwargs):
            await asyncio.sleep(0.025)  # Simulate 25ms network call
            return mock_response

        client.client.post = fast_post

        async def run_suggestion():
            return await client.suggest_action(
                current_url="https://example.com",
                goal="login to account",
                page_html="<button class='login'>Login</button>" * 50
            )

        result = benchmark.pedantic(
            lambda: asyncio.run(run_suggestion()),
            rounds=10,
            iterations=1
        )

        assert result["action"] == "click"

        await client.close()

    @pytest.mark.benchmark
    @pytest.mark.asyncio
    async def test_auto_heal_performance(self, benchmark):
        """Benchmark auto-heal endpoint performance."""
        client = PenelopeClient()
        client.client = AsyncMock()

        mock_response = MagicMock()
        mock_response.json.return_value = {
            "healed": True,
            "alternative_action": {
                "action": "click",
                "selector": "button[type='submit']"
            }
        }

        async def fast_post(*args, **kwargs):
            await asyncio.sleep(0.02)  # Simulate 20ms network call
            return mock_response

        client.client.post = fast_post

        async def run_heal():
            return await client.auto_heal(
                failed_action={"action": "click", "selector": "button.missing"},
                error_message="Element not found",
                page_html="<button type='submit'>Submit</button>"
            )

        result = benchmark.pedantic(
            lambda: asyncio.run(run_heal()),
            rounds=10,
            iterations=1
        )

        assert result["healed"] is True

        await client.close()


class TestConcurrentOperations:
    """Benchmark concurrent PENELOPE operations."""

    @pytest.mark.benchmark
    @pytest.mark.asyncio
    async def test_concurrent_healing_operations(self, benchmark):
        """Benchmark multiple concurrent healing operations."""
        analyzer = AsyncMock()
        analyzer.suggest_selectors = AsyncMock(return_value=["button.alt"])

        healer = AutoHealer(analyzer=analyzer)

        async def run_concurrent_healing():
            # Simulate 10 concurrent healing attempts
            tasks = [
                healer.heal_failed_action(
                    failed_action={"action": "click", "selector": f"button{i}"},
                    error_message="Element not found",
                    page_html="<button class='alt'>Click</button>"
                )
                for i in range(10)
            ]

            results = await asyncio.gather(*tasks)
            return results

        results = benchmark.pedantic(
            lambda: asyncio.run(run_concurrent_healing()),
            rounds=5,
            iterations=1
        )

        assert len(results) == 10

    @pytest.mark.benchmark
    @pytest.mark.asyncio
    async def test_concurrent_analysis_throughput(self, benchmark):
        """Benchmark analysis throughput with concurrent requests."""
        analyzer = PageAnalyzer(api_key="test-key")
        analyzer.client = AsyncMock()

        mock_response = MagicMock()
        mock_response.content = [MagicMock(text="Analysis result")]

        async def fast_create(*args, **kwargs):
            await asyncio.sleep(0.01)
            return mock_response

        analyzer.client.messages.create = fast_create

        async def run_concurrent_analysis():
            # Simulate 20 concurrent analysis requests
            tasks = [
                analyzer.analyze_html_structure(
                    html=f"<div>Page {i}</div>",
                    url=f"https://example.com/{i}"
                )
                for i in range(20)
            ]

            results = await asyncio.gather(*tasks)
            return results

        results = benchmark.pedantic(
            lambda: asyncio.run(run_concurrent_analysis()),
            rounds=5,
            iterations=1
        )

        assert len(results) == 20

        await analyzer.close()


class TestResourceUsage:
    """Test resource usage and efficiency."""

    @pytest.mark.asyncio
    async def test_memory_usage_with_large_history(self):
        """Test memory usage with large healing history."""
        import sys

        healer = AutoHealer(max_history_size=1000)
        healer.analyzer = AsyncMock()
        healer.analyzer.suggest_selectors = AsyncMock(return_value=["button"])

        # Measure initial size
        initial_size = sys.getsizeof(healer.healing_history)

        # Add 2000 entries (should trim to 1000)
        for i in range(2000):
            await healer.heal_failed_action(
                failed_action={"action": "click", "selector": f"button{i}"},
                error_message="not found",
                page_html="<button>Click</button>"
            )

        # Measure final size
        final_size = sys.getsizeof(healer.healing_history)

        # History should be trimmed, not grow unbounded
        assert len(healer.healing_history) == 1000

        # Size should be reasonable (not gigabytes)
        assert final_size < 1024 * 1024  # Less than 1MB

    @pytest.mark.asyncio
    async def test_client_connection_pooling(self):
        """Test that client properly reuses connections."""
        client = PenelopeClient()

        # Client should have a single HTTP client instance
        assert client.client is not None

        # Multiple requests should reuse same client
        client_id = id(client.client)

        # Simulate multiple operations (with mocked responses)
        client.client = AsyncMock()
        mock_response = MagicMock()
        mock_response.json.return_value = {"status": "ok"}
        client.client.get = AsyncMock(return_value=mock_response)

        for _ in range(10):
            await client.health_check()

        # Client instance should remain the same
        assert id(client.client) == client_id

        await client.close()


# Performance targets for documentation
PERFORMANCE_TARGETS = {
    "screenshot_analysis_ms": 50,  # Target: < 50ms (excluding Claude API time)
    "html_truncation_ms": 10,  # Target: < 10ms for 1MB HTML
    "selector_suggestion_ms": 50,  # Target: < 50ms (excluding Claude API time)
    "healing_operation_ms": 100,  # Target: < 100ms total
    "concurrent_throughput": 20,  # Target: 20 concurrent operations
    "max_history_memory_mb": 1,  # Target: < 1MB for 1000 entries
}


def test_performance_targets_documented():
    """Test that performance targets are documented."""
    assert "screenshot_analysis_ms" in PERFORMANCE_TARGETS
    assert "html_truncation_ms" in PERFORMANCE_TARGETS
    assert "selector_suggestion_ms" in PERFORMANCE_TARGETS
    assert "healing_operation_ms" in PERFORMANCE_TARGETS
    assert "concurrent_throughput" in PERFORMANCE_TARGETS
    assert "max_history_memory_mb" in PERFORMANCE_TARGETS
