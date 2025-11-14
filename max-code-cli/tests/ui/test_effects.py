"""
Tests for Effects System (ui/effects.py)

Validates:
- All effect types (beams, decrypt, matrix, slide)
- Performance (<500ms target per effect)
- Gradient colors (neon palette)
- Animation output
- Convenience functions
- Error handling

DEBT-002: Sprint 1 UI Testing (Part 2/3)
"""

import pytest
import sys
import time
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path


from ui.effects import (
    EffectsManager,
    animate_banner,
    flash_success,
    flash_warning,
    flash_error
)


class TestEffectsManager:
    """Test suite for EffectsManager class"""

    def test_neon_colors_defined(self):
        """Test neon color palette is defined"""
        assert len(EffectsManager.NEON_GRADIENT) == 4
        assert EffectsManager.NEON_GREEN == '#0FFF50'
        assert EffectsManager.NEON_CYAN == '#00F0FF'
        assert EffectsManager.NEON_BLUE == '#0080FF'
        assert EffectsManager.NEON_YELLOW == '#FFFF00'

        # Verify all colors are hex format
        for color in EffectsManager.NEON_GRADIENT:
            assert color.startswith('#')
            assert len(color) == 7

    def test_matrix_colors_defined(self):
        """Test matrix green colors are defined"""
        assert len(EffectsManager.MATRIX_GREEN) == 3
        assert all(color.startswith('#') for color in EffectsManager.MATRIX_GREEN)
        assert all('00' in color for color in EffectsManager.MATRIX_GREEN)  # All have green

    @pytest.mark.slow
    def test_beams_effect(self):
        """Test beams effect works"""
        text = "TEST"
        result = EffectsManager.beams(text)

        # Should return some text (animated or original)
        assert result is not None
        assert isinstance(result, str)
        assert len(result) >= len(text)

    @pytest.mark.slow
    def test_beams_with_custom_gradient(self):
        """Test beams with custom gradient"""
        text = "CUSTOM"
        custom_gradient = ['#FF0000', '#00FF00', '#0000FF']

        result = EffectsManager.beams(text, gradient=custom_gradient)

        assert result is not None
        assert isinstance(result, str)

    @pytest.mark.slow
    def test_decrypt_effect(self):
        """Test decrypt effect works"""
        text = "SECRET"
        result = EffectsManager.decrypt(text)

        assert result is not None
        assert isinstance(result, str)
        assert len(result) >= len(text)

    @pytest.mark.slow
    def test_decrypt_with_custom_gradient(self):
        """Test decrypt with custom gradient"""
        text = "DATA"
        custom_gradient = ['#00FF00', '#008800']

        result = EffectsManager.decrypt(text, gradient=custom_gradient)

        assert result is not None
        assert isinstance(result, str)

    @pytest.mark.slow
    def test_slide_effect_left(self):
        """Test slide effect (left direction)"""
        text = "SLIDE"
        result = EffectsManager.slide(text, direction="left")

        assert result is not None
        assert isinstance(result, str)

    @pytest.mark.slow
    def test_slide_effect_right(self):
        """Test slide effect (right direction)"""
        text = "SLIDE"
        result = EffectsManager.slide(text, direction="right")

        assert result is not None
        assert isinstance(result, str)

    @pytest.mark.slow
    def test_slide_with_custom_gradient(self):
        """Test slide with custom gradient"""
        text = "MOVE"
        custom_gradient = ['#FF00FF', '#00FFFF']

        result = EffectsManager.slide(text, gradient=custom_gradient)

        assert result is not None
        assert isinstance(result, str)

    @pytest.mark.slow
    def test_matrix_rain_effect(self):
        """Test matrix rain effect works"""
        text = "MATRIX"
        result = EffectsManager.matrix_rain(text)

        assert result is not None
        assert isinstance(result, str)

    def test_quick_flash(self):
        """Test quick flash effect"""
        text = "FLASH"
        result = EffectsManager.quick_flash(text)

        assert result is not None
        assert isinstance(result, str)
        # Flash currently returns text as-is (animation would need loop)
        assert result == text

    def test_quick_flash_with_custom_color(self):
        """Test quick flash with custom color"""
        text = "COLOR"
        result = EffectsManager.quick_flash(text, color="#FF0000")

        assert result is not None
        assert isinstance(result, str)


class TestConvenienceFunctions:
    """Test convenience animation functions"""

    @pytest.mark.slow
    def test_animate_banner_beams(self):
        """Test animate_banner with beams effect"""
        text = "BANNER"
        result = animate_banner(text, effect_type="beams")

        assert result is not None
        assert isinstance(result, str)

    @pytest.mark.slow
    def test_animate_banner_decrypt(self):
        """Test animate_banner with decrypt effect"""
        text = "BANNER"
        result = animate_banner(text, effect_type="decrypt")

        assert result is not None
        assert isinstance(result, str)

    @pytest.mark.slow
    def test_animate_banner_matrix(self):
        """Test animate_banner with matrix effect"""
        text = "BANNER"
        result = animate_banner(text, effect_type="matrix")

        assert result is not None
        assert isinstance(result, str)

    @pytest.mark.slow
    def test_animate_banner_slide(self):
        """Test animate_banner with slide effect"""
        text = "BANNER"
        result = animate_banner(text, effect_type="slide")

        assert result is not None
        assert isinstance(result, str)

    def test_animate_banner_no_effect(self):
        """Test animate_banner with no effect (returns original)"""
        text = "PLAIN"
        result = animate_banner(text, effect_type="none")

        # Should return original text if effect unknown
        assert result == text

    def test_animate_banner_invalid_effect(self):
        """Test animate_banner with invalid effect type"""
        text = "INVALID"
        result = animate_banner(text, effect_type="invalid_effect_type")

        # Should return original text
        assert result == text

    def test_flash_success(self):
        """Test flash_success convenience function"""
        text = "SUCCESS"
        result = flash_success(text)

        assert result is not None
        assert isinstance(result, str)

    def test_flash_warning(self):
        """Test flash_warning convenience function"""
        text = "WARNING"
        result = flash_warning(text)

        assert result is not None
        assert isinstance(result, str)

    def test_flash_error(self):
        """Test flash_error convenience function"""
        text = "ERROR"
        result = flash_error(text)

        assert result is not None
        assert isinstance(result, str)


class TestPerformance:
    """Performance tests for effects system"""

    @pytest.mark.benchmark
    @pytest.mark.slow
    def test_beams_performance(self):
        """Test beams effect completes in <500ms"""
        text = "PERFORMANCE"

        start = time.time()
        EffectsManager.beams(text)
        elapsed = time.time() - start

        # Target: <500ms per effect
        assert elapsed < 0.5, f"Beams effect took {elapsed:.3f}s (target: <0.5s)"

    @pytest.mark.benchmark
    @pytest.mark.slow
    def test_decrypt_performance(self):
        """Test decrypt effect completes in <500ms"""
        text = "PERFORMANCE"

        start = time.time()
        EffectsManager.decrypt(text)
        elapsed = time.time() - start

        assert elapsed < 0.5, f"Decrypt effect took {elapsed:.3f}s (target: <0.5s)"

    @pytest.mark.benchmark
    @pytest.mark.slow
    def test_slide_performance(self):
        """Test slide effect completes in <500ms"""
        text = "PERFORMANCE"

        start = time.time()
        EffectsManager.slide(text)
        elapsed = time.time() - start

        assert elapsed < 0.5, f"Slide effect took {elapsed:.3f}s (target: <0.5s)"

    @pytest.mark.benchmark
    @pytest.mark.slow
    def test_matrix_performance(self):
        """Test matrix effect completes in reasonable time (<1s)"""
        text = "PERFORMANCE"

        start = time.time()
        EffectsManager.matrix_rain(text)
        elapsed = time.time() - start

        # Matrix is more complex, allow up to 1s
        assert elapsed < 1.0, f"Matrix effect took {elapsed:.3f}s (target: <1.0s)"

    @pytest.mark.benchmark
    def test_quick_flash_performance(self):
        """Test quick flash is instant (<10ms)"""
        text = "FLASH"

        start = time.time()
        EffectsManager.quick_flash(text)
        elapsed = time.time() - start

        # Flash should be nearly instant
        assert elapsed < 0.01, f"Quick flash took {elapsed:.3f}s (target: <0.01s)"

    @pytest.mark.benchmark
    @pytest.mark.slow
    def test_animate_banner_performance(self):
        """Test animate_banner completes in <500ms"""
        text = "BANNER TEST"

        start = time.time()
        animate_banner(text, effect_type="beams")
        elapsed = time.time() - start

        assert elapsed < 0.5, f"animate_banner took {elapsed:.3f}s (target: <0.5s)"


class TestEdgeCases:
    """Test edge cases and error handling"""

    def test_empty_text(self):
        """Test effects handle empty text"""
        result = EffectsManager.quick_flash("")
        assert result == ""

    @pytest.mark.slow
    def test_long_text_beams(self):
        """Test beams with longer text"""
        text = "THIS IS A LONGER TEXT TO TEST PERFORMANCE WITH MORE CHARACTERS"
        result = EffectsManager.beams(text)

        assert result is not None
        assert len(result) > 0

    @pytest.mark.slow
    def test_multiline_text(self):
        """Test effects with multiline text"""
        text = "LINE1\nLINE2\nLINE3"
        result = EffectsManager.beams(text)

        assert result is not None
        assert len(result) > 0

    def test_unicode_text(self):
        """Test effects with unicode characters"""
        text = "UNICODE: ∞ ⚡ ♥ ◆ ✦ ⚙"
        result = EffectsManager.quick_flash(text)

        # Quick flash should handle unicode
        assert result is not None

    @pytest.mark.slow
    def test_special_characters(self):
        """Test effects with special characters"""
        text = "SPECIAL: !@#$%^&*()"
        result = EffectsManager.beams(text)

        assert result is not None

    def test_gradient_validation(self):
        """Test gradient colors are valid hex"""
        for color in EffectsManager.NEON_GRADIENT:
            # Should be 7 chars (#RRGGBB)
            assert len(color) == 7
            assert color.startswith('#')
            # Should be valid hex
            int(color[1:], 16)  # Raises ValueError if invalid

        for color in EffectsManager.MATRIX_GREEN:
            assert len(color) == 7
            assert color.startswith('#')
            int(color[1:], 16)

    @pytest.mark.slow
    def test_effect_error_handling(self):
        """Test effects handle errors gracefully"""
        # Mock effect to raise exception
        with patch('terminaltexteffects.effects.effect_beams.Beams', side_effect=Exception("Effect error")):
            with pytest.raises(Exception):
                EffectsManager.beams("ERROR")

        # This is expected - effects can fail, should be handled by caller


class TestIntegration:
    """Integration tests for effects with banner system"""

    @pytest.mark.slow
    def test_effects_with_banner_ascii_art(self):
        """Test effects work with banner ASCII art"""
        # Simulate banner ASCII art
        banner_text = """
    ███╗   ███╗ █████╗ ██╗  ██╗
    ████╗ ████║██╔══██╗╚██╗██╔╝
    ██╔████╔██║███████║ ╚███╔╝
    """

        result = animate_banner(banner_text, effect_type="beams")

        assert result is not None
        assert len(result) > 0

    @pytest.mark.slow
    def test_all_effects_with_same_text(self):
        """Test all effects work with the same text"""
        text = "MAXCODE"

        effects = ["beams", "decrypt", "matrix", "slide"]

        for effect_type in effects:
            result = animate_banner(text, effect_type=effect_type)
            assert result is not None, f"Effect {effect_type} failed"
            assert len(result) > 0, f"Effect {effect_type} returned empty"


# Test configuration
pytest_plugins = []


# Test execution report
if __name__ == "__main__":
    print("=" * 70)
    print("EFFECTS TESTING SUITE - DEBT-002 (Part 2/3)")
    print("=" * 70)
    print()
    print("Running tests...")
    print("Note: Tests marked @pytest.mark.slow involve actual animations")
    print("      and may take several seconds to complete.")
    print()

    pytest.main([__file__, "-v", "--tb=short", "-m", "not slow"])
    print("\nRun with: pytest test_effects.py -v -m slow")
    print("to execute slow animation tests.")
