"""Auto-Healing System for Failed Browser Actions.

Day 5: PENELOPE's healing touch - automatically fixes failed actions.

When a browser action fails, AutoHealer analyzes the failure and attempts
to find alternative approaches using Claude's intelligence.

Author: Vértice Platform Team
License: Proprietary
"""
import logging
from typing import Any, Dict, List, Optional

from .analyzer import PageAnalyzer
from .client import PenelopeClient

logger = logging.getLogger(__name__)


class AutoHealer:
    """Automatically heal failed browser actions.
    
    PENELOPE's resilience - when things break, she fixes them.
    Uses both local Claude analysis and PENELOPE service.
    """

    def __init__(
        self,
        analyzer: Optional[PageAnalyzer] = None,
        penelope_client: Optional[PenelopeClient] = None,
        max_heal_attempts: int = 3,
    ):
        """Initialize auto-healer.

        Args:
            analyzer: PageAnalyzer for local healing
            penelope_client: PenelopeClient for service-based healing
            max_heal_attempts: Maximum number of healing attempts per action
        """
        self.analyzer = analyzer or PageAnalyzer()
        self.penelope_client = penelope_client
        self.max_heal_attempts = max_heal_attempts
        
        self.healing_history: List[Dict[str, Any]] = []
        
        logger.info("🔧 AutoHealer initialized")

    async def heal_failed_action(
        self,
        failed_action: Dict[str, Any],
        error_message: str,
        page_html: Optional[str] = None,
        screenshot: Optional[str] = None,
        attempt: int = 1,
    ) -> Optional[Dict[str, Any]]:
        """Attempt to heal a failed browser action.

        Args:
            failed_action: The action that failed
            error_message: Error message from the failure
            page_html: Current page HTML
            screenshot: Current page screenshot
            attempt: Current healing attempt number

        Returns:
            Healed action to try, or None if healing failed

        Example failed_action:
            {
                "action": "click",
                "selector": "button.missing",
                "url": "https://example.com"
            }

        Example return:
            {
                "action": "click",
                "selector": "button[type='submit']",
                "healing_strategy": "alternative_selector",
                "confidence": 0.85,
                "reasoning": "Original selector not found, trying type attribute"
            }
        """
        if attempt > self.max_heal_attempts:
            logger.warning(
                f"⚠️ Max healing attempts ({self.max_heal_attempts}) reached"
            )
            return None

        logger.info(
            f"🔧 Healing attempt {attempt}/{self.max_heal_attempts} for failed {failed_action.get('action')}"
        )

        # Try PENELOPE service first (if available)
        if self.penelope_client:
            try:
                healed = await self._heal_with_penelope(
                    failed_action, error_message, page_html, screenshot
                )
                if healed:
                    return healed
            except Exception as e:
                logger.warning(f"⚠️ PENELOPE healing failed: {e}, trying local")

        # Fall back to local Claude-based healing
        healed = await self._heal_locally(
            failed_action, error_message, page_html, screenshot
        )

        # Record healing attempt
        self.healing_history.append(
            {
                "failed_action": failed_action,
                "error": error_message,
                "healed_action": healed,
                "attempt": attempt,
                "success": healed is not None,
            }
        )

        return healed

    async def _heal_with_penelope(
        self,
        failed_action: Dict[str, Any],
        error_message: str,
        page_html: Optional[str],
        screenshot: Optional[str],
    ) -> Optional[Dict[str, Any]]:
        """Heal using PENELOPE service.

        Args:
            failed_action: Failed action
            error_message: Error message
            page_html: Page HTML
            screenshot: Screenshot

        Returns:
            Healed action or None
        """
        try:
            result = await self.penelope_client.auto_heal(
                failed_action=failed_action,
                error_message=error_message,
                page_html=page_html,
                screenshot=screenshot,
            )

            if result.get("healed"):
                logger.info("✅ PENELOPE healed the action")
                return result.get("alternative_action")
            else:
                logger.warning("⚠️ PENELOPE could not heal action")
                return None

        except Exception as e:
            logger.error(f"❌ PENELOPE healing error: {e}")
            return None

    async def _heal_locally(
        self,
        failed_action: Dict[str, Any],
        error_message: str,
        page_html: Optional[str],
        screenshot: Optional[str],
    ) -> Optional[Dict[str, Any]]:
        """Heal using local Claude analysis.

        Args:
            failed_action: Failed action
            error_message: Error message
            page_html: Page HTML
            screenshot: Screenshot

        Returns:
            Healed action or None
        """
        action_type = failed_action.get("action")
        selector = failed_action.get("selector")

        # Different healing strategies based on error
        if "not found" in error_message.lower() or "timeout" in error_message.lower():
            # Element not found - try to find alternative selectors
            return await self._heal_selector_not_found(
                action_type, selector, page_html, screenshot
            )

        elif "clickable" in error_message.lower():
            # Element not clickable - suggest waiting or scrolling
            return {
                "action": "wait",
                "duration_ms": 1000,
                "healing_strategy": "wait_before_action",
                "confidence": 0.7,
                "reasoning": "Element may need time to become interactive",
                "then_retry": failed_action,
            }

        elif "visible" in error_message.lower():
            # Element not visible - try scrolling
            return {
                "action": "scroll",
                "selector": selector,
                "healing_strategy": "scroll_to_element",
                "confidence": 0.75,
                "reasoning": "Element may be off-screen",
                "then_retry": failed_action,
            }

        else:
            logger.warning(f"⚠️ Unknown error type: {error_message}")
            return None

    async def _heal_selector_not_found(
        self,
        action_type: str,
        failed_selector: str,
        page_html: Optional[str],
        screenshot: Optional[str],
    ) -> Optional[Dict[str, Any]]:
        """Heal selector not found errors.

        Args:
            action_type: Type of action (click, type, etc.)
            failed_selector: Selector that didn't work
            page_html: Page HTML
            screenshot: Screenshot

        Returns:
            Healed action with alternative selector
        """
        if not page_html:
            logger.warning("⚠️ Cannot heal without HTML")
            return None

        try:
            # Infer what element user was trying to interact with
            element_description = self._infer_element_description(
                action_type, failed_selector
            )

            # Ask Claude for alternative selectors
            alternative_selectors = await self.analyzer.suggest_selectors(
                html=page_html,
                element_description=element_description,
            )

            if alternative_selectors:
                # Try first alternative
                best_alternative = alternative_selectors[0]
                
                logger.info(
                    f"🔧 Healing selector: {failed_selector} → {best_alternative}"
                )

                return {
                    "action": action_type,
                    "selector": best_alternative,
                    "healing_strategy": "alternative_selector",
                    "confidence": 0.8,
                    "reasoning": f"Original selector not found. Trying: {best_alternative}",
                    "alternatives": alternative_selectors[1:],  # Backup options
                }
            else:
                logger.warning("⚠️ No alternative selectors found")
                return None

        except Exception as e:
            logger.error(f"❌ Selector healing failed: {e}")
            return None

    def _infer_element_description(
        self, action_type: str, selector: str
    ) -> str:
        """Infer what element the user was looking for.

        Args:
            action_type: Type of action
            selector: Failed selector

        Returns:
            Human-readable description of element
        """
        # Extract hints from selector
        if "submit" in selector.lower():
            return f"{action_type} submit button"
        elif "login" in selector.lower():
            return f"{action_type} login button"
        elif "button" in selector.lower():
            return f"{action_type} button"
        elif "input" in selector.lower():
            return f"{action_type} input field"
        elif "form" in selector.lower():
            return f"{action_type} form"
        elif "link" in selector.lower() or selector.startswith("a"):
            return f"{action_type} link"
        else:
            # Generic description
            return f"{action_type} element matching {selector}"

    def get_healing_stats(self) -> Dict[str, Any]:
        """Get statistics about healing attempts.

        Returns:
            Healing statistics

        Example:
            {
                "total_attempts": 15,
                "successful": 12,
                "failed": 3,
                "success_rate": 0.8,
                "most_common_errors": ["selector not found", "timeout"]
            }
        """
        if not self.healing_history:
            return {
                "total_attempts": 0,
                "successful": 0,
                "failed": 0,
                "success_rate": 0.0,
            }

        total = len(self.healing_history)
        successful = sum(1 for h in self.healing_history if h["success"])
        failed = total - successful

        return {
            "total_attempts": total,
            "successful": successful,
            "failed": failed,
            "success_rate": successful / total if total > 0 else 0.0,
            "average_attempts": sum(h["attempt"] for h in self.healing_history) / total,
        }

    async def close(self):
        """Close analyzer and client."""
        if self.analyzer:
            await self.analyzer.close()
        if self.penelope_client:
            await self.penelope_client.close()
        logger.info("🔧 AutoHealer closed")
