"""Page Analyzer with Claude Vision.

Day 5: Direct Claude API integration for intelligent page analysis.

Uses Claude Sonnet with vision to analyze screenshots and HTML,
providing intelligent insights about web pages.

Author: Vértice Platform Team
License: Proprietary
"""
import base64
import logging
import os
from typing import Any, Dict, List, Optional

from anthropic import Anthropic, AsyncAnthropic

logger = logging.getLogger(__name__)


class PageAnalyzer:
    """Analyze web pages using Claude's vision and reasoning.
    
    PENELOPE's eyes and mind - sees screenshots, understands structure,
    and provides intelligent analysis of web pages.
    """

    def __init__(self, api_key: Optional[str] = None):
        """Initialize page analyzer with Claude API.

        Args:
            api_key: Anthropic API key (or from ANTHROPIC_API_KEY env)
        """
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        
        if not self.api_key:
            logger.warning("⚠️ No Anthropic API key provided - analyzer disabled")
            self.client = None
        else:
            self.client = AsyncAnthropic(api_key=self.api_key)
            logger.info("🧠 PENELOPE PageAnalyzer initialized with Claude")

    async def analyze_screenshot(
        self,
        screenshot_b64: str,
        url: str,
        question: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Analyze a page screenshot with Claude vision.

        Args:
            screenshot_b64: Base64 encoded screenshot
            url: Page URL for context
            question: Specific question about the page

        Returns:
            Analysis results with insights

        Example:
            {
                "analysis": "This is a login page with email/password fields...",
                "elements_found": ["email input", "password input", "submit button"],
                "suggested_actions": ["Fill email", "Fill password", "Click submit"],
                "confidence": 0.95
            }
        """
        if not self.client:
            raise ValueError("Anthropic API key not configured")

        # Build prompt
        prompt = f"Analyze this screenshot from {url}."
        if question:
            prompt += f"\n\nSpecific question: {question}"
        else:
            prompt += """

Please provide:
1. What type of page is this? (login, form, dashboard, article, etc.)
2. What interactive elements are visible? (buttons, links, forms, etc.)
3. What actions can a user take on this page?
4. Any notable patterns or UI elements?

Be concise but thorough."""

        try:
            # Call Claude with vision
            message = await self.client.messages.create(
                model="claude-sonnet-4-5-20250929",  # Latest Sonnet with vision
                max_tokens=2000,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "image",
                                "source": {
                                    "type": "base64",
                                    "media_type": "image/png",
                                    "data": screenshot_b64,
                                },
                            },
                            {
                                "type": "text",
                                "text": prompt,
                            },
                        ],
                    }
                ],
            )

            analysis_text = message.content[0].text

            logger.info(f"👁️ Analyzed screenshot of {url}")

            return {
                "analysis": analysis_text,
                "model": "claude-sonnet-4-5",
                "url": url,
                "confidence": 0.9,  # High confidence with Claude vision
            }

        except Exception as e:
            logger.error(f"❌ Screenshot analysis failed: {e}")
            raise

    async def analyze_html_structure(
        self,
        html: str,
        url: str,
        goal: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Analyze HTML structure to find interaction points.

        Args:
            html: Page HTML content
            url: Page URL
            goal: Optional user goal to guide analysis

        Returns:
            Structured analysis of HTML

        Example:
            {
                "forms": [{"action": "/login", "fields": ["email", "password"]}],
                "buttons": [{"text": "Submit", "selector": "button[type='submit']"}],
                "links": [{"text": "Register", "href": "/register"}],
                "recommendations": ["Fill login form", "Click submit button"]
            }
        """
        if not self.client:
            raise ValueError("Anthropic API key not configured")

        # Truncate HTML if too long (Claude has token limits)
        html_truncated = html[:50000] if len(html) > 50000 else html

        prompt = f"""Analyze this HTML from {url}.

<html>
{html_truncated}
</html>
"""

        if goal:
            prompt += f"\n\nUser goal: {goal}"
            prompt += "\n\nBased on the goal, what elements should the user interact with?"
        else:
            prompt += """

Please identify:
1. All forms and their fields
2. All interactive buttons
3. All navigation links
4. Any data that could be extracted

Provide a structured analysis."""

        try:
            message = await self.client.messages.create(
                model="claude-sonnet-4-5-20250929",
                max_tokens=3000,
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
            )

            analysis_text = message.content[0].text

            logger.info(f"🔍 Analyzed HTML structure of {url}")

            return {
                "analysis": analysis_text,
                "model": "claude-sonnet-4-5",
                "url": url,
                "html_length": len(html),
            }

        except Exception as e:
            logger.error(f"❌ HTML analysis failed: {e}")
            raise

    async def suggest_selectors(
        self,
        html: str,
        element_description: str,
    ) -> List[str]:
        """Ask Claude to suggest CSS selectors for an element.

        Args:
            html: Page HTML
            element_description: Description of element to find

        Returns:
            List of suggested CSS selectors, ordered by confidence

        Example:
            element_description="login button"
            returns: ["button.login", "button[type='submit']", "#login-btn"]
        """
        if not self.client:
            raise ValueError("Anthropic API key not configured")

        html_truncated = html[:30000] if len(html) > 30000 else html

        prompt = f"""Given this HTML, suggest CSS selectors to find: {element_description}

<html>
{html_truncated}
</html>

Provide 3-5 CSS selectors that might match this element, ordered by confidence.
Format as a simple list, one per line.
Only provide the selectors, no explanation."""

        try:
            message = await self.client.messages.create(
                model="claude-sonnet-4-5-20250929",
                max_tokens=500,
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
            )

            # Parse selectors from response
            response_text = message.content[0].text
            selectors = [
                line.strip()
                for line in response_text.split("\n")
                if line.strip() and not line.strip().startswith("#")
            ]

            logger.info(
                f"🎯 Suggested {len(selectors)} selectors for '{element_description}'"
            )

            return selectors

        except Exception as e:
            logger.error(f"❌ Selector suggestion failed: {e}")
            raise

    async def extract_with_llm(
        self,
        html: str,
        schema: Dict[str, str],
    ) -> Dict[str, Any]:
        """Use Claude to extract structured data from HTML.

        Args:
            html: Page HTML
            schema: Schema describing what to extract

        Returns:
            Extracted data matching schema

        Example:
            schema = {"title": "Product title", "price": "Price in dollars"}
            returns: {"title": "Cool Product", "price": "$99.99"}
        """
        if not self.client:
            raise ValueError("Anthropic API key not configured")

        html_truncated = html[:40000] if len(html) > 40000 else html

        schema_desc = "\n".join([f"- {key}: {desc}" for key, desc in schema.items()])

        prompt = f"""Extract the following information from this HTML:

{schema_desc}

<html>
{html_truncated}
</html>

Provide the extracted data as a JSON object with the exact keys from the schema.
If a field is not found, use null.

Example format:
{{"title": "value", "price": "value"}}

Only respond with the JSON object, no other text."""

        try:
            message = await self.client.messages.create(
                model="claude-sonnet-4-5-20250929",
                max_tokens=2000,
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
            )

            # Parse JSON from response
            import json

            response_text = message.content[0].text
            # Try to extract JSON from response
            try:
                extracted_data = json.loads(response_text)
            except json.JSONDecodeError:
                # Try to find JSON in response
                import re

                json_match = re.search(r"\{.*\}", response_text, re.DOTALL)
                if json_match:
                    extracted_data = json.loads(json_match.group())
                else:
                    raise ValueError("Could not parse JSON from Claude response")

            logger.info(f"📊 Extracted {len(extracted_data)} fields with Claude")

            return extracted_data

        except Exception as e:
            logger.error(f"❌ LLM extraction failed: {e}")
            raise

    async def close(self):
        """Close the Claude client."""
        if self.client:
            await self.client.close()
            logger.info("🧠 PageAnalyzer closed")
