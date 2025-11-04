"""
EPL (Emoji Protocol Language)

A semantic compression language for human-AI communication.

"No princípio era o Verbo, e o Verbo estava com Deus, e o Verbo era Deus."
(João 1:1)

In EPL, in the beginning was the EMOJI, and the emoji WAS the concept.
"""

from .vocabulary import (
    EMOJI_VOCABULARY,
    OPERATORS,
    EmojiCategory,
    EmojiDefinition,
    get_emoji_definition,
    get_emoji_by_alias,
    get_emojis_by_category,
    calculate_compression_ratio,
)

from .lexer import (
    Lexer,
    Token,
    TokenType,
    tokenize,
    is_epl_only,
    is_natural_language_only,
    extract_emojis,
    extract_words,
)

from .parser import (
    Parser,
    ASTNode,
    ASTNodeType,
    parse,
    print_ast,
)

from .nlp_engine import (
    NLPEngine,
    Intent,
    IntentType,
    Language,
)

from .pattern_matcher import (
    PatternMatcher,
    Pattern,
    MatchResult,
)

from .translator import (
    Translator,
    TranslationResult,
    translate_to_epl,
    translate_to_nl,
)

from .executor import (
    EPLExecutor,
    ExecutionResult,
    ExecutionStatus,
)

from .learning_mode import (
    LearningMode,
    LearningPhase,
    LearningHint,
    UserProgress,
)

__all__ = [
    # Vocabulary
    'EMOJI_VOCABULARY',
    'OPERATORS',
    'EmojiCategory',
    'EmojiDefinition',
    'get_emoji_definition',
    'get_emoji_by_alias',
    'get_emojis_by_category',
    'calculate_compression_ratio',

    # Lexer
    'Lexer',
    'Token',
    'TokenType',
    'tokenize',
    'is_epl_only',
    'is_natural_language_only',
    'extract_emojis',
    'extract_words',

    # Parser
    'Parser',
    'ASTNode',
    'ASTNodeType',
    'parse',
    'print_ast',

    # NLP
    'NLPEngine',
    'Intent',
    'IntentType',
    'Language',

    # Pattern Matcher
    'PatternMatcher',
    'Pattern',
    'MatchResult',

    # Translator
    'Translator',
    'TranslationResult',
    'translate_to_epl',
    'translate_to_nl',

    # Executor
    'EPLExecutor',
    'ExecutionResult',
    'ExecutionStatus',

    # Learning Mode
    'LearningMode',
    'LearningPhase',
    'LearningHint',
    'UserProgress',
]

__version__ = '1.0.0'
