"""
NIS Client

Client for NIS (Narrative Intelligence System) - Port 8152.

NIS performs:
- Narrative documentation generation
- Story-based explanations of code changes
- Visual data for understanding
- Commit message generation

NIS = Narrative Intelligence System

v2.1: Refactored to use centralized settings (FASE 3.3)
"""

import aiohttp
import asyncio
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from enum import Enum

from config.settings import get_settings


# ============================================================================
# ENUMS
# ============================================================================

class NarrativeStyle(str, Enum):
    """Narrative style"""
    TECHNICAL = "technical"        # Technical documentation
    STORY = "story"                # Story-based explanation
    TUTORIAL = "tutorial"          # Step-by-step tutorial
    SUMMARY = "summary"            # Executive summary
    CHANGELOG = "changelog"        # Changelog format


# ============================================================================
# DATA MODELS
# ============================================================================

@dataclass
class CodeChange:
    """Represents a code change"""
    file_path: str
    change_type: str  # "added", "modified", "deleted"
    lines_added: int
    lines_deleted: int
    description: Optional[str] = None
    diff: Optional[str] = None


@dataclass
class KeyInsight:
    """A key insight about changes"""
    category: str  # "architecture", "security", "performance", etc
    insight: str
    importance: str  # "LOW", "MEDIUM", "HIGH", "CRITICAL"


@dataclass
class VisualizationData:
    """Data for visualizing changes"""
    change_distribution: Dict[str, int]  # {"added": 50, "modified": 30, "deleted": 10}
    file_impact: Dict[str, float]  # {"auth.py": 0.8, "utils.py": 0.3}
    complexity_trend: List[float]  # Complexity over time
    test_coverage: Optional[float] = None


@dataclass
class Narrative:
    """Complete narrative from NIS"""
    title: str
    story: str
    key_insights: List[KeyInsight]
    summary: str
    visualization_data: VisualizationData
    confidence: float
    style: NarrativeStyle


# ============================================================================
# NIS CLIENT
# ============================================================================

class NISClient:
    """
    Client for NIS (Narrative Intelligence System).

    NIS specializes in:
    - Converting code changes into human-readable stories
    - Extracting key insights
    - Generating visualizations
    - Creating commit messages and changelogs

    Example:
        client = NISClient(url="http://localhost:8152")

        narrative = await client.generate_narrative(
            changes=[
                CodeChange(
                    file_path="auth.py",
                    change_type="modified",
                    lines_added=50,
                    lines_deleted=20,
                    description="Refactored authentication"
                )
            ],
            style=NarrativeStyle.STORY
        )

        print(narrative.story)
        for insight in narrative.key_insights:
            print(f"💡 {insight.insight}")
    """

    def __init__(
        self,
        url: Optional[str] = None,
        timeout: Optional[float] = None,
    ):
        """
        Initialize NIS client.

        Args:
            url: NIS service URL (default: from settings)
            timeout: Request timeout in seconds (default: from settings)
        """
        # Load settings
        settings = get_settings()

        # Use provided values or fallback to settings
        self.url = (url or settings.maximus.nis_url).rstrip("/")
        self.timeout = timeout if timeout is not None else float(settings.maximus.timeout_seconds)
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
    # GENERATE NARRATIVE
    # ========================================================================

    async def generate_narrative(
        self,
        changes: List[CodeChange],
        style: NarrativeStyle = NarrativeStyle.STORY,
        context: Optional[Dict[str, Any]] = None,
    ) -> Narrative:
        """
        Generate narrative documentation from code changes.

        Args:
            changes: List of code changes
            style: Narrative style
            context: Optional context (project name, purpose, etc)

        Returns:
            Narrative with story, insights, and visualization data

        Example:
            narrative = await client.generate_narrative(
                changes=[
                    CodeChange(
                        file_path="auth.py",
                        change_type="modified",
                        lines_added=50,
                        lines_deleted=20,
                        description="Added OAuth 2.0 support"
                    ),
                    CodeChange(
                        file_path="tests/test_auth.py",
                        change_type="added",
                        lines_added=100,
                        lines_deleted=0,
                        description="Added OAuth tests"
                    )
                ],
                style=NarrativeStyle.STORY,
                context={"project": "user_service", "purpose": "secure authentication"}
            )

            print(narrative.title)
            print(narrative.story)

            for insight in narrative.key_insights:
                if insight.importance in ["HIGH", "CRITICAL"]:
                    print(f"⚠️ {insight.insight}")
        """
        context = context or {}

        # Serialize changes
        changes_data = [
            {
                "file_path": c.file_path,
                "change_type": c.change_type,
                "lines_added": c.lines_added,
                "lines_deleted": c.lines_deleted,
                "description": c.description,
                "diff": c.diff,
            }
            for c in changes
        ]

        payload = {
            "changes": changes_data,
            "style": style.value,
            "context": context,
        }

        session = await self._get_session()

        async with session.post(f"{self.url}/api/v1/narrative", json=payload) as response:
            if response.status != 200:
                raise Exception(f"NIS error {response.status}: {await response.text()}")

            data = await response.json()

            # Parse key insights
            key_insights = [
                KeyInsight(
                    category=insight["category"],
                    insight=insight["insight"],
                    importance=insight["importance"],
                )
                for insight in data["key_insights"]
            ]

            # Parse visualization data
            viz_data = data["visualization_data"]
            visualization = VisualizationData(
                change_distribution=viz_data["change_distribution"],
                file_impact=viz_data["file_impact"],
                complexity_trend=viz_data["complexity_trend"],
                test_coverage=viz_data.get("test_coverage"),
            )

            return Narrative(
                title=data["title"],
                story=data["story"],
                key_insights=key_insights,
                summary=data["summary"],
                visualization_data=visualization,
                confidence=data["confidence"],
                style=NarrativeStyle(data["style"]),
            )

    # ========================================================================
    # GENERATE COMMIT MESSAGE
    # ========================================================================

    async def generate_commit_message(
        self,
        changes: List[CodeChange],
        conventional: bool = True,
    ) -> str:
        """
        Generate commit message from changes.

        Args:
            changes: List of code changes
            conventional: Use Conventional Commits format (default: True)

        Returns:
            Commit message

        Example:
            message = await client.generate_commit_message(
                changes=[
                    CodeChange(
                        file_path="auth.py",
                        change_type="modified",
                        lines_added=50,
                        lines_deleted=20,
                        description="Added OAuth support"
                    )
                ],
                conventional=True
            )

            print(message)
            # "feat(auth): add OAuth 2.0 PKCE support
            #
            # - Implemented authorization code flow with PKCE
            # - Added token refresh mechanism
            # - Updated tests to cover new flow
            #
            # 🤖 Generated with Max-Code CLI"
        """
        changes_data = [
            {
                "file_path": c.file_path,
                "change_type": c.change_type,
                "lines_added": c.lines_added,
                "lines_deleted": c.lines_deleted,
                "description": c.description,
            }
            for c in changes
        ]

        payload = {
            "changes": changes_data,
            "conventional": conventional,
        }

        session = await self._get_session()

        async with session.post(f"{self.url}/api/v1/commit_message", json=payload) as response:
            if response.status != 200:
                raise Exception(f"NIS error {response.status}: {await response.text()}")

            data = await response.json()
            return data["commit_message"]

    # ========================================================================
    # GENERATE CHANGELOG
    # ========================================================================

    async def generate_changelog(
        self,
        changes: List[CodeChange],
        version: str,
        previous_version: Optional[str] = None,
    ) -> str:
        """
        Generate changelog from changes.

        Args:
            changes: List of code changes
            version: New version (e.g., "2.0.0")
            previous_version: Previous version (optional)

        Returns:
            Changelog in markdown format

        Example:
            changelog = await client.generate_changelog(
                changes=[...],
                version="2.0.0",
                previous_version="1.5.0"
            )

            print(changelog)
            # "## [2.0.0] - 2025-11-04
            #
            # ### Added
            # - OAuth 2.0 PKCE authentication flow
            # - Token refresh mechanism
            #
            # ### Changed
            # - Refactored authentication module
            #
            # ### Fixed
            # - Fixed timing attack vulnerability
            # ..."
        """
        changes_data = [
            {
                "file_path": c.file_path,
                "change_type": c.change_type,
                "lines_added": c.lines_added,
                "lines_deleted": c.lines_deleted,
                "description": c.description,
            }
            for c in changes
        ]

        payload = {
            "changes": changes_data,
            "version": version,
            "previous_version": previous_version,
        }

        session = await self._get_session()

        async with session.post(f"{self.url}/api/v1/changelog", json=payload) as response:
            if response.status != 200:
                raise Exception(f"NIS error {response.status}: {await response.text()}")

            data = await response.json()
            return data["changelog"]

    # ========================================================================
    # EXPLAIN CODE
    # ========================================================================

    async def explain_code(
        self,
        code: str,
        style: NarrativeStyle = NarrativeStyle.TUTORIAL,
    ) -> str:
        """
        Generate narrative explanation of code.

        Args:
            code: Code to explain
            style: Explanation style

        Returns:
            Narrative explanation

        Example:
            explanation = await client.explain_code(
                code=\"\"\"
                def authenticate(username, password):
                    user = User.query.filter_by(username=username).first()
                    if user and user.check_password(password):
                        return generate_token(user)
                    return None
                \"\"\",
                style=NarrativeStyle.TUTORIAL
            )

            print(explanation)
            # "This authentication function implements a secure login process:
            #
            # 1. **User Lookup**: First, we search for a user with the given username...
            # 2. **Password Verification**: If a user exists, we verify their password...
            # 3. **Token Generation**: Upon successful authentication, we generate..."
        """
        payload = {
            "code": code,
            "style": style.value,
        }

        session = await self._get_session()

        async with session.post(f"{self.url}/api/v1/explain", json=payload) as response:
            if response.status != 200:
                raise Exception(f"NIS error {response.status}: {await response.text()}")

            data = await response.json()
            return data["explanation"]

    # ========================================================================
    # HEALTH CHECK
    # ========================================================================

    async def health_check(self) -> bool:
        """
        Check if NIS is healthy.

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

class NISClientContext:
    """Context manager for NIS client"""

    def __init__(self, **kwargs):
        self.client = NISClient(**kwargs)

    async def __aenter__(self):
        return self.client

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.client.close()
