"""
EPL Lexer - Tokenization Engine

Tokenizes both natural language and EPL (emoji) input.

Biblical Foundation:
"Toda palavra de Deus é pura" (Provérbios 30:5)

Every token is pure - no ambiguity in lexical analysis.
"""

from typing import List, Optional, Set
from dataclasses import dataclass
from enum import Enum
import re

from .vocabulary import (
from config.logging_config import get_logger

logger = get_logger(__name__)
    EMOJI_VOCABULARY,
    OPERATORS,
    get_emoji_by_alias,
    get_emoji_definition,
)


class TokenType(Enum):
    """Types of tokens in EPL"""
    # EPL-specific
    EMOJI = "emoji"              # 🌳, 🔒, etc
    OPERATOR = "operator"        # →, +, |, !, ?, ✓

    # Natural language
    WORD = "word"                # tree, thoughts, auth
    NUMBER = "number"            # 3, 42
    PUNCTUATION = "punctuation"  # ., !, ?

    # Special
    WHITESPACE = "whitespace"    # spaces, tabs
    NEWLINE = "newline"          # \n
    EOF = "eof"                  # End of input


@dataclass
class Token:
    """A single token"""
    type: TokenType
    value: str
    line: int
    column: int

    # EPL-specific metadata
    emoji_meaning: Optional[str] = None  # If EMOJI, what it means
    operator_meaning: Optional[str] = None  # If OPERATOR, what it does

    def __repr__(self) -> str:
        if self.type == TokenType.EMOJI and self.emoji_meaning:
            return f"Token({self.type.value}, '{self.value}', meaning='{self.emoji_meaning}')"
        elif self.type == TokenType.OPERATOR and self.operator_meaning:
            return f"Token({self.type.value}, '{self.value}', op='{self.operator_meaning}')"
        else:
            return f"Token({self.type.value}, '{self.value}')"


class Lexer:
    """
    EPL Lexer

    Tokenizes input into stream of tokens.
    Supports both:
    - Natural language: "Use tree of thoughts to analyze auth"
    - EPL: "🌳📊🔒"
    - Mixed: "Use 🌳 for 🔒 analysis"
    """

    def __init__(self, source: str):
        self.source = source
        self.position = 0
        self.line = 1
        self.column = 1

        # Cache for performance
        self._emoji_set: Set[str] = set(EMOJI_VOCABULARY.keys())
        self._operator_set: Set[str] = set(OPERATORS.keys())

    def tokenize(self) -> List[Token]:
        """
        Tokenize entire input

        Returns:
            List of tokens
        """
        tokens: List[Token] = []

        while not self._is_eof():
            token = self._next_token()
            if token:
                # Skip whitespace tokens (but keep for debugging if needed)
                if token.type not in [TokenType.WHITESPACE]:
                    tokens.append(token)

        # Add EOF token
        tokens.append(Token(
            type=TokenType.EOF,
            value="",
            line=self.line,
            column=self.column
        ))

        return tokens

    def _next_token(self) -> Optional[Token]:
        """Get next token from input"""
        if self._is_eof():
            return None

        current_char = self._current_char()

        # Whitespace
        if current_char in ' \t':
            return self._read_whitespace()

        # Newline
        if current_char in '\n\r':
            return self._read_newline()

        # Emoji (EPL)
        if self._is_emoji(current_char):
            return self._read_emoji()

        # Operator (EPL)
        if current_char in self._operator_set:
            return self._read_operator()

        # Number
        if current_char.isdigit():
            return self._read_number()

        # Word (natural language)
        if current_char.isalpha() or current_char == '_':
            return self._read_word()

        # Punctuation
        if current_char in '.,;:!?':
            return self._read_punctuation()

        # Unknown character - skip
        self._advance()
        return self._next_token()

    def _read_emoji(self) -> Token:
        """Read emoji token"""
        start_line = self.line
        start_column = self.column

        emoji = self._current_char()
        self._advance()

        # Get emoji meaning
        definition = get_emoji_definition(emoji)
        meaning = definition.primary_meaning if definition else emoji

        return Token(
            type=TokenType.EMOJI,
            value=emoji,
            line=start_line,
            column=start_column,
            emoji_meaning=meaning
        )

    def _read_operator(self) -> Token:
        """Read operator token"""
        start_line = self.line
        start_column = self.column

        operator = self._current_char()
        self._advance()

        # Get operator meaning
        meaning = OPERATORS.get(operator, operator)

        return Token(
            type=TokenType.OPERATOR,
            value=operator,
            line=start_line,
            column=start_column,
            operator_meaning=meaning
        )

    def _read_word(self) -> Token:
        """Read word token (natural language)"""
        start_line = self.line
        start_column = self.column

        word = ""
        while not self._is_eof() and (self._current_char().isalnum() or self._current_char() == '_'):
            word += self._current_char()
            self._advance()

        return Token(
            type=TokenType.WORD,
            value=word,
            line=start_line,
            column=start_column
        )

    def _read_number(self) -> Token:
        """Read number token"""
        start_line = self.line
        start_column = self.column

        number = ""
        while not self._is_eof() and self._current_char().isdigit():
            number += self._current_char()
            self._advance()

        return Token(
            type=TokenType.NUMBER,
            value=number,
            line=start_line,
            column=start_column
        )

    def _read_punctuation(self) -> Token:
        """Read punctuation token"""
        start_line = self.line
        start_column = self.column

        punct = self._current_char()
        self._advance()

        return Token(
            type=TokenType.PUNCTUATION,
            value=punct,
            line=start_line,
            column=start_column
        )

    def _read_whitespace(self) -> Token:
        """Read whitespace token"""
        start_line = self.line
        start_column = self.column

        whitespace = ""
        while not self._is_eof() and self._current_char() in ' \t':
            whitespace += self._current_char()
            self._advance()

        return Token(
            type=TokenType.WHITESPACE,
            value=whitespace,
            line=start_line,
            column=start_column
        )

    def _read_newline(self) -> Token:
        """Read newline token"""
        start_line = self.line
        start_column = self.column

        newline = self._current_char()
        self._advance()

        return Token(
            type=TokenType.NEWLINE,
            value=newline,
            line=start_line,
            column=start_column
        )

    # ========================================================================
    # HELPER METHODS
    # ========================================================================

    def _current_char(self) -> str:
        """Get current character"""
        if self._is_eof():
            return '\0'
        return self.source[self.position]

    def _peek(self, offset: int = 1) -> str:
        """Peek ahead without consuming"""
        pos = self.position + offset
        if pos >= len(self.source):
            return '\0'
        return self.source[pos]

    def _advance(self):
        """Move to next character"""
        if self._is_eof():
            return

        if self.source[self.position] == '\n':
            self.line += 1
            self.column = 1
        else:
            self.column += 1

        self.position += 1

    def _is_eof(self) -> bool:
        """Check if end of input"""
        return self.position >= len(self.source)

    def _is_emoji(self, char: str) -> bool:
        """
        Check if character is an emoji

        NOTE: This is a simple implementation.
        Production version should use proper Unicode emoji detection.
        """
        return char in self._emoji_set


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def tokenize(source: str) -> List[Token]:
    """
    Convenience function to tokenize input

    Args:
        source: Input string (natural language or EPL)

    Returns:
        List of tokens

    Example:
        >>> tokens = tokenize("Use 🌳 for 🔒")
        >>> for token in tokens:
        ...     print(token)
        Token(word, 'Use')
        Token(emoji, '🌳', meaning='Tree of Thoughts')
        Token(word, 'for')
        Token(emoji, '🔒', meaning='Security')
    """
    lexer = Lexer(source)
    return lexer.tokenize()


def is_epl_only(tokens: List[Token]) -> bool:
    """
    Check if tokens are pure EPL (only emojis and operators)

    Args:
        tokens: List of tokens

    Returns:
        True if pure EPL, False if contains natural language
    """
    for token in tokens:
        if token.type == TokenType.EOF:
            continue
        if token.type not in [TokenType.EMOJI, TokenType.OPERATOR]:
            return False
    return True


def is_natural_language_only(tokens: List[Token]) -> bool:
    """
    Check if tokens are pure natural language (no emojis)

    Args:
        tokens: List of tokens

    Returns:
        True if pure natural language, False if contains EPL
    """
    for token in tokens:
        if token.type == TokenType.EOF:
            continue
        if token.type in [TokenType.EMOJI, TokenType.OPERATOR]:
            return False
    return True


def extract_emojis(tokens: List[Token]) -> List[Token]:
    """Extract only emoji tokens"""
    return [token for token in tokens if token.type == TokenType.EMOJI]


def extract_words(tokens: List[Token]) -> List[Token]:
    """Extract only word tokens"""
    return [token for token in tokens if token.type == TokenType.WORD]


if __name__ == "__main__":
    # Demo
    logger.info("🧬 EPL Lexer Demo\n")
    test_cases = [
        "Use tree of thoughts to analyze auth",
        "🌳📊🔒",
        "Use 🌳 for 🔒 analysis",
        "🔴→🟢→🔄",
        "👑:🌳→💡💡💡→🏆",
        "Fix 🐛 urgently using 🏥",
    ]

    for i, test in enumerate(test_cases, 1):
        print(f"Test {i}: \"{test}\"")
        tokens = tokenize(test)

        logger.info(f"  Tokens ({len(tokens)} total):")
        for token in tokens:
            if token.type != TokenType.EOF:
                logger.info(f"    {token}")
        # Classification
        epl_only = is_epl_only(tokens)
        natural_only = is_natural_language_only(tokens)

        if epl_only:
            logger.info(f"  Classification: Pure EPL ✨")
        elif natural_only:
            logger.info(f"  Classification: Pure Natural Language 📝")
        else:
            logger.info(f"  Classification: Mixed (Hybrid) 🔀")
        print()
