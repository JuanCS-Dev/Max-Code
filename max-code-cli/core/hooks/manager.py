"""
Hook Manager - Central lifecycle hooks management

Manages hook registration, configuration loading, and triggering.
Singleton pattern for global access.

Biblical Foundation:
"Tudo quanto te vier à mão para fazer, faze-o conforme as tuas forças" (Eclesiastes 9:10)
"""

import logging
import json
import asyncio
from typing import Dict, List, Optional, Any
from pathlib import Path

from .types import (
    HookEvent,
    HookPayload,
    HookResult,
    HookConfig,
    HookDefinition,
    SessionSource,
)
from .executor import HookExecutor

logger = logging.getLogger(__name__)


class HookManagerError(Exception):
    """Base exception for hook manager errors"""
    pass


class HookConfigNotFoundError(HookManagerError):
    """Hook configuration file not found"""
    pass


class HookManager:
    """
    Central hook lifecycle management.

    Singleton pattern for global access.
    Loads configuration from settings.json and triggers hooks.
    """

    _instance: Optional["HookManager"] = None
    _lock = asyncio.Lock()

    def __new__(cls):
        """Singleton pattern"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        """Initialize hook manager (only once due to singleton)"""
        if self._initialized:
            return

        self.config = HookConfig()
        self.executor = HookExecutor(timeout=30)
        self.enabled = True
        self._config_path: Optional[Path] = None
        self._initialized = True

        logger.info("HookManager initialized")

    def load_config(self, config_path: str | Path) -> None:
        """
        Load hook configuration from settings.json.

        Args:
            config_path: Path to settings.json file

        Raises:
            HookConfigNotFoundError: If config file not found
            json.JSONDecodeError: If config file is invalid JSON
        """
        path = Path(config_path).expanduser()

        if not path.exists():
            raise HookConfigNotFoundError(f"Config file not found: {path}")

        try:
            with open(path, "r") as f:
                config_dict = json.load(f)

            self.config = HookConfig.from_dict(config_dict)
            self._config_path = path

            hook_count = sum(len(hooks) for hooks in self.config.hooks.values())
            logger.info(f"Loaded {hook_count} hooks from {path}")

        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in config file: {e}")
            raise

        except Exception as e:
            logger.error(f"Failed to load hook config: {e}")
            raise HookManagerError(f"Failed to load config: {e}") from e

    def register_hook(
        self,
        event: HookEvent,
        matcher: str,
        command: str,
        enabled: bool = True,
    ) -> HookDefinition:
        """
        Register hook programmatically (without settings.json).

        Args:
            event: Hook event
            matcher: Tool name pattern
            command: Shell command
            enabled: Whether hook is enabled

        Returns:
            HookDefinition that was registered
        """
        hook = HookDefinition(
            event=event,
            matcher=matcher,
            command=command,
            enabled=enabled,
        )

        self.config.add_hook(hook)
        logger.info(f"Registered hook: {event} / {matcher}")

        return hook

    async def trigger(
        self,
        event: HookEvent,
        payload: HookPayload,
        tool_name: Optional[str] = None,
    ) -> HookResult:
        """
        Trigger hooks for an event.

        Args:
            event: Hook event to trigger
            payload: Hook payload
            tool_name: Tool name (for PreToolUse/PostToolUse)

        Returns:
            HookResult aggregating all hook results

        For PreToolUse:
        - If ANY hook blocks, return blocked result
        - Otherwise, return allowed result
        """
        if not self.enabled:
            return HookResult.allow()

        # Get matching hooks
        hooks = self.config.get_matching_hooks(event, tool_name)

        if not hooks:
            # No hooks registered for this event
            return HookResult.allow()

        logger.debug(f"Triggering {len(hooks)} hook(s) for event {event}")

        # Execute all hooks
        results: List[HookResult] = []

        for hook in hooks:
            try:
                result = self.executor.execute(
                    command=hook.command,
                    payload=payload,
                )
                results.append(result)

                # For PreToolUse: if any hook blocks, stop and block
                if event == HookEvent.PRE_TOOL_USE and not result.allow_execution:
                    logger.warning(f"PreToolUse hook blocked execution: {result.feedback}")
                    return result

            except Exception as e:
                logger.error(f"Hook execution failed: {e}", exc_info=True)
                # Continue with other hooks
                results.append(HookResult.error(str(e)))

        # Aggregate results
        return self._aggregate_results(results, event)

    def _aggregate_results(self, results: List[HookResult], event: HookEvent) -> HookResult:
        """
        Aggregate multiple hook results.

        For PreToolUse:
        - If any blocked: return blocked
        - Otherwise: return allowed

        For other events:
        - Always return success (non-blocking)
        """
        if not results:
            return HookResult.allow()

        # Check if any hook blocked (PreToolUse only)
        if event == HookEvent.PRE_TOOL_USE:
            for result in results:
                if not result.allow_execution:
                    return result

        # All hooks allowed or event is non-blocking
        feedbacks = [r.feedback for r in results if r.feedback]
        combined_feedback = "\n".join(feedbacks) if feedbacks else None

        return HookResult.allow(feedback=combined_feedback)

    def enable(self):
        """Enable hook system"""
        self.enabled = True
        logger.info("Hook system enabled")

    def disable(self):
        """Disable hook system (hooks won't trigger)"""
        self.enabled = False
        logger.info("Hook system disabled")

    def is_enabled(self) -> bool:
        """Check if hook system is enabled"""
        return self.enabled

    def get_hook_count(self) -> int:
        """Get total number of registered hooks"""
        return sum(len(hooks) for hooks in self.config.hooks.values())

    def list_hooks(self, event: Optional[HookEvent] = None) -> List[HookDefinition]:
        """
        List registered hooks.

        Args:
            event: Optional event filter

        Returns:
            List of HookDefinition
        """
        if event is None:
            # All hooks
            all_hooks = []
            for hooks in self.config.hooks.values():
                all_hooks.extend(hooks)
            return all_hooks

        return self.config.get_hooks(event)

    def clear(self):
        """Clear all hooks (useful for testing)"""
        self.config = HookConfig()
        logger.warning("All hooks cleared")

    def __repr__(self) -> str:
        return f"<HookManager: {self.get_hook_count()} hooks, enabled={self.enabled}>"

    def __str__(self) -> str:
        return f"HookManager({self.get_hook_count()} hooks)"


# Global singleton instance
_manager = HookManager()


def get_hook_manager() -> HookManager:
    """Get the global hook manager instance"""
    return _manager
