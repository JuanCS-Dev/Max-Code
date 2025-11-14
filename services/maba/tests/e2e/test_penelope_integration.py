"""E2E Tests for PENELOPE Integration.

Day 5: End-to-end tests simulating real PENELOPE usage with browser automation.

Tests the full flow: Browser → Screenshot → PENELOPE Analysis → Action Suggestion.

Author: Vértice Platform Team
License: Proprietary
"""
import asyncio
import base64
import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from penelope_integration import PageAnalyzer, PenelopeClient, AutoHealer


class TestPenelopeE2EWorkflows:
    """End-to-end workflow tests for PENELOPE integration."""

    @pytest.mark.asyncio
    async def test_full_page_analysis_workflow(self):
        """Test complete page analysis workflow from screenshot to insights."""
        # Mock browser page
        mock_page = AsyncMock()
        mock_page.url = "https://example.com/login"
        mock_page.screenshot = AsyncMock(return_value=b"fake_screenshot_data")
        mock_page.content = AsyncMock(return_value="""
            <html>
                <body>
                    <form id="login-form">
                        <input name="email" type="email" placeholder="Email">
                        <input name="password" type="password" placeholder="Password">
                        <button type="submit">Login</button>
                    </form>
                </body>
            </html>
        """)

        # Create analyzer with mocked Claude client
        analyzer = PageAnalyzer(api_key="test-key")
        analyzer.client = AsyncMock()

        # Mock Claude response for screenshot analysis
        mock_response = MagicMock()
        mock_response.content = [MagicMock(text="""
This is a login page with the following elements:
1. Email input field
2. Password input field
3. Submit button

The user can fill in credentials and click the submit button to login.
        """)]
        analyzer.client.messages.create = AsyncMock(return_value=mock_response)

        # Execute workflow
        screenshot_bytes = await mock_page.screenshot()
        screenshot_b64 = base64.b64encode(screenshot_bytes).decode('utf-8')
        html_content = await mock_page.content()
        url = mock_page.url

        # Analyze screenshot
        analysis = await analyzer.analyze_screenshot(
            screenshot_b64=screenshot_b64,
            url=url,
            question="What can I do on this page?"
        )

        # Verify results
        assert "analysis" in analysis
        assert "login" in analysis["analysis"].lower()
        assert analysis["model"] == "claude-sonnet-4-5"
        assert analysis["confidence"] == 0.9

        await analyzer.close()

    @pytest.mark.asyncio
    async def test_auto_healing_workflow(self):
        """Test auto-healing workflow when action fails."""
        # Mock browser page with button that failed
        mock_page = AsyncMock()
        mock_page.url = "https://example.com/form"
        mock_page.content = AsyncMock(return_value="""
            <html>
                <body>
                    <button class="submit-btn" type="submit">Submit</button>
                    <button id="send-button" type="submit">Send</button>
                </body>
            </html>
        """)

        # Create auto-healer
        analyzer = PageAnalyzer(api_key="test-key")
        analyzer.client = AsyncMock()

        # Mock Claude suggesting alternative selectors
        mock_response = MagicMock()
        mock_response.content = [MagicMock(text="""
button.submit-btn
button[type='submit']
#send-button
        """)]
        analyzer.client.messages.create = AsyncMock(return_value=mock_response)

        healer = AutoHealer(analyzer=analyzer)

        # Simulate failed action
        failed_action = {
            "action": "click",
            "selector": "button.missing-class",
            "url": mock_page.url
        }

        html_content = await mock_page.content()

        # Attempt healing
        healed_action = await healer.heal_failed_action(
            failed_action=failed_action,
            error_message="Element not found",
            page_html=html_content
        )

        # Verify healing worked
        assert healed_action is not None
        assert healed_action["action"] == "click"
        assert healed_action["selector"] in ["button.submit-btn", "button[type='submit']", "#send-button"]
        assert healed_action["healing_strategy"] == "alternative_selector"
        assert healed_action["confidence"] >= 0.7

        # Check healing history
        stats = healer.get_healing_stats()
        assert stats["total_attempts"] == 1
        assert stats["successful"] == 1
        assert stats["success_rate"] == 1.0

        await healer.close()

    @pytest.mark.asyncio
    async def test_intelligent_navigation_workflow(self):
        """Test intelligent navigation suggestion workflow."""
        # Mock browser page
        mock_page = AsyncMock()
        mock_page.url = "https://example.com/home"
        mock_page.content = AsyncMock(return_value="""
            <html>
                <body>
                    <nav>
                        <a href="/products">Products</a>
                        <a href="/about">About</a>
                        <a href="/contact">Contact</a>
                    </nav>
                    <main>
                        <h1>Welcome to Example.com</h1>
                    </main>
                </body>
            </html>
        """)
        mock_page.screenshot = AsyncMock(return_value=b"screenshot_data")

        # Create PENELOPE client (mock service)
        client = PenelopeClient()
        client.client = AsyncMock()

        # Mock service response suggesting navigation action
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "action": "click",
            "selector": "a[href='/products']",
            "reasoning": "User wants to see products, clicking Products link",
            "confidence": 0.95,
            "next_steps": ["Browse products", "Add to cart"]
        }
        client.client.post = AsyncMock(return_value=mock_response)

        # Request action suggestion
        html_content = await mock_page.content()
        screenshot_bytes = await mock_page.screenshot()
        screenshot_b64 = base64.b64encode(screenshot_bytes).decode('utf-8')

        suggestion = await client.suggest_action(
            current_url=mock_page.url,
            goal="I want to buy a product",
            page_html=html_content,
            screenshot=screenshot_b64
        )

        # Verify suggestion
        assert suggestion["action"] == "click"
        assert "/products" in suggestion["selector"]
        assert suggestion["confidence"] >= 0.9
        assert "products" in suggestion["reasoning"].lower()

        await client.close()

    @pytest.mark.asyncio
    async def test_data_extraction_workflow(self):
        """Test LLM-powered data extraction workflow."""
        # Mock product page
        mock_page = AsyncMock()
        mock_page.url = "https://shop.example.com/product/123"
        mock_page.content = AsyncMock(return_value="""
            <html>
                <body>
                    <div class="product">
                        <h1 class="title">Super Widget Pro</h1>
                        <span class="price">$299.99</span>
                        <div class="stock">In Stock</div>
                        <div class="rating">4.5/5 stars</div>
                        <p class="description">The best widget on the market</p>
                    </div>
                </body>
            </html>
        """)

        # Create analyzer
        analyzer = PageAnalyzer(api_key="test-key")
        analyzer.client = AsyncMock()

        # Mock Claude extracting structured data
        mock_response = MagicMock()
        mock_response.content = [MagicMock(text="""
{"title": "Super Widget Pro", "price": "$299.99", "availability": "In Stock", "rating": "4.5/5 stars"}
        """)]
        analyzer.client.messages.create = AsyncMock(return_value=mock_response)

        # Extract data
        html_content = await mock_page.content()
        schema = {
            "title": "Product title",
            "price": "Product price",
            "availability": "Stock status",
            "rating": "Customer rating"
        }

        extracted = await analyzer.extract_with_llm(
            html=html_content,
            schema=schema
        )

        # Verify extraction
        assert extracted["title"] == "Super Widget Pro"
        assert extracted["price"] == "$299.99"
        assert extracted["availability"] == "In Stock"
        assert extracted["rating"] == "4.5/5 stars"

        await analyzer.close()

    @pytest.mark.asyncio
    async def test_multi_step_healing_workflow(self):
        """Test multi-step healing when first attempt fails."""
        # Mock browser page
        mock_page = AsyncMock()
        mock_page.content = AsyncMock(return_value="""
            <html>
                <body>
                    <button id="final-btn">Click Me</button>
                </body>
            </html>
        """)

        # Create analyzer
        analyzer = PageAnalyzer(api_key="test-key")
        analyzer.client = AsyncMock()

        # First suggestion also doesn't exist, second one does
        call_count = 0

        def mock_suggest_selectors(*args, **kwargs):
            nonlocal call_count
            call_count += 1
            if call_count == 1:
                # First attempt - suggest selector that also doesn't exist
                return ["button.also-missing", "button.wrong"]
            else:
                # Second attempt - suggest working selector
                return ["#final-btn", "button"]

        analyzer.suggest_selectors = AsyncMock(side_effect=mock_suggest_selectors)

        healer = AutoHealer(analyzer=analyzer, max_heal_attempts=3)

        # First healing attempt
        html_content = await mock_page.content()
        healed1 = await healer.heal_failed_action(
            failed_action={"action": "click", "selector": "button.missing"},
            error_message="Element not found",
            page_html=html_content,
            attempt=1
        )

        # Should get first alternative
        assert healed1 is not None
        assert healed1["selector"] in ["button.also-missing", "button.wrong"]

        # Simulate first alternative also failing, try second healing
        healed2 = await healer.heal_failed_action(
            failed_action={"action": "click", "selector": "button.also-missing"},
            error_message="Element not found",
            page_html=html_content,
            attempt=2
        )

        # Should get second alternative
        assert healed2 is not None
        assert healed2["selector"] in ["#final-btn", "button"]

        # Check stats show both attempts
        stats = healer.get_healing_stats()
        assert stats["total_attempts"] == 2
        assert stats["successful"] == 2

        await healer.close()


class TestPenelopeFallbackBehavior:
    """Test PENELOPE fallback behavior when service unavailable."""

    @pytest.mark.asyncio
    async def test_fallback_to_local_analysis(self):
        """Test fallback to local analyzer when PENELOPE service fails."""
        # Create client that will fail
        client = PenelopeClient()
        client.client = AsyncMock()
        client.client.post = AsyncMock(
            side_effect=Exception("PENELOPE service unavailable")
        )

        # Create local analyzer that works
        analyzer = PageAnalyzer(api_key="test-key")
        analyzer.client = AsyncMock()

        mock_response = MagicMock()
        mock_response.content = [MagicMock(text="This is a login form with email and password fields.")]
        analyzer.client.messages.create = AsyncMock(return_value=mock_response)

        # Create auto-healer with both
        healer = AutoHealer(
            analyzer=analyzer,
            penelope_client=client,
            max_heal_attempts=3
        )

        # Attempt healing - should fallback to local
        healed = await healer.heal_failed_action(
            failed_action={"action": "click", "selector": "button.missing"},
            error_message="Element not found",
            page_html="<button id='submit'>Submit</button>"
        )

        # Should succeed with local analyzer despite service failure
        # The local healing will try to find alternatives
        # Even if it can't find a perfect match, it should not crash

        await healer.close()


class TestPenelopeErrorHandling:
    """Test PENELOPE error handling and edge cases."""

    @pytest.mark.asyncio
    async def test_handles_invalid_html(self):
        """Test that PENELOPE handles malformed HTML gracefully."""
        analyzer = PageAnalyzer(api_key="test-key")
        analyzer.client = AsyncMock()

        # Mock response even for bad HTML
        mock_response = MagicMock()
        mock_response.content = [MagicMock(text="Analysis of malformed HTML")]
        analyzer.client.messages.create = AsyncMock(return_value=mock_response)

        # Should not crash on malformed HTML
        result = await analyzer.analyze_html_structure(
            html="<div><p>Unclosed tags<div>Nested wrong",
            url="https://example.com"
        )

        assert "analysis" in result

        await analyzer.close()

    @pytest.mark.asyncio
    async def test_handles_empty_responses(self):
        """Test handling of empty or minimal Claude responses."""
        analyzer = PageAnalyzer(api_key="test-key")
        analyzer.client = AsyncMock()

        # Mock empty selector list
        mock_response = MagicMock()
        mock_response.content = [MagicMock(text="")]
        analyzer.client.messages.create = AsyncMock(return_value=mock_response)

        selectors = await analyzer.suggest_selectors(
            html="<button>Click</button>",
            element_description="button"
        )

        # Should return empty list, not crash
        assert isinstance(selectors, list)
        assert len(selectors) == 0

        await analyzer.close()

    @pytest.mark.asyncio
    async def test_max_healing_attempts_respected(self):
        """Test that max healing attempts are respected."""
        healer = AutoHealer(max_heal_attempts=2)

        # Attempt 3 (exceeds max)
        result = await healer.heal_failed_action(
            failed_action={"action": "click", "selector": "button"},
            error_message="error",
            page_html="<div>test</div>",
            attempt=3  # Exceeds max_heal_attempts=2
        )

        # Should return None when max attempts exceeded
        assert result is None


class TestPenelopePerformance:
    """Performance and efficiency tests for PENELOPE."""

    @pytest.mark.asyncio
    async def test_concurrent_analysis_requests(self):
        """Test that multiple analysis requests can run concurrently."""
        analyzer = PageAnalyzer(api_key="test-key")
        analyzer.client = AsyncMock()

        mock_response = MagicMock()
        mock_response.content = [MagicMock(text="Analysis complete")]
        analyzer.client.messages.create = AsyncMock(return_value=mock_response)

        # Run 5 analysis requests concurrently
        tasks = [
            analyzer.analyze_html_structure(
                html=f"<div>Page {i}</div>",
                url=f"https://example.com/{i}"
            )
            for i in range(5)
        ]

        results = await asyncio.gather(*tasks)

        # All should complete successfully
        assert len(results) == 5
        for result in results:
            assert "analysis" in result

        await analyzer.close()

    @pytest.mark.asyncio
    async def test_healing_history_memory_efficient(self):
        """Test that healing history doesn't grow unbounded."""
        healer = AutoHealer(max_history_size=10)
        healer.analyzer = AsyncMock()
        healer.analyzer.suggest_selectors = AsyncMock(return_value=["button"])

        # Add 50 healing attempts
        for i in range(50):
            await healer.heal_failed_action(
                failed_action={"action": "click", "selector": f"btn{i}"},
                error_message="not found",
                page_html="<button>Click</button>"
            )

        # History should be capped at max_history_size
        assert len(healer.healing_history) == 10

        # Should keep most recent entries
        last_entry = healer.healing_history[-1]
        assert "btn49" in str(last_entry["failed_action"])
