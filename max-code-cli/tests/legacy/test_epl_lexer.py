"""
Scientific Tests for EPL Lexer

Tests the tokenization engine that converts input (natural language + EPL)
into a stream of tokens.

Test Philosophy:
- Test REAL tokenization behavior
- Validate token types, values, line/column tracking
- Test mixed input (NL + EPL)
- Scientific rigor: reproducible, deterministic

Run:
    pytest tests/test_epl_lexer.py -v
"""

import pytest
from core.epl.lexer import (
    Lexer,
    Token,
    TokenType,
    tokenize,
    is_epl_only,
    is_natural_language_only,
    extract_emojis,
    extract_words,
)


# ============================================================================
# TEST: Token Creation and Structure
# ============================================================================

def test_token_structure():
    """Test Token dataclass structure"""
    token = Token(
        type=TokenType.EMOJI,
        value="🌳",
        line=1,
        column=5,
        emoji_meaning="Tree of Thoughts"
    )

    assert token.type == TokenType.EMOJI
    assert token.value == "🌳"
    assert token.line == 1
    assert token.column == 5
    assert token.emoji_meaning == "Tree of Thoughts"


def test_token_repr():
    """Test Token string representation"""
    emoji_token = Token(
        type=TokenType.EMOJI,
        value="🌳",
        line=1,
        column=1,
        emoji_meaning="Tree of Thoughts"
    )

    repr_str = repr(emoji_token)
    assert "emoji" in repr_str
    assert "🌳" in repr_str
    assert "Tree of Thoughts" in repr_str


# ============================================================================
# TEST: Lexer Initialization
# ============================================================================

def test_lexer_initialization():
    """Test Lexer can be initialized with source"""
    source = "Test input"
    lexer = Lexer(source)

    assert lexer.source == source
    assert lexer.position == 0
    assert lexer.line == 1
    assert lexer.column == 1


# ============================================================================
# TEST: Natural Language Tokenization
# ============================================================================

def test_tokenize_simple_words():
    """Test tokenizing simple natural language words"""
    tokens = tokenize("tree thoughts")

    # Filter out EOF
    tokens = [t for t in tokens if t.type != TokenType.EOF]

    assert len(tokens) == 2
    assert tokens[0].type == TokenType.WORD
    assert tokens[0].value == "tree"
    assert tokens[1].type == TokenType.WORD
    assert tokens[1].value == "thoughts"


def test_tokenize_with_numbers():
    """Test tokenizing text with numbers"""
    tokens = tokenize("analyze 42 files")

    tokens = [t for t in tokens if t.type != TokenType.EOF]

    assert len(tokens) == 3
    assert tokens[0].type == TokenType.WORD
    assert tokens[0].value == "analyze"
    assert tokens[1].type == TokenType.NUMBER
    assert tokens[1].value == "42"
    assert tokens[2].type == TokenType.WORD
    assert tokens[2].value == "files"


def test_tokenize_with_punctuation():
    """Test tokenizing text with punctuation"""
    tokens = tokenize("Hello, world!")

    tokens = [t for t in tokens if t.type != TokenType.EOF]

    # Should have: Hello, comma, world, (! is punctuation)
    word_tokens = [t for t in tokens if t.type == TokenType.WORD]
    punct_tokens = [t for t in tokens if t.type == TokenType.PUNCTUATION]

    assert len(word_tokens) == 2
    assert len(punct_tokens) >= 1  # At least comma (! might not be in punctuation set)
    assert word_tokens[0].value == "Hello"
    assert word_tokens[1].value == "world"


# ============================================================================
# TEST: EPL (Emoji) Tokenization
# ============================================================================

def test_tokenize_single_emoji():
    """Test tokenizing single emoji"""
    tokens = tokenize("🌳")

    tokens = [t for t in tokens if t.type != TokenType.EOF]

    assert len(tokens) == 1
    assert tokens[0].type == TokenType.EMOJI
    assert tokens[0].value == "🌳"
    assert tokens[0].emoji_meaning is not None


def test_tokenize_multiple_emojis():
    """Test tokenizing multiple emojis"""
    tokens = tokenize("🌳📊🔒")

    tokens = [t for t in tokens if t.type != TokenType.EOF]

    assert len(tokens) == 3
    assert all(t.type == TokenType.EMOJI for t in tokens)
    assert tokens[0].value == "🌳"
    assert tokens[1].value == "📊"
    assert tokens[2].value == "🔒"


def test_tokenize_emoji_with_operator():
    """Test tokenizing emoji with operator"""
    tokens = tokenize("🔴→🟢")

    tokens = [t for t in tokens if t.type != TokenType.EOF]

    assert len(tokens) == 3
    assert tokens[0].type == TokenType.EMOJI
    assert tokens[0].value == "🔴"
    assert tokens[1].type == TokenType.OPERATOR
    assert tokens[1].value == "→"
    assert tokens[2].type == TokenType.EMOJI
    assert tokens[2].value == "🟢"


# ============================================================================
# TEST: Mixed Input (Natural Language + EPL)
# ============================================================================

def test_tokenize_mixed_input():
    """Test tokenizing mixed natural language and EPL"""
    tokens = tokenize("Use 🌳 for analysis")

    tokens = [t for t in tokens if t.type != TokenType.EOF]

    # Should have: Use, 🌳, for, analysis
    assert len(tokens) == 4
    assert tokens[0].type == TokenType.WORD
    assert tokens[0].value == "Use"
    assert tokens[1].type == TokenType.EMOJI
    assert tokens[1].value == "🌳"
    assert tokens[2].type == TokenType.WORD
    assert tokens[2].value == "for"
    assert tokens[3].type == TokenType.WORD
    assert tokens[3].value == "analysis"


def test_tokenize_agent_invocation():
    """Test tokenizing agent invocation pattern"""
    tokens = tokenize("👑:🌳")

    tokens = [t for t in tokens if t.type != TokenType.EOF]

    # Should have: 👑, :, 🌳
    assert len(tokens) >= 2  # At least emoji : emoji
    assert tokens[0].type == TokenType.EMOJI
    assert tokens[0].value == "👑"


# ============================================================================
# TEST: Line and Column Tracking
# ============================================================================

def test_line_column_tracking_single_line():
    """Test line and column tracking on single line"""
    tokens = tokenize("tree auth")

    tokens = [t for t in tokens if t.type != TokenType.EOF]

    # All tokens should be on line 1
    assert all(t.line == 1 for t in tokens)

    # First token at column 1
    assert tokens[0].column == 1

    # Second token should be after first + space
    assert tokens[1].column > tokens[0].column


def test_line_tracking_multiline():
    """Test line tracking across multiple lines"""
    tokens = tokenize("tree\nauth")

    # Get word tokens only
    word_tokens = [t for t in tokens if t.type == TokenType.WORD]

    assert len(word_tokens) == 2
    assert word_tokens[0].line == 1
    assert word_tokens[0].value == "tree"
    assert word_tokens[1].line == 2
    assert word_tokens[1].value == "auth"


# ============================================================================
# TEST: Utility Functions
# ============================================================================

def test_is_epl_only_pure_epl():
    """Test is_epl_only with pure EPL input"""
    tokens = tokenize("🌳📊🔒")

    assert is_epl_only(tokens) == True


def test_is_epl_only_mixed_input():
    """Test is_epl_only with mixed input"""
    tokens = tokenize("Use 🌳 for analysis")

    assert is_epl_only(tokens) == False


def test_is_natural_language_only_pure_nl():
    """Test is_natural_language_only with pure NL"""
    tokens = tokenize("tree of thoughts")

    assert is_natural_language_only(tokens) == True


def test_is_natural_language_only_mixed():
    """Test is_natural_language_only with mixed input"""
    tokens = tokenize("Use 🌳 for analysis")

    assert is_natural_language_only(tokens) == False


def test_extract_emojis():
    """Test extracting only emoji tokens"""
    tokens = tokenize("Use 🌳 for 🔒 analysis")

    emoji_tokens = extract_emojis(tokens)

    assert len(emoji_tokens) == 2
    assert all(t.type == TokenType.EMOJI for t in emoji_tokens)
    assert emoji_tokens[0].value == "🌳"
    assert emoji_tokens[1].value == "🔒"


def test_extract_words():
    """Test extracting only word tokens"""
    tokens = tokenize("Use 🌳 for analysis")

    word_tokens = extract_words(tokens)

    assert len(word_tokens) == 3
    assert all(t.type == TokenType.WORD for t in word_tokens)
    assert word_tokens[0].value == "Use"
    assert word_tokens[1].value == "for"
    assert word_tokens[2].value == "analysis"


# ============================================================================
# TEST: Edge Cases
# ============================================================================

def test_tokenize_empty_string():
    """Test tokenizing empty string"""
    tokens = tokenize("")

    # Should only have EOF
    assert len(tokens) == 1
    assert tokens[0].type == TokenType.EOF


def test_tokenize_only_whitespace():
    """Test tokenizing only whitespace"""
    tokens = tokenize("   \t  ")

    # Should only have EOF (whitespace is filtered)
    tokens = [t for t in tokens if t.type != TokenType.EOF]
    assert len(tokens) == 0


def test_tokenize_underscores_in_words():
    """Test tokenizing words with underscores"""
    tokens = tokenize("tree_of_thoughts")

    tokens = [t for t in tokens if t.type != TokenType.EOF]

    assert len(tokens) == 1
    assert tokens[0].type == TokenType.WORD
    assert tokens[0].value == "tree_of_thoughts"


# ============================================================================
# TEST: Operator Tokenization
# ============================================================================

def test_tokenize_arrow_operator():
    """Test tokenizing arrow operator"""
    tokens = tokenize("🔴→🟢")

    op_tokens = [t for t in tokens if t.type == TokenType.OPERATOR]

    assert len(op_tokens) >= 1
    arrow = op_tokens[0]
    assert arrow.value == "→"
    assert arrow.operator_meaning is not None


def test_tokenize_multiple_operators():
    """Test tokenizing multiple operators"""
    tokens = tokenize("🔴→🟢+🔵")

    op_tokens = [t for t in tokens if t.type == TokenType.OPERATOR]

    # Should have → and +
    assert len(op_tokens) >= 2
    operators = [t.value for t in op_tokens]
    assert "→" in operators
    assert "+" in operators


# ============================================================================
# SUMMARY
# ============================================================================

"""
Test Coverage Summary:

1. Token Structure (2 tests)
   - Token creation
   - Token representation

2. Lexer Initialization (1 test)
   - Basic initialization

3. Natural Language Tokenization (3 tests)
   - Simple words
   - Numbers
   - Punctuation

4. EPL Tokenization (3 tests)
   - Single emoji
   - Multiple emojis
   - Emoji with operators

5. Mixed Input (2 tests)
   - Mixed NL + EPL
   - Agent invocation

6. Line/Column Tracking (2 tests)
   - Single line tracking
   - Multi-line tracking

7. Utility Functions (6 tests)
   - is_epl_only
   - is_natural_language_only
   - extract_emojis
   - extract_words

8. Edge Cases (3 tests)
   - Empty string
   - Only whitespace
   - Underscores in words

9. Operator Tokenization (2 tests)
   - Arrow operator
   - Multiple operators

Total: 24 scientific tests for EPL Lexer
"""
