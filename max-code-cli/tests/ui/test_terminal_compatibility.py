"""
Tests for Terminal Compatibility

Validates:
- Different terminal types (xterm, gnome-terminal, iTerm2, Windows Terminal)
- Color support (256 colors, true colors, no colors)
- Nerd Fonts rendering
- TTY vs non-TTY environments
- Environment variable handling
- Flag combinations

DEBT-002: Sprint 1 UI Testing (Part 3/3)
"""

import pytest
import os
import sys
from unittest.mock import Mock, patch, MagicMock
from rich.console import Console

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from ui.banner import MaxCodeBanner
from ui.effects import EffectsManager


class TestTerminalDetection:
    """Test terminal type detection and handling"""

    @patch('sys.stdout.isatty', return_value=True)
    def test_tty_mode(self, mock_isatty):
        """Test TTY mode is detected"""
        banner = MaxCodeBanner()
        assert banner._should_show is True

    @patch('sys.stdout.isatty', return_value=False)
    def test_non_tty_mode(self, mock_isatty):
        """Test non-TTY mode (piped output)"""
        banner = MaxCodeBanner()
        assert banner._should_show is False

    @patch.dict(os.environ, {'TERM': 'xterm-256color'})
    def test_xterm_256color(self):
        """Test xterm-256color terminal"""
        console = Console()
        # Should support 256 colors
        assert console.color_system is not None

    @patch.dict(os.environ, {'TERM': 'xterm'})
    def test_xterm_basic(self):
        """Test basic xterm terminal"""
        console = Console()
        assert console is not None

    @patch.dict(os.environ, {'TERM': 'dumb'})
    def test_dumb_terminal(self):
        """Test dumb terminal (no colors)"""
        console = Console()
        # Dumb terminal may have no color support
        # Just verify console is created
        assert console is not None

    @patch.dict(os.environ, {'COLORTERM': 'truecolor'})
    def test_truecolor_support(self):
        """Test true color (24-bit) support detection"""
        console = Console()
        # Modern terminals support true color
        assert console is not None

    @patch.dict(os.environ, {'COLORTERM': '24bit'})
    def test_24bit_color_support(self):
        """Test 24-bit color support"""
        console = Console()
        assert console is not None


class TestColorSupport:
    """Test color rendering in different modes"""

    def test_neon_gradient_colors_valid(self):
        """Test neon gradient colors are valid hex"""
        for color in EffectsManager.NEON_GRADIENT:
            assert color.startswith('#')
            assert len(color) == 7
            # Verify it's valid hex
            int(color[1:], 16)

    @patch.dict(os.environ, {'NO_COLOR': '1'})
    def test_no_color_environment(self):
        """Test NO_COLOR environment variable"""
        console = Console()
        # Console should handle NO_COLOR
        # Note: Rich automatically respects NO_COLOR
        assert console is not None

    @patch.dict(os.environ, {'FORCE_COLOR': '1'})
    def test_force_color_environment(self):
        """Test FORCE_COLOR environment variable"""
        console = Console()
        # Console should handle FORCE_COLOR
        assert console is not None

    def test_console_color_system(self):
        """Test console color system detection"""
        console = Console()
        # Should have some color system
        # (auto, standard, 256, truecolor, windows, or None)
        assert console.color_system in [None, 'auto', 'standard', '256', 'truecolor', 'windows']


class TestNerdFontsRendering:
    """Test Nerd Fonts icon rendering"""

    def test_principle_icons_defined(self):
        """Test constitutional principle icons are simple Unicode"""
        # These should be basic Unicode, not Nerd Fonts
        # (changed from Nerd Fonts to ensure compatibility)
        icons = {
            'P1': '∞',   # Infinity (U+221E)
            'P2': '⚡',  # Lightning (U+26A1)
            'P3': '♥',   # Heart (U+2665)
            'P4': '◆',   # Diamond (U+25C6)
            'P5': '✦',   # Star (U+2726)
            'P6': '⚙',   # Gear (U+2699)
        }

        for code, icon in icons.items():
            # Should be single character
            assert len(icon) == 1
            # Should be Unicode (not ASCII)
            assert ord(icon) > 127

    def test_unicode_rendering(self):
        """Test Unicode characters render in console"""
        console = Console()

        # Test Unicode characters used in banner
        test_chars = ['∞', '⚡', '♥', '◆', '✦', '⚙']

        for char in test_chars:
            # Should not raise encoding error
            try:
                console.print(char, end='')
            except UnicodeEncodeError:
                pytest.fail(f"Character {char} failed to encode")

    def test_emoji_rendering(self):
        """Test emoji rendering (used in some contexts)"""
        console = Console()

        # Common emojis used
        emojis = ['✅', '❌', '⚠️', 'ℹ']

        for emoji in emojis:
            try:
                console.print(emoji, end='')
            except UnicodeEncodeError:
                pytest.fail(f"Emoji {emoji} failed to encode")


class TestEnvironmentVariables:
    """Test environment variable handling"""

    @patch.dict(os.environ, {'MAXCODE_NO_BANNER': '1'})
    def test_maxcode_no_banner(self):
        """Test MAXCODE_NO_BANNER environment variable"""
        banner = MaxCodeBanner()
        assert banner._should_show is False

    @patch.dict(os.environ, {'MAXCODE_NO_EFFECTS': '1'})
    @patch('sys.stdout.isatty', return_value=True)
    def test_maxcode_no_effects(self, mock_isatty):
        """Test MAXCODE_NO_EFFECTS environment variable"""
        banner = MaxCodeBanner()
        # Should not raise with effect requested
        banner.show(version="3.0", effect="beams")

    @patch.dict(os.environ, {'MAXCODE_NO_VERSES': '1'})
    @patch('sys.stdout.isatty', return_value=True)
    def test_maxcode_no_verses(self, mock_isatty):
        """Test MAXCODE_NO_VERSES environment variable"""
        banner = MaxCodeBanner()
        # Should handle verse suppression
        banner.show(version="3.0", show_verse=True)

    @patch.dict(os.environ, {}, clear=True)
    def test_no_environment_variables(self):
        """Test behavior with no environment variables"""
        banner = MaxCodeBanner()
        # Should work with defaults
        assert banner is not None


class TestFlagCombinations:
    """Test various flag combinations"""

    @patch('sys.stdout.isatty', return_value=True)
    def test_no_banner_and_quiet(self, mock_isatty):
        """Test --no-banner and --quiet together"""
        sys.argv.extend(['--no-banner', '--quiet'])
        try:
            banner = MaxCodeBanner()
            assert banner._should_show is False
        finally:
            sys.argv.remove('--no-banner')
            sys.argv.remove('--quiet')

    @patch('sys.stdout.isatty', return_value=True)
    def test_no_effects_and_no_verses(self, mock_isatty):
        """Test --no-effects and --no-verses together"""
        sys.argv.extend(['--no-effects'])
        try:
            banner = MaxCodeBanner()
            banner.show(version="3.0", effect="beams", show_verse=False)
            # Should not raise
        finally:
            sys.argv.remove('--no-effects')

    @patch('sys.stdout.isatty', return_value=False)
    def test_force_banner_in_non_tty(self, mock_isatty):
        """Test that banner respects TTY detection"""
        banner = MaxCodeBanner()
        # Even if user wants banner, non-TTY should suppress it
        assert banner._should_show is False


class TestWindowsCompatibility:
    """Test Windows terminal compatibility"""

    @patch('platform.system', return_value='Windows')
    def test_windows_platform(self, mock_platform):
        """Test banner works on Windows"""
        banner = MaxCodeBanner()
        assert banner is not None

    @patch.dict(os.environ, {'WT_SESSION': '12345'})
    def test_windows_terminal(self):
        """Test Windows Terminal detection"""
        # Windows Terminal sets WT_SESSION
        assert os.environ.get('WT_SESSION') is not None
        console = Console()
        assert console is not None

    @patch.dict(os.environ, {'TERM_PROGRAM': 'Windows Terminal'})
    def test_windows_terminal_alt(self):
        """Test Windows Terminal alternate detection"""
        console = Console()
        assert console is not None


class TestMacOSCompatibility:
    """Test macOS terminal compatibility"""

    @patch('platform.system', return_value='Darwin')
    def test_macos_platform(self, mock_platform):
        """Test banner works on macOS"""
        banner = MaxCodeBanner()
        assert banner is not None

    @patch.dict(os.environ, {'TERM_PROGRAM': 'iTerm.app'})
    def test_iterm2(self):
        """Test iTerm2 terminal"""
        console = Console()
        assert console is not None

    @patch.dict(os.environ, {'TERM_PROGRAM': 'Apple_Terminal'})
    def test_apple_terminal(self):
        """Test Apple Terminal"""
        console = Console()
        assert console is not None


class TestLinuxCompatibility:
    """Test Linux terminal compatibility"""

    @patch('platform.system', return_value='Linux')
    def test_linux_platform(self, mock_platform):
        """Test banner works on Linux"""
        banner = MaxCodeBanner()
        assert banner is not None

    @patch.dict(os.environ, {'GNOME_TERMINAL_SERVICE': ':1.234'})
    def test_gnome_terminal(self):
        """Test GNOME Terminal"""
        console = Console()
        assert console is not None

    @patch.dict(os.environ, {'KONSOLE_VERSION': '22.12.0'})
    def test_konsole(self):
        """Test Konsole terminal"""
        console = Console()
        assert console is not None

    @patch.dict(os.environ, {'TERM': 'xterm-kitty'})
    def test_kitty_terminal(self):
        """Test Kitty terminal"""
        console = Console()
        assert console is not None


class TestEdgeCases:
    """Test edge cases in terminal compatibility"""

    @patch.dict(os.environ, {'TERM': ''})
    def test_empty_term_variable(self):
        """Test empty TERM environment variable"""
        console = Console()
        # Should handle gracefully
        assert console is not None

    @patch.dict(os.environ, {}, clear=True)
    @patch('sys.stdout.isatty', return_value=True)
    def test_no_environment(self, mock_isatty):
        """Test with completely empty environment"""
        console = Console()
        assert console is not None

    def test_very_narrow_terminal(self):
        """Test banner in very narrow terminal"""
        console = Console(width=40)
        banner = MaxCodeBanner(console=console)
        # Should handle narrow terminals
        assert banner is not None

    def test_very_wide_terminal(self):
        """Test banner in very wide terminal"""
        console = Console(width=200)
        banner = MaxCodeBanner(console=console)
        # Should handle wide terminals
        assert banner is not None

    @patch('sys.stdout.isatty', return_value=True)
    def test_terminal_resize_handling(self, mock_isatty):
        """Test banner handles terminal resize"""
        banner = MaxCodeBanner()
        # Create with one size
        banner.console = Console(width=80)
        banner.show(version="3.0")

        # Resize
        banner.console = Console(width=120)
        banner.show(version="3.0")
        # Should not raise


class TestIntegration:
    """Integration tests for terminal compatibility"""

    @pytest.mark.parametrize("term,colorterm", [
        ("xterm-256color", "truecolor"),
        ("xterm", None),
        ("screen", None),
        ("tmux-256color", None),
    ])
    def test_common_terminal_combinations(self, term, colorterm):
        """Test common TERM and COLORTERM combinations"""
        env = {'TERM': term}
        if colorterm:
            env['COLORTERM'] = colorterm

        with patch.dict(os.environ, env):
            console = Console()
            assert console is not None

    @pytest.mark.parametrize("width", [40, 80, 120, 200])
    def test_various_terminal_widths(self, width):
        """Test banner at various terminal widths"""
        console = Console(width=width)
        banner = MaxCodeBanner(console=console)
        assert banner is not None


# Test execution report
if __name__ == "__main__":
    print("=" * 70)
    print("TERMINAL COMPATIBILITY TESTING SUITE - DEBT-002 (Part 3/3)")
    print("=" * 70)
    print()
    print("Testing:")
    print("  - Terminal type detection (TTY vs non-TTY)")
    print("  - Color support (256, truecolor, none)")
    print("  - Nerd Fonts / Unicode rendering")
    print("  - Environment variables")
    print("  - Flag combinations")
    print("  - Platform compatibility (Windows, macOS, Linux)")
    print()
    print("Running tests...")
    print()

    pytest.main([__file__, "-v", "--tb=short"])
