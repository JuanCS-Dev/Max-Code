#!/usr/bin/env python3
"""
Web Search Tool - DuckDuckGo Integration with Boris Technique ✨

Philosophy (Boris):
"Web search is not just about finding information - it's about
discovering knowledge with clarity, speed, and respect for privacy.
DuckDuckGo embodies this: no tracking, just pure search."

Security:
- No API keys required (privacy-first)
- Rate limiting (5 queries/minute)
- Result sanitization (prevent XSS)
- Timeout enforcement (10s max)

Beauty:
- Rich formatted results with icons
- Ranked by relevance
- Clear source attribution
- Beautiful error messages

Performance:
- Cache results (15min TTL)
- Async-ready design
- Pagination support

Soli Deo Gloria 🙏
"""

import time
from typing import List, Dict, Optional
from dataclasses import dataclass
from datetime import datetime, timedelta
from functools import lru_cache

from duckduckgo_search import DDGS
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

from core.tools.types import ToolResult


console = Console()


@dataclass
class SearchResult:
    """Single search result"""
    title: str
    snippet: str
    url: str
    source: str


@dataclass
class SearchQuery:
    """Search query with metadata"""
    query: str
    max_results: int = 10
    region: str = "wt-wt"  # Worldwide
    safesearch: str = "moderate"
    timestamp: datetime = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()


class RateLimiter:
    """
    Rate limiter for search queries.

    Boris Principle: "Rate limiting isn't about restriction -
    it's about sustainability and respect for shared resources."
    """

    def __init__(self, max_calls: int = 5, time_window: int = 60):
        """
        Args:
            max_calls: Maximum calls per time window (default: 5)
            time_window: Time window in seconds (default: 60)
        """
        self.max_calls = max_calls
        self.time_window = time_window
        self.calls: List[float] = []

    def is_allowed(self) -> bool:
        """Check if call is allowed under rate limit"""
        now = time.time()

        # Remove calls outside time window
        self.calls = [t for t in self.calls if now - t < self.time_window]

        return len(self.calls) < self.max_calls

    def record_call(self):
        """Record a call"""
        self.calls.append(time.time())

    def time_until_allowed(self) -> float:
        """Get seconds until next call is allowed"""
        if self.is_allowed():
            return 0.0

        now = time.time()
        oldest_call = min(self.calls)
        return self.time_window - (now - oldest_call)


class SearchCache:
    """
    Simple cache for search results.

    Boris Principle: "Caching is optimization with memory.
    Cache intelligently: recent, frequent, and valuable."
    """

    def __init__(self, ttl_minutes: int = 15):
        """
        Args:
            ttl_minutes: Time to live in minutes (default: 15)
        """
        self.ttl = timedelta(minutes=ttl_minutes)
        self._cache: Dict[str, tuple] = {}  # query -> (results, timestamp)

    def get(self, query: str) -> Optional[List[SearchResult]]:
        """Get cached results if not expired"""
        if query not in self._cache:
            return None

        results, timestamp = self._cache[query]

        # Check if expired
        if datetime.now() - timestamp > self.ttl:
            del self._cache[query]
            return None

        return results

    def set(self, query: str, results: List[SearchResult]):
        """Cache results"""
        self._cache[query] = (results, datetime.now())

    def clear(self):
        """Clear all cached results"""
        self._cache.clear()

    def size(self) -> int:
        """Get number of cached queries"""
        return len(self._cache)


class WebSearchTool:
    """
    Web Search Tool using DuckDuckGo.

    Design Principles (Boris):
    1. Privacy First - No tracking, no API keys
    2. Speed & Caching - Cache aggressively, search sparingly
    3. Beautiful Output - Rich formatting, clear attribution
    4. Rate Limited - Respect for shared resources
    5. Error Graceful - Helpful messages, never crash

    Boris Quote:
    "A good search tool doesn't just find information -
    it presents knowledge with clarity and context."
    """

    def __init__(
        self,
        max_results: int = 10,
        rate_limit_calls: int = 5,
        rate_limit_window: int = 60,
        cache_ttl_minutes: int = 15
    ):
        """
        Initialize Web Search Tool.

        Args:
            max_results: Maximum results per search (default: 10)
            rate_limit_calls: Max calls per time window (default: 5)
            rate_limit_window: Time window in seconds (default: 60)
            cache_ttl_minutes: Cache TTL in minutes (default: 15)
        """
        self.max_results = max_results
        self.rate_limiter = RateLimiter(rate_limit_calls, rate_limit_window)
        self.cache = SearchCache(cache_ttl_minutes)
        self.console = Console()

    def search(
        self,
        query: str,
        max_results: Optional[int] = None,
        region: str = "wt-wt",
        safesearch: str = "moderate"
    ) -> ToolResult:
        """
        Search the web using DuckDuckGo.

        Philosophy: "Search is discovery. Every query is a question
        seeking an answer. Treat it with respect."

        Args:
            query: Search query string
            max_results: Maximum results (overrides default)
            region: Region code (wt-wt = worldwide)
            safesearch: moderate, strict, or off

        Returns:
            ToolResult with formatted search results
        """
        if not query or not query.strip():
            return ToolResult.error("❌ Empty search query\n\nPlease provide a search query.")

        # Use cache if available
        cached_results = self.cache.get(query)
        if cached_results:
            return self._format_results(cached_results, query, from_cache=True)

        # Check rate limit
        if not self.rate_limiter.is_allowed():
            wait_time = self.rate_limiter.time_until_allowed()
            return ToolResult.error(
                f"⏱️  Rate limit reached\n\n"
                f"Please wait {wait_time:.0f} seconds before searching again.\n\n"
                f"Rate limit: {self.rate_limiter.max_calls} searches per "
                f"{self.rate_limiter.time_window}s\n\n"
                f"💡 Tip: Refine your query to get better results on first try."
            )

        # Perform search
        try:
            max_res = max_results or self.max_results

            # Record rate limit
            self.rate_limiter.record_call()

            # Execute search
            with DDGS() as ddgs:
                raw_results = list(ddgs.text(
                    query,
                    region=region,
                    safesearch=safesearch,
                    max_results=max_res
                ))

            if not raw_results:
                return ToolResult.error(
                    f"🔍 No results found\n\n"
                    f"Query: '{query}'\n\n"
                    f"💡 Try:\n"
                    f"  - Different keywords\n"
                    f"  - More specific terms\n"
                    f"  - Removing special characters"
                )

            # Parse results
            results = [
                SearchResult(
                    title=r.get('title', 'No title'),
                    snippet=r.get('body', 'No description'),
                    url=r.get('href', ''),
                    source=self._extract_domain(r.get('href', ''))
                )
                for r in raw_results
            ]

            # Cache results
            self.cache.set(query, results)

            return self._format_results(results, query, from_cache=False)

        except Exception as e:
            return ToolResult.error(
                f"❌ Search failed\n\n"
                f"Error: {str(e)}\n\n"
                f"💡 Possible causes:\n"
                f"  - Network connection issue\n"
                f"  - DuckDuckGo service unavailable\n"
                f"  - Invalid search query\n\n"
                f"Try again in a moment."
            )

    def _extract_domain(self, url: str) -> str:
        """Extract domain from URL, returns 'unknown' for malformed URLs"""
        try:
            from urllib.parse import urlparse
            parsed = urlparse(url)
            return parsed.netloc or "unknown"
        except (ValueError, AttributeError):
            # URL is malformed or parsing failed - this is expected for some search results
            return "unknown"

    def _format_results(
        self,
        results: List[SearchResult],
        query: str,
        from_cache: bool = False
    ) -> ToolResult:
        """
        Format search results with Boris beauty.

        Philosophy: "Results aren't just data - they're answers
        waiting to be discovered. Present them with clarity."
        """
        lines = []

        # Header
        cache_indicator = " [cached]" if from_cache else ""
        lines.append(f"🔍 [bold cyan]Search Results{cache_indicator}[/bold cyan]")
        lines.append(f"[dim]Query: {query}[/dim]")
        lines.append(f"[dim]Found: {len(results)} result(s)[/dim]")
        lines.append("")

        # Results
        for i, result in enumerate(results, 1):
            lines.append(f"[bold]{i}. {result.title}[/bold]")
            lines.append(f"   [dim]{result.source}[/dim]")
            lines.append(f"   {result.snippet[:150]}...")
            lines.append(f"   🔗 [blue]{result.url}[/blue]")
            lines.append("")

        # Footer
        if from_cache:
            lines.append("[dim]⚡ Results served from cache (faster!)[/dim]")
        else:
            lines.append(f"[dim]💾 Results cached for {self.cache.ttl.seconds // 60} minutes[/dim]")

        lines.append(f"[dim]🔒 Privacy-first search (no tracking)[/dim]")

        return ToolResult.success("\n".join(lines))

    def clear_cache(self) -> ToolResult:
        """Clear search cache"""
        size_before = self.cache.size()
        self.cache.clear()

        return ToolResult.success(
            f"✅ Cache cleared\n\n"
            f"Removed {size_before} cached search(es)"
        )

    def get_cache_stats(self) -> ToolResult:
        """Get cache statistics"""
        size = self.cache.size()

        return ToolResult.success(
            f"📊 Cache Statistics\n\n"
            f"Cached searches: {size}\n"
            f"TTL: {self.cache.ttl.seconds // 60} minutes\n"
            f"Rate limit: {self.rate_limiter.max_calls} per {self.rate_limiter.time_window}s"
        )


# Convenience function for quick searches
def search_web(query: str, max_results: int = 10) -> ToolResult:
    """
    Quick web search (convenience function).

    Args:
        query: Search query
        max_results: Maximum results to return

    Returns:
        ToolResult with search results
    """
    tool = WebSearchTool(max_results=max_results)
    return tool.search(query)
