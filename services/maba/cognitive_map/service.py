"""MABA Cognitive Map Service.

Day 3: Learn from browser interactions and build knowledge graph.

The CognitiveMap learns from every browser action, storing:
- Successful element selectors for each page
- Navigation paths between URLs
- Page importance based on visit frequency and success rate
- Recommended actions based on historical patterns

This enables MABA to get smarter over time, learning which selectors work
and which navigation paths are most reliable.

Constitution Compliance:
- P1 (Completude): Complete learning from all browser actions
- P2 (Validação): Validate patterns before recommendations
- P4 (Rastreabilidade): Full audit trail of learned patterns
- P5 (Consciência Sistêmica): Continuous improvement from feedback

Author: Vértice Platform Team
License: Proprietary
"""
import hashlib
import logging
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

from sqlalchemy import and_, desc, func, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from ..db.models import BrowserAction, CognitiveMapPage, NavigationPath

logger = logging.getLogger(__name__)

# ============================================================================
# COGNITIVE MAP SERVICE
# ============================================================================


class CognitiveMapService:
    """Service for learning from browser interactions and building knowledge."""

    def __init__(self, db: AsyncSession):
        """Initialize cognitive map service.

        Args:
            db: Async database session
        """
        self.db = db

    # ========================================================================
    # PAGE LEARNING
    # ========================================================================

    async def learn_from_action(
        self,
        action: BrowserAction,
        elements_snapshot: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Learn from a browser action and update cognitive map.

        Args:
            action: BrowserAction that was just logged
            elements_snapshot: Optional snapshot of page elements

        This method is called after each browser action to:
        1. Update page visit count and timestamps
        2. Store successful element selectors
        3. Update navigation paths
        4. Recalculate page importance
        """
        if not action.url:
            return  # Can't learn from actions without URL

        url_hash = CognitiveMapPage.hash_url(action.url)

        # Get or create cognitive map page
        page = await self._get_or_create_page(action.url, url_hash)

        # Update visit count and timestamp
        page.visited_count += 1
        page.last_visited = datetime.utcnow()

        # Update page title if available
        if elements_snapshot and "title" in elements_snapshot:
            page.title = elements_snapshot["title"]

        # Learn from successful actions
        if action.success and action.selector:
            await self._learn_selector(page, action)

        # Store elements snapshot if provided
        if elements_snapshot:
            await self._update_elements_snapshot(page, elements_snapshot)

        # Recalculate importance score
        await self._recalculate_importance(page)

        await self.db.commit()
        logger.debug(f"✅ Learned from action {action.action_type} on {action.url}")

    async def _get_or_create_page(
        self, url: str, url_hash: str
    ) -> CognitiveMapPage:
        """Get existing page or create new one.

        Args:
            url: Full URL
            url_hash: SHA256 hash of URL

        Returns:
            CognitiveMapPage instance
        """
        # Try to get existing page
        result = await self.db.execute(
            select(CognitiveMapPage).where(CognitiveMapPage.url_hash == url_hash)
        )
        page = result.scalar_one_or_none()

        if page is None:
            # Create new page
            # Extract domain from URL
            from urllib.parse import urlparse

            parsed = urlparse(url)
            domain = parsed.netloc

            page = CognitiveMapPage(
                url=url,
                url_hash=url_hash,
                domain=domain,
                visited_count=0,
                importance_score=0.0,
            )
            self.db.add(page)
            await self.db.flush()  # Get the ID
            logger.info(f"📍 New page added to cognitive map: {url}")

        return page

    async def _learn_selector(
        self, page: CognitiveMapPage, action: BrowserAction
    ) -> None:
        """Learn a successful selector for a page element.

        Args:
            page: CognitiveMapPage being updated
            action: Successful BrowserAction with selector

        Stores selectors in the format:
        {
            "selectors": {
                "action_type": {
                    "selector": {
                        "count": 5,
                        "last_used": "2025-11-14T...",
                        "avg_duration_ms": 150
                    }
                }
            }
        }
        """
        if not page.elements_snapshot:
            page.elements_snapshot = {"selectors": {}}

        selectors = page.elements_snapshot.get("selectors", {})

        # Organize by action type
        if action.action_type not in selectors:
            selectors[action.action_type] = {}

        action_selectors = selectors[action.action_type]

        # Update or create selector entry
        if action.selector not in action_selectors:
            action_selectors[action.selector] = {
                "count": 0,
                "last_used": None,
                "avg_duration_ms": 0,
            }

        selector_data = action_selectors[action.selector]
        selector_data["count"] += 1
        selector_data["last_used"] = datetime.utcnow().isoformat()

        # Update average duration
        if action.duration_ms:
            current_avg = selector_data["avg_duration_ms"]
            count = selector_data["count"]
            new_avg = ((current_avg * (count - 1)) + action.duration_ms) / count
            selector_data["avg_duration_ms"] = int(new_avg)

        page.elements_snapshot["selectors"] = selectors
        logger.debug(f"📚 Learned selector '{action.selector}' for {action.action_type}")

    async def _update_elements_snapshot(
        self, page: CognitiveMapPage, elements_snapshot: Dict[str, Any]
    ) -> None:
        """Update page elements snapshot with new data.

        Args:
            page: CognitiveMapPage being updated
            elements_snapshot: New elements data to merge
        """
        if not page.elements_snapshot:
            page.elements_snapshot = {}

        # Merge new snapshot data (preserve existing selectors)
        for key, value in elements_snapshot.items():
            if key != "selectors":  # Don't overwrite learned selectors
                page.elements_snapshot[key] = value

    async def _recalculate_importance(self, page: CognitiveMapPage) -> None:
        """Recalculate page importance score based on multiple factors.

        Importance score (0-100) considers:
        - Visit frequency (higher = more important)
        - Recency of visits (recent = more important)
        - Success rate of actions (higher = more important)
        - Number of learned selectors (more = more important)

        Args:
            page: CognitiveMapPage to score
        """
        score = 0.0

        # Factor 1: Visit frequency (0-40 points)
        # Normalize visit count (cap at 100 visits = 40 points)
        visit_score = min(page.visited_count / 100 * 40, 40)
        score += visit_score

        # Factor 2: Recency (0-20 points)
        # Pages visited in last 24h get full points, decay over 30 days
        if page.last_visited:
            hours_since_visit = (datetime.utcnow() - page.last_visited).total_seconds() / 3600
            recency_score = max(20 - (hours_since_visit / 24 * 20 / 30), 0)
            score += recency_score

        # Factor 3: Success rate (0-20 points)
        # Get success rate from recent actions
        success_rate = await self._get_page_success_rate(page.url_hash)
        score += success_rate * 20

        # Factor 4: Learned selectors (0-20 points)
        # More learned selectors = better understanding of page
        if page.elements_snapshot and "selectors" in page.elements_snapshot:
            selector_count = sum(
                len(selectors)
                for selectors in page.elements_snapshot["selectors"].values()
            )
            selector_score = min(selector_count / 10 * 20, 20)  # Cap at 10 selectors
            score += selector_score

        page.importance_score = round(score, 2)
        logger.debug(f"📊 Page importance: {page.importance_score}/100 ({page.url})")

    async def _get_page_success_rate(self, url_hash: str) -> float:
        """Get success rate for actions on a specific page.

        Args:
            url_hash: SHA256 hash of page URL

        Returns:
            Success rate as float (0.0 to 1.0)
        """
        # Get page URL from hash
        result = await self.db.execute(
            select(CognitiveMapPage.url).where(CognitiveMapPage.url_hash == url_hash)
        )
        url = result.scalar_one_or_none()

        if not url:
            return 0.0

        # Count successful and total actions for this URL
        total_result = await self.db.execute(
            select(func.count()).where(BrowserAction.url == url)
        )
        total = total_result.scalar_one()

        if total == 0:
            return 0.0

        success_result = await self.db.execute(
            select(func.count()).where(
                and_(BrowserAction.url == url, BrowserAction.success == True)
            )
        )
        successful = success_result.scalar_one()

        return successful / total

    # ========================================================================
    # NAVIGATION PATH LEARNING
    # ========================================================================

    async def learn_navigation_path(
        self,
        from_url: str,
        to_url: str,
        actions: List[Dict[str, Any]],
        success: bool,
        duration_ms: int,
    ) -> None:
        """Learn a navigation path between two pages.

        Args:
            from_url: Starting URL
            to_url: Destination URL
            actions: List of actions taken to navigate
            success: Whether navigation succeeded
            duration_ms: Time taken in milliseconds
        """
        from_hash = CognitiveMapPage.hash_url(from_url)
        to_hash = CognitiveMapPage.hash_url(to_url)

        # Get or create navigation path
        result = await self.db.execute(
            select(NavigationPath).where(
                and_(
                    NavigationPath.from_url_hash == from_hash,
                    NavigationPath.to_url_hash == to_hash,
                )
            )
        )
        path = result.scalar_one_or_none()

        if path is None:
            # Create new path
            path = NavigationPath(
                from_url_hash=from_hash,
                to_url_hash=to_hash,
                action_sequence=actions,
                success_count=0,
                failure_count=0,
                confidence_score=0.0,
            )
            self.db.add(path)
            logger.info(f"🗺️  New navigation path: {from_url} → {to_url}")

        # Update counts
        if success:
            path.success_count += 1
        else:
            path.failure_count += 1

        # Update average duration
        if path.avg_duration_ms:
            total_attempts = path.success_count + path.failure_count
            current_avg = path.avg_duration_ms
            new_avg = ((current_avg * (total_attempts - 1)) + duration_ms) / total_attempts
            path.avg_duration_ms = int(new_avg)
        else:
            path.avg_duration_ms = duration_ms

        # Update action sequence if this was successful
        if success:
            path.action_sequence = actions

        # Recalculate confidence score
        total = path.success_count + path.failure_count
        success_rate = path.success_count / total if total > 0 else 0
        # Confidence increases with both success rate and attempt count
        attempt_factor = min(total / 10, 1.0)  # Cap at 10 attempts
        path.confidence_score = round(success_rate * attempt_factor, 2)

        path.last_used = datetime.utcnow()

        await self.db.commit()
        logger.debug(
            f"✅ Navigation path updated: {from_url} → {to_url} "
            f"(confidence: {path.confidence_score})"
        )

    async def get_navigation_path(
        self, from_url: str, to_url: str
    ) -> Optional[NavigationPath]:
        """Get learned navigation path between two URLs.

        Args:
            from_url: Starting URL
            to_url: Destination URL

        Returns:
            NavigationPath if learned, None otherwise
        """
        from_hash = CognitiveMapPage.hash_url(from_url)
        to_hash = CognitiveMapPage.hash_url(to_url)

        result = await self.db.execute(
            select(NavigationPath).where(
                and_(
                    NavigationPath.from_url_hash == from_hash,
                    NavigationPath.to_url_hash == to_hash,
                )
            )
        )
        return result.scalar_one_or_none()

    # ========================================================================
    # RECOMMENDATIONS
    # ========================================================================

    async def recommend_selector(
        self, url: str, action_type: str, limit: int = 5
    ) -> List[Dict[str, Any]]:
        """Recommend selectors for an action based on learned patterns.

        Args:
            url: Page URL
            action_type: Type of action (click, type, etc.)
            limit: Maximum number of recommendations

        Returns:
            List of recommended selectors with metadata:
            [
                {
                    "selector": "button.submit",
                    "count": 10,
                    "last_used": "2025-11-14T...",
                    "avg_duration_ms": 150
                },
                ...
            ]
        """
        url_hash = CognitiveMapPage.hash_url(url)

        # Get page from cognitive map
        result = await self.db.execute(
            select(CognitiveMapPage).where(CognitiveMapPage.url_hash == url_hash)
        )
        page = result.scalar_one_or_none()

        if not page or not page.elements_snapshot:
            return []

        selectors = page.elements_snapshot.get("selectors", {})
        action_selectors = selectors.get(action_type, {})

        # Sort by count (most used first)
        recommendations = [
            {"selector": selector, **data}
            for selector, data in action_selectors.items()
        ]
        recommendations.sort(key=lambda x: x["count"], reverse=True)

        return recommendations[:limit]

    async def get_important_pages(
        self, min_score: float = 50.0, limit: int = 10
    ) -> List[CognitiveMapPage]:
        """Get most important pages from cognitive map.

        Args:
            min_score: Minimum importance score (0-100)
            limit: Maximum number of pages to return

        Returns:
            List of CognitiveMapPage sorted by importance
        """
        result = await self.db.execute(
            select(CognitiveMapPage)
            .where(CognitiveMapPage.importance_score >= min_score)
            .order_by(desc(CognitiveMapPage.importance_score))
            .limit(limit)
        )
        return list(result.scalars().all())

    async def get_recent_pages(
        self, hours: int = 24, limit: int = 10
    ) -> List[CognitiveMapPage]:
        """Get recently visited pages.

        Args:
            hours: Number of hours to look back
            limit: Maximum number of pages

        Returns:
            List of CognitiveMapPage sorted by recency
        """
        cutoff = datetime.utcnow() - timedelta(hours=hours)

        result = await self.db.execute(
            select(CognitiveMapPage)
            .where(CognitiveMapPage.last_visited >= cutoff)
            .order_by(desc(CognitiveMapPage.last_visited))
            .limit(limit)
        )
        return list(result.scalars().all())

    # ========================================================================
    # STATISTICS
    # ========================================================================

    async def get_statistics(self) -> Dict[str, Any]:
        """Get cognitive map statistics.

        Returns:
            Statistics dict with:
            - total_pages: Total pages in cognitive map
            - total_navigation_paths: Total learned paths
            - avg_importance_score: Average page importance
            - top_domains: Most visited domains
        """
        # Total pages
        total_pages_result = await self.db.execute(
            select(func.count()).select_from(CognitiveMapPage)
        )
        total_pages = total_pages_result.scalar_one()

        # Total navigation paths
        total_paths_result = await self.db.execute(
            select(func.count()).select_from(NavigationPath)
        )
        total_paths = total_paths_result.scalar_one()

        # Average importance
        avg_importance_result = await self.db.execute(
            select(func.avg(CognitiveMapPage.importance_score))
        )
        avg_importance = avg_importance_result.scalar_one() or 0.0

        # Top domains
        top_domains_result = await self.db.execute(
            select(
                CognitiveMapPage.domain,
                func.count(CognitiveMapPage.id).label("count"),
            )
            .group_by(CognitiveMapPage.domain)
            .order_by(desc("count"))
            .limit(10)
        )
        top_domains = [
            {"domain": row[0], "count": row[1]} for row in top_domains_result.all()
        ]

        return {
            "total_pages": total_pages,
            "total_navigation_paths": total_paths,
            "avg_importance_score": round(avg_importance, 2),
            "top_domains": top_domains,
        }
