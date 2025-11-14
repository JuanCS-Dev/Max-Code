"""MABA Pydantic Models.

Request/response models for all MABA endpoints and internal data structures.

Author: Vértice Platform Team
License: Proprietary
"""

import os
from datetime import datetime
from enum import Enum
from typing import Any

# Day 3: Browser and Cognitive Map imports
from browser import BrowserController
from cognitive_map import CognitiveMapService
from db import get_db, init_db
from pydantic import BaseModel, Field, field_validator
from libs.common.maximus_integration import MaximusIntegrationMixin, RiskLevel, ToolCategory

# Shared library imports (work when in ~/vertice-dev/backend/services/)
from libs.common.subordinate_service import SubordinateServiceBase


class BrowserAction(str, Enum):
    """Supported browser actions."""

    NAVIGATE = "navigate"
    CLICK = "click"
    TYPE = "type"
    SCROLL = "scroll"
    SCREENSHOT = "screenshot"
    EXTRACT = "extract"
    WAIT = "wait"
    GO_BACK = "go_back"
    GO_FORWARD = "go_forward"
    REFRESH = "refresh"


class NavigationRequest(BaseModel):
    """Request to navigate to a URL."""

    url: str = Field(..., description="Target URL")
    wait_until: str = Field(
        default="networkidle",
        description="When to consider navigation complete (load, domcontentloaded, networkidle)",
    )
    timeout_ms: int = Field(
        default=30000, description="Navigation timeout in milliseconds"
    )

    @field_validator("url")
    @classmethod
    def validate_url(cls, v):
        """Validate URL format."""
        if not v.startswith(("http://", "https://")):
            raise ValueError("URL must start with http:// or https://")
        return v


class ClickRequest(BaseModel):
    """Request to click an element."""

    selector: str = Field(..., description="CSS selector for element to click")
    button: str = Field(
        default="left", description="Mouse button (left, right, middle)"
    )
    click_count: int = Field(default=1, description="Number of clicks")
    timeout_ms: int = Field(default=30000, description="Timeout in milliseconds")


class TypeRequest(BaseModel):
    """Request to type text into an element."""

    selector: str = Field(..., description="CSS selector for element")
    text: str = Field(..., description="Text to type")
    delay_ms: int = Field(
        default=0, description="Delay between key presses in milliseconds"
    )


class ScreenshotRequest(BaseModel):
    """Request to take a screenshot."""

    full_page: bool = Field(default=False, description="Capture full scrollable page")
    selector: str | None = Field(
        default=None, description="CSS selector to screenshot specific element"
    )
    format: str = Field(default="png", description="Image format (png, jpeg)")


class ExtractRequest(BaseModel):
    """Request to extract data from page."""

    selectors: dict[str, str] = Field(
        ..., description="Map of field names to CSS selectors"
    )
    extract_all: bool = Field(
        default=False, description="Extract all matching elements"
    )


class BrowserSessionRequest(BaseModel):
    """Request to create a new browser session."""

    headless: bool = Field(default=True, description="Run browser in headless mode")
    viewport_width: int = Field(default=1920, description="Viewport width")
    viewport_height: int = Field(default=1080, description="Viewport height")
    user_agent: str | None = Field(default=None, description="Custom user agent")


class BrowserActionRequest(BaseModel):
    """Generic browser action request."""

    action: BrowserAction = Field(..., description="Action to perform")
    parameters: dict[str, Any] = Field(
        default_factory=dict, description="Action parameters"
    )
    session_id: str | None = Field(default=None, description="Browser session ID")


class BrowserActionResponse(BaseModel):
    """Browser action response."""

    status: str = Field(..., description="Action status")
    result: dict[str, Any] | None = Field(default=None, description="Action result")
    error: str | None = Field(default=None, description="Error message if failed")
    execution_time_ms: float | None = Field(
        default=None, description="Execution time in milliseconds"
    )
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat())


class CognitiveMapQueryRequest(BaseModel):
    """Request to query the cognitive map."""

    domain: str | None = Field(
        default=None,
        description="Website domain (optional, can be inferred from URL in parameters)",
    )
    query_type: str = Field(
        ..., description="Query type (find_element, get_path, etc.)"
    )
    parameters: dict[str, Any] = Field(
        default_factory=dict, description="Query parameters"
    )


class CognitiveMapQueryResponse(BaseModel):
    """Cognitive map query response."""

    found: bool = Field(..., description="Whether result was found")
    result: dict[str, Any] | None = Field(default=None, description="Query result")
    confidence: float = Field(..., description="Confidence score 0-1")


class PageAnalysisRequest(BaseModel):
    """Request to analyze a page with LLM."""

    url: str | None = Field(
        default=None, description="URL to analyze (if not current page)"
    )
    analysis_type: str = Field(
        default="general",
        description="Type of analysis (general, form, navigation, data)",
    )
    instructions: str | None = Field(
        default=None, description="Specific instructions for analysis"
    )


class PageAnalysisResponse(BaseModel):
    """Page analysis response."""

    analysis: str = Field(..., description="LLM analysis result")
    structured_data: dict[str, Any] | None = Field(
        default=None, description="Structured extraction"
    )
    recommendations: list[str] = Field(
        default_factory=list, description="Recommended actions"
    )


class MABAService(SubordinateServiceBase, MaximusIntegrationMixin):
    """
    MABA (MAXIMUS Browser Agent) Service Implementation.

    This class integrates browser automation capabilities with MAXIMUS Core,
    providing autonomous web navigation, data extraction, and interaction.

    Attributes:
        browser_controller: Playwright browser controller
        cognitive_map: Graph-based learned website structure
    """

    def __init__(
        self,
        service_name: str,
        service_version: str,
        maximus_endpoint: str | None = None,
    ):
        """Initialize MABA service."""
        super().__init__(service_name, service_version, maximus_endpoint)

        self.browser_controller: BrowserController | None = None
        # Note: cognitive_map is created per-request with db session from get_db()

    async def initialize(self) -> bool:
        """
        Initialize MABA-specific resources.

        Day 3: Initialize database, browser controller, and register tools.

        Returns:
            True if initialization succeeded, False otherwise
        """
        try:
            # Day 3: Initialize database connection
            logger.info("🔌 Initializing database connection...")
            await init_db(create_tables=False)  # Use Alembic migrations, not create_all
            logger.info("✅ Database connection initialized")

            # Initialize browser controller
            logger.info("🌐 Initializing browser controller...")
            self.browser_controller = BrowserController()
            await self.browser_controller.initialize()
            logger.info("✅ Browser controller initialized")

            # Register tools with MAXIMUS
            tools = self._get_tool_manifest()
            await self.register_tools_with_maximus(tools)

            return True

        except Exception as e:
            logger.error(f"Failed to initialize MABA: {e}", exc_info=True)
            return False

    async def shutdown(self) -> None:
        """Shutdown MABA-specific resources.

        Day 3: Cleanup browser controller and database connections.
        """
        try:
            if self.browser_controller:
                await self.browser_controller.shutdown()
                logger.info("✅ Browser controller shut down")

            # Day 3: Close database connections
            from db.database import close_db
            await close_db()
            logger.info("✅ Database connections closed")

        except Exception as e:
            logger.error(f"Error during MABA shutdown: {e}")

    async def health_check(self) -> dict[str, Any]:
        """
        Perform MABA health checks.

        Day 3: Check browser controller and database connectivity.

        Returns:
            Dict with health status
        """
        base_health = await self.get_base_health_info()

        components = {}

        # Check browser controller
        if self.browser_controller:
            browser_health = await self.browser_controller.health_check()
            components["browser_controller"] = browser_health
        else:
            components["browser_controller"] = {"status": "not_initialized"}

        # Day 3: Check database connectivity
        try:
            from db.database import check_db_health
            db_health = await check_db_health()
            components["database"] = db_health
        except Exception as e:
            components["database"] = {"status": "unhealthy", "error": str(e)}

        base_health["components"] = components

        return base_health

    def _get_tool_manifest(self) -> list[dict[str, Any]]:
        """
        Get list of tools provided by MABA.

        Returns:
            List of tool definitions for MAXIMUS
        """
        return [
            self.create_tool_definition(
                name="navigate_url",
                description="Navigate browser to a specific URL",
                category=ToolCategory.BROWSER,
                parameters={
                    "url": {
                        "type": "string",
                        "required": True,
                        "description": "Target URL",
                    },
                    "wait_until": {
                        "type": "string",
                        "required": False,
                        "default": "networkidle",
                    },
                },
                handler=None,  # Handler is in routes.py
                risk_level=RiskLevel.LOW,
            ),
            self.create_tool_definition(
                name="click_element",
                description="Click an element on the current page",
                category=ToolCategory.BROWSER,
                parameters={
                    "selector": {
                        "type": "string",
                        "required": True,
                        "description": "CSS selector",
                    }
                },
                handler=None,
                risk_level=RiskLevel.MEDIUM,
            ),
            self.create_tool_definition(
                name="extract_data",
                description="Extract structured data from current page",
                category=ToolCategory.BROWSER,
                parameters={
                    "selectors": {
                        "type": "object",
                        "required": True,
                        "description": "Field to selector map",
                    }
                },
                handler=None,
                risk_level=RiskLevel.LOW,
            ),
            self.create_tool_definition(
                name="take_screenshot",
                description="Take screenshot of current page or element",
                category=ToolCategory.BROWSER,
                parameters={
                    "full_page": {
                        "type": "boolean",
                        "required": False,
                        "default": False,
                    }
                },
                handler=None,
                risk_level=RiskLevel.LOW,
            ),
            self.create_tool_definition(
                name="analyze_page",
                description="Analyze page content with LLM",
                category=ToolCategory.BROWSER,
                parameters={
                    "analysis_type": {
                        "type": "string",
                        "required": False,
                        "default": "general",
                    }
                },
                handler=None,
                risk_level=RiskLevel.LOW,
            ),
        ]


# Import logger
import logging

logger = logging.getLogger(__name__)
