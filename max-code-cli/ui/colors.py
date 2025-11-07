"""
MAXIMUS SHELL - Color System v3.0
Tri-color neon gradient system for spectacular terminal UI.

Official MAXIMUS Neon Palette:
- PRIMARY: #00FF41 (neon green) → #FFFF00 (electric yellow) → #00D4FF (cyan blue)
- CONSTITUTIONAL: P1-P6 principle colors with semantic meaning
- ACCENTS: Status colors, highlights, warnings

Technical Implementation:
- RGB interpolation for smooth gradients
- Rich-compatible color codes
- Fallback for non-RGB terminals
- Performance-optimized with caching

"Let there be light; and there was light. And God saw that the light was good."
(Genesis 1:3-4)
"""

from typing import List, Tuple, Optional
from dataclasses import dataclass
import colorsys


@dataclass
class ColorPalette:
    """
    MAXIMUS color palette with semantic meaning.

    Each color group serves a specific purpose in the Constitutional AI framework.
    """

    # ═══════════════════════════════════════════════════════════════════════
    # PRIMARY NEON GRADIENT (Official MAXIMUS Identity)
    # ═══════════════════════════════════════════════════════════════════════
    NEON_GREEN = "#00FF41"      # Start: Digital awakening, Matrix-style
    ELECTRIC_YELLOW = "#FFFF00"  # Middle: Energy peak, divine illumination
    CYAN_BLUE = "#00D4FF"        # End: Transcendence, sky connection

    # ═══════════════════════════════════════════════════════════════════════
    # CONSTITUTIONAL PRINCIPLES (P1-P6)
    # ═══════════════════════════════════════════════════════════════════════
    P1_TRANSCENDENCE = "#9D4EDD"  # Violet: Connection to divine
    P2_REASONING = "#3A86FF"      # Blue: Logic and truth
    P3_CARE = "#06D6A0"           # Green: Compassion and empathy
    P4_WISDOM = "#FFD60A"         # Yellow: Knowledge and discernment
    P5_BEAUTY = "#FF006E"         # Magenta: Aesthetics and harmony
    P6_AUTONOMY = "#00F5FF"       # Cyan: Freedom and self-determination

    # ═══════════════════════════════════════════════════════════════════════
    # STATUS & SEMANTIC COLORS
    # ═══════════════════════════════════════════════════════════════════════
    SUCCESS = "#00FF88"
    WARNING = "#FFB347"
    ERROR = "#FF3B30"
    INFO = "#00D4FF"

    # Agent states
    AGENT_ACTIVE = "#00FF41"
    AGENT_IDLE = "#808080"
    AGENT_THINKING = "#FFD60A"

    # ═══════════════════════════════════════════════════════════════════════
    # UI ELEMENTS
    # ═══════════════════════════════════════════════════════════════════════
    BACKGROUND = "#0A0E14"
    PANEL_BG = "#131821"
    BORDER = "#1E2433"
    TEXT_PRIMARY = "#E6EDF3"
    TEXT_SECONDARY = "#8B949E"
    TEXT_DIM = "#6E7681"


class GradientColors:
    """
    Gradient color generator for MAXIMUS neon effects.

    Implements smooth RGB interpolation for tri-color gradients with caching.

    Usage:
        gradient = GradientColors()
        colors = gradient.neon_gradient(steps=50)
        text = gradient.apply_gradient("MAXIMUS SHELL", colors)
    """

    def __init__(self, palette: Optional[ColorPalette] = None):
        """
        Initialize gradient generator.

        Args:
            palette: Color palette to use (defaults to ColorPalette)
        """
        self.palette = palette or ColorPalette()
        self._cache = {}

    def hex_to_rgb(self, hex_color: str) -> Tuple[int, int, int]:
        """
        Convert hex color to RGB tuple.

        Args:
            hex_color: Hex color string (e.g., "#00FF41")

        Returns:
            RGB tuple (r, g, b) with values 0-255
        """
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

    def rgb_to_hex(self, rgb: Tuple[int, int, int]) -> str:
        """
        Convert RGB tuple to hex color.

        Args:
            rgb: RGB tuple (r, g, b) with values 0-255

        Returns:
            Hex color string (e.g., "#00FF41")
        """
        return f"#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}"

    def interpolate_color(
        self,
        color1: str,
        color2: str,
        factor: float
    ) -> str:
        """
        Interpolate between two colors.

        Args:
            color1: Starting hex color
            color2: Ending hex color
            factor: Interpolation factor (0.0 to 1.0)

        Returns:
            Interpolated hex color
        """
        rgb1 = self.hex_to_rgb(color1)
        rgb2 = self.hex_to_rgb(color2)

        # Linear RGB interpolation
        rgb = tuple(
            int(rgb1[i] + (rgb2[i] - rgb1[i]) * factor)
            for i in range(3)
        )

        return self.rgb_to_hex(rgb)

    def neon_gradient(
        self,
        steps: int = 100,
        colors: Optional[List[str]] = None
    ) -> List[str]:
        """
        Generate MAXIMUS tri-color neon gradient.

        Args:
            steps: Number of color steps to generate
            colors: Custom color list (defaults to NEON_GREEN → YELLOW → CYAN)

        Returns:
            List of hex colors forming smooth gradient
        """
        # Use cache for performance
        cache_key = f"neon_{steps}_{colors}"
        if cache_key in self._cache:
            return self._cache[cache_key]

        if colors is None:
            colors = [
                self.palette.NEON_GREEN,
                self.palette.ELECTRIC_YELLOW,
                self.palette.CYAN_BLUE
            ]

        if len(colors) < 2:
            return colors * steps

        gradient = []
        segments = len(colors) - 1
        steps_per_segment = steps // segments

        for i in range(segments):
            start_color = colors[i]
            end_color = colors[i + 1]

            # Handle last segment to reach exact step count
            segment_steps = steps_per_segment
            if i == segments - 1:
                segment_steps = steps - len(gradient)

            for j in range(segment_steps):
                factor = j / segment_steps if segment_steps > 0 else 0
                color = self.interpolate_color(start_color, end_color, factor)
                gradient.append(color)

        self._cache[cache_key] = gradient
        return gradient

    def apply_gradient(
        self,
        text: str,
        colors: Optional[List[str]] = None,
        rich_markup: bool = True
    ) -> str:
        """
        Apply gradient colors to text.

        Args:
            text: Text to colorize
            colors: Color list (generates neon gradient if None)
            rich_markup: Use Rich markup (True) or ANSI codes (False)

        Returns:
            Colorized text with gradient
        """
        if colors is None:
            colors = self.neon_gradient(steps=len(text))

        # Adjust colors to match text length
        if len(colors) < len(text):
            # Repeat gradient if too short
            colors = (colors * ((len(text) // len(colors)) + 1))[:len(text)]
        elif len(colors) > len(text):
            # Sample evenly if too long
            step = len(colors) / len(text)
            colors = [colors[int(i * step)] for i in range(len(text))]

        if rich_markup:
            # Use Rich markup format
            result = ""
            for char, color in zip(text, colors):
                if char.isspace():
                    result += char
                else:
                    result += f"[{color}]{char}[/{color}]"
            return result
        else:
            # Use ANSI escape codes (fallback)
            result = ""
            for char, color in zip(text, colors):
                if char.isspace():
                    result += char
                else:
                    rgb = self.hex_to_rgb(color)
                    result += f"\033[38;2;{rgb[0]};{rgb[1]};{rgb[2]}m{char}\033[0m"
            return result

    def constitutional_colors(self) -> List[Tuple[str, str, str]]:
        """
        Get Constitutional Principles colors (P1-P6).

        Returns:
            List of (code, name, color) tuples
        """
        return [
            ("P1", "Transcendence", self.palette.P1_TRANSCENDENCE),
            ("P2", "Reasoning", self.palette.P2_REASONING),
            ("P3", "Care", self.palette.P3_CARE),
            ("P4", "Wisdom", self.palette.P4_WISDOM),
            ("P5", "Beauty", self.palette.P5_BEAUTY),
            ("P6", "Autonomy", self.palette.P6_AUTONOMY),
        ]


# ═══════════════════════════════════════════════════════════════════════════
# CONVENIENCE FUNCTIONS (for quick usage)
# ═══════════════════════════════════════════════════════════════════════════

_gradient_instance = None

def get_gradient() -> GradientColors:
    """Get singleton gradient instance (cached)."""
    global _gradient_instance
    if _gradient_instance is None:
        _gradient_instance = GradientColors()
    return _gradient_instance


def neon(text: str, steps: Optional[int] = None) -> str:
    """
    Quick function to apply MAXIMUS neon gradient to text.

    Args:
        text: Text to colorize
        steps: Number of gradient steps (defaults to text length)

    Returns:
        Text with neon gradient applied

    Example:
        >>> from ui.colors import neon
        >>> print(neon("MAXIMUS SHELL"))
    """
    gradient = get_gradient()
    colors = gradient.neon_gradient(steps=steps or len(text))
    return gradient.apply_gradient(text, colors)


def constitutional_gradient(text: str) -> str:
    """
    Apply gradient using P1-P6 Constitutional colors.

    Args:
        text: Text to colorize

    Returns:
        Text with constitutional gradient
    """
    gradient = get_gradient()
    colors = gradient.neon_gradient(
        steps=len(text),
        colors=[
            gradient.palette.P1_TRANSCENDENCE,
            gradient.palette.P2_REASONING,
            gradient.palette.P3_CARE,
            gradient.palette.P4_WISDOM,
            gradient.palette.P5_BEAUTY,
            gradient.palette.P6_AUTONOMY,
        ]
    )
    return gradient.apply_gradient(text, colors)


# ═══════════════════════════════════════════════════════════════════════════
# DEMO / TESTING
# ═══════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    from rich.console import Console

    console = Console()
    gradient = GradientColors()

    console.print("\n" + "=" * 70)
    console.print("MAXIMUS SHELL - COLOR SYSTEM DEMONSTRATION")
    console.print("=" * 70 + "\n")

    # Test 1: Neon gradient
    console.print("1. NEON GRADIENT (Official MAXIMUS Identity):")
    neon_text = gradient.apply_gradient("MAXIMUS SHELL - SPECTACULAR TERMINAL",
                                         gradient.neon_gradient(steps=100))
    console.print(f"   {neon_text}\n")

    # Test 2: Constitutional gradient
    console.print("2. CONSTITUTIONAL GRADIENT (P1-P6):")
    const_text = constitutional_gradient("Constitutional AI Framework")
    console.print(f"   {const_text}\n")

    # Test 3: Quick neon() function
    console.print("3. QUICK neon() FUNCTION:")
    console.print(f"   {neon('AGI Development System')}\n")

    # Test 4: Constitutional colors
    console.print("4. CONSTITUTIONAL PRINCIPLES:")
    for code, name, color in gradient.constitutional_colors():
        console.print(f"   [{color}]●[/{color}] {code}: {name}")

    console.print("\n" + "=" * 70)
    console.print("DEMO COMPLETE - Colors ready for MAXIMUS SHELL")
    console.print("=" * 70 + "\n")
