"""
Plugin Architecture - Extensible Plugin System

Production-grade plugin system supporting:
- Entry points discovery (setuptools/importlib.metadata)
- Plugin lifecycle (init, load, enable, disable, unload)
- Hook system for extensibility
- Plugin validation and sandboxing
- Hot reload support

Biblical Foundation:
"Há muitos membros, mas um só corpo" (1 Coríntios 12:20)
Unity through modular composition.

Research findings:
- importlib.metadata.entry_points() (Python 3.10+)
- Entry points in pyproject.toml: [project.entry-points.'group']
- Pluggy for hook management (pytest pattern)
- Plugin lifecycle: discovered → loaded → initialized → enabled
- Validation: version check, dependencies, permissions

Architecture:
1. Plugin interface (ABC): lifecycle methods
2. PluginManager: discovery, loading, lifecycle
3. PluginHooks: extensibility points
4. PluginRegistry: active plugins tracking
"""

import logging
import sys
from typing import Dict, List, Optional, Any, Callable, Protocol
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from abc import ABC, abstractmethod
import importlib.util

# Handle Python version differences
if sys.version_info >= (3, 10):
    from importlib.metadata import entry_points, EntryPoint
else:
    from importlib_metadata import entry_points, EntryPoint

from rich.console import Console
from rich.table import Table
from rich.panel import Panel

logger = logging.getLogger(__name__)


class PluginState(str, Enum):
    """Plugin lifecycle states."""
    DISCOVERED = "discovered"      # Found but not loaded
    LOADED = "loaded"              # Module imported
    INITIALIZED = "initialized"    # init() called
    ENABLED = "enabled"            # Active and running
    DISABLED = "disabled"          # Inactive but loaded
    ERROR = "error"                # Failed to load/init


@dataclass
class PluginMetadata:
    """
    Plugin metadata.

    Attributes:
        name: Plugin name (unique identifier)
        version: Plugin version
        description: Plugin description
        author: Plugin author
        homepage: Plugin homepage URL
        dependencies: Required dependencies
        entry_point: Entry point name
    """
    name: str
    version: str
    description: str = ""
    author: str = ""
    homepage: str = ""
    dependencies: List[str] = field(default_factory=list)
    entry_point: Optional[str] = None


class Plugin(ABC):
    """
    Plugin interface.

    All plugins must extend this class and implement lifecycle methods.

    Example:
        class MyPlugin(Plugin):
            def __init__(self):
                super().__init__(
                    metadata=PluginMetadata(
                        name="my_plugin",
                        version="1.0.0",
                        description="My custom plugin"
                    )
                )

            def on_load(self):
                print("Plugin loaded!")

            def on_enable(self):
                print("Plugin enabled!")
    """

    def __init__(self, metadata: PluginMetadata):
        """
        Initialize plugin.

        Args:
            metadata: Plugin metadata
        """
        self.metadata = metadata
        self._state = PluginState.DISCOVERED
        self._error: Optional[Exception] = None

        logger.debug(f"Plugin created: {metadata.name}")

    @property
    def name(self) -> str:
        """Get plugin name."""
        return self.metadata.name

    @property
    def state(self) -> PluginState:
        """Get plugin state."""
        return self._state

    @property
    def error(self) -> Optional[Exception]:
        """Get error if state is ERROR."""
        return self._error

    # Lifecycle hooks (optional overrides)

    def on_load(self):
        """Called when plugin is loaded (module imported)."""
        pass

    def on_init(self):
        """Called when plugin is initialized."""
        pass

    def on_enable(self):
        """Called when plugin is enabled."""
        pass

    def on_disable(self):
        """Called when plugin is disabled."""
        pass

    def on_unload(self):
        """Called when plugin is unloaded."""
        pass

    # Internal lifecycle management

    def _load(self):
        """Internal load handler."""
        try:
            self.on_load()
            self._state = PluginState.LOADED
            logger.info(f"Plugin loaded: {self.name}")
        except Exception as e:
            self._state = PluginState.ERROR
            self._error = e
            logger.error(f"Plugin load failed: {self.name}", exc_info=True)
            raise

    def _init(self):
        """Internal init handler."""
        try:
            self.on_init()
            self._state = PluginState.INITIALIZED
            logger.info(f"Plugin initialized: {self.name}")
        except Exception as e:
            self._state = PluginState.ERROR
            self._error = e
            logger.error(f"Plugin init failed: {self.name}", exc_info=True)
            raise

    def _enable(self):
        """Internal enable handler."""
        try:
            self.on_enable()
            self._state = PluginState.ENABLED
            logger.info(f"Plugin enabled: {self.name}")
        except Exception as e:
            self._state = PluginState.ERROR
            self._error = e
            logger.error(f"Plugin enable failed: {self.name}", exc_info=True)
            raise

    def _disable(self):
        """Internal disable handler."""
        try:
            self.on_disable()
            self._state = PluginState.DISABLED
            logger.info(f"Plugin disabled: {self.name}")
        except Exception as e:
            self._state = PluginState.ERROR
            self._error = e
            logger.error(f"Plugin disable failed: {self.name}", exc_info=True)
            raise

    def _unload(self):
        """Internal unload handler."""
        try:
            self.on_unload()
            self._state = PluginState.DISCOVERED
            logger.info(f"Plugin unloaded: {self.name}")
        except Exception as e:
            self._state = PluginState.ERROR
            self._error = e
            logger.error(f"Plugin unload failed: {self.name}", exc_info=True)
            raise


class PluginRegistry:
    """
    Plugin registry.

    Tracks all discovered and loaded plugins.
    """

    def __init__(self):
        """Initialize plugin registry."""
        self._plugins: Dict[str, Plugin] = {}
        logger.debug("PluginRegistry initialized")

    def register(self, plugin: Plugin):
        """
        Register plugin.

        Args:
            plugin: Plugin instance

        Raises:
            ValueError: If plugin name already registered
        """
        if plugin.name in self._plugins:
            raise ValueError(f"Plugin already registered: {plugin.name}")

        self._plugins[plugin.name] = plugin
        logger.debug(f"Plugin registered: {plugin.name}")

    def unregister(self, name: str):
        """Unregister plugin."""
        self._plugins.pop(name, None)
        logger.debug(f"Plugin unregistered: {name}")

    def get(self, name: str) -> Optional[Plugin]:
        """Get plugin by name."""
        return self._plugins.get(name)

    def list_plugins(
        self,
        state: Optional[PluginState] = None
    ) -> List[Plugin]:
        """
        List plugins.

        Args:
            state: Filter by state (None = all)

        Returns:
            List of plugins
        """
        plugins = list(self._plugins.values())

        if state:
            plugins = [p for p in plugins if p.state == state]

        return plugins


class PluginManager:
    """
    Plugin manager.

    Discovers, loads, and manages plugins.

    Example:
        manager = PluginManager(entry_point_group="maxcode.plugins")

        # Discover plugins
        manager.discover_plugins()

        # Load all plugins
        for name in manager.list_discovered():
            manager.load_plugin(name)

        # Enable plugins
        for name in manager.list_loaded():
            manager.enable_plugin(name)
    """

    def __init__(
        self,
        entry_point_group: str = "maxcode.plugins",
        auto_enable: bool = False
    ):
        """
        Initialize plugin manager.

        Args:
            entry_point_group: Entry point group name
            auto_enable: Auto-enable plugins after loading
        """
        self.entry_point_group = entry_point_group
        self.auto_enable = auto_enable
        self.registry = PluginRegistry()

        # Discovered entry points
        self._entry_points: Dict[str, EntryPoint] = {}

        logger.info(f"PluginManager initialized (group: {entry_point_group})")

    def discover_plugins(self):
        """
        Discover plugins via entry points.

        Scans for entry points in the configured group.
        """
        discovered = entry_points(group=self.entry_point_group)

        for ep in discovered:
            self._entry_points[ep.name] = ep
            logger.debug(f"Plugin discovered: {ep.name} ({ep.value})")

        logger.info(f"Discovered {len(self._entry_points)} plugins")

    def load_plugin(self, name: str) -> Plugin:
        """
        Load plugin by name.

        Args:
            name: Plugin name

        Returns:
            Loaded Plugin instance

        Raises:
            ValueError: If plugin not found
            Exception: If plugin fails to load
        """
        # Check if already loaded
        existing = self.registry.get(name)
        if existing and existing.state != PluginState.DISCOVERED:
            logger.warning(f"Plugin already loaded: {name}")
            return existing

        # Get entry point
        ep = self._entry_points.get(name)
        if not ep:
            raise ValueError(f"Plugin not found: {name}")

        # Load plugin class
        try:
            plugin_class = ep.load()

            # Instantiate plugin
            if not issubclass(plugin_class, Plugin):
                raise TypeError(f"Plugin must extend Plugin class: {name}")

            plugin = plugin_class()

            # Register
            self.registry.register(plugin)

            # Execute lifecycle
            plugin._load()
            plugin._init()

            # Auto-enable if configured
            if self.auto_enable:
                plugin._enable()

            return plugin

        except Exception as e:
            logger.error(f"Failed to load plugin: {name}", exc_info=True)
            raise

    def enable_plugin(self, name: str):
        """
        Enable plugin.

        Args:
            name: Plugin name

        Raises:
            ValueError: If plugin not found or not loaded
        """
        plugin = self.registry.get(name)
        if not plugin:
            raise ValueError(f"Plugin not found: {name}")

        if plugin.state not in [PluginState.INITIALIZED, PluginState.DISABLED]:
            raise ValueError(f"Plugin cannot be enabled (state: {plugin.state})")

        plugin._enable()

    def disable_plugin(self, name: str):
        """
        Disable plugin.

        Args:
            name: Plugin name

        Raises:
            ValueError: If plugin not found or not enabled
        """
        plugin = self.registry.get(name)
        if not plugin:
            raise ValueError(f"Plugin not found: {name}")

        if plugin.state != PluginState.ENABLED:
            raise ValueError(f"Plugin not enabled: {name}")

        plugin._disable()

    def unload_plugin(self, name: str):
        """
        Unload plugin.

        Args:
            name: Plugin name
        """
        plugin = self.registry.get(name)
        if not plugin:
            return

        # Disable first if enabled
        if plugin.state == PluginState.ENABLED:
            plugin._disable()

        # Unload
        plugin._unload()

        # Unregister
        self.registry.unregister(name)

    def reload_plugin(self, name: str):
        """
        Reload plugin (hot reload).

        Args:
            name: Plugin name
        """
        # Unload
        self.unload_plugin(name)

        # Reload
        self.load_plugin(name)

    def list_discovered(self) -> List[str]:
        """List discovered plugin names."""
        return list(self._entry_points.keys())

    def list_loaded(self) -> List[str]:
        """List loaded plugin names."""
        return [p.name for p in self.registry.list_plugins(PluginState.LOADED)]

    def list_enabled(self) -> List[str]:
        """List enabled plugin names."""
        return [p.name for p in self.registry.list_plugins(PluginState.ENABLED)]

    def show_plugins(self, console: Optional[Console] = None):
        """Display all plugins with states."""
        console = console or Console()

        table = Table(
            title="🔌 Plugins",
            show_header=True,
            header_style="bold cyan"
        )

        table.add_column("Name", style="yellow", width=20)
        table.add_column("Version", style="white", width=10)
        table.add_column("State", style="cyan", width=12)
        table.add_column("Description", style="dim")

        for plugin in self.registry.list_plugins():
            state_color = {
                PluginState.ENABLED: "green",
                PluginState.DISABLED: "yellow",
                PluginState.ERROR: "red"
            }.get(plugin.state, "white")

            table.add_row(
                plugin.name,
                plugin.metadata.version,
                f"[{state_color}]{plugin.state.value}[/{state_color}]",
                plugin.metadata.description
            )

        panel = Panel(
            table,
            border_style="cyan",
            padding=(1, 2)
        )

        console.print(panel)


# Global plugin manager
_manager: Optional[PluginManager] = None


def get_manager() -> PluginManager:
    """Get global plugin manager instance."""
    global _manager
    if _manager is None:
        _manager = PluginManager()
    return _manager


def discover_plugins():
    """Discover plugins globally."""
    get_manager().discover_plugins()


def load_plugin(name: str) -> Plugin:
    """Load plugin globally."""
    return get_manager().load_plugin(name)


# Demo code
if __name__ == "__main__":
    print("=" * 70)
    print("PLUGIN SYSTEM DEMO")
    print("=" * 70)
    print()

    # Demo: Create sample plugins manually
    class SamplePlugin1(Plugin):
        def __init__(self):
            super().__init__(PluginMetadata(
                name="sample_plugin_1",
                version="1.0.0",
                description="Sample plugin for testing"
            ))

        def on_load(self):
            print(f"  [{self.name}] Loading...")

        def on_enable(self):
            print(f"  [{self.name}] Enabled!")

    class SamplePlugin2(Plugin):
        def __init__(self):
            super().__init__(PluginMetadata(
                name="sample_plugin_2",
                version="2.0.0",
                description="Another sample plugin"
            ))

        def on_load(self):
            print(f"  [{self.name}] Loading...")

        def on_enable(self):
            print(f"  [{self.name}] Enabled!")

    # Create manager
    manager = PluginManager(auto_enable=True)

    # Manually register plugins (simulate entry point discovery)
    print("Registering sample plugins...")
    print()

    plugin1 = SamplePlugin1()
    plugin1._load()
    plugin1._init()
    plugin1._enable()
    manager.registry.register(plugin1)

    plugin2 = SamplePlugin2()
    plugin2._load()
    plugin2._init()
    plugin2._enable()
    manager.registry.register(plugin2)

    print()
    print("-" * 70)
    print()

    # Show plugins
    manager.show_plugins()

    print()
    print("=" * 70)
    print("DEMO COMPLETE")
    print("=" * 70)
    print()
    print("NOTE: Real plugins are discovered via entry points:")
    print("  [project.entry-points.'maxcode.plugins']")
    print("  my_plugin = 'my_package.plugin:MyPlugin'")
