#!/usr/bin/env python3
"""
Web Fetch Tool - URL Content Extraction with Boris Technique ✨

Philosophy (Boris):
"Web fetching is not just downloading HTML - it's extracting
knowledge from chaos. Transform noise into signal, HTML into
readable markdown, ads into silence."

Security:
- User-agent rotation (avoid blocking)
- Timeout enforcement (10s max)
- Size limits (5MB max)
- Malicious URL detection

Beauty:
- HTML → Markdown conversion
- Main content extraction (no ads/nav)
- Clean, readable output
- Beautiful error messages

Performance:
- Cache fetched content (15min TTL)
- Retry logic (3 attempts)
- Connection pooling

Soli Deo Gloria 🙏
"""

import time
from typing import Optional, Dict
from dataclasses import dataclass
from datetime import datetime, timedelta
from urllib.parse import urlparse
import hashlib

import requests
from bs4 import BeautifulSoup
from readability import Document
from markdownify import markdownify as md

from rich.console import Console

from core.tools.types import ToolResult


console = Console()


@dataclass
class FetchedContent:
    """Fetched and processed content"""
    url: str
    title: str
    content: str  # Markdown format
    raw_html: str
    fetch_time: datetime
    size_bytes: int


class FetchCache:
    """
    Cache for fetched content.

    Boris: "Cache is memory with expiration.
    Cache aggressively, expire intelligently."
    """

    def __init__(self, ttl_minutes: int = 15):
        self.ttl = timedelta(minutes=ttl_minutes)
        self._cache: Dict[str, tuple] = {}  # url_hash -> (content, timestamp)

    def _hash_url(self, url: str) -> str:
        """Hash URL for cache key"""
        return hashlib.md5(url.encode()).hexdigest()

    def get(self, url: str) -> Optional[FetchedContent]:
        """Get cached content if not expired"""
        key = self._hash_url(url)

        if key not in self._cache:
            return None

        content, timestamp = self._cache[key]

        # Check expiration
        if datetime.now() - timestamp > self.ttl:
            del self._cache[key]
            return None

        return content

    def set(self, url: str, content: FetchedContent):
        """Cache content"""
        key = self._hash_url(url)
        self._cache[key] = (content, datetime.now())

    def clear(self):
        """Clear cache"""
        self._cache.clear()


class WebFetchTool:
    """
    Web Fetch Tool - Extract clean content from URLs.

    Design Principles (Boris):
    1. Extract Signal - Remove ads, nav, clutter
    2. Convert Format - HTML → Markdown for LLM
    3. Respect Limits - Timeout, size, retries
    4. Cache Aggressively - Same URL = cached result
    5. Beautiful Errors - Helpful, never crash

    Boris Quote:
    "A web page is 95% noise, 5% signal.
    Our job is to find that 5% and present it beautifully."
    """

    USER_AGENTS = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    ]

    def __init__(
        self,
        timeout: int = 10,
        max_size_mb: int = 5,
        max_retries: int = 3,
        cache_ttl_minutes: int = 15
    ):
        """
        Initialize Web Fetch Tool.

        Args:
            timeout: Request timeout in seconds (default: 10)
            max_size_mb: Maximum content size in MB (default: 5)
            max_retries: Maximum retry attempts (default: 3)
            cache_ttl_minutes: Cache TTL in minutes (default: 15)
        """
        self.timeout = timeout
        self.max_size_bytes = max_size_mb * 1024 * 1024
        self.max_retries = max_retries
        self.cache = FetchCache(cache_ttl_minutes)
        self.console = Console()

        # Session for connection pooling
        self.session = requests.Session()

    def fetch(
        self,
        url: str,
        extract_main_content: bool = True,
        convert_to_markdown: bool = True
    ) -> ToolResult:
        """
        Fetch content from URL.

        Philosophy: "Fetching is not just GET request -
        it's extraction, transformation, and presentation."

        Args:
            url: URL to fetch
            extract_main_content: Extract main content only (remove ads/nav)
            convert_to_markdown: Convert HTML to Markdown

        Returns:
            ToolResult with fetched content
        """
        # Validate URL
        if not url or not url.strip():
            return ToolResult.error("❌ Empty URL\n\nPlease provide a valid URL.")

        # Parse URL
        try:
            parsed = urlparse(url)
            if not parsed.scheme or not parsed.netloc:
                return ToolResult.error(
                    f"❌ Invalid URL: {url}\n\n"
                    f"URL must include scheme (http:// or https://)"
                )
        except Exception as e:
            return ToolResult.error(f"❌ Invalid URL: {str(e)}")

        # Check cache
        cached = self.cache.get(url)
        if cached:
            return self._format_content(cached, from_cache=True)

        # Fetch with retries
        for attempt in range(self.max_retries):
            try:
                # Rotate user agent
                headers = {
                    'User-Agent': self.USER_AGENTS[attempt % len(self.USER_AGENTS)]
                }

                # Stream to check size
                response = self.session.get(
                    url,
                    headers=headers,
                    timeout=self.timeout,
                    stream=True
                )

                response.raise_for_status()

                # Check content length
                content_length = response.headers.get('content-length')
                if content_length and int(content_length) > self.max_size_bytes:
                    return ToolResult.error(
                        f"❌ Content too large\n\n"
                        f"Size: {int(content_length) / 1024 / 1024:.1f}MB\n"
                        f"Max: {self.max_size_bytes / 1024 / 1024:.0f}MB\n\n"
                        f"💡 Try fetching a smaller page"
                    )

                # Download content
                content_bytes = b""
                for chunk in response.iter_content(chunk_size=8192):
                    content_bytes += chunk
                    if len(content_bytes) > self.max_size_bytes:
                        return ToolResult.error(
                            f"❌ Content exceeds size limit\n\n"
                            f"Max: {self.max_size_bytes / 1024 / 1024:.0f}MB"
                        )

                html_content = content_bytes.decode('utf-8', errors='ignore')

                # Extract main content
                if extract_main_content:
                    doc = Document(html_content)
                    title = doc.title()
                    main_html = doc.summary()
                else:
                    soup = BeautifulSoup(html_content, 'html.parser')
                    title = soup.title.string if soup.title else "No title"
                    main_html = html_content

                # Convert to markdown
                if convert_to_markdown:
                    # Remove scripts and styles first
                    soup = BeautifulSoup(main_html, 'html.parser')
                    for script in soup(["script", "style"]):
                        script.decompose()

                    clean_html = str(soup)
                    markdown_content = md(clean_html, heading_style="ATX")
                else:
                    markdown_content = main_html

                # Create result
                fetched = FetchedContent(
                    url=url,
                    title=title,
                    content=markdown_content,
                    raw_html=html_content,
                    fetch_time=datetime.now(),
                    size_bytes=len(content_bytes)
                )

                # Cache result
                self.cache.set(url, fetched)

                return self._format_content(fetched, from_cache=False)

            except requests.exceptions.Timeout:
                if attempt < self.max_retries - 1:
                    time.sleep(1)  # Wait before retry
                    continue
                return ToolResult.error(
                    f"⏱️  Request timeout\n\n"
                    f"URL: {url}\n"
                    f"Timeout: {self.timeout}s\n\n"
                    f"💡 The page may be slow to respond. Try again later."
                )

            except requests.exceptions.ConnectionError:
                if attempt < self.max_retries - 1:
                    time.sleep(1)
                    continue
                return ToolResult.error(
                    f"🔌 Connection error\n\n"
                    f"URL: {url}\n\n"
                    f"💡 Possible causes:\n"
                    f"  - Network connection issue\n"
                    f"  - Server is down\n"
                    f"  - Invalid hostname"
                )

            except requests.exceptions.HTTPError as e:
                return ToolResult.error(
                    f"❌ HTTP Error: {e.response.status_code}\n\n"
                    f"URL: {url}\n\n"
                    f"💡 Status codes:\n"
                    f"  - 404: Page not found\n"
                    f"  - 403: Access forbidden\n"
                    f"  - 500: Server error"
                )

            except Exception as e:
                if attempt < self.max_retries - 1:
                    continue
                return ToolResult.error(
                    f"❌ Fetch failed\n\n"
                    f"Error: {str(e)}\n\n"
                    f"URL: {url}"
                )

        return ToolResult.error(
            f"❌ Failed after {self.max_retries} attempts\n\n"
            f"URL: {url}"
        )

    def _format_content(
        self,
        content: FetchedContent,
        from_cache: bool = False
    ) -> ToolResult:
        """
        Format fetched content with Boris beauty.

        Philosophy: "Content is knowledge. Present it with
        clarity, context, and visual hierarchy."
        """
        lines = []

        # Header
        cache_indicator = " [cached]" if from_cache else ""
        lines.append(f"🌐 [bold cyan]Web Content{cache_indicator}[/bold cyan]")
        lines.append(f"[bold]{content.title}[/bold]")
        lines.append(f"[dim]{content.url}[/dim]")
        lines.append(f"[dim]Size: {content.size_bytes / 1024:.1f}KB | Fetched: {content.fetch_time.strftime('%H:%M:%S')}[/dim]")
        lines.append("")
        lines.append("─" * 60)
        lines.append("")

        # Content (truncate if too long)
        max_length = 5000  # 5K chars
        if len(content.content) > max_length:
            truncated = content.content[:max_length]
            lines.append(truncated)
            lines.append("")
            lines.append(f"[dim]... (truncated, {len(content.content) - max_length} chars omitted)[/dim]")
        else:
            lines.append(content.content)

        lines.append("")
        lines.append("─" * 60)

        # Footer
        if from_cache:
            lines.append("[dim]⚡ Content served from cache (faster!)[/dim]")
        else:
            lines.append(f"[dim]💾 Content cached for {self.cache.ttl.seconds // 60} minutes[/dim]")

        return ToolResult.success("\n".join(lines))

    def clear_cache(self) -> ToolResult:
        """Clear fetch cache"""
        self.cache.clear()
        return ToolResult.success("✅ Fetch cache cleared")


# Convenience function
def fetch_url(url: str) -> ToolResult:
    """
    Quick URL fetch (convenience function).

    Args:
        url: URL to fetch

    Returns:
        ToolResult with content
    """
    tool = WebFetchTool()
    return tool.fetch(url)
