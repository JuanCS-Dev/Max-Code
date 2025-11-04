"""
Penelope Service Client

Interfaces with Penelope NLP Service for:
- 7 Biblical Articles governance (Christian principles)
- Sabbath observance (rest and reflection)
- Healing and wellness (autonomous healing)
- Wisdom base (historical precedent learning)
- Ethical reasoning

PRODUCTION IMPLEMENTATION

The 7 Biblical Articles:
1. Love God (Agape Dei)
2. Love Neighbor (Agape Neighbor)
3. Seek Truth (Veritas)
4. Pursue Justice (Justitia)
5. Practice Mercy (Misericordia)
6. Walk Humbly (Humilitas)
7. Steward Creation (Oikonomia)
"""

from typing import Dict, Any, Optional, List
from integration.base_client import BaseServiceClient, ServiceResponse


class PenelopeClient(BaseServiceClient):
    """
    Client for Penelope NLP Service.

    PENELOPE = Christian Autonomous Healing Service
    Provides ethical governance through 7 Biblical Articles,
    Sabbath observance, and wisdom-based reasoning.
    """

    def __init__(self, base_url: str, timeout: int = 30, max_retries: int = 3):
        """
        Initialize Penelope client.

        Args:
            base_url: Penelope service URL
            timeout: Request timeout in seconds
            max_retries: Maximum retry attempts
        """
        super().__init__(base_url, "Penelope", timeout, max_retries)

    # ========================================================================
    # 7 BIBLICAL ARTICLES
    # ========================================================================

    def evaluate_against_articles(self, action: Dict[str, Any]) -> ServiceResponse:
        """
        Evaluate action against 7 Biblical Articles.

        Articles:
        1. Agape Dei - Love God (worship, devotion)
        2. Agape Neighbor - Love Neighbor (compassion, service)
        3. Veritas - Seek Truth (honesty, integrity)
        4. Justitia - Pursue Justice (fairness, righteousness)
        5. Misericordia - Practice Mercy (forgiveness, grace)
        6. Humilitas - Walk Humbly (humility, meekness)
        7. Oikonomia - Steward Creation (responsibility, care)

        Args:
            action: Action to evaluate with 'description' and optional 'context'

        Returns:
            ServiceResponse with article compliance scores
        """
        payload = {
            "action": action.get("description", ""),
            "context": action.get("context", {})
        }
        return self.post("/api/governance/evaluate", json=payload)

    def get_article_guidance(self, article_number: int) -> ServiceResponse:
        """
        Get guidance for specific Biblical Article.

        Args:
            article_number: Article number (1-7)

        Returns:
            ServiceResponse with article guidance and principles
        """
        if not 1 <= article_number <= 7:
            return ServiceResponse(
                success=False,
                error=f"Invalid article number: {article_number}. Must be 1-7."
            )
        return self.get(f"/api/governance/articles/{article_number}")

    def get_all_articles(self) -> ServiceResponse:
        """
        Get all 7 Biblical Articles with their principles.

        Returns:
            ServiceResponse with complete articles documentation
        """
        return self.get("/api/governance/articles")

    # ========================================================================
    # SABBATH OBSERVANCE
    # ========================================================================

    def check_sabbath_status(self) -> ServiceResponse:
        """
        Check if Sabbath mode is active (Sunday in UTC).

        Sabbath Protocol:
        - No autonomous patches deployed
        - Only observation and reflection
        - Emergency override available for critical issues

        Returns:
            ServiceResponse with Sabbath status and next Sabbath time
        """
        return self.get("/api/sabbath/status")

    def is_sabbath(self) -> bool:
        """
        Quick check if currently in Sabbath mode.

        Returns:
            True if Sabbath active
        """
        response = self.check_sabbath_status()
        if response.success and response.data:
            return response.data.get("is_sabbath", False)
        return False

    # ========================================================================
    # HEALING & WELLNESS
    # ========================================================================

    def request_healing(self, anomaly: Dict[str, Any]) -> ServiceResponse:
        """
        Request autonomous healing for system anomaly.

        Args:
            anomaly: Anomaly details with 'description', 'severity', 'metrics'

        Returns:
            ServiceResponse with healing plan and diagnosis
        """
        return self.post("/api/healing/request", json=anomaly)

    def get_healing_history(self, limit: int = 10) -> ServiceResponse:
        """
        Get recent healing interventions.

        Args:
            limit: Maximum number of records

        Returns:
            ServiceResponse with healing history
        """
        return self.get(f"/api/healing/history?limit={limit}")

    # ========================================================================
    # WISDOM BASE
    # ========================================================================

    def query_wisdom(self, question: str, context: Optional[Dict[str, Any]] = None) -> ServiceResponse:
        """
        Query wisdom base for historical precedent.

        The wisdom base learns from past decisions and outcomes,
        providing guidance based on accumulated experience.

        Args:
            question: Question to ask wisdom base
            context: Optional context for query

        Returns:
            ServiceResponse with wisdom insights
        """
        payload = {
            "question": question,
            "context": context or {}
        }
        return self.post("/api/wisdom/query", json=payload)

    def add_wisdom_entry(self, lesson: Dict[str, Any]) -> ServiceResponse:
        """
        Add lesson/experience to wisdom base.

        Args:
            lesson: Dict with 'situation', 'action', 'outcome', 'learning'

        Returns:
            ServiceResponse with confirmation
        """
        return self.post("/api/wisdom/add", json=lesson)

    def get_wisdom_stats(self) -> ServiceResponse:
        """
        Get wisdom base statistics.

        Returns:
            ServiceResponse with wisdom base metrics
        """
        return self.get("/api/wisdom/stats")

    # ========================================================================
    # METRICS & MONITORING
    # ========================================================================

    def get_governance_metrics(self) -> ServiceResponse:
        """
        Get governance metrics (7 Articles compliance).

        Returns:
            ServiceResponse with governance metrics
        """
        return self.get("/metrics")

    def get_service_health(self) -> ServiceResponse:
        """
        Get Penelope service health.

        Returns:
            ServiceResponse with health status
        """
        return self.get("/health")

    # ========================================================================
    # INTEGRATION HELPERS
    # ========================================================================

    def evaluate_code_action(self, action_description: str, code_context: Optional[str] = None) -> ServiceResponse:
        """
        Evaluate a code-related action against Biblical Articles.

        Convenience method for code generation/modification evaluation.

        Args:
            action_description: Description of the code action
            code_context: Optional code context

        Returns:
            ServiceResponse with ethical evaluation
        """
        action = {
            "description": action_description,
            "context": {
                "domain": "code",
                "code_context": code_context
            }
        }
        return self.evaluate_against_articles(action)

    def can_perform_action(self, action_description: str) -> bool:
        """
        Quick check if action is ethically permissible.

        Args:
            action_description: Description of action

        Returns:
            True if action passes ethical checks
        """
        # Don't allow actions during Sabbath (unless emergency)
        if self.is_sabbath() and "emergency" not in action_description.lower():
            return False

        # Evaluate against articles
        response = self.evaluate_against_articles({"description": action_description})
        if response.success and response.data:
            # Check if any article has critical violations
            scores = response.data.get("scores", {})
            return all(score >= 0.5 for score in scores.values())

        return False  # Fail closed on errors
