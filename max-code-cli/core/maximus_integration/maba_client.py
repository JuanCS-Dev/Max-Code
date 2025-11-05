"""
MABA Client

Client for MABA (Multi-Agent Browser Assistant) - Port 8151.

MABA performs:
- Web searches (documentation, best practices)
- API documentation lookups
- Library/framework research
- Code examples search

MABA = Multi-Agent Browser Assistant

v2.1: Refactored to use centralized settings (FASE 3.3)
"""

import aiohttp
import asyncio
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from enum import Enum

from config.settings import get_settings
from config.logging_config import get_logger

logger = get_logger(__name__)


# ============================================================================
# ENUMS
# ============================================================================

class SearchType(str, Enum):
    """Type of search"""
    DOCUMENTATION = "documentation"
    BEST_PRACTICES = "best_practices"
    LIBRARY_RESEARCH = "library_research"
    CODE_EXAMPLES = "code_examples"
    API_REFERENCE = "api_reference"


# ============================================================================
# DATA MODELS
# ============================================================================

@dataclass
class SearchResult:
    """Single search result"""
    title: str
    url: str
    snippet: str
    relevance: float  # 0.0 to 1.0
    source: str  # e.g., "stackoverflow", "github", "official_docs"


@dataclass
class MABASearchResult:
    """Complete search result from MABA"""
    query: str
    query_understanding: str
    results: List[SearchResult]
    total_results: int
    confidence: float
    suggested_refinements: List[str]


# ============================================================================
# MABA CLIENT
# ============================================================================

class MABAClient:
    """
    Client for MABA (Multi-Agent Browser Assistant).

    MABA specializes in:
    - Intelligent web searches
    - Documentation lookups
    - Finding code examples
    - Library/framework research

    Example:
        client = MABAClient(url="http://localhost:8151")

        results = await client.search(
            query="OAuth 2.0 PKCE implementation best practices",
            search_type=SearchType.BEST_PRACTICES
        )

        for result in results.results[:3]:
            logger.info(f"{result.title}: {result.url}")
    """

    def __init__(
        self,
        url: Optional[str] = None,
        timeout: Optional[float] = None,  # Web searches can be slower
    ):
        """
        Initialize MABA client.

        Args:
            url: MABA service URL (default: from settings)
            timeout: Request timeout in seconds (default: from settings, or 10.0 if not set)
        """
        # Load settings
        settings = get_settings()

        # Use provided values or fallback to settings
        self.url = (url or settings.maximus.maba_url).rstrip("/")
        # MABA default timeout is 10.0 (web searches are slower)
        self.timeout = timeout if timeout is not None else 10.0
        self._session: Optional[aiohttp.ClientSession] = None

    async def _get_session(self) -> aiohttp.ClientSession:
        """Get or create session"""
        if self._session is None or self._session.closed:
            self._session = aiohttp.ClientSession(
                timeout=aiohttp.ClientTimeout(total=self.timeout)
            )
        return self._session

    async def close(self):
        """Close client session"""
        if self._session and not self._session.closed:
            await self._session.close()

    # ========================================================================
    # SEARCH
    # ========================================================================

    async def search(
        self,
        query: str,
        search_type: Optional[SearchType] = None,
        context: Optional[str] = None,
        max_results: int = 10,
    ) -> MABASearchResult:
        """
        Perform web search using MABA.

        Args:
            query: Search query
            search_type: Type of search (optional, MABA will infer)
            context: Additional context for query understanding
            max_results: Maximum results to return (default: 10)

        Returns:
            MABASearchResult with ranked results

        Example:
            results = await client.search(
                query="FastAPI async database connections",
                search_type=SearchType.BEST_PRACTICES,
                context="Building REST API with PostgreSQL"
            )

            logger.info(f"Found {results.total_results} results")
            logger.info(f"Query understood as: {results.query_understanding}")
            for result in results.results:
                logger.info(f"- {result.title} ({result.relevance:.2f})")
                logger.info(f"  {result.url}")
        """
        payload = {
            "query": query,
            "search_type": search_type.value if search_type else None,
            "context": context or "",
            "max_results": max_results,
        }

        session = await self._get_session()

        async with session.post(f"{self.url}/api/v1/search", json=payload) as response:
            if response.status != 200:
                raise Exception(f"MABA error {response.status}: {await response.text()}")

            data = await response.json()

            # Parse results
            results = [
                SearchResult(
                    title=r["title"],
                    url=r["url"],
                    snippet=r["snippet"],
                    relevance=r["relevance"],
                    source=r["source"],
                )
                for r in data["results"]
            ]

            # Sort by relevance
            results.sort(key=lambda r: r.relevance, reverse=True)

            return MABASearchResult(
                query=data["query"],
                query_understanding=data["query_understanding"],
                results=results,
                total_results=data["total_results"],
                confidence=data["confidence"],
                suggested_refinements=data["suggested_refinements"],
            )

    # ========================================================================
    # SPECIALIZED SEARCHES
    # ========================================================================

    async def search_documentation(
        self,
        library: str,
        topic: str,
        version: Optional[str] = None,
    ) -> MABASearchResult:
        """
        Search for official documentation.

        Args:
            library: Library/framework name (e.g., "FastAPI")
            topic: Topic to search (e.g., "async database")
            version: Optional version (e.g., "0.100.0")

        Returns:
            MABASearchResult focused on official docs

        Example:
            results = await client.search_documentation(
                library="FastAPI",
                topic="dependency injection",
                version="0.100.0"
            )
        """
        query = f"{library} {topic}"
        if version:
            query += f" version {version}"

        context = f"Looking for official {library} documentation"

        return await self.search(
            query=query,
            search_type=SearchType.DOCUMENTATION,
            context=context
        )

    async def search_best_practices(
        self,
        technology: str,
        context: str,
    ) -> MABASearchResult:
        """
        Search for best practices.

        Args:
            technology: Technology/pattern (e.g., "OAuth 2.0")
            context: Context (e.g., "mobile authentication")

        Returns:
            MABASearchResult focused on best practices

        Example:
            results = await client.search_best_practices(
                technology="OAuth 2.0 PKCE",
                context="Single-page application authentication"
            )
        """
        query = f"{technology} best practices"

        return await self.search(
            query=query,
            search_type=SearchType.BEST_PRACTICES,
            context=context
        )

    async def search_code_examples(
        self,
        description: str,
        language: Optional[str] = None,
    ) -> MABASearchResult:
        """
        Search for code examples.

        Args:
            description: What you want to do
            language: Programming language (optional)

        Returns:
            MABASearchResult focused on code examples

        Example:
            results = await client.search_code_examples(
                description="async retry with exponential backoff",
                language="Python"
            )
        """
        query = description
        if language:
            query = f"{language} {query}"

        context = "Looking for code examples and implementations"

        return await self.search(
            query=query,
            search_type=SearchType.CODE_EXAMPLES,
            context=context
        )

    async def research_library(
        self,
        library_name: str,
        purpose: str,
    ) -> MABASearchResult:
        """
        Research a library/framework.

        Args:
            library_name: Library name
            purpose: What you want to use it for

        Returns:
            MABASearchResult with library info, docs, examples

        Example:
            results = await client.research_library(
                library_name="aiohttp",
                purpose="async HTTP requests in Python"
            )
        """
        query = f"{library_name} library"
        context = f"Researching {library_name} for: {purpose}"

        return await self.search(
            query=query,
            search_type=SearchType.LIBRARY_RESEARCH,
            context=context
        )

    # ========================================================================
    # FETCH URL CONTENT
    # ========================================================================

    async def fetch_url(self, url: str) -> Dict[str, Any]:
        """
        Fetch and extract content from URL.

        Useful for getting full documentation pages.

        Args:
            url: URL to fetch

        Returns:
            Dict with:
            - title: Page title
            - content: Extracted text content
            - code_snippets: List of code snippets found
            - links: Relevant links

        Example:
            content = await client.fetch_url(
                "https://fastapi.tiangolo.com/tutorial/dependencies/"
            )

            print(content["title"])
            for snippet in content["code_snippets"]:
                print(snippet)
        """
        payload = {"url": url}

        session = await self._get_session()

        async with session.post(f"{self.url}/api/v1/fetch", json=payload) as response:
            if response.status != 200:
                raise Exception(f"MABA error {response.status}: {await response.text()}")

            return await response.json()

    # ========================================================================
    # HEALTH CHECK
    # ========================================================================

    async def health_check(self) -> bool:
        """
        Check if MABA is healthy.

        Returns:
            True if healthy, False otherwise
        """
        try:
            session = await self._get_session()
            async with session.get(f"{self.url}/api/v1/health") as response:
                return response.status == 200
        except Exception:
            return False


# ============================================================================
# CONTEXT MANAGER
# ============================================================================

class MABAClientContext:
    """Context manager for MABA client"""

    def __init__(self, **kwargs):
        self.client = MABAClient(**kwargs)

    async def __aenter__(self):
        return self.client

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.client.close()
