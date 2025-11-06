"""
Terminal Text Effects Wrapper

Wrapper clean para terminaltexteffects com nossa identidade visual.
Paleta: Neon green → Blue → Yellow
Filosofia: Cinematográfico mas rápido (<500ms)

"Porque Deus não nos deu espírito de covardia, mas de poder, amor e moderação"
(2 Timóteo 1:7)
"""

from typing import Optional, List
from terminaltexteffects.effects import effect_beams, effect_decrypt, effect_matrix, effect_slide


class EffectsManager:
    """
    Gerenciador de efeitos cinematográficos

    Design principles:
    - Performance: <500ms per effect
    - Visual impact: Alto
    - Neon palette: #0FFF50 → #0080FF → #FFFF00
    """

    # Paleta neon oficial
    NEON_GRADIENT = ['#0FFF50', '#00F0FF', '#0080FF', '#FFFF00']
    NEON_GREEN = '#0FFF50'
    NEON_CYAN = '#00F0FF'
    NEON_BLUE = '#0080FF'
    NEON_YELLOW = '#FFFF00'

    # Matrix green for special effects
    MATRIX_GREEN = ['#00FF00', '#00CC00', '#008800']

    @classmethod
    def beams(cls, text: str, gradient: Optional[List[str]] = None) -> str:
        """
        Efeito de beams luminosos (perfeito para banners)

        Args:
            text: Texto para animar
            gradient: Lista de cores hex (default: NEON_GRADIENT)

        Returns:
            Texto animado
        """
        if gradient is None:
            gradient = cls.NEON_GRADIENT

        effect = effect_beams.Beams(text)
        effect.effect_config.beam_gradient_stops = gradient
        effect.effect_config.beam_row_symbols = "▂▄▆█▆▄▂"
        effect.effect_config.beam_delay = 10  # ms entre frames (fast)
        effect.effect_config.final_gradient_stops = gradient

        # Run animation
        output = ""
        with effect.terminal_output() as terminal:
            for frame in effect:
                output = frame

        return output

    @classmethod
    def decrypt(cls, text: str, gradient: Optional[List[str]] = None) -> str:
        """
        Efeito de decrypt/Matrix (bom para revelações)

        Args:
            text: Texto para animar
            gradient: Lista de cores hex (default: MATRIX_GREEN)

        Returns:
            Texto animado
        """
        if gradient is None:
            gradient = cls.MATRIX_GREEN

        effect = effect_decrypt.Decrypt(text)
        effect.effect_config.encrypted_gradient_stops = gradient
        effect.effect_config.decrypted_gradient_stops = [cls.NEON_GREEN, cls.NEON_CYAN]

        output = ""
        with effect.terminal_output() as terminal:
            for frame in effect:
                output = frame

        return output

    @classmethod
    def slide(cls, text: str, direction: str = "left", gradient: Optional[List[str]] = None) -> str:
        """
        Efeito de slide (bom para transições)

        Args:
            text: Texto para animar
            direction: "left", "right", "up", "down"
            gradient: Lista de cores hex (default: NEON_GRADIENT)

        Returns:
            Texto animado
        """
        if gradient is None:
            gradient = cls.NEON_GRADIENT

        effect = effect_slide.Slide(text)
        effect.effect_config.merge_gradient_stops = gradient
        effect.effect_config.movement_speed = 1.5  # Fast

        output = ""
        with effect.terminal_output() as terminal:
            for frame in effect:
                output = frame

        return output

    @classmethod
    def matrix_rain(cls, text: str) -> str:
        """
        Efeito Matrix rain (para momentos especiais)

        Args:
            text: Texto para animar

        Returns:
            Texto animado
        """
        effect = effect_matrix.Matrix(text)
        effect.effect_config.matrix_gradient_stops = cls.MATRIX_GREEN
        effect.effect_config.final_gradient_stops = [cls.NEON_GREEN]

        output = ""
        with effect.terminal_output() as terminal:
            for frame in effect:
                output = frame

        return output

    @classmethod
    def quick_flash(cls, text: str, color: str = NEON_GREEN) -> str:
        """
        Flash rápido de cor (para alertas/sucesso)

        Args:
            text: Texto para flash
            color: Cor do flash (hex)

        Returns:
            Texto com flash
        """
        # Simple gradient flash
        from rich.text import Text
        from rich.console import Console
        from io import StringIO

        console = Console(file=StringIO())
        styled_text = Text(text, style=f"bold {color}")
        console.print(styled_text)

        return text  # For now, just return text (flash would need animation loop)


# Convenience functions
def animate_banner(text: str, effect_type: str = "beams") -> str:
    """
    Anima banner com efeito especificado

    Args:
        text: Banner text (ASCII art)
        effect_type: "beams", "decrypt", "matrix", "slide"

    Returns:
        Animated banner
    """
    if effect_type == "beams":
        return EffectsManager.beams(text)
    elif effect_type == "decrypt":
        return EffectsManager.decrypt(text)
    elif effect_type == "matrix":
        return EffectsManager.matrix_rain(text)
    elif effect_type == "slide":
        return EffectsManager.slide(text)
    else:
        return text  # No animation


def flash_success(text: str) -> str:
    """Flash verde para sucesso"""
    return EffectsManager.quick_flash(text, EffectsManager.NEON_GREEN)


def flash_warning(text: str) -> str:
    """Flash amarelo para warning"""
    return EffectsManager.quick_flash(text, EffectsManager.NEON_YELLOW)


def flash_error(text: str) -> str:
    """Flash vermelho para erro"""
    return EffectsManager.quick_flash(text, "#FF0040")
