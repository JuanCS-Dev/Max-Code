"""MABA API Routes.

Day 2: JWT Authentication
Day 3: Database integration with CognitiveMap learning

FastAPI routes for MABA browser automation operations.

Author: Vértice Platform Team
License: Proprietary
"""

import asyncio
import logging
import time

from fastapi import Depends, APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

# Day 2: JWT Authentication
from libs.auth import verify_token

# Day 3: Database and Cognitive Map
from db import get_db
from cognitive_map import CognitiveMapService

from models import (
    BrowserActionResponse,
    BrowserSessionRequest,
    ClickRequest,
    CognitiveMapQueryRequest,
    CognitiveMapQueryResponse,
    ExtractRequest,
    NavigationRequest,
    PageAnalysisRequest,
    PageAnalysisResponse,
    ScreenshotRequest,
    TypeRequest,
)

logger = logging.getLogger(__name__)

router = APIRouter(tags=["MABA"])


# Dependency to get MABA service instance
# This will be set by main.py after service initialization
_maba_service_instance = None


def set_maba_service(service):
    """Set the global MABA service instance."""
    global _maba_service_instance
    _maba_service_instance = service


def get_maba_service():
    """Get the MABA service instance."""
    if _maba_service_instance is None:
        raise HTTPException(status_code=503, detail="MABA service not initialized")
    return _maba_service_instance


@router.post("/sessions")
async def create_browser_session(
    request: BrowserSessionRequest,
    token_data: dict = Depends(verify_token),  # Day 2: JWT Auth
    service=Depends(get_maba_service)
):
    """
    Create a new browser session. **Auth required.**

    Args:
        request: Browser session configuration
        token_data: JWT token (auto-injected)

    Returns:
        Session details including ID and status
    """
    try:
        result = await service.browser_controller.create_session(
            viewport_width=request.viewport_width,
            viewport_height=request.viewport_height,
            user_agent=request.user_agent,
        )

        # Handle both dict response and string response
        if isinstance(result, dict):
            return result
        else:
            return {"session_id": result, "status": "created"}

    except Exception as e:
        logger.error(f"Failed to create browser session: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/sessions/{session_id}")
async def close_browser_session(
    session_id: str,
    token_data: dict = Depends(verify_token),  # Day 2: JWT Auth
    service=Depends(get_maba_service)
):
    """
    Close a browser session. **Auth required.**

    Args:
        session_id: Session ID to close
        token_data: JWT token (auto-injected)

    Returns:
        Success message
    """
    try:
        result = await service.browser_controller.close_session(session_id)

        # Handle both dict response and None response
        if isinstance(result, dict):
            return result
        else:
            return {"status": "closed", "message": f"Session {session_id} closed"}

    except Exception as e:
        logger.error(f"Failed to close session: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/navigate", response_model=BrowserActionResponse)
async def navigate(
    request: NavigationRequest,
    session_id: str,
    token_data: dict = Depends(verify_token),  # Day 2: JWT Auth
    service=Depends(get_maba_service)
):
    """
    Navigate to a URL. **Auth required.**

    Args:
        request: Navigation request
        session_id: Browser session ID
        token_data: JWT token (auto-injected)

    Returns:
        Navigation result
    """
    try:
        start_time = time.time()

        result = await service.browser_controller.navigate(
            session_id=session_id,
            url=request.url,
            wait_until=request.wait_until,
            timeout_ms=request.timeout_ms,
        )

        execution_time_ms = (time.time() - start_time) * 1000

        return BrowserActionResponse(
            status=result.get("status", "failed"),
            result=result,
            execution_time_ms=execution_time_ms,
        )

    except Exception as e:
        logger.error(f"Navigation failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/click", response_model=BrowserActionResponse)
async def click(
    request: ClickRequest,
    session_id: str,
    token_data: dict = Depends(verify_token),  # Day 2: JWT Auth
    service=Depends(get_maba_service)
):
    """
    Click an element. **Auth required.**

    Args:
        request: Click request
        session_id: Browser session ID
        token_data: JWT token (auto-injected)

    Returns:
        Click result
    """
    try:
        result = await service.browser_controller.click(
            session_id=session_id,
            selector=request.selector,
            timeout_ms=request.timeout_ms,
        )

        return BrowserActionResponse(
            status=result.get("status", "failed"), result=result, execution_time_ms=0.0
        )

    except Exception as e:
        logger.error(f"Click failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/type", response_model=BrowserActionResponse)
async def type_text(
    request: TypeRequest,
    session_id: str,
    token_data: dict = Depends(verify_token),  # Day 2: JWT Auth
    service=Depends(get_maba_service)
):
    """
    Type text into an element. **Auth required.**

    Args:
        request: Type request
        session_id: Browser session ID
        token_data: JWT token (auto-injected)

    Returns:
        Type result
    """
    try:
        result = await service.browser_controller.type_text(
            session_id=session_id,
            selector=request.selector,
            text=request.text,
            delay_ms=request.delay_ms,
        )

        return BrowserActionResponse(
            status=result.get("status", "failed"), result=result, execution_time_ms=0.0
        )

    except Exception as e:
        logger.error(f"Type failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/screenshot", response_model=BrowserActionResponse)
async def screenshot(
    request: ScreenshotRequest,
    session_id: str,
    token_data: dict = Depends(verify_token),  # Day 2: JWT Auth
    service=Depends(get_maba_service)
):
    """
    Take a screenshot. **Auth required.**

    Args:
        request: Screenshot request
        session_id: Browser session ID
        token_data: JWT token (auto-injected)

    Returns:
        Screenshot result with base64 data
    """
    try:
        result = await service.browser_controller.screenshot(
            session_id=session_id,
            full_page=request.full_page,
            selector=request.selector,
        )

        return BrowserActionResponse(
            status=result.get("status", "failed"), result=result, execution_time_ms=0.0
        )

    except Exception as e:
        logger.error(f"Screenshot failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/extract", response_model=BrowserActionResponse)
async def extract_data(
    request: ExtractRequest,
    session_id: str,
    token_data: dict = Depends(verify_token),  # Day 2: JWT Auth
    service=Depends(get_maba_service)
):
    """
    Extract data from current page. **Auth required.**

    Args:
        request: Extract request
        session_id: Browser session ID
        token_data: JWT token (auto-injected)

    Returns:
        Extracted data
    """
    try:
        result = await service.browser_controller.extract_data(
            session_id=session_id,
            selectors=request.selectors,
            extract_all=request.extract_all,
        )

        return BrowserActionResponse(
            status=result.get("status", "failed"), result=result, execution_time_ms=0.0
        )

    except Exception as e:
        logger.error(f"Extract failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/cognitive-map/query", response_model=CognitiveMapQueryResponse)
async def query_cognitive_map(
    request: CognitiveMapQueryRequest,
    token_data: dict = Depends(verify_token),  # Day 2: JWT Auth
    db: AsyncSession = Depends(get_db),  # Day 3: Database session
):
    """
    Query the cognitive map for learned information. **Auth required.**

    Day 3: Uses database-backed CognitiveMapService for intelligent recommendations.

    Args:
        request: Cognitive map query request
        token_data: JWT token (auto-injected)
        db: Database session (auto-injected)

    Returns:
        Query results with confidence scores
    """
    try:
        # Create cognitive map service with database session
        cognitive_map = CognitiveMapService(db)

        if request.query_type == "recommend_selector":
            # Get selector recommendations for a URL and action type
            recommendations = await cognitive_map.recommend_selector(
                url=request.parameters.get("url"),
                action_type=request.parameters.get("action_type", "click"),
                limit=request.parameters.get("limit", 5),
            )

            if recommendations:
                return CognitiveMapQueryResponse(
                    found=True,
                    result={"recommendations": recommendations},
                    confidence=min(recommendations[0]["count"] / 100, 1.0) if recommendations else 0.0,
                )
            else:
                return CognitiveMapQueryResponse(
                    found=False, result=None, confidence=0.0
                )

        elif request.query_type == "get_path":
            # Get learned navigation path
            path = await cognitive_map.get_navigation_path(
                from_url=request.parameters.get("from_url"),
                to_url=request.parameters.get("to_url"),
            )

            if path:
                return CognitiveMapQueryResponse(
                    found=True,
                    result={
                        "action_sequence": path.action_sequence,
                        "success_count": path.success_count,
                        "failure_count": path.failure_count,
                        "confidence_score": path.confidence_score,
                        "avg_duration_ms": path.avg_duration_ms,
                    },
                    confidence=path.confidence_score,
                )
            else:
                return CognitiveMapQueryResponse(
                    found=False, result=None, confidence=0.0
                )

        else:
            raise ValueError(f"Unknown query type: {request.query_type}")

    except Exception as e:
        logger.error(f"Cognitive map query failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/analyze", response_model=PageAnalysisResponse)
async def analyze_page(
    request: PageAnalysisRequest,
    session_id: str,
    token_data: dict = Depends(verify_token),  # Day 2: JWT Auth
    service=Depends(get_maba_service)
):
    """
    Analyze current page with LLM. **Auth required.**

    This endpoint uses Claude to analyze the page content and provide
    insights, recommendations, or structured data extraction.

    NOTE: LLM-based page analysis is planned for future implementation.
    This endpoint currently returns HTTP 501 Not Implemented.

    Args:
        request: Page analysis request
        session_id: Browser session ID

    Returns:
        Analysis results

    Raises:
        HTTPException: 501 - Feature not yet implemented
    """
    raise HTTPException(
        status_code=501,
        detail={
            "error": "Not Implemented",
            "message": "LLM-based page analysis is not yet implemented",
            "planned_for": "Phase 2 (MVP expansion)",
            "alternative": "Use /extract endpoint for structured data extraction",
            "documentation": "/docs#tag/MABA/operation/extract_data_extract_post",
        },
    )


@router.get("/cognitive-map/important-pages")
async def get_important_pages(
    min_score: float = 50.0,
    limit: int = 10,
    token_data: dict = Depends(verify_token),  # Day 2: JWT Auth
    db: AsyncSession = Depends(get_db),  # Day 3: Database session
):
    """
    Get most important pages from cognitive map. **Auth required.**

    Day 3: Returns pages ranked by importance score (visit frequency, recency,
    success rate, learned selectors).

    Args:
        min_score: Minimum importance score (0-100)
        limit: Maximum number of pages to return
        token_data: JWT token (auto-injected)
        db: Database session (auto-injected)

    Returns:
        List of important pages with metadata
    """
    try:
        cognitive_map = CognitiveMapService(db)
        pages = await cognitive_map.get_important_pages(
            min_score=min_score, limit=limit
        )
        return {"pages": [page.to_dict() for page in pages], "count": len(pages)}

    except Exception as e:
        logger.error(f"Failed to get important pages: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/cognitive-map/recent-pages")
async def get_recent_pages(
    hours: int = 24,
    limit: int = 10,
    token_data: dict = Depends(verify_token),  # Day 2: JWT Auth
    db: AsyncSession = Depends(get_db),  # Day 3: Database session
):
    """
    Get recently visited pages. **Auth required.**

    Day 3: Returns pages visited within the specified time window.

    Args:
        hours: Number of hours to look back
        limit: Maximum number of pages
        token_data: JWT token (auto-injected)
        db: Database session (auto-injected)

    Returns:
        List of recent pages
    """
    try:
        cognitive_map = CognitiveMapService(db)
        pages = await cognitive_map.get_recent_pages(hours=hours, limit=limit)
        return {"pages": [page.to_dict() for page in pages], "count": len(pages)}

    except Exception as e:
        logger.error(f"Failed to get recent pages: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/stats")
async def get_stats(
    token_data: dict = Depends(verify_token),  # Day 2: JWT Auth
    service=Depends(get_maba_service),
    db: AsyncSession = Depends(get_db),  # Day 3: Database session
):
    """
    Get MABA statistics. **Auth required.**

    Day 3: Returns comprehensive statistics including cognitive map metrics
    from database.

    Args:
        token_data: JWT token (auto-injected)
        service: MABA service instance (auto-injected)
        db: Database session (auto-injected)

    Returns:
        Statistics dict with cognitive map and browser info
    """
    try:
        # Check if service has a get_stats method (for testing/mocking)
        if hasattr(service, "get_stats") and callable(service.get_stats):
            # If mock returns a value directly, use it
            stats = service.get_stats()
            if not asyncio.iscoroutine(stats):
                return stats
            return await stats

        # Day 3: Collect stats from components
        cognitive_map = CognitiveMapService(db)
        cognitive_map_stats = await cognitive_map.get_statistics()

        browser_health = (
            await service.browser_controller.health_check()
            if service.browser_controller
            else {}
        )

        return {
            "cognitive_map": cognitive_map_stats,
            "browser": browser_health,
            "uptime_seconds": (
                service.get_uptime_seconds()
                if hasattr(service, "get_uptime_seconds")
                else 0
            ),
        }

    except Exception as e:
        logger.error(f"Failed to get stats: {e}")
        raise HTTPException(status_code=500, detail=str(e))
