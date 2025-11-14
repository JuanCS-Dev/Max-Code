"""PENELOPE Client for MABA Integration.

Day 5: Communication bridge between MABA and PENELOPE service.

Enables MABA to request intelligent analysis and decision-making
from PENELOPE's Claude-powered reasoning engine.

Author: Vértice Platform Team
License: Proprietary
"""
import logging
import os
from typing import Any, Dict, List, Optional

import httpx
from httpx import AsyncClient, Timeout

logger = logging.getLogger(__name__)


class PenelopeClient:
    """Client for communicating with PENELOPE service.
    
    PENELOPE provides:
    - Intelligent page analysis
    - Vision-based screenshot understanding
    - Decision-making for navigation
    - Auto-healing suggestions
    - Reasoning about web structure
    """

    def __init__(
        self,
        penelope_url: Optional[str] = None,
        timeout: int = 30,
        api_key: Optional[str] = None,
    ):
        """Initialize PENELOPE client.

        Args:
            penelope_url: URL of PENELOPE service
            timeout: Request timeout in seconds
            api_key: Optional API key for authentication
        """
        self.penelope_url = penelope_url or os.getenv(
            "PENELOPE_URL", "http://vertice-penelope-service:8153"
        )
        self.timeout = Timeout(timeout)
        self.api_key = api_key or os.getenv("PENELOPE_API_KEY")
        
        # Initialize HTTP client
        headers = {}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        
        self.client = AsyncClient(
            base_url=self.penelope_url,
            timeout=self.timeout,
            headers=headers,
        )

        logger.info(f"🧠 PENELOPE client initialized: {self.penelope_url}")

    async def analyze_page(
        self,
        html: Optional[str] = None,
        url: Optional[str] = None,
        screenshot: Optional[str] = None,
        analysis_type: str = "general",
        instructions: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Request PENELOPE to analyze a page.

        Args:
            html: Page HTML content
            url: Page URL
            screenshot: Base64 encoded screenshot
            analysis_type: Type of analysis (general, form, navigation, data)
            instructions: Specific analysis instructions

        Returns:
            Analysis results from PENELOPE

        Raises:
            httpx.HTTPError: If request fails
        """
        payload = {
            "html": html,
            "url": url,
            "screenshot": screenshot,
            "analysis_type": analysis_type,
            "instructions": instructions,
        }

        try:
            response = await self.client.post(
                "/api/v1/analyze/page",
                json=payload,
            )
            response.raise_for_status()
            result = response.json()
            
            logger.info(f"✅ PENELOPE analyzed page: {url}")
            return result

        except httpx.HTTPError as e:
            logger.error(f"❌ PENELOPE analysis failed: {e}")
            raise

    async def suggest_action(
        self,
        current_url: str,
        goal: str,
        page_html: Optional[str] = None,
        screenshot: Optional[str] = None,
        previous_actions: Optional[List[Dict]] = None,
    ) -> Dict[str, Any]:
        """Ask PENELOPE to suggest next browser action.

        Args:
            current_url: Current page URL
            goal: User's goal or task
            page_html: Current page HTML
            screenshot: Current page screenshot
            previous_actions: History of actions taken

        Returns:
            Suggested action with confidence score

        Example response:
            {
                "action": "click",
                "selector": "button.login",
                "reasoning": "Login button is visible and required for goal",
                "confidence": 0.95
            }
        """
        if not current_url:
            raise ValueError("current_url is required")
        if not goal:
            raise ValueError("goal is required")

        payload = {
            "current_url": current_url,
            "goal": goal,
            "page_html": page_html,
            "screenshot": screenshot,
            "previous_actions": previous_actions or [],
        }

        try:
            response = await self.client.post(
                "/api/v1/suggest/action",
                json=payload,
            )
            response.raise_for_status()
            result = response.json()
            
            logger.info(
                f"🎯 PENELOPE suggested: {result.get('action')} on {result.get('selector')}"
            )
            return result

        except httpx.HTTPError as e:
            logger.error(f"❌ PENELOPE suggestion failed: {e}")
            raise

    async def auto_heal(
        self,
        failed_action: Dict[str, Any],
        error_message: str,
        page_html: Optional[str] = None,
        screenshot: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Request PENELOPE to suggest healing for failed action.

        Args:
            failed_action: The action that failed
            error_message: Error message from failure
            page_html: Current page HTML
            screenshot: Current page screenshot

        Returns:
            Healing suggestion with alternative approach

        Example response:
            {
                "healed": true,
                "alternative_action": {
                    "action": "click",
                    "selector": "button[type='submit']",
                    "reasoning": "Original selector not found, trying type attribute"
                },
                "confidence": 0.85
            }
        """
        if not failed_action or not isinstance(failed_action, dict):
            raise ValueError("failed_action must be a dictionary")
        if not error_message:
            raise ValueError("error_message is required")

        payload = {
            "failed_action": failed_action,
            "error_message": error_message,
            "page_html": page_html,
            "screenshot": screenshot,
        }

        try:
            response = await self.client.post(
                "/api/v1/heal/action",
                json=payload,
            )
            response.raise_for_status()
            result = response.json()
            
            if result.get("healed"):
                logger.info(f"🔧 PENELOPE healed failed action")
            else:
                logger.warning(f"⚠️ PENELOPE could not heal action")
            
            return result

        except httpx.HTTPError as e:
            logger.error(f"❌ PENELOPE healing failed: {e}")
            raise

    async def extract_structured_data(
        self,
        html: str,
        url: str,
        schema: Dict[str, str],
        screenshot: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Request PENELOPE to extract structured data using LLM.

        Args:
            html: Page HTML
            url: Page URL
            schema: Expected data schema
            screenshot: Optional screenshot for vision

        Returns:
            Extracted structured data

        Example schema:
            {
                "title": "Main page title",
                "price": "Product price",
                "availability": "Stock status"
            }
        """
        if not html:
            raise ValueError("html is required")
        if not url:
            raise ValueError("url is required")
        if not schema or not isinstance(schema, dict):
            raise ValueError("schema must be a dictionary")

        payload = {
            "html": html,
            "url": url,
            "schema": schema,
            "screenshot": screenshot,
        }

        try:
            response = await self.client.post(
                "/api/v1/extract/structured",
                json=payload,
            )
            response.raise_for_status()
            result = response.json()
            
            logger.info(f"📊 PENELOPE extracted data from {url}")
            return result

        except httpx.HTTPError as e:
            logger.error(f"❌ PENELOPE extraction failed: {e}")
            raise

    async def health_check(self) -> Dict[str, Any]:
        """Check PENELOPE service health.

        Returns:
            Health status

        Raises:
            httpx.HTTPError: If PENELOPE is unreachable
        """
        try:
            response = await self.client.get("/health")
            response.raise_for_status()
            return response.json()

        except httpx.HTTPError as e:
            logger.error(f"❌ PENELOPE health check failed: {e}")
            raise

    async def close(self):
        """Close the HTTP client."""
        await self.client.aclose()
        logger.info("🧠 PENELOPE client closed")

    async def __aenter__(self):
        """Async context manager entry."""
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self.close()
