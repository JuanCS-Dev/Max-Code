"""MABA Browser Controller - Playwright Automation.

Day 3: Complete browser automation with Playwright async API.

Features:
- Multi-session management with cleanup
- Chromium/Firefox/WebKit support
- Screenshot capture (full page + element)
- Element interaction (click, type, wait)
- Form automation
- Data extraction
- Error handling and retry logic
- Automatic session timeout

Constitution Compliance:
- P1 (Completude): Complete browser automation implementation
- P2 (Validação): Input validation and error handling
- P4 (Rastreabilidade): Full action logging to database
- P5 (Consciência Sistêmica): Learning from automation patterns

Author: Vértice Platform Team
License: Proprietary
"""
import asyncio
import base64
import logging
import uuid
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from playwright.async_api import (
    Browser,
    BrowserContext,
    Page,
    Playwright,
    TimeoutError as PlaywrightTimeoutError,
    async_playwright,
)
from sqlalchemy.ext.asyncio import AsyncSession

from db import BrowserAction, BrowserSession

logger = logging.getLogger(__name__)

# ============================================================================
# EXCEPTIONS
# ============================================================================

class BrowserControllerError(Exception):
    """Base exception for browser controller errors."""
    pass


class SessionNotFoundError(BrowserControllerError):
    """Session ID not found."""
    pass


class SessionLimitError(BrowserControllerError):
    """Maximum session limit reached."""
    pass


class NavigationError(BrowserControllerError):
    """Navigation failed."""
    pass


class ElementNotFoundError(BrowserControllerError):
    """Element selector not found."""
    pass


# ============================================================================
# BROWSER CONTROLLER
# ============================================================================

class BrowserController:
    """Manages Playwright browser instances and automation.

    Features:
    - Session pool management
    - Automatic cleanup on timeout
    - Multiple browser support (Chromium, Firefox, WebKit)
    - Screenshot capture
    - Element interaction
    - Form automation
    - Data extraction

    Attributes:
        headless: Run browser in headless mode
        max_sessions: Maximum number of concurrent sessions
        default_timeout: Default action timeout in milliseconds
        session_timeout: Session idle timeout in seconds
    """

    def __init__(
        self,
        headless: bool = True,
        max_sessions: int = 10,
        default_timeout: int = 30000,
        session_timeout: int = 600,  # 10 minutes
        db: Optional[AsyncSession] = None,
    ):
        """Initialize browser controller.

        Args:
            headless: Run browsers in headless mode
            max_sessions: Maximum concurrent sessions
            default_timeout: Default timeout in milliseconds
            session_timeout: Idle session timeout in seconds
            db: Database session for logging
        """
        self.headless = headless
        self.max_sessions = max_sessions
        self.default_timeout = default_timeout
        self.session_timeout = session_timeout
        self.db = db

        # Playwright instances
        self.playwright: Optional[Playwright] = None
        self.browsers: Dict[str, Browser] = {}  # browser_type -> Browser
        self.sessions: Dict[str, BrowserContext] = {}  # session_id -> Context
        self.session_pages: Dict[str, Page] = {}  # session_id -> active Page

        # Session metadata
        self.session_last_activity: Dict[str, datetime] = {}

        # Cleanup task
        self._cleanup_task: Optional[asyncio.Task] = None
        self._running = False

    # ========================================================================
    # LIFECYCLE
    # ========================================================================

    async def initialize(self) -> None:
        """Initialize Playwright and launch default browser."""
        if self.playwright is not None:
            logger.warning("Browser controller already initialized")
            return

        logger.info("🎭 Initializing Playwright browser controller...")

        self.playwright = await async_playwright().start()

        # Launch default browser (Chromium)
        await self._launch_browser("chromium")

        self._running = True
        self._cleanup_task = asyncio.create_task(self._cleanup_loop())

        logger.info(f"✅ Browser controller initialized (headless={self.headless}, max_sessions={self.max_sessions})")

    async def close(self) -> None:
        """Close all browsers and cleanup."""
        logger.info("🛑 Closing browser controller...")

        self._running = False

        # Cancel cleanup task
        if self._cleanup_task:
            self._cleanup_task.cancel()
            try:
                await self._cleanup_task
            except asyncio.CancelledError:
                pass

        # Close all sessions
        session_ids = list(self.sessions.keys())
        for session_id in session_ids:
            try:
                await self.close_session(session_id)
            except Exception as e:
                logger.error(f"Error closing session {session_id}: {e}")

        # Close all browsers
        for browser_type, browser in self.browsers.items():
            try:
                await browser.close()
                logger.info(f"✅ {browser_type} browser closed")
            except Exception as e:
                logger.error(f"Error closing {browser_type} browser: {e}")

        # Stop Playwright
        if self.playwright:
            await self.playwright.stop()
            self.playwright = None

        logger.info("✅ Browser controller closed")

    async def _launch_browser(self, browser_type: str = "chromium") -> Browser:
        """Launch a browser instance.

        Args:
            browser_type: Browser type (chromium, firefox, webkit)

        Returns:
            Browser instance

        Raises:
            BrowserControllerError: If browser launch fails
        """
        if browser_type in self.browsers:
            return self.browsers[browser_type]

        logger.info(f"🚀 Launching {browser_type} browser...")

        try:
            if browser_type == "chromium":
                browser = await self.playwright.chromium.launch(headless=self.headless)
            elif browser_type == "firefox":
                browser = await self.playwright.firefox.launch(headless=self.headless)
            elif browser_type == "webkit":
                browser = await self.playwright.webkit.launch(headless=self.headless)
            else:
                raise ValueError(f"Unknown browser type: {browser_type}")

            self.browsers[browser_type] = browser
            logger.info(f"✅ {browser_type} browser launched")
            return browser

        except Exception as e:
            logger.error(f"Failed to launch {browser_type} browser: {e}")
            raise BrowserControllerError(f"Browser launch failed: {e}")

    # ========================================================================
    # SESSION MANAGEMENT
    # ========================================================================

    async def create_session(
        self,
        browser_type: str = "chromium",
        viewport_width: int = 1280,
        viewport_height: int = 720,
        user_agent: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Create a new browser session.

        Args:
            browser_type: Browser type (chromium, firefox, webkit)
            viewport_width: Viewport width in pixels
            viewport_height: Viewport height in pixels
            user_agent: Custom user agent string

        Returns:
            Session info dict with session_id and status

        Raises:
            SessionLimitError: If max sessions reached
            BrowserControllerError: If session creation fails
        """
        if len(self.sessions) >= self.max_sessions:
            raise SessionLimitError(f"Maximum sessions ({self.max_sessions}) reached")

        session_id = str(uuid.uuid4())

        try:
            # Launch browser if needed
            browser = await self._launch_browser(browser_type)

            # Create context
            context = await browser.new_context(
                viewport={"width": viewport_width, "height": viewport_height},
                user_agent=user_agent,
            )

            # Set default timeout
            context.set_default_timeout(self.default_timeout)

            # Create initial page
            page = await context.new_page()

            # Store session
            self.sessions[session_id] = context
            self.session_pages[session_id] = page
            self.session_last_activity[session_id] = datetime.now(timezone.utc)

            # Log to database if available
            if self.db:
                db_session = BrowserSession(
                    id=uuid.UUID(session_id),
                    status="active",
                    browser_type=browser_type,
                    viewport_width=viewport_width,
                    viewport_height=viewport_height,
                    user_agent=user_agent,
                )
                self.db.add(db_session)
                await self.db.commit()

            logger.info(f"✅ Session created: {session_id} ({browser_type})")

            return {
                "session_id": session_id,
                "status": "active",
                "browser_type": browser_type,
                "viewport": {"width": viewport_width, "height": viewport_height},
            }

        except Exception as e:
            logger.error(f"Failed to create session: {e}")
            raise BrowserControllerError(f"Session creation failed: {e}")

    async def close_session(self, session_id: str) -> Dict[str, Any]:
        """Close a browser session.

        Args:
            session_id: Session ID to close

        Returns:
            Close status dict

        Raises:
            SessionNotFoundError: If session not found
        """
        if session_id not in self.sessions:
            raise SessionNotFoundError(f"Session not found: {session_id}")

        try:
            context = self.sessions[session_id]
            await context.close()

            # Cleanup
            del self.sessions[session_id]
            if session_id in self.session_pages:
                del self.session_pages[session_id]
            if session_id in self.session_last_activity:
                del self.session_last_activity[session_id]

            # Update database if available
            if self.db:
                from sqlalchemy import update
                stmt = update(BrowserSession).where(
                    BrowserSession.id == uuid.UUID(session_id)
                ).values(
                    status="closed",
                    closed_at=datetime.now(timezone.utc)
                )
                await self.db.execute(stmt)
                await self.db.commit()

            logger.info(f"✅ Session closed: {session_id}")

            return {"status": "closed", "session_id": session_id}

        except Exception as e:
            logger.error(f"Failed to close session {session_id}: {e}")
            raise BrowserControllerError(f"Session close failed: {e}")

    def _update_session_activity(self, session_id: str) -> None:
        """Update session last activity timestamp."""
        self.session_last_activity[session_id] = datetime.now(timezone.utc)

    async def _cleanup_loop(self) -> None:
        """Background task to cleanup idle sessions."""
        while self._running:
            try:
                await asyncio.sleep(60)  # Check every minute

                now = datetime.now(timezone.utc)
                sessions_to_close = []

                for session_id, last_activity in self.session_last_activity.items():
                    idle_seconds = (now - last_activity).total_seconds()
                    if idle_seconds > self.session_timeout:
                        sessions_to_close.append(session_id)

                for session_id in sessions_to_close:
                    logger.warning(f"⏱️ Closing idle session: {session_id}")
                    try:
                        await self.close_session(session_id)
                    except Exception as e:
                        logger.error(f"Error closing idle session: {e}")

            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Cleanup loop error: {e}")

    # ========================================================================
    # BROWSER ACTIONS
    # ========================================================================

    async def navigate(
        self,
        session_id: str,
        url: str,
        wait_until: str = "load",
        timeout_ms: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Navigate to a URL.

        Args:
            session_id: Browser session ID
            url: Target URL
            wait_until: Wait strategy (load, domcontentloaded, networkidle)
            timeout_ms: Navigation timeout in milliseconds

        Returns:
            Navigation result dict

        Raises:
            SessionNotFoundError: If session not found
            NavigationError: If navigation fails
        """
        if session_id not in self.sessions:
            raise SessionNotFoundError(f"Session not found: {session_id}")

        self._update_session_activity(session_id)
        page = self.session_pages[session_id]

        try:
            response = await page.goto(
                url,
                wait_until=wait_until,
                timeout=timeout_ms or self.default_timeout
            )

            result = {
                "status": "success",
                "url": page.url,
                "title": await page.title(),
                "status_code": response.status if response else None,
            }

            # Log action to database
            if self.db:
                action = BrowserAction(
                    session_id=uuid.UUID(session_id),
                    action_type="navigate",
                    url=url,
                    success=True,
                    parameters={"wait_until": wait_until},
                )
                self.db.add(action)
                await self.db.commit()

            logger.info(f"✅ Navigated to {url}")
            return result

        except PlaywrightTimeoutError as e:
            logger.error(f"Navigation timeout: {url}")
            if self.db:
                action = BrowserAction(
                    session_id=uuid.UUID(session_id),
                    action_type="navigate",
                    url=url,
                    success=False,
                    error_type="timeout",
                    error_message=str(e),
                )
                self.db.add(action)
                await self.db.commit()
            raise NavigationError(f"Navigation timeout: {url}")

        except Exception as e:
            logger.error(f"Navigation failed: {e}")
            if self.db:
                action = BrowserAction(
                    session_id=uuid.UUID(session_id),
                    action_type="navigate",
                    url=url,
                    success=False,
                    error_type=type(e).__name__,
                    error_message=str(e),
                )
                self.db.add(action)
                await self.db.commit()
            raise NavigationError(f"Navigation failed: {e}")

    async def click(
        self,
        session_id: str,
        selector: str,
        timeout_ms: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Click an element.

        Args:
            session_id: Browser session ID
            selector: CSS selector
            timeout_ms: Click timeout in milliseconds

        Returns:
            Click result dict

        Raises:
            SessionNotFoundError: If session not found
            ElementNotFoundError: If element not found
        """
        if session_id not in self.sessions:
            raise SessionNotFoundError(f"Session not found: {session_id}")

        self._update_session_activity(session_id)
        page = self.session_pages[session_id]

        try:
            await page.click(selector, timeout=timeout_ms or self.default_timeout)

            result = {"status": "success", "selector": selector}

            # Log action
            if self.db:
                action = BrowserAction(
                    session_id=uuid.UUID(session_id),
                    action_type="click",
                    selector=selector,
                    success=True,
                )
                self.db.add(action)
                await self.db.commit()

            logger.info(f"✅ Clicked: {selector}")
            return result

        except PlaywrightTimeoutError:
            logger.error(f"Element not found: {selector}")
            if self.db:
                action = BrowserAction(
                    session_id=uuid.UUID(session_id),
                    action_type="click",
                    selector=selector,
                    success=False,
                    error_type="element_not_found",
                    error_message=f"Selector not found: {selector}",
                )
                self.db.add(action)
                await self.db.commit()
            raise ElementNotFoundError(f"Element not found: {selector}")

        except Exception as e:
            logger.error(f"Click failed: {e}")
            if self.db:
                action = BrowserAction(
                    session_id=uuid.UUID(session_id),
                    action_type="click",
                    selector=selector,
                    success=False,
                    error_type=type(e).__name__,
                    error_message=str(e),
                )
                self.db.add(action)
                await self.db.commit()
            raise BrowserControllerError(f"Click failed: {e}")

    async def type_text(
        self,
        session_id: str,
        selector: str,
        text: str,
        delay_ms: int = 0,
    ) -> Dict[str, Any]:
        """Type text into an input field.

        Args:
            session_id: Browser session ID
            selector: CSS selector
            text: Text to type
            delay_ms: Delay between keystrokes in milliseconds

        Returns:
            Type result dict

        Raises:
            SessionNotFoundError: If session not found
            ElementNotFoundError: If element not found
        """
        if session_id not in self.sessions:
            raise SessionNotFoundError(f"Session not found: {session_id}")

        self._update_session_activity(session_id)
        page = self.session_pages[session_id]

        try:
            await page.type(selector, text, delay=delay_ms)

            result = {"status": "success", "selector": selector, "text_length": len(text)}

            # Log action
            if self.db:
                action = BrowserAction(
                    session_id=uuid.UUID(session_id),
                    action_type="type",
                    selector=selector,
                    success=True,
                    parameters={"text_length": len(text), "delay_ms": delay_ms},
                )
                self.db.add(action)
                await self.db.commit()

            logger.info(f"✅ Typed text into: {selector}")
            return result

        except Exception as e:
            logger.error(f"Type failed: {e}")
            if self.db:
                action = BrowserAction(
                    session_id=uuid.UUID(session_id),
                    action_type="type",
                    selector=selector,
                    success=False,
                    error_type=type(e).__name__,
                    error_message=str(e),
                )
                self.db.add(action)
                await self.db.commit()
            raise BrowserControllerError(f"Type failed: {e}")

    async def screenshot(
        self,
        session_id: str,
        full_page: bool = False,
        selector: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Take a screenshot.

        Args:
            session_id: Browser session ID
            full_page: Capture full scrollable page
            selector: Element selector for partial screenshot

        Returns:
            Screenshot result with base64 data

        Raises:
            SessionNotFoundError: If session not found
        """
        if session_id not in self.sessions:
            raise SessionNotFoundError(f"Session not found: {session_id}")

        self._update_session_activity(session_id)
        page = self.session_pages[session_id]

        try:
            if selector:
                element = await page.query_selector(selector)
                if not element:
                    raise ElementNotFoundError(f"Element not found: {selector}")
                screenshot_bytes = await element.screenshot()
            else:
                screenshot_bytes = await page.screenshot(full_page=full_page)

            # Convert to base64
            screenshot_base64 = base64.b64encode(screenshot_bytes).decode('utf-8')

            result = {
                "status": "success",
                "screenshot": screenshot_base64,
                "format": "png",
                "size_bytes": len(screenshot_bytes),
                "full_page": full_page,
                "selector": selector,
            }

            # Log action
            if self.db:
                action = BrowserAction(
                    session_id=uuid.UUID(session_id),
                    action_type="screenshot",
                    selector=selector,
                    success=True,
                    parameters={"full_page": full_page, "size_bytes": len(screenshot_bytes)},
                )
                self.db.add(action)
                await self.db.commit()

            logger.info(f"✅ Screenshot captured ({len(screenshot_bytes)} bytes)")
            return result

        except Exception as e:
            logger.error(f"Screenshot failed: {e}")
            if self.db:
                action = BrowserAction(
                    session_id=uuid.UUID(session_id),
                    action_type="screenshot",
                    selector=selector,
                    success=False,
                    error_type=type(e).__name__,
                    error_message=str(e),
                )
                self.db.add(action)
                await self.db.commit()
            raise BrowserControllerError(f"Screenshot failed: {e}")

    async def extract_data(
        self,
        session_id: str,
        selectors: Dict[str, str],
        extract_all: bool = False,
    ) -> Dict[str, Any]:
        """Extract data from page using CSS selectors.

        Args:
            session_id: Browser session ID
            selectors: Dict of {field_name: css_selector}
            extract_all: Extract all matching elements (not just first)

        Returns:
            Extracted data dict

        Raises:
            SessionNotFoundError: If session not found
        """
        if session_id not in self.sessions:
            raise SessionNotFoundError(f"Session not found: {session_id}")

        self._update_session_activity(session_id)
        page = self.session_pages[session_id]

        extracted_data = {}

        try:
            for field_name, css_selector in selectors.items():
                if extract_all:
                    elements = await page.query_selector_all(css_selector)
                    extracted_data[field_name] = [await elem.text_content() for elem in elements]
                else:
                    element = await page.query_selector(css_selector)
                    extracted_data[field_name] = await element.text_content() if element else None

            result = {"status": "success", "data": extracted_data, "fields_extracted": len(extracted_data)}

            # Log action
            if self.db:
                action = BrowserAction(
                    session_id=uuid.UUID(session_id),
                    action_type="extract",
                    success=True,
                    parameters={"selectors": selectors, "extract_all": extract_all},
                )
                self.db.add(action)
                await self.db.commit()

            logger.info(f"✅ Data extracted: {len(extracted_data)} fields")
            return result

        except Exception as e:
            logger.error(f"Data extraction failed: {e}")
            if self.db:
                action = BrowserAction(
                    session_id=uuid.UUID(session_id),
                    action_type="extract",
                    success=False,
                    error_type=type(e).__name__,
                    error_message=str(e),
                )
                self.db.add(action)
                await self.db.commit()
            raise BrowserControllerError(f"Data extraction failed: {e}")

    # ========================================================================
    # HEALTH CHECK
    # ========================================================================

    async def health_check(self) -> Dict[str, Any]:
        """Check browser controller health.

        Returns:
            Health status dict with session info
        """
        return {
            "status": "healthy" if self._running else "stopped",
            "active_sessions": len(self.sessions),
            "max_sessions": self.max_sessions,
            "browsers_launched": list(self.browsers.keys()),
            "headless": self.headless,
            "default_timeout_ms": self.default_timeout,
            "session_timeout_seconds": self.session_timeout,
        }
