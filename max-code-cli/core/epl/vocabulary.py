"""
EPL Vocabulary - Emoji → Concept Mapping

Defines the core vocabulary for Emoji Protocol Language (EPL).

Biblical Foundation:
"No princípio era o Verbo, e o Verbo estava com Deus, e o Verbo era Deus."
(João 1:1)

Em EPL, no princípio era o EMOJI, e o emoji ERA o conceito.
"""

from typing import Dict, List, Optional, Set
from dataclasses import dataclass
from enum import Enum
from config.logging_config import get_logger

logger = get_logger(__name__)


class EmojiCategory(Enum):
    """Categories of emojis"""
    AGENT = "agent"              # Agents & Systems (👑, 🧠, 🏥)
    ACTION = "action"            # Actions (🌳, 🔍, 💻)
    STATE = "state"              # States (🔴, 🟢, ✅)
    CONCEPT = "concept"          # Concepts (🔒, 🐛, ✨)
    OPERATOR = "operator"        # Operators (→, +, |)
    MODIFIER = "modifier"        # Modifiers (🔥, ⚠️, !)


@dataclass
class EmojiDefinition:
    """Definition of a single emoji"""
    emoji: str
    primary_meaning: str
    category: EmojiCategory
    aliases: List[str]           # Alternative names
    context_meanings: Dict[str, str]  # Context-specific meanings
    examples: List[str]          # Usage examples
    token_equivalent: int        # How many tokens this emoji replaces


# ============================================================================
# CORE VOCABULARY
# ============================================================================

EMOJI_VOCABULARY: Dict[str, EmojiDefinition] = {
    # AGENTS & SYSTEMS
    "👑": EmojiDefinition(
        emoji="👑",
        primary_meaning="Sophia (Architect Agent)",
        category=EmojiCategory.AGENT,
        aliases=["sophia", "architect", "queen"],
        context_meanings={
            "alone": "Invoke Sophia for architectural decision",
            "with_action": "Sophia performs this action",
        },
        examples=["👑:🌳", "👑→💡💡💡"],
        token_equivalent=3,  # "Sophia Architect Agent"
    ),

    "🧠": EmojiDefinition(
        emoji="🧠",
        primary_meaning="MAXIMUS (Systemic Analysis)",
        category=EmojiCategory.AGENT,
        aliases=["maximus", "brain", "systemic"],
        context_meanings={
            "alone": "Use MAXIMUS for analysis",
            "with_!": "MAXIMUS offline, use fallback",
        },
        examples=["🧠📊", "!🧠→fallback"],
        token_equivalent=2,  # "MAXIMUS AI"
    ),

    "🏥": EmojiDefinition(
        emoji="🏥",
        primary_meaning="PENELOPE (Code Healing)",
        category=EmojiCategory.AGENT,
        aliases=["penelope", "healing", "hospital"],
        context_meanings={
            "with_bug": "Heal bug with root cause analysis",
            "alone": "Invoke PENELOPE service",
        },
        examples=["🐛→🏥", "🏥✓"],
        token_equivalent=2,  # "PENELOPE Service"
    ),

    "🎯": EmojiDefinition(
        emoji="🎯",
        primary_meaning="MABA (Bias Detection)",
        category=EmojiCategory.AGENT,
        aliases=["maba", "bias", "target"],
        context_meanings={
            "with_code": "Detect bias in code/decisions",
            "alone": "Invoke MABA service",
        },
        examples=["🎯✓", "code→🎯"],
        token_equivalent=2,  # "MABA Bias"
    ),

    "📖": EmojiDefinition(
        emoji="📖",
        primary_meaning="NIS (Narrative Intelligence)",
        category=EmojiCategory.AGENT,
        aliases=["nis", "narrative", "story"],
        context_meanings={
            "with_docs": "Generate narrative documentation",
            "alone": "Invoke NIS service",
        },
        examples=["📝→📖", "changes→📖"],
        token_equivalent=3,  # "NIS Narrative System"
    ),

    # ACTIONS
    "🌳": EmojiDefinition(
        emoji="🌳",
        primary_meaning="Tree of Thoughts (ToT)",
        category=EmojiCategory.ACTION,
        aliases=["tot", "tree", "explore"],
        context_meanings={
            "with_target": "Explore multiple approaches for target",
            "with_agent": "Agent uses ToT methodology",
        },
        examples=["🌳🔒", "👑:🌳→💡💡💡"],
        token_equivalent=4,  # "Tree of Thoughts exploration"
    ),

    "🔍": EmojiDefinition(
        emoji="🔍",
        primary_meaning="Explore / Search",
        category=EmojiCategory.ACTION,
        aliases=["search", "find", "explore"],
        context_meanings={
            "with_codebase": "Explore codebase structure",
            "with_pattern": "Search for pattern",
        },
        examples=["🔍pattern", "🔍codebase"],
        token_equivalent=2,  # "Explore codebase"
    ),

    "💻": EmojiDefinition(
        emoji="💻",
        primary_meaning="Code Generation",
        category=EmojiCategory.ACTION,
        aliases=["code", "generate", "write"],
        context_meanings={
            "alone": "Generate code",
            "with_target": "Generate code for target",
        },
        examples=["💻function", "💻→🧪"],
        token_equivalent=2,  # "Generate code"
    ),

    "🧪": EmojiDefinition(
        emoji="🧪",
        primary_meaning="Test / TDD",
        category=EmojiCategory.ACTION,
        aliases=["test", "tdd", "testing"],
        context_meanings={
            "alone": "Run tests",
            "with_code": "Test this code",
            "in_cycle": "Part of TDD cycle",
        },
        examples=["🧪code", "🔴→🟢→🔄"],
        token_equivalent=2,  # "Run tests"
    ),

    "🔧": EmojiDefinition(
        emoji="🔧",
        primary_meaning="Fix / Repair",
        category=EmojiCategory.ACTION,
        aliases=["fix", "repair", "patch"],
        context_meanings={
            "with_bug": "Fix this bug",
            "after_healing": "Apply fix from PENELOPE",
        },
        examples=["🐛→🔧", "🏥→🔧"],
        token_equivalent=2,  # "Fix bug"
    ),

    "📝": EmojiDefinition(
        emoji="📝",
        primary_meaning="Documentation",
        category=EmojiCategory.ACTION,
        aliases=["docs", "document", "write"],
        context_meanings={
            "with_code": "Document this code",
            "with_narrative": "Generate narrative docs",
        },
        examples=["📝function", "📝→📖"],
        token_equivalent=2,  # "Write documentation"
    ),

    "🚀": EmojiDefinition(
        emoji="🚀",
        primary_meaning="Deploy / Launch",
        category=EmojiCategory.ACTION,
        aliases=["deploy", "launch", "ship"],
        context_meanings={
            "after_tests": "Deploy after tests pass",
            "urgent": "Fast deployment needed",
        },
        examples=["🧪✅→🚀", "🔥🚀"],
        token_equivalent=1,  # "Deploy"
    ),

    # STATES
    "🔴": EmojiDefinition(
        emoji="🔴",
        primary_meaning="RED (TDD - Tests Failing)",
        category=EmojiCategory.STATE,
        aliases=["red", "fail", "failing"],
        context_meanings={
            "in_tdd": "RED phase - tests should fail",
            "alone": "Tests are failing",
        },
        examples=["🔴→🟢", "🔴🧪"],
        token_equivalent=3,  # "RED phase failing"
    ),

    "🟢": EmojiDefinition(
        emoji="🟢",
        primary_meaning="GREEN (TDD - Tests Passing)",
        category=EmojiCategory.STATE,
        aliases=["green", "pass", "passing"],
        context_meanings={
            "in_tdd": "GREEN phase - tests pass",
            "alone": "Tests are passing",
        },
        examples=["🔴→🟢", "🟢✅"],
        token_equivalent=3,  # "GREEN phase passing"
    ),

    "🔄": EmojiDefinition(
        emoji="🔄",
        primary_meaning="REFACTOR",
        category=EmojiCategory.STATE,
        aliases=["refactor", "improve", "optimize"],
        context_meanings={
            "in_tdd": "REFACTOR phase",
            "alone": "Refactor code",
        },
        examples=["🟢→🔄", "🔄code"],
        token_equivalent=1,  # "Refactor"
    ),

    "✅": EmojiDefinition(
        emoji="✅",
        primary_meaning="Success / Done / Approved",
        category=EmojiCategory.STATE,
        aliases=["success", "done", "approved", "pass"],
        context_meanings={
            "after_action": "Action completed successfully",
            "review": "Approved by review",
        },
        examples=["🧪✅", "🏛️✅"],
        token_equivalent=1,  # "Success"
    ),

    "❌": EmojiDefinition(
        emoji="❌",
        primary_meaning="Fail / Rejected / Error",
        category=EmojiCategory.STATE,
        aliases=["fail", "error", "rejected", "no"],
        context_meanings={
            "after_action": "Action failed",
            "review": "Rejected by review",
        },
        examples=["🧪❌", "🏛️❌"],
        token_equivalent=1,  # "Failed"
    ),

    "⚠️": EmojiDefinition(
        emoji="⚠️",
        primary_meaning="Warning / Attention",
        category=EmojiCategory.STATE,
        aliases=["warning", "caution", "attention"],
        context_meanings={
            "with_principle": "Constitutional warning",
            "with_action": "Proceed with caution",
        },
        examples=["⚠️P5", "⚠️🔒"],
        token_equivalent=1,  # "Warning"
    ),

    "🔥": EmojiDefinition(
        emoji="🔥",
        primary_meaning="Urgent / Hot / Critical",
        category=EmojiCategory.MODIFIER,
        aliases=["urgent", "critical", "hot", "fire"],
        context_meanings={
            "before_action": "High priority",
            "with_bug": "Critical bug",
        },
        examples=["🔥🐛", "🔥🚀"],
        token_equivalent=1,  # "Urgent"
    ),

    # CONCEPTS
    "🔒": EmojiDefinition(
        emoji="🔒",
        primary_meaning="Security / Authentication / Lock",
        category=EmojiCategory.CONCEPT,
        aliases=["security", "auth", "authentication", "lock"],
        context_meanings={
            "with_code": "Security check needed",
            "with_analysis": "Analyze security",
        },
        examples=["🔒✓", "🌳🔒"],
        token_equivalent=1,  # "Security"
    ),

    "🐛": EmojiDefinition(
        emoji="🐛",
        primary_meaning="Bug / Error / Issue",
        category=EmojiCategory.CONCEPT,
        aliases=["bug", "error", "issue", "problem"],
        context_meanings={
            "alone": "Bug exists",
            "with_fix": "Fix this bug",
        },
        examples=["🐛→🔧", "🔥🐛"],
        token_equivalent=1,  # "Bug"
    ),

    "✨": EmojiDefinition(
        emoji="✨",
        primary_meaning="Feature / New / Enhancement",
        category=EmojiCategory.CONCEPT,
        aliases=["feature", "new", "enhancement", "sparkle"],
        context_meanings={
            "with_code": "New feature",
            "with_idea": "Feature suggestion",
        },
        examples=["✨auth", "💡✨"],
        token_equivalent=1,  # "Feature"
    ),

    "💡": EmojiDefinition(
        emoji="💡",
        primary_meaning="Idea / Option / Suggestion",
        category=EmojiCategory.CONCEPT,
        aliases=["idea", "option", "suggestion", "light"],
        context_meanings={
            "from_tot": "Option generated by ToT",
            "alone": "Suggestion",
        },
        examples=["🌳→💡💡💡", "💡idea"],
        token_equivalent=1,  # "Option"
    ),

    "🏆": EmojiDefinition(
        emoji="🏆",
        primary_meaning="Winner / Best / Selected",
        category=EmojiCategory.CONCEPT,
        aliases=["winner", "best", "selected", "trophy"],
        context_meanings={
            "after_options": "Best option selected",
            "after_analysis": "Highest score",
        },
        examples=["💡💡💡→🏆", "🏆option2"],
        token_equivalent=2,  # "Best option"
    ),

    "📊": EmojiDefinition(
        emoji="📊",
        primary_meaning="Analysis / Metrics / Data",
        category=EmojiCategory.CONCEPT,
        aliases=["analysis", "metrics", "data", "chart"],
        context_meanings={
            "with_systemic": "Systemic analysis",
            "with_metrics": "Show metrics",
        },
        examples=["🧠📊", "📊LEI"],
        token_equivalent=1,  # "Analysis"
    ),

    "🏛️": EmojiDefinition(
        emoji="🏛️",
        primary_meaning="Constitutional Review (P1-P6)",
        category=EmojiCategory.CONCEPT,
        aliases=["constitutional", "principles", "temple"],
        context_meanings={
            "with_code": "Review code constitutionally",
            "with_check": "Constitutional validation",
        },
        examples=["🏛️✓", "code→🏛️"],
        token_equivalent=3,  # "Constitutional Review P1-P6"
    ),

    "⚖️": EmojiDefinition(
        emoji="⚖️",
        primary_meaning="Ethical Review (4 Frameworks)",
        category=EmojiCategory.CONCEPT,
        aliases=["ethical", "ethics", "balance", "justice"],
        context_meanings={
            "with_code": "Ethical review of code",
            "with_decision": "Ethical implications",
        },
        examples=["⚖️✓", "decision→⚖️"],
        token_equivalent=3,  # "Ethical Review 4 frameworks"
    ),

    # ========================================================================
    # TRUTH ENGINE & VITAL SYSTEM (Audit Vocabulary Extension)
    # ========================================================================

    "🔎": EmojiDefinition(
        emoji="🔎",
        primary_meaning="Independent Auditor / Truth Verification",
        category=EmojiCategory.AGENT,
        aliases=["auditor", "truth", "verify", "inspect"],
        context_meanings={
            "with_code": "Audit code implementation",
            "with_report": "Verify claims in report",
        },
        examples=["🔎→report", "code→🔎✓"],
        token_equivalent=4,  # "Independent Auditor Verification"
    ),

    "📋": EmojiDefinition(
        emoji="📋",
        primary_meaning="Requirements / Audit Report",
        category=EmojiCategory.CONCEPT,
        aliases=["requirements", "report", "evidence", "audit"],
        context_meanings={
            "with_check": "Requirements validated",
            "with_count": "Requirement count",
        },
        examples=["📋7→✅2🎭3❌2", "📋✓"],
        token_equivalent=2,  # "Audit Report"
    ),

    "🎚️": EmojiDefinition(
        emoji="🎚️",
        primary_meaning="Vital Signs / System Health",
        category=EmojiCategory.CONCEPT,
        aliases=["vitals", "health", "metrics", "status"],
        context_meanings={
            "with_emoji": "Vital system dashboard",
            "with_percent": "Health percentage",
        },
        examples=["🎚️💎100%", "🎚️🔴30%"],
        token_equivalent=3,  # "Vital System Health"
    ),

    "🔬": EmojiDefinition(
        emoji="🔬",
        primary_meaning="Deep Analysis / Truth Test",
        category=EmojiCategory.ACTION,
        aliases=["analyze", "inspect", "test", "examine"],
        context_meanings={
            "with_code": "Deep code analysis",
            "with_claim": "Verify claim truth",
        },
        examples=["code→🔬→📊", "🔬✓"],
        token_equivalent=3,  # "Deep Truth Analysis"
    ),

    "⚗️": EmojiDefinition(
        emoji="⚗️",
        primary_meaning="Truth Synthesis / Verification Process",
        category=EmojiCategory.ACTION,
        aliases=["synthesis", "process", "transform", "verify"],
        context_meanings={
            "with_data": "Process and verify data",
            "with_result": "Synthesized truth",
        },
        examples=["data→⚗️→truth", "⚗️✓"],
        token_equivalent=3,  # "Truth Synthesis Process"
    ),

    # 7 VITAL PILLARS

    "🌱": EmojiDefinition(
        emoji="🌱",
        primary_meaning="Growth / Learning (Vital Pilar 1)",
        category=EmojiCategory.STATE,
        aliases=["growth", "crescimento", "learning", "develop"],
        context_meanings={
            "with_percent": "Growth level",
            "with_up": "Learning increased",
        },
        examples=["🌱💎100%", "🌱🟢80%", "🌱↑"],
        token_equivalent=2,  # "Growth Level"
    ),

    "🍎": EmojiDefinition(
        emoji="🍎",
        primary_meaning="Nutrition / Energy (Vital Pilar 2)",
        category=EmojiCategory.STATE,
        aliases=["nutrition", "nutricao", "energy", "context"],
        context_meanings={
            "with_percent": "Energy level",
            "with_food": "Context feeding",
        },
        examples=["🍎💎100%", "🍎🟡50%"],
        token_equivalent=2,  # "Nutrition Level"
    ),

    "💚": EmojiDefinition(
        emoji="💚",
        primary_meaning="Healing / Recovery (Vital Pilar 3)",
        category=EmojiCategory.STATE,
        aliases=["healing", "cura", "recovery", "repair"],
        context_meanings={
            "with_percent": "Healing capacity",
            "with_error": "Error recovery",
        },
        examples=["💚💎100%", "💚🟢70%", "error→💚"],
        token_equivalent=2,  # "Healing Level"
    ),

    "🛡️": EmojiDefinition(
        emoji="🛡️",
        primary_meaning="Protection / Trust (Vital Pilar 4)",
        category=EmojiCategory.STATE,
        aliases=["protection", "protecao", "trust", "confidence"],
        context_meanings={
            "with_percent": "Trust level",
            "with_down": "Trust degraded",
        },
        examples=["🛡️💎100%", "🛡️🔴20%", "lie→🛡️↓"],
        token_equivalent=2,  # "Protection Level"
    ),

    "💪": EmojiDefinition(
        emoji="💪",
        primary_meaning="Survival / Existence (Vital Pilar 6)",
        category=EmojiCategory.STATE,
        aliases=["survival", "sobrevivencia", "strength", "vitality"],
        context_meanings={
            "with_percent": "Survival capacity",
            "with_critical": "Critical survival",
        },
        examples=["💪💎100%", "💪🔴15%"],
        token_equivalent=2,  # "Survival Level"
    ),

    # LEVEL INDICATORS (already partially covered, adding missing ones)

    "💎": EmojiDefinition(
        emoji="💎",
        primary_meaning="Excellent Level (90-100%)",
        category=EmojiCategory.STATE,
        aliases=["excellent", "perfect", "premium", "optimal"],
        context_meanings={
            "with_vital": "Vital at excellent level",
            "with_quality": "Excellent quality",
        },
        examples=["🌱💎", "quality💎"],
        token_equivalent=1,  # "Excellent"
    ),

    "🎭": EmojiDefinition(
        emoji="🎭",
        primary_meaning="Mock / Stub / Fake Implementation",
        category=EmojiCategory.STATE,
        aliases=["mock", "stub", "fake", "placeholder"],
        context_meanings={
            "with_code": "Mock implementation",
            "with_count": "Number of mocks",
        },
        examples=["🎭3", "func→🎭"],
        token_equivalent=2,  # "Mock Implementation"
    ),
}


# ============================================================================
# OPERATORS (Special syntax)
# ============================================================================

OPERATORS: Dict[str, str] = {
    "→": "then / flow / leads to",
    "+": "and / combine / with",
    "|": "or / alternative / either",
    "!": "not / negate / without",
    "?": "query / question / check",
    "✓": "validate / check / verify",
    ":": "agent performs / subject action",
}


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def get_emoji_definition(emoji: str) -> Optional[EmojiDefinition]:
    """Get definition for an emoji"""
    return EMOJI_VOCABULARY.get(emoji)


def get_emoji_by_alias(alias: str) -> Optional[str]:
    """Find emoji by alias (e.g., 'sophia' → '👑')"""
    alias_lower = alias.lower()
    for emoji, definition in EMOJI_VOCABULARY.items():
        if alias_lower in [a.lower() for a in definition.aliases]:
            return emoji
    return None


def get_emojis_by_category(category: EmojiCategory) -> List[str]:
    """Get all emojis in a category"""
    return [
        emoji
        for emoji, definition in EMOJI_VOCABULARY.items()
        if definition.category == category
    ]


def calculate_compression_ratio(text: str, epl: str) -> float:
    """Calculate token compression ratio"""
    # Rough estimate: 1 word ≈ 1.3 tokens
    text_tokens = len(text.split()) * 1.3
    # Each emoji ≈ 1 token (in practice, varies)
    epl_tokens = len([c for c in epl if c in EMOJI_VOCABULARY or c in OPERATORS])

    if text_tokens == 0:
        return 0.0

    return (text_tokens - epl_tokens) / text_tokens


def get_all_emojis() -> Set[str]:
    """Get set of all valid EPL emojis"""
    return set(EMOJI_VOCABULARY.keys())


def get_all_operators() -> Set[str]:
    """Get set of all valid EPL operators"""
    return set(OPERATORS.keys())


# ============================================================================
# CONTEXTUAL INTERPRETATION
# ============================================================================

def interpret_emoji_in_context(
    emoji: str,
    context: List[str]
) -> str:
    """
    Interpret emoji meaning based on surrounding context

    Args:
        emoji: The emoji to interpret
        context: List of surrounding emojis/tokens

    Returns:
        Contextual meaning
    """
    definition = get_emoji_definition(emoji)
    if not definition:
        return emoji  # Unknown emoji, return as-is

    # Check for specific context patterns
    if context:
        # Check if previous token modifies meaning
        if context[-1] == "!":
            # Negation
            return f"NOT {definition.primary_meaning}"

        if context[-1] == "🔥":
            # Urgency modifier
            return f"URGENT {definition.primary_meaning}"

    # Default to primary meaning
    return definition.primary_meaning


if __name__ == "__main__":
    # Demo
    logger.info("🧬 EPL Vocabulary Demo\n")
    logger.info("📖 Core Vocabulary:")
    for category in EmojiCategory:
        emojis = get_emojis_by_category(category)
        logger.info(f"\n{category.value.upper()}:")
        for emoji in emojis:
            definition = get_emoji_definition(emoji)
            logger.info(f"  {emoji} = {definition.primary_meaning}")
    logger.info("\n\n🔧 Operators:")
    for op, meaning in OPERATORS.items():
        logger.info(f"  {op} = {meaning}")
    logger.debug("\n\n🔍 Alias Lookup Examples:")
    logger.info(f"  'sophia' → {get_emoji_by_alias('sophia')}")
    logger.info(f"  'tot' → {get_emoji_by_alias('tot')}")
    logger.info(f"  'bug' → {get_emoji_by_alias('bug')}")
    logger.info("\n\n📊 Compression Examples:")
    examples = [
        ("Use tree of thoughts to analyze security", "🌳📊🔒"),
        ("Fix bug urgently", "🔥🐛→🔧"),
        ("Sophia generates 3 options and selects best", "👑:🌳→💡💡💡→🏆"),
    ]
    for text, epl in examples:
        ratio = calculate_compression_ratio(text, epl)
        logger.info(f"  '{text}'")
        logger.info(f"  → {epl}")
        logger.info(f"  Compression: {ratio:.1%}\n")