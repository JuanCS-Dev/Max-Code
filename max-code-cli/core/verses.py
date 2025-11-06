"""
Biblical Verse Manager

Gerencia exibição contextual de versículos bíblicos durante operações.
Filosofia: Natural, não invasivo, contextualmente apropriado.

"Thy word is a lamp unto my feet, and a light unto my path"
(Psalm 119:105)
"""

import os
import sys
import random
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass


@dataclass
class BiblicalVerse:
    """Um versículo bíblico com contexto"""
    text: str
    reference: str
    context: str  # wisdom, work, encouragement, excellence, perseverance


class BiblicalVerseManager:
    """
    Gerenciador de versículos bíblicos

    Design Principles:
    - Contextual: verso apropriado para a situação
    - Non-invasive: apenas em momentos naturais
    - Optional: flag --no-verses para desabilitar
    - Balanced: 30% chance (não overwhelming)
    """

    # Database de versículos por contexto
    VERSES: Dict[str, List[Tuple[str, str]]] = {
        'wisdom': [
            ("If any of you lacks wisdom, let him ask God", "James 1:5"),
            ("The fear of the Lord is the beginning of wisdom", "Proverbs 9:10"),
            ("Get wisdom, get understanding; do not forget my words", "Proverbs 4:5"),
            ("For the Lord gives wisdom; from His mouth come knowledge and understanding", "Proverbs 2:6"),
            ("Wisdom is supreme; therefore get wisdom", "Proverbs 4:7"),
        ],
        'work': [
            ("Whatever you do, work at it with all your heart", "Colossians 3:23"),
            ("In all your ways acknowledge Him", "Proverbs 3:6"),
            ("Commit to the Lord whatever you do", "Proverbs 16:3"),
            ("The plans of the diligent lead to profit", "Proverbs 21:5"),
            ("Do your best to present yourself to God as one approved", "2 Timothy 2:15"),
        ],
        'encouragement': [
            ("I can do all things through Christ who strengthens me", "Philippians 4:13"),
            ("Be strong and courageous", "Joshua 1:9"),
            ("Do not be anxious about anything", "Philippians 4:6"),
            ("Cast all your anxiety on Him because He cares for you", "1 Peter 5:7"),
            ("The Lord is my strength and my shield", "Psalm 28:7"),
        ],
        'excellence': [
            ("Let all that you do be done in love", "1 Corinthians 16:14"),
            ("Whatever is true, whatever is noble, think about such things", "Philippians 4:8"),
            ("Do not be overcome by evil, but overcome evil with good", "Romans 12:21"),
            ("Let your light shine before others", "Matthew 5:16"),
            ("Be perfect, therefore, as your heavenly Father is perfect", "Matthew 5:48"),
        ],
        'perseverance': [
            ("Let us not become weary in doing good", "Galatians 6:9"),
            ("Run with perseverance the race marked out for us", "Hebrews 12:1"),
            ("Consider it pure joy when you face trials", "James 1:2-3"),
            ("Suffering produces perseverance", "Romans 5:3-4"),
            ("Be steadfast, immovable, always abounding in the work of the Lord", "1 Corinthians 15:58"),
        ],
        'truth': [
            ("You will know the truth, and the truth will set you free", "John 8:32"),
            ("Love does not delight in evil but rejoices with the truth", "1 Corinthians 13:6"),
            ("Buy the truth and do not sell it", "Proverbs 23:23"),
            ("The Lord detests lying lips", "Proverbs 12:22"),
            ("Speak the truth in love", "Ephesians 4:15"),
        ],
        'patience': [
            ("Be patient, bearing with one another in love", "Ephesians 4:2"),
            ("The Lord is not slow in keeping His promise", "2 Peter 3:9"),
            ("Wait for the Lord; be strong and take heart", "Psalm 27:14"),
            ("A patient person has great understanding", "Proverbs 14:29"),
        ],
    }

    def __init__(self):
        self.enabled = self._check_if_enabled()
        self.display_probability = 0.3  # 30% chance

    def _check_if_enabled(self) -> bool:
        """
        Checa se versículos estão habilitados

        Disabled by:
        - Environment var MAXCODE_NO_VERSES
        - Command line flag --no-verses
        """
        if os.environ.get('MAXCODE_NO_VERSES'):
            return False

        if '--no-verses' in sys.argv:
            return False

        return True

    def should_show_verse(self) -> bool:
        """
        Decide se deve mostrar versículo (probabilístico)

        Returns:
            True se deve mostrar (30% chance quando enabled)
        """
        if not self.enabled:
            return False

        return random.random() < self.display_probability

    def get_verse(
        self,
        context: str = 'wisdom',
        dim: bool = True,
        force: bool = False
    ) -> str:
        """
        Retorna versículo formatado para contexto

        Args:
            context: Tipo de contexto (wisdom, work, encouragement, etc.)
            dim: Se deve usar estilo dim/italic
            force: Se True, ignora should_show_verse() check

        Returns:
            Versículo formatado ou string vazia
        """
        # Check if should show (unless forced)
        if not force and not self.should_show_verse():
            return ""

        # Get verses for context (default to wisdom)
        verses = self.VERSES.get(context, self.VERSES['wisdom'])

        # Select random verse
        text, ref = random.choice(verses)

        # Format with Rich markup
        style = "dim italic" if dim else "italic"
        return f'\n[{style}]"{text}"[/{style}]\n[dim]{" " * 40}- {ref}[/dim]\n'

    def get_verse_for_operation(self, operation_type: str) -> str:
        """
        Retorna versículo apropriado para tipo de operação

        Args:
            operation_type: analyze, generate, test, fix, review, etc.

        Returns:
            Versículo formatado
        """
        # Map operation types to contexts
        context_map = {
            'analyze': 'wisdom',
            'generate': 'work',
            'test': 'perseverance',
            'fix': 'patience',
            'review': 'excellence',
            'code': 'work',
            'docs': 'truth',
            'explore': 'wisdom',
            'plan': 'wisdom',
        }

        context = context_map.get(operation_type, 'wisdom')
        return self.get_verse(context=context)

    def get_startup_verse(self) -> str:
        """
        Retorna versículo para startup (sempre mostra se enabled)

        Returns:
            Versículo de wisdom/excellence
        """
        if not self.enabled:
            return ""

        # For startup, alternate between wisdom and excellence
        context = random.choice(['wisdom', 'excellence'])
        return self.get_verse(context=context, dim=True, force=True)

    def get_success_verse(self) -> str:
        """
        Retorna versículo para operação bem-sucedida

        Returns:
            Versículo de encouragement
        """
        return self.get_verse(context='encouragement', dim=True)

    def get_error_verse(self) -> str:
        """
        NEVER returns verse for errors (would seem insensitive)

        Returns:
            Empty string always
        """
        return ""  # Never show verses on errors

    def get_all_verses(self, context: Optional[str] = None) -> List[BiblicalVerse]:
        """
        Retorna todos os versículos (para documentação/referência)

        Args:
            context: Se fornecido, apenas deste contexto

        Returns:
            Lista de BiblicalVerse objects
        """
        verses = []

        if context:
            # Specific context only
            for text, ref in self.VERSES.get(context, []):
                verses.append(BiblicalVerse(
                    text=text,
                    reference=ref,
                    context=context
                ))
        else:
            # All contexts
            for ctx, verse_list in self.VERSES.items():
                for text, ref in verse_list:
                    verses.append(BiblicalVerse(
                        text=text,
                        reference=ref,
                        context=ctx
                    ))

        return verses


# Global instance (singleton pattern)
_verse_manager: Optional[BiblicalVerseManager] = None


def get_verse_manager() -> BiblicalVerseManager:
    """Get global verse manager instance"""
    global _verse_manager
    if _verse_manager is None:
        _verse_manager = BiblicalVerseManager()
    return _verse_manager


# Convenience functions
def get_verse(context: str = 'wisdom', **kwargs) -> str:
    """Get verse from global manager"""
    return get_verse_manager().get_verse(context=context, **kwargs)


def get_startup_verse() -> str:
    """Get startup verse"""
    return get_verse_manager().get_startup_verse()


def get_operation_verse(operation: str) -> str:
    """Get verse for operation type"""
    return get_verse_manager().get_verse_for_operation(operation)


def get_success_verse() -> str:
    """Get success verse"""
    return get_verse_manager().get_success_verse()
