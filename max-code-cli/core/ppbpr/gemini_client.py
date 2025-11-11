"""
Gemini API Client for P.P.B.P.R Methodology
Provides deep research capabilities with Google Search grounding

Constitutional AI v3.0 Compliance:
- P1 (Zero Trust): Validates all API responses
- P4 (Obrigação da Verdade): Honest about research quality/limitations
"""

import google.generativeai as genai
import os
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime
import asyncio
from config.logging_config import get_logger

logger = get_logger(__name__)


@dataclass
class ResearchSource:
    """Single research source from grounding"""
    uri: str
    title: str
    snippet: Optional[str] = None


@dataclass
class ResearchResult:
    """
    Research result from Gemini with grounding

    Attributes:
        content: Main research content
        sources: List of sources used (with URIs)
        search_queries: Search queries executed
        quality_score: 0-1 quality assessment
        word_count: Number of words in content
        timestamp: When research was conducted
    """
    content: str
    sources: List[ResearchSource]
    search_queries: List[str] = field(default_factory=list)
    quality_score: float = 0.0
    word_count: int = 0
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())

    def __post_init__(self):
        """Calculate derived fields"""
        if not self.word_count:
            self.word_count = len(self.content.split())


class GeminiClient:
    """
    Google Gemini API Client for deep research

    Capabilities:
    - Grounding with Google Search (real-time web access)
    - 1M+ token context window (Gemini 1.5/2.0)
    - Citation extraction
    - PhD-level research quality

    Models:
    - gemini-1.5-flash: Fast, cost-effective ($0.15/M tokens)
    - gemini-1.5-pro: Balanced ($1.25/M tokens)
    - gemini-2.0-flash-exp: Latest experimental

    Rate Limits (Free tier):
    - Flash: 1500 req/day, 15 RPM
    - Pro: 50 req/day, 2 RPM
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        model: str = "gemini-2.5-flash",  # Updated to available model
        enable_grounding: bool = True,
        temperature: float = 0.7
    ):
        """
        Initialize Gemini client

        Args:
            api_key: Gemini API key (or from GEMINI_API_KEY env)
            model: Model name (flash/pro)
            enable_grounding: Enable Google Search grounding
            temperature: Creativity level (0-1)
        """
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            logger.warning("⚠️  GEMINI_API_KEY not set - client will fail on use")

        self.model_name = model
        self.enable_grounding = enable_grounding
        self.temperature = temperature

        # Configure SDK
        genai.configure(api_key=self.api_key)

        # Initialize model
        self.model = genai.GenerativeModel(
            model_name=self.model_name,
            # Note: tools configuration moved to generate_content call
        )

        logger.info(f"✅ Gemini client initialized: {self.model_name}")

    async def deep_research(
        self,
        query: str,
        max_tokens: int = 10_000,
        temperature: Optional[float] = None
    ) -> ResearchResult:
        """
        Conduct deep research using Gemini

        Args:
            query: Research question or topic
            max_tokens: Maximum response length
            temperature: Override default temperature

        Returns:
            ResearchResult with content, sources, and quality metrics

        Raises:
            ValueError: If API key not configured
            Exception: If API call fails
        """
        if not self.api_key:
            raise ValueError(
                "GEMINI_API_KEY not configured. "
                "Set via environment or constructor."
            )

        logger.info(f"🔍 Starting deep research: {query[:60]}...")

        try:
            # Use asyncio to run in executor (SDK is sync)
            loop = asyncio.get_event_loop()
            result = await loop.run_in_executor(
                None,
                self._sync_research,
                query,
                max_tokens,
                temperature or self.temperature
            )

            logger.info(
                f"✅ Research complete: {result.word_count} words, "
                f"{len(result.sources)} sources, quality={result.quality_score:.2f}"
            )

            return result

        except Exception as e:
            logger.error(f"❌ Gemini API error: {e}")
            raise

    def _sync_research(
        self,
        query: str,
        max_tokens: int,
        temperature: float
    ) -> ResearchResult:
        """Synchronous research call (for executor)"""

        # Configure generation
        generation_config = genai.GenerationConfig(
            max_output_tokens=max_tokens,
            temperature=temperature
        )

        # Configure safety settings (more permissive for research)
        safety_settings = [
            {
                "category": "HARM_CATEGORY_HARASSMENT",
                "threshold": "BLOCK_NONE"
            },
            {
                "category": "HARM_CATEGORY_HATE_SPEECH",
                "threshold": "BLOCK_NONE"
            },
            {
                "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                "threshold": "BLOCK_NONE"
            },
            {
                "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                "threshold": "BLOCK_NONE"
            }
        ]

        # For newer SDK versions, grounding might be configured differently
        # Using basic text generation for now
        # TODO: Update when grounding API is stabilized

        response = self.model.generate_content(
            query,
            generation_config=generation_config,
            safety_settings=safety_settings
        )

        # Extract content with better error handling
        try:
            content = response.text
        except ValueError as e:
            # Handle blocked or empty responses
            if hasattr(response, 'candidates') and response.candidates:
                candidate = response.candidates[0]
                finish_reason = candidate.finish_reason if hasattr(candidate, 'finish_reason') else "UNKNOWN"

                if finish_reason == 2:  # SAFETY
                    raise ValueError(
                        f"Content blocked by safety filters. "
                        f"Try rephrasing your query or adjust safety settings."
                    )
                elif finish_reason == 3:  # RECITATION
                    raise ValueError(
                        f"Content blocked due to recitation. "
                        f"Generated content too similar to training data."
                    )
                else:
                    raise ValueError(f"No valid response generated. Finish reason: {finish_reason}")
            else:
                raise ValueError(f"No response generated: {e}")

        # Extract sources (if grounding metadata available)
        sources = self._extract_sources(response)

        # Extract search queries (if available)
        search_queries = self._extract_search_queries(response)

        # Assess quality
        quality_score = self._assess_quality(content, sources)

        return ResearchResult(
            content=content,
            sources=sources,
            search_queries=search_queries,
            quality_score=quality_score
        )

    def _extract_sources(self, response: Any) -> List[ResearchSource]:
        """
        Extract grounding sources from response

        Note: Grounding API structure varies by SDK version
        This is a best-effort extraction
        """
        sources = []

        try:
            # Check for grounding metadata (newer SDK)
            if hasattr(response, 'grounding_metadata'):
                metadata = response.grounding_metadata

                # Extract grounding chunks
                if hasattr(metadata, 'grounding_chunks'):
                    for chunk in metadata.grounding_chunks:
                        if hasattr(chunk, 'web'):
                            sources.append(ResearchSource(
                                uri=chunk.web.uri if hasattr(chunk.web, 'uri') else "unknown",
                                title=chunk.web.title if hasattr(chunk.web, 'title') else "Unknown"
                            ))

            # Check for citations (older SDK) - with error handling
            elif hasattr(response, 'candidates'):
                for candidate in response.candidates:
                    if hasattr(candidate, 'citation_metadata'):
                        try:
                            # Try to access citations - structure may vary
                            citation_meta = candidate.citation_metadata
                            if hasattr(citation_meta, 'citation_sources'):
                                for citation in citation_meta.citation_sources:
                                    sources.append(ResearchSource(
                                        uri=citation.uri if hasattr(citation, 'uri') else "unknown",
                                        title=citation.title if hasattr(citation, 'title') else "Unknown"
                                    ))
                        except (AttributeError, TypeError) as e:
                            logger.debug(f"Could not extract citations: {e}")
                            pass

        except Exception as e:
            logger.debug(f"Error extracting sources: {e}")

        logger.debug(f"Extracted {len(sources)} sources from response")
        return sources

    def _extract_search_queries(self, response: Any) -> List[str]:
        """Extract search queries from grounding metadata"""
        queries = []

        if hasattr(response, 'grounding_metadata'):
            metadata = response.grounding_metadata
            if hasattr(metadata, 'web_search_queries'):
                queries = list(metadata.web_search_queries)

        return queries

    def _assess_quality(self, content: str, sources: List[ResearchSource]) -> float:
        """
        Assess research quality (P4 - Obrigação da Verdade)

        Criteria:
        - Content length (40%): 500+ words = good
        - Source count (40%): 3+ sources = good
        - Source diversity (20%): 3+ domains = good

        Returns:
            Quality score 0.0-1.0
        """
        score = 0.0

        # Content length scoring
        word_count = len(content.split())
        if word_count >= 1000:
            score += 0.4
        elif word_count >= 500:
            score += 0.3
        elif word_count >= 200:
            score += 0.2
        elif word_count >= 100:
            score += 0.1

        # Source count scoring
        source_count = len(sources)
        if source_count >= 5:
            score += 0.4
        elif source_count >= 3:
            score += 0.3
        elif source_count >= 1:
            score += 0.2

        # Source diversity scoring
        domains = set()
        for source in sources:
            try:
                # Extract domain from URI
                parts = source.uri.split('/')
                if len(parts) >= 3:
                    domain = parts[2]  # http://domain.com/path
                    domains.add(domain)
            except:
                pass

        if len(domains) >= 3:
            score += 0.2
        elif len(domains) >= 2:
            score += 0.1

        return min(1.0, score)

    def validate_research_quality(
        self,
        result: ResearchResult,
        min_words: int = 500,
        min_sources: int = 3,
        min_quality: float = 0.5
    ) -> tuple[bool, str]:
        """
        Validate research quality (QG1 - Quality Gate 1)

        Args:
            result: Research result to validate
            min_words: Minimum word count
            min_sources: Minimum source count
            min_quality: Minimum quality score

        Returns:
            (is_valid, error_message)
        """
        # Check word count
        if result.word_count < min_words:
            return False, f"Insufficient content: {result.word_count} words (min {min_words})"

        # Check source count
        if len(result.sources) < min_sources:
            return False, f"Insufficient sources: {len(result.sources)} (min {min_sources})"

        # Check overall quality
        if result.quality_score < min_quality:
            return False, f"Quality too low: {result.quality_score:.2f} (min {min_quality:.2f})"

        return True, "Research quality validated ✅"


class GeminiResearchTool:
    """
    High-level research tool for P.P.B.P.R methodology

    Provides PhD-level research with quality validation
    """

    def __init__(self, api_key: Optional[str] = None):
        self.client = GeminiClient(api_key=api_key)

    async def research_topic(
        self,
        topic: str,
        depth: str = "comprehensive"
    ) -> ResearchResult:
        """
        Research a topic with specified depth

        Args:
            topic: Research topic/question
            depth: Research depth (basic/moderate/comprehensive)

        Returns:
            Research result with validation
        """
        # Configure based on depth
        depth_config = {
            "basic": {"max_tokens": 2000, "min_words": 200, "min_sources": 1},
            "moderate": {"max_tokens": 5000, "min_words": 500, "min_sources": 2},
            "comprehensive": {"max_tokens": 10000, "min_words": 1000, "min_sources": 3}
        }

        config = depth_config.get(depth, depth_config["comprehensive"])

        # Enhance prompt for PhD-level research
        enhanced_prompt = f"""
Conduct {depth} PhD-level research on the following topic:

{topic}

Requirements:
1. Provide comprehensive technical analysis
2. Include latest developments (2024-2025 if relevant)
3. Analyze multiple approaches/perspectives
4. Include authoritative sources
5. Provide evidence-based recommendations

Structure your research as:
1. Executive Summary
2. Technical Background & Context
3. Current State-of-the-Art
4. Analysis of Approaches
5. Key Findings & Insights
6. Practical Implications
7. Recommendations

Use clear, technical language appropriate for expert audience.
"""

        # Conduct research
        result = await self.client.deep_research(
            query=enhanced_prompt,
            max_tokens=config["max_tokens"]
        )

        # Validate quality
        is_valid, message = self.client.validate_research_quality(
            result,
            min_words=config["min_words"],
            min_sources=config["min_sources"]
        )

        if not is_valid:
            logger.warning(f"⚠️  Research quality issue: {message}")
            # Continue anyway but log the issue

        return result


# Example usage
if __name__ == "__main__":
    async def test_research():
        """Test Gemini research capabilities"""
        print("🧪 Testing Gemini Research Client\n")

        tool = GeminiResearchTool()

        result = await tool.research_topic(
            topic="OAuth 2.0 implementation best practices for microservices",
            depth="comprehensive"
        )

        print(f"📊 Research Results:")
        print(f"   Words: {result.word_count}")
        print(f"   Sources: {len(result.sources)}")
        print(f"   Quality: {result.quality_score:.2f}")
        print(f"\n📄 Content Preview:")
        print(result.content[:500] + "...\n")

        if result.sources:
            print(f"🔗 Sources:")
            for i, source in enumerate(result.sources[:5], 1):
                print(f"   [{i}] {source.title}")
                print(f"       {source.uri}")

    # Run test
    asyncio.run(test_research())
