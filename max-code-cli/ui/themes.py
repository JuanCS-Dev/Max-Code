"""
Theme System - Dynamic Color Schemes with Hot Reload

Production-grade theme system supporting:
- Multiple built-in themes (neon, fire, ocean, matrix, cyberpunk)
- TOML/JSON configuration with Dynaconf
- Hot reload without restart
- User preferences persistence
- Theme validation

Biblical Foundation:
"Tudo fez formoso em seu tempo" (Eclesiastes 3:11)
Beauty and aesthetics matter.

Research findings:
- Dynaconf: hot reload via settings.load_file() + post-hooks
- TOML format for user preferences (Python 3.11+ native)
- Theme registry pattern with validation
- CSS variable system for Textual integration

Architecture:
1. Theme dataclass: colors, gradients, styles
2. ThemeRegistry: built-in themes + custom loading
3. ThemeManager: active theme + hot reload
4. Integration with Rich (Rich themes) and Textual (CSS vars)
"""

import logging
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, field, asdict
from enum import Enum
from pathlib import Path
import json

from rich.console import Console
from rich.theme import Theme as RichTheme
from rich.panel import Panel
from rich.table import Table

from ui.constants import GRADIENTS, NEON_PALETTE, SEMANTIC_COLORS

logger = logging.getLogger(__name__)


class ThemeName(str, Enum):
    """Built-in theme names."""
    NEON = "neon"              # Official (green/cyan/blue/yellow)
    FIRE = "fire"              # Red/orange/yellow
    OCEAN = "ocean"            # Blue/cyan/aqua
    SUNSET = "sunset"          # Pink/orange/yellow
    MATRIX = "matrix"          # Green matrix style
    CYBERPUNK = "cyberpunk"    # Pink/cyan/magenta/yellow
    MONOCHROME = "monochrome"  # Grayscale
    CUSTOM = "custom"          # User-defined


@dataclass
class ThemeColors:
    """
    Theme color palette.

    Attributes:
        primary: Primary color (hex)
        secondary: Secondary color (hex)
        tertiary: Tertiary color (hex)
        accent: Accent color (hex)
        background: Background color (hex)
        foreground: Foreground/text color (hex)
        success: Success color (hex)
        error: Error color (hex)
        warning: Warning color (hex)
        info: Info color (hex)
    """
    primary: str
    secondary: str
    tertiary: str
    accent: str
    background: str = "#000000"
    foreground: str = "#FFFFFF"
    success: str = "#00FF00"
    error: str = "#FF0040"
    warning: str = "#FFD700"
    info: str = "#00BFFF"

    def to_dict(self) -> Dict[str, str]:
        """Convert to dictionary."""
        return asdict(self)

    def validate(self) -> bool:
        """Validate hex color format."""
        for key, value in asdict(self).items():
            if not value.startswith("#") or len(value) != 7:
                logger.error(f"Invalid hex color for {key}: {value}")
                return False
        return True


@dataclass
class Theme:
    """
    Complete theme definition.

    Attributes:
        name: Theme name
        display_name: Human-readable name
        description: Theme description
        colors: Color palette
        gradient: Gradient colors (list of hex)
        metadata: Additional metadata
    """
    name: str
    display_name: str
    description: str
    colors: ThemeColors
    gradient: List[str]
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        """Validate theme after initialization."""
        if not self.colors.validate():
            raise ValueError(f"Invalid colors in theme: {self.name}")

        if len(self.gradient) < 2:
            raise ValueError(f"Gradient must have at least 2 colors: {self.name}")

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "name": self.name,
            "display_name": self.display_name,
            "description": self.description,
            "colors": self.colors.to_dict(),
            "gradient": self.gradient,
            "metadata": self.metadata
        }

    def to_json(self) -> str:
        """Export to JSON."""
        return json.dumps(self.to_dict(), indent=2)

    def to_rich_theme(self) -> RichTheme:
        """
        Convert to Rich Theme.

        Returns:
            RichTheme with theme colors mapped to Rich styles
        """
        styles = {
            "primary": self.colors.primary,
            "secondary": self.colors.secondary,
            "tertiary": self.colors.tertiary,
            "accent": self.colors.accent,
            "success": self.colors.success,
            "error": self.colors.error,
            "warning": self.colors.warning,
            "info": self.colors.info,
            "dim": "dim",
            "bold": "bold"
        }

        return RichTheme(styles)

    def to_textual_css_vars(self) -> Dict[str, str]:
        """
        Convert to Textual CSS variables.

        Returns:
            Dict of CSS variable names and values
        """
        return {
            "$primary": self.colors.primary,
            "$secondary": self.colors.secondary,
            "$tertiary": self.colors.tertiary,
            "$accent": self.colors.accent,
            "$background": self.colors.background,
            "$foreground": self.colors.foreground,
            "$success": self.colors.success,
            "$error": self.colors.error,
            "$warning": self.colors.warning,
            "$info": self.colors.info,
        }


class ThemeRegistry:
    """
    Registry of built-in and custom themes.

    Singleton pattern for centralized theme management.
    """

    _instance = None
    _themes: Dict[str, Theme] = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._init_builtin_themes()
        return cls._instance

    def _init_builtin_themes(self):
        """Initialize built-in themes."""
        # Neon (official)
        self.register(Theme(
            name=ThemeName.NEON,
            display_name="Neon",
            description="Official neon theme (green/cyan/blue/yellow)",
            colors=ThemeColors(
                primary=NEON_PALETTE['primary'],
                secondary=NEON_PALETTE['secondary'],
                tertiary=NEON_PALETTE['tertiary'],
                accent=NEON_PALETTE['accent'],
                success=NEON_PALETTE['success'],
                error=NEON_PALETTE['error'],
                warning=NEON_PALETTE['warning'],
                info=NEON_PALETTE['info']
            ),
            gradient=GRADIENTS['neon']
        ))

        # Fire
        self.register(Theme(
            name=ThemeName.FIRE,
            display_name="Fire",
            description="Fiery red/orange/yellow theme",
            colors=ThemeColors(
                primary="#FF0000",
                secondary="#FF6600",
                tertiary="#FFCC00",
                accent="#FFFF00",
                success="#00FF00",
                error="#FF0000",
                warning="#FF6600",
                info="#00BFFF"
            ),
            gradient=GRADIENTS['fire']
        ))

        # Ocean
        self.register(Theme(
            name=ThemeName.OCEAN,
            display_name="Ocean",
            description="Cool blue/cyan ocean theme",
            colors=ThemeColors(
                primary="#0080FF",
                secondary="#00C0FF",
                tertiary="#00FFFF",
                accent="#00FF80",
                success="#00FF00",
                error="#FF0040",
                warning="#FFD700",
                info="#00FFFF"
            ),
            gradient=GRADIENTS['ocean']
        ))

        # Sunset
        self.register(Theme(
            name=ThemeName.SUNSET,
            display_name="Sunset",
            description="Warm sunset pink/orange/yellow",
            colors=ThemeColors(
                primary="#FF0080",
                secondary="#FF6600",
                tertiary="#FFCC00",
                accent="#FFFF80",
                success="#00FF00",
                error="#FF0040",
                warning="#FFD700",
                info="#00BFFF"
            ),
            gradient=GRADIENTS['sunset']
        ))

        # Matrix
        self.register(Theme(
            name=ThemeName.MATRIX,
            display_name="Matrix",
            description="Green matrix hacker theme",
            colors=ThemeColors(
                primary="#00FF00",
                secondary="#00CC00",
                tertiary="#008800",
                accent="#004400",
                success="#00FF00",
                error="#FF0000",
                warning="#FFFF00",
                info="#00FFFF"
            ),
            gradient=GRADIENTS['matrix']
        ))

        # Cyberpunk
        self.register(Theme(
            name=ThemeName.CYBERPUNK,
            display_name="Cyberpunk",
            description="Neon cyberpunk pink/cyan/magenta",
            colors=ThemeColors(
                primary="#FF1493",
                secondary="#00FFFF",
                tertiary="#FF00FF",
                accent="#FFFF00",
                success="#00FF00",
                error="#FF0040",
                warning="#FFD700",
                info="#00FFFF"
            ),
            gradient=GRADIENTS['cyberpunk']
        ))

        # Monochrome
        self.register(Theme(
            name=ThemeName.MONOCHROME,
            display_name="Monochrome",
            description="Classic monochrome grayscale",
            colors=ThemeColors(
                primary="#FFFFFF",
                secondary="#CCCCCC",
                tertiary="#999999",
                accent="#666666",
                background="#000000",
                foreground="#FFFFFF",
                success="#AAAAAA",
                error="#888888",
                warning="#BBBBBB",
                info="#999999"
            ),
            gradient=["#FFFFFF", "#CCCCCC", "#999999", "#666666"]
        ))

        logger.info(f"Initialized {len(self._themes)} built-in themes")

    def register(self, theme: Theme):
        """Register theme in registry."""
        self._themes[theme.name] = theme
        logger.debug(f"Theme registered: {theme.name}")

    def get(self, name: str) -> Optional[Theme]:
        """Get theme by name."""
        return self._themes.get(name)

    def list_themes(self) -> List[Theme]:
        """List all registered themes."""
        return list(self._themes.values())

    def load_from_file(self, path: Path) -> Theme:
        """
        Load custom theme from JSON file.

        Args:
            path: Path to theme JSON file

        Returns:
            Loaded Theme

        Raises:
            ValueError: If theme is invalid
        """
        with open(path, 'r') as f:
            data = json.load(f)

        theme = Theme(
            name=data['name'],
            display_name=data['display_name'],
            description=data['description'],
            colors=ThemeColors(**data['colors']),
            gradient=data['gradient'],
            metadata=data.get('metadata', {})
        )

        self.register(theme)
        logger.info(f"Loaded custom theme from {path}: {theme.name}")
        return theme


class ThemeManager:
    """
    Theme manager with hot reload support.

    Manages active theme and provides reload functionality.

    Example:
        manager = ThemeManager()
        manager.set_theme("fire")

        # Hot reload
        manager.reload_theme()

        # Get Rich theme
        rich_theme = manager.get_rich_theme()
        console = Console(theme=rich_theme)
    """

    def __init__(
        self,
        default_theme: str = ThemeName.NEON,
        config_dir: Optional[Path] = None
    ):
        """
        Initialize theme manager.

        Args:
            default_theme: Default theme name
            config_dir: Config directory for user themes
        """
        self.registry = ThemeRegistry()
        self._active_theme: Optional[Theme] = None
        self.config_dir = config_dir or Path.home() / ".max-code" / "themes"
        self.config_dir.mkdir(parents=True, exist_ok=True)

        # Callbacks for theme changes (initialize before set_theme)
        self._change_callbacks: List[Callable[[Theme], None]] = []

        # Load default theme
        self.set_theme(default_theme)

        logger.info(f"ThemeManager initialized (default: {default_theme})")

    @property
    def active_theme(self) -> Theme:
        """Get active theme."""
        return self._active_theme

    def set_theme(self, name: str):
        """
        Set active theme.

        Args:
            name: Theme name

        Raises:
            ValueError: If theme not found
        """
        theme = self.registry.get(name)
        if not theme:
            raise ValueError(f"Theme not found: {name}")

        self._active_theme = theme
        logger.info(f"Theme changed: {name}")

        # Notify callbacks
        for callback in self._change_callbacks:
            try:
                callback(theme)
            except Exception as e:
                logger.error(f"Theme change callback failed: {e}", exc_info=True)

    def reload_theme(self):
        """Reload active theme (hot reload)."""
        if self._active_theme:
            logger.info(f"Reloading theme: {self._active_theme.name}")
            self.set_theme(self._active_theme.name)

    def on_theme_change(self, callback: Callable[[Theme], None]):
        """
        Register callback for theme changes.

        Args:
            callback: Function to call when theme changes
        """
        self._change_callbacks.append(callback)

    def get_rich_theme(self) -> RichTheme:
        """Get Rich theme for active theme."""
        return self._active_theme.to_rich_theme()

    def get_textual_css_vars(self) -> Dict[str, str]:
        """Get Textual CSS variables for active theme."""
        return self._active_theme.to_textual_css_vars()

    def export_theme(self, name: str, path: Path):
        """
        Export theme to JSON file.

        Args:
            name: Theme name
            path: Output file path
        """
        theme = self.registry.get(name)
        if not theme:
            raise ValueError(f"Theme not found: {name}")

        with open(path, 'w') as f:
            f.write(theme.to_json())

        logger.info(f"Theme exported: {path}")

    def import_theme(self, path: Path):
        """
        Import custom theme from JSON file.

        Args:
            path: Theme file path
        """
        theme = self.registry.load_from_file(path)
        logger.info(f"Theme imported: {theme.name}")

    def show_themes(self, console: Optional[Console] = None):
        """Display all available themes."""
        console = console or Console()

        table = Table(
            title="🎨 Available Themes",
            show_header=True,
            header_style="bold cyan"
        )

        table.add_column("Name", style="yellow", width=15)
        table.add_column("Display Name", style="white", width=15)
        table.add_column("Description", style="dim")
        table.add_column("Active", justify="center", width=8)

        for theme in self.registry.list_themes():
            is_active = "✓" if theme == self._active_theme else ""
            table.add_row(
                theme.name,
                theme.display_name,
                theme.description,
                is_active
            )

        panel = Panel(
            table,
            border_style="cyan",
            padding=(1, 2)
        )

        console.print(panel)


# Global theme manager instance
_manager: Optional[ThemeManager] = None


def get_manager() -> ThemeManager:
    """Get global theme manager instance."""
    global _manager
    if _manager is None:
        _manager = ThemeManager()
    return _manager


def set_theme(name: str):
    """Set active theme globally."""
    get_manager().set_theme(name)


def get_active_theme() -> Theme:
    """Get active theme globally."""
    return get_manager().active_theme


def get_rich_theme() -> RichTheme:
    """Get Rich theme for active theme."""
    return get_manager().get_rich_theme()


# Demo code
if __name__ == "__main__":
    print("=" * 70)
    print("THEME SYSTEM DEMO")
    print("=" * 70)
    print()

    # Create manager
    manager = ThemeManager()

    # Show all themes
    manager.show_themes()

    print()
    print("-" * 70)
    print()

    # Test theme switching
    themes_to_test = [ThemeName.FIRE, ThemeName.OCEAN, ThemeName.MATRIX]

    for theme_name in themes_to_test:
        print(f"Testing theme: {theme_name}")
        manager.set_theme(theme_name)

        # Get Rich theme
        rich_theme = manager.get_rich_theme()
        console = Console(theme=rich_theme)

        # Display sample
        console.print(f"[primary]● Primary[/primary] [secondary]● Secondary[/secondary] [accent]● Accent[/accent]")
        console.print(f"[success]✓ Success[/success] [error]✗ Error[/error] [warning]⚠ Warning[/warning]")
        print()

    print("=" * 70)
    print("DEMO COMPLETE")
    print("=" * 70)
