"""
Max-Code CLI Banner System

Creates a MAGNIFICENT banner with:
- ASCII art logo (PyFiglet)
- Neon green → blue → yellow gradient
- Optional cinematic effects (beams, decrypt, matrix)
- Biblical verses (contextual, optional)
- Constitutional principles status (with Nerd Fonts icons)
- Dynamic context display
- Multiple styles
- Performance optimized with caching

"In the beginning was the Word, and the Word was with God, and the Word was God"
(John 1:1)

Usage:
    from ui.banner import MaxCodeBanner

    banner = MaxCodeBanner()
    banner.show(version="3.0", context={'model': 'Claude Sonnet 4.5'})
"""

from rich.console import Console
from rich.panel import Panel
import pyfiglet
from typing import Optional, Dict, TYPE_CHECKING
from pathlib import Path
import os
import sys
import hashlib

# Lazy imports for performance
if TYPE_CHECKING:
    from rich_gradient import Gradient

class MaxCodeBanner:
    """
    Handles magnificent banner display for Max-Code CLI.

    Features:
    - Beautiful ASCII art with gradient
    - Constitutional principles status
    - Dynamic context display
    - Caching for performance
    - Multiple styles
    - Suppressible for scripts
    """

    # Neon green → blue → yellow gradient colors (OFFICIAL PALETTE)
    GRADIENT_COLORS = ['#0FFF50', '#00F0FF', '#0080FF', '#FFFF00']

    # Available ASCII art styles
    FONTS = {
        'default': 'slant',       # Gemini-style slanted (clean, horizontal) ⭐ RECOMMENDED
        'block': 'block',         # Solid block letters
        'isometric': 'isometric1',# FILLED 3D blocks
        'banner': 'banner3',      # Bold banner style
        'minimal': 'small',       # Compact for minimal mode
        'bold': 'doom',           # Bold doom style
        'tech': 'digital',        # Tech aesthetic
        'cyber': 'cybermedium',   # Cyberpunk vibe
        'colossal': 'colossal',   # HUGE filled letters
        'graffiti': 'graffiti',   # Street art style
    }

    # Constitutional principles with colors
    PRINCIPLES = [
        ("P1", "Transcendence", "violet"),
        ("P2", "Reasoning", "blue"),
        ("P3", "Care", "green"),
        ("P4", "Wisdom", "yellow"),
        ("P5", "Beauty", "magenta"),
        ("P6", "Autonomy", "cyan"),
    ]

    def __init__(self, console: Optional[Console] = None):
        """
        Initialize banner handler.

        Args:
            console: Rich Console instance (creates new if None)
        """
        self.console = console or Console()
        self._should_show = self._check_should_show()
        self._cache_dir = Path('.cache/banner_cache')
        self._cache_dir.mkdir(parents=True, exist_ok=True)

    def _check_should_show(self) -> bool:
        """
        Check if banner should be displayed.

        Respects:
        - --no-banner flag
        - --quiet/-q flag
        - MAXCODE_NO_BANNER environment variable
        - NO_COLOR environment variable
        - TTY detection (only show in interactive mode)

        Returns:
            bool: True if banner should be shown
        """
        # Check command line flags
        if '--no-banner' in sys.argv:
            return False
        if '--quiet' in sys.argv or '-q' in sys.argv:
            return False

        # Check environment variables
        if os.environ.get('MAXCODE_NO_BANNER'):
            return False

        # Only show in interactive mode (TTY)
        if not sys.stdout.isatty():
            return False

        return True

    def _get_cached_ascii_art(self, text: str, font: str) -> Optional[str]:
        """
        Get cached ASCII art or generate and cache it.

        Args:
            text: Text to convert to ASCII art
            font: PyFiglet font name

        Returns:
            str: ASCII art text
        """
        # Create cache key from text + font
        cache_key = hashlib.md5(f"{text}:{font}".encode(), usedforsecurity=False).hexdigest()
        cache_file = self._cache_dir / f"{cache_key}.txt"

        # Try to load from cache
        if cache_file.exists():
            try:
                return cache_file.read_text(encoding='utf-8')
            except (OSError, UnicodeDecodeError):
                pass  # Cache miss, regenerate

        # Generate ASCII art
        try:
            ascii_art = pyfiglet.figlet_format(text, font=font)

            # Cache for next time
            try:
                cache_file.write_text(ascii_art, encoding='utf-8')
            except (OSError, PermissionError):
                pass  # Cache write failed, not critical

            return ascii_art
        except (ImportError, AttributeError, Exception):
            # Fallback to simple text if PyFiglet fails
            return text

    def show(
        self,
        version: str = "3.0",
        context: Optional[Dict] = None,
        style: str = "default",
        effect: Optional[str] = None,
        show_verse: bool = True
    ):
        """
        Display the magnificent banner.

        Args:
            version: Version string to display
            context: Additional context (model, session, etc.)
            style: Banner style (default, minimal, bold, tech, cyber)
            effect: Optional cinematic effect ("beams", "decrypt", "matrix", None)
            show_verse: Whether to show biblical verse (default: True, respects --no-verses)
        """
        if not self._should_show:
            return

        # Get font for selected style
        font = self.FONTS.get(style, self.FONTS['default'])

        # Generate ASCII art (with caching)
        ascii_art = self._get_cached_ascii_art("MAX-CODE", font)

        # Apply cinematic effect if requested (and --no-effects not present)
        if effect and '--no-effects' not in sys.argv and not os.environ.get('MAXCODE_NO_EFFECTS'):
            try:
                from ui.effects import animate_banner
                ascii_art = animate_banner(ascii_art, effect_type=effect)
            except (ImportError, Exception):
                pass  # Fall back to gradient only

        # Apply magnificent MAXIMUS neon gradient (our own system!)
        from ui.colors import neon
        title = neon(ascii_art)

        # Display in Gemini style (clean, no borders, minimal info)
        self.console.print("\n")
        self.console.print(title, justify="center")  # Giant gradient ASCII art
        self.console.print()

        # Single minimal line: version • Constitutional AI
        self.console.print(
            f"[dim]v{version}[/dim] [cyan]•[/cyan] [dim]Constitutional AI[/dim]",
            justify="center"
        )
        self.console.print()

        # Constitutional principles (one clean line with emojis)
        self._show_principles()

        # Biblical verse (optional, minimal)
        if show_verse:
            try:
                from core.verses import get_startup_verse
                verse = get_startup_verse()
                if verse:
                    self.console.print()
                    self.console.print(verse)
            except (ImportError, Exception):
                pass

        self.console.print()

    def _show_principles(self):
        """Display constitutional principles status with beautiful colors and simple emojis."""
        # Use simple Unicode symbols that work in all terminals
        # No Nerd Fonts required - these are standard Unicode
        principle_icons = {
            'P1': '∞',   # Transcendence (infinity)
            'P2': '⚡',  # Reasoning (lightning)
            'P3': '♥',   # Care (heart)
            'P4': '◆',   # Wisdom (diamond)
            'P5': '✦',   # Beauty (star)
            'P6': '⚙',   # Autonomy (gear)
        }

        status_parts = []

        for code, name, color in self.PRINCIPLES:
            icon = principle_icons.get(code, '●')
            status_parts.append(f"[{color}]{icon}[/{color}] {code}")

        status_line = "  ".join(status_parts)
        self.console.print(f"  {status_line}", justify="center")

    def show_minimal(self, version: str = "3.0"):
        """
        Display minimal banner for script mode.

        Args:
            version: Version string to display
        """
        self.console.print(f"\nMAX-CODE CLI v{version} | Constitutional AI Framework")
        self.console.print("─" * 60)
        self.console.print()

    def show_with_status(
        self,
        version: str = "3.0",
        context: Optional[Dict] = None,
        style: str = "default",
        status_message: Optional[str] = None
    ):
        """
        Display banner with additional status message.

        Args:
            version: Version string
            context: Additional context
            style: Banner style
            status_message: Status message to display below banner
        """
        self.show(version, context, style)

        if status_message:
            self.console.print(f"[cyan]ℹ[/cyan] {status_message}\n")

    def clear_cache(self):
        """Clear ASCII art cache."""
        for cache_file in self._cache_dir.glob("*.txt"):
            try:
                cache_file.unlink()
            except (OSError, FileNotFoundError, PermissionError):
                pass

    def get_available_styles(self) -> list:
        """
        Get list of available banner styles.

        Returns:
            list: Available style names
        """
        return list(self.FONTS.keys())


# Convenience function
def show_banner(
    version: str = "3.0",
    context: Optional[Dict] = None,
    style: str = "default",
    console: Optional[Console] = None
):
    """
    Convenience function to show banner quickly.

    Args:
        version: Version string
        context: Additional context
        style: Banner style
        console: Rich Console instance
    """
    banner = MaxCodeBanner(console=console)
    banner.show(version, context, style)


def print_banner():
    """
    Helper function for Enhanced REPL - prints welcome banner with animations.

    Features:
    - ASCII art with MAXIMUS neon gradient (verde → amarelo → azul)
    - Animated initialization sequence
    - Constitutional AI status
    - MAXIMUS integration indicators

    Cinematográfico mas clean - como Apple ou Vercel + Anthropic.
    """
    console = Console()

    # ASCII art clean (não excessivo)
    logo = """
    ███╗   ███╗ █████╗ ██╗  ██╗      ██████╗ ██████╗ ██████╗ ███████╗
    ████╗ ████║██╔══██╗╚██╗██╔╝     ██╔════╝██╔═══██╗██╔══██╗██╔════╝
    ██╔████╔██║███████║ ╚███╔╝█████╗██║     ██║   ██║██║  ██║█████╗
    ██║╚██╔╝██║██╔══██║ ██╔██╗╚════╝██║     ██║   ██║██║  ██║██╔══╝
    ██║ ╚═╝ ██║██║  ██║██╔╝ ██╗     ╚██████╗╚██████╔╝██████╔╝███████╗
    ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝      ╚═════╝ ╚═════╝ ╚═════╝ ╚══════╝
    """

    # Apply MAXIMUS neon gradient (verde → amarelo → azul)
    from ui.colors import neon
    logo_gradient = neon(logo)

    # Info concisa
    info = (
        "[bold cyan]MAXIMUS SHELL[/bold cyan] [dim]v1.0.0[/dim]\n"
        "[dim]AGI Development System powered by Claude & Constitutional AI[/dim]\n\n"
        "[green]●[/green] 8 specialized agents  "
        "[blue]●[/blue] Constitutional AI  "
        "[magenta]●[/magenta] MAXIMUS ecosystem"
    )

    # Panel com gradiente neon (Padrão Pagani: clean, minimal, memorável)
    from rich import box
    panel = Panel(
        f"{logo_gradient}\n\n{info}",
        border_style="cyan",
        box=box.DOUBLE,
        padding=(1, 2)
    )

    console.print("\n")
    console.print(panel)

    # Animated initialization sequence
    import time
    with console.status("[bold green]Initializing...", spinner="dots") as status:
        time.sleep(0.3)
        status.update("[bold yellow]⚡ Loading neural networks...")
        time.sleep(0.3)
        status.update("[bold cyan]🔗 Connecting to MAXIMUS ecosystem...")
        time.sleep(0.3)
        status.update("[bold magenta]⚖️  Loading constitutional principles...")
        time.sleep(0.3)

    console.print("[bold green]✨ System ready[/bold green]")
    console.print()


# Demo/test code
if __name__ == "__main__":
    import time

    print("=" * 70)
    print("MAX-CODE CLI BANNER DEMONSTRATION")
    print("=" * 70)
    print()

    # Test 1: Default banner
    print("1. DEFAULT STYLE:")
    banner = MaxCodeBanner()
    banner.show(
        version="3.0",
        context={
            'model': 'Claude Sonnet 4.5',
            'session': 'demo_abc123'
        },
        style='default'
    )

    time.sleep(2)

    # Test 2: Bold style
    print("\n2. BOLD STYLE:")
    banner.show(
        version="3.0",
        context={'model': 'Claude Sonnet 4.5'},
        style='bold'
    )

    time.sleep(2)

    # Test 3: Tech style
    print("\n3. TECH STYLE:")
    banner.show(
        version="3.0",
        context={'model': 'Claude Sonnet 4.5'},
        style='tech'
    )

    time.sleep(2)

    # Test 4: Minimal
    print("\n4. MINIMAL MODE:")
    banner.show_minimal("3.0")

    # Test 5: Available styles
    print("\n5. AVAILABLE STYLES:")
    print(f"   {', '.join(banner.get_available_styles())}")

    print("\n" + "=" * 70)
    print("DEMO COMPLETE")
    print("=" * 70)
