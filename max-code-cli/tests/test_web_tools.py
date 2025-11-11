#!/usr/bin/env python3
"""
Testes para Web Search e Web Fetch Tools

Testing:
- WebSearchTool (search, cache, rate limit)
- WebFetchTool (fetch, HTML→MD, cache)
- Rate limiting
- Cache functionality
"""

import pytest
import time
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime

from core.tools.web_search_tool import WebSearchTool, RateLimiter, SearchCache
from core.tools.web_fetch_tool import WebFetchTool, FetchCache, FetchedContent


class TestRateLimiter:
    """Test rate limiting functionality"""

    def test_rate_limiter_allows_within_limit(self):
        """Test that calls within limit are allowed"""
        limiter = RateLimiter(max_calls=5, time_window=60)

        # First 5 calls should be allowed
        for _ in range(5):
            assert limiter.is_allowed() is True
            limiter.record_call()

        # 6th call should be blocked
        assert limiter.is_allowed() is False

    def test_rate_limiter_resets_after_window(self):
        """Test that rate limiter resets after time window"""
        limiter = RateLimiter(max_calls=2, time_window=1)  # 1 second window

        # Use up quota
        assert limiter.is_allowed() is True
        limiter.record_call()
        assert limiter.is_allowed() is True
        limiter.record_call()
        assert limiter.is_allowed() is False

        # Wait for window to pass
        time.sleep(1.1)

        # Should be allowed again
        assert limiter.is_allowed() is True

    def test_time_until_allowed(self):
        """Test time_until_allowed calculation"""
        limiter = RateLimiter(max_calls=1, time_window=60)

        limiter.record_call()
        wait_time = limiter.time_until_allowed()

        assert wait_time > 0
        assert wait_time <= 60


class TestSearchCache:
    """Test search cache functionality"""

    def test_cache_stores_and_retrieves(self):
        """Test basic cache store/retrieve"""
        cache = SearchCache(ttl_minutes=15)

        results = [{"title": "Test", "url": "https://test.com"}]
        cache.set("python", results)

        cached = cache.get("python")
        assert cached == results

    def test_cache_expires(self):
        """Test that cache expires after TTL"""
        cache = SearchCache(ttl_minutes=0)  # Instant expiration

        results = [{"title": "Test"}]
        cache.set("python", results)

        time.sleep(0.1)

        cached = cache.get("python")
        assert cached is None

    def test_cache_returns_none_for_missing_key(self):
        """Test cache miss returns None"""
        cache = SearchCache()

        cached = cache.get("nonexistent")
        assert cached is None

    def test_cache_clear(self):
        """Test cache clear"""
        cache = SearchCache()

        cache.set("key1", ["data1"])
        cache.set("key2", ["data2"])

        cache.clear()

        assert cache.get("key1") is None
        assert cache.get("key2") is None


class TestWebSearchTool:
    """Test WebSearchTool"""

    def test_web_search_tool_initialization(self):
        """Test tool initializes correctly"""
        tool = WebSearchTool(max_results=5)

        assert tool.max_results == 5
        assert isinstance(tool.rate_limiter, RateLimiter)
        assert isinstance(tool.cache, SearchCache)

    @patch('core.tools.web_search_tool.DDGS')
    def test_search_success(self, mock_ddgs):
        """Test successful search"""
        # Mock DuckDuckGo results
        mock_ddgs_instance = MagicMock()
        mock_ddgs_instance.text.return_value = [
            {
                'title': 'Python Tutorial',
                'href': 'https://python.org',
                'body': 'Learn Python'
            }
        ]
        mock_ddgs.return_value.__enter__.return_value = mock_ddgs_instance

        tool = WebSearchTool(max_results=10)
        result = tool.search("python tutorial")

        assert result.type == "success"
        assert "Python Tutorial" in result.content[0].text

    def test_search_uses_cache(self):
        """Test that search uses cache on repeated queries"""
        from dataclasses import dataclass

        @dataclass
        class MockResult:
            title: str
            url: str
            snippet: str
            source: str = "DuckDuckGo"

        tool = WebSearchTool()

        # Pre-populate cache with proper Result objects
        cached_results = [
            MockResult(title="Cached", url="https://cached.com", snippet="Cached result", source="DuckDuckGo")
        ]
        tool.cache.set("python", cached_results)

        result = tool.search("python")

        assert result.type == "success"
        assert "cached" in result.content[0].text.lower()

    def test_search_respects_rate_limit(self):
        """Test rate limiting is enforced"""
        tool = WebSearchTool()

        # Exhaust rate limit
        for _ in range(5):
            tool.rate_limiter.record_call()

        result = tool.search("test query")

        assert result.type == "error"
        assert "Rate limit" in result.content[0].text


class TestFetchCache:
    """Test FetchCache"""

    def test_fetch_cache_stores_and_retrieves(self):
        """Test cache stores and retrieves content"""
        cache = FetchCache(ttl_minutes=15)

        content = FetchedContent(
            url="https://test.com",
            title="Test",
            content="Test content",
            raw_html="<html></html>",
            fetch_time=datetime.now(),
            size_bytes=100
        )

        cache.set("https://test.com", content)
        cached = cache.get("https://test.com")

        assert cached is not None
        assert cached.title == "Test"
        assert cached.content == "Test content"


class TestWebFetchTool:
    """Test WebFetchTool"""

    def test_web_fetch_tool_initialization(self):
        """Test tool initializes correctly"""
        tool = WebFetchTool(timeout=10, max_size_mb=5)

        assert tool.timeout == 10
        assert tool.max_size_bytes == 5 * 1024 * 1024
        assert isinstance(tool.cache, FetchCache)

    def test_fetch_validates_empty_url(self):
        """Test fetch rejects empty URL"""
        tool = WebFetchTool()
        result = tool.fetch("")

        assert result.type == "error"
        assert "Empty URL" in result.content[0].text

    def test_fetch_validates_url_format(self):
        """Test fetch validates URL format"""
        tool = WebFetchTool()
        result = tool.fetch("not-a-valid-url")

        assert result.type == "error"
        assert "Invalid URL" in result.content[0].text

    def test_fetch_uses_cache(self):
        """Test fetch uses cache on repeated requests"""
        tool = WebFetchTool()

        # Pre-populate cache
        cached_content = FetchedContent(
            url="https://example.com",
            title="Example",
            content="# Example\n\nTest content",
            raw_html="<html></html>",
            fetch_time=datetime.now(),
            size_bytes=100
        )
        tool.cache.set("https://example.com", cached_content)

        result = tool.fetch("https://example.com")

        assert result.type == "success"
        assert "cached" in result.content[0].text.lower()
        assert "Example" in result.content[0].text

    @patch('core.tools.web_fetch_tool.requests.Session.get')
    def test_fetch_timeout_handling(self, mock_get):
        """Test fetch handles timeout"""
        import requests
        mock_get.side_effect = requests.exceptions.Timeout()

        tool = WebFetchTool()
        result = tool.fetch("https://slow-site.com")

        assert result.type == "error"
        assert "timeout" in result.content[0].text.lower()

    def test_clear_cache(self):
        """Test cache can be cleared"""
        tool = WebFetchTool()

        # Add to cache
        content = FetchedContent(
            url="https://test.com",
            title="Test",
            content="Content",
            raw_html="<html></html>",
            fetch_time=datetime.now(),
            size_bytes=100
        )
        tool.cache.set("https://test.com", content)

        # Clear
        result = tool.clear_cache()

        assert result.type == "success"
        assert tool.cache.get("https://test.com") is None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
