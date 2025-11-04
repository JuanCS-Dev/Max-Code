"""
Scientific Tests for EPL Parser

Tests the parser that converts token stream into Abstract Syntax Tree (AST).

Test Philosophy:
- Test REAL AST construction
- Validate node types, structure, parent-child relationships
- Test complex grammar patterns
- Scientific rigor: reproducible, deterministic

Run:
    pytest tests/test_epl_parser.py -v
"""

import pytest
from core.epl.parser import (
    Parser,
    ASTNode,
    ASTNodeType,
    parse,
    print_ast,
)
from core.epl.lexer import tokenize


# ============================================================================
# TEST: AST Node Structure
# ============================================================================

def test_ast_node_creation():
    """Test ASTNode can be created"""
    node = ASTNode(
        node_type=ASTNodeType.EMOJI,
        line=1,
        column=1,
        value="🌳",
        meaning="Tree of Thoughts"
    )

    assert node.node_type == ASTNodeType.EMOJI
    assert node.line == 1
    assert node.column == 1
    assert node.value == "🌳"
    assert node.meaning == "Tree of Thoughts"
    assert len(node.children) == 0


def test_ast_node_with_children():
    """Test ASTNode with children"""
    parent = ASTNode(
        node_type=ASTNodeType.PROGRAM,
        line=1,
        column=1
    )

    child = ASTNode(
        node_type=ASTNodeType.EMOJI,
        line=1,
        column=1,
        value="🌳"
    )

    parent.children.append(child)

    assert len(parent.children) == 1
    assert parent.children[0] == child


def test_ast_node_to_dict():
    """Test ASTNode serialization to dict"""
    node = ASTNode(
        node_type=ASTNodeType.EMOJI,
        line=1,
        column=5,
        value="🌳",
        meaning="Tree of Thoughts"
    )

    node_dict = node.to_dict()

    assert node_dict['type'] == 'emoji'
    assert node_dict['line'] == 1
    assert node_dict['column'] == 5
    assert node_dict['value'] == "🌳"
    assert node_dict['meaning'] == "Tree of Thoughts"


# ============================================================================
# TEST: Parser Initialization
# ============================================================================

def test_parser_initialization():
    """Test Parser can be initialized with tokens"""
    tokens = tokenize("🌳")
    parser = Parser(tokens)

    assert parser.tokens == tokens
    assert parser.position == 0


# ============================================================================
# TEST: Simple EPL Parsing
# ============================================================================

def test_parse_single_emoji():
    """Test parsing single emoji"""
    ast = parse("🌳")

    assert ast.node_type == ASTNodeType.PROGRAM
    assert len(ast.children) >= 1

    # First child should be emoji node
    first_stmt = ast.children[0]
    assert first_stmt.value == "🌳"


def test_parse_multiple_emojis():
    """Test parsing multiple emojis in sequence"""
    ast = parse("🌳📊🔒")

    assert ast.node_type == ASTNodeType.PROGRAM

    # Should have statement(s) containing emojis
    assert len(ast.children) >= 1


def test_parse_emoji_sequence_without_operators():
    """Test parsing emoji sequence (no operators)"""
    ast = parse("🌳📊")

    assert ast.node_type == ASTNodeType.PROGRAM
    assert len(ast.children) >= 1


# ============================================================================
# TEST: Chain Parsing (→ operator)
# ============================================================================

def test_parse_simple_chain():
    """Test parsing simple chain with → operator"""
    ast = parse("🔴→🟢")

    assert ast.node_type == ASTNodeType.PROGRAM
    assert len(ast.children) >= 1

    # First child should be a chain
    chain = ast.children[0]
    assert chain.node_type == ASTNodeType.CHAIN

    # Chain should have multiple children (emojis and operators)
    assert len(chain.children) >= 2


def test_parse_long_chain():
    """Test parsing long chain"""
    ast = parse("🔴→🟢→🔄")

    assert ast.node_type == ASTNodeType.PROGRAM

    chain = ast.children[0]
    assert chain.node_type == ASTNodeType.CHAIN

    # Should have at least 3 emojis (🔴, 🟢, 🔄)
    emoji_children = [c for c in chain.children if c.node_type == ASTNodeType.EMOJI]
    assert len(emoji_children) >= 3


def test_parse_chain_with_complex_emojis():
    """Test parsing chain with various emojis"""
    ast = parse("🌳→💡→🏆")

    chain = ast.children[0]
    assert chain.node_type == ASTNodeType.CHAIN

    emoji_children = [c for c in chain.children if c.node_type == ASTNodeType.EMOJI]
    assert len(emoji_children) == 3


# ============================================================================
# TEST: Agent Invocation Parsing (👑:...)
# ============================================================================

def test_parse_simple_agent_invocation():
    """Test parsing simple agent invocation"""
    ast = parse("👑:🌳")

    assert ast.node_type == ASTNodeType.PROGRAM
    assert len(ast.children) >= 1

    # First child should be agent invocation
    agent_invoke = ast.children[0]
    assert agent_invoke.node_type == ASTNodeType.AGENT_INVOKE
    assert agent_invoke.value == "👑"

    # Should have action as child
    assert len(agent_invoke.children) >= 1


def test_parse_agent_invocation_with_chain():
    """Test parsing agent invocation with chain"""
    ast = parse("👑:🌳→💡→🏆")

    agent_invoke = ast.children[0]
    assert agent_invoke.node_type == ASTNodeType.AGENT_INVOKE
    assert agent_invoke.value == "👑"

    # Action should be a chain
    action = agent_invoke.children[0]
    assert action.node_type == ASTNodeType.CHAIN


def test_parse_agent_invocation_with_single_action():
    """Test parsing agent invocation with single action"""
    ast = parse("👑:🌳")

    agent_invoke = ast.children[0]
    assert agent_invoke.node_type == ASTNodeType.AGENT_INVOKE

    # Should have one action
    assert len(agent_invoke.children) >= 1


# ============================================================================
# TEST: Binary Operator Parsing (+, |)
# ============================================================================

def test_parse_plus_operator():
    """Test parsing + operator"""
    ast = parse("🔒+🌳")

    assert ast.node_type == ASTNodeType.PROGRAM

    # Should have binary op or expression
    stmt = ast.children[0]

    # The structure might vary, but should contain both emojis
    # Let's check if we can find both emojis in the tree
    def find_emojis(node):
        emojis = []
        if node.node_type == ASTNodeType.EMOJI:
            emojis.append(node.value)
        for child in node.children:
            emojis.extend(find_emojis(child))
        return emojis

    emojis = find_emojis(ast)
    assert "🔒" in emojis
    assert "🌳" in emojis


def test_parse_or_operator():
    """Test parsing | operator"""
    ast = parse("🌳|📊")

    # Should parse successfully
    assert ast.node_type == ASTNodeType.PROGRAM
    assert len(ast.children) >= 1


# ============================================================================
# TEST: Complex Grammar Combinations
# ============================================================================

def test_parse_multiple_statements():
    """Test parsing multiple statements (separated by newlines)"""
    ast = parse("🌳📊\n🔒🔐")

    assert ast.node_type == ASTNodeType.PROGRAM

    # Should have 2 statements
    assert len(ast.children) >= 2


def test_parse_nested_complex_structure():
    """Test parsing complex nested structure"""
    ast = parse("👑:🌳→💡💡💡→🏆")

    # Should parse as agent invocation with chain
    agent_invoke = ast.children[0]
    assert agent_invoke.node_type == ASTNodeType.AGENT_INVOKE

    # Action should be a chain
    action = agent_invoke.children[0]
    assert action.node_type == ASTNodeType.CHAIN


# ============================================================================
# TEST: Mixed Natural Language + EPL Parsing
# ============================================================================

def test_parse_mixed_input_with_words():
    """Test parsing mixed natural language and EPL"""
    # Parser should handle mixed input gracefully
    # (Words might be skipped or treated as terminals)
    ast = parse("Use 🌳 for analysis")

    assert ast.node_type == ASTNodeType.PROGRAM

    # Should have parsed something
    assert ast is not None


# ============================================================================
# TEST: Edge Cases
# ============================================================================

def test_parse_empty_string():
    """Test parsing empty string"""
    ast = parse("")

    assert ast.node_type == ASTNodeType.PROGRAM

    # Empty program has no statements
    assert len(ast.children) == 0


def test_parse_only_operators():
    """Test parsing only operators (edge case)"""
    ast = parse("→→")

    # Should parse without crashing
    assert ast.node_type == ASTNodeType.PROGRAM


def test_parse_incomplete_chain():
    """Test parsing incomplete chain (ends with →)"""
    ast = parse("🔴→")

    # Should parse what it can
    assert ast.node_type == ASTNodeType.PROGRAM


# ============================================================================
# TEST: Parser Helper Methods
# ============================================================================

def test_parser_current_token():
    """Test parser's current token tracking"""
    tokens = tokenize("🌳📊")
    parser = Parser(tokens)

    # Should start at position 0
    first_token = parser._current_token()
    assert first_token == tokens[0]


def test_parser_advance():
    """Test parser advance method"""
    tokens = tokenize("🌳📊")
    parser = Parser(tokens)

    initial_pos = parser.position
    parser._advance()

    assert parser.position == initial_pos + 1


def test_parser_is_eof():
    """Test parser EOF detection"""
    tokens = tokenize("🌳")
    parser = Parser(tokens)

    # Should not be EOF at start
    assert parser._is_eof() == False

    # Advance past all tokens
    while parser.position < len(tokens):
        parser._advance()

    # Should be EOF now
    assert parser._is_eof() == True


# ============================================================================
# TEST: AST Utility Functions
# ============================================================================

def test_print_ast_function():
    """Test print_ast utility function"""
    ast = parse("👑:🌳")

    # Should not crash when printing
    import io
    import sys
    old_stdout = sys.stdout
    sys.stdout = buffer = io.StringIO()

    try:
        print_ast(ast)
        output = buffer.getvalue()

        # Should have printed something
        assert len(output) > 0
    finally:
        sys.stdout = old_stdout


# ============================================================================
# TEST: Real-World EPL Patterns
# ============================================================================

def test_parse_tdd_workflow():
    """Test parsing TDD workflow pattern"""
    ast = parse("🔴→🟢→🔄")

    chain = ast.children[0]
    assert chain.node_type == ASTNodeType.CHAIN

    # Find emoji values in order
    emojis = [c.value for c in chain.children if c.node_type == ASTNodeType.EMOJI]
    assert "🔴" in emojis
    assert "🟢" in emojis
    assert "🔄" in emojis


def test_parse_sophia_tot_pattern():
    """Test parsing Sophia with Tree of Thoughts pattern"""
    ast = parse("👑:🌳→💡→🏆")

    agent_invoke = ast.children[0]
    assert agent_invoke.node_type == ASTNodeType.AGENT_INVOKE
    assert agent_invoke.value == "👑"

    # Should have chain as action
    action = agent_invoke.children[0]
    assert action.node_type == ASTNodeType.CHAIN


def test_parse_security_analysis_pattern():
    """Test parsing security analysis pattern"""
    ast = parse("🌳📊🔒")

    # Should parse successfully
    assert ast.node_type == ASTNodeType.PROGRAM
    assert len(ast.children) >= 1


# ============================================================================
# TEST: Parser Robustness
# ============================================================================

def test_parser_handles_unknown_tokens_gracefully():
    """Test parser handles unknown tokens without crashing"""
    # Even with unexpected input, parser should not crash
    tokens = tokenize("???")
    parser = Parser(tokens)

    # Should complete parsing
    ast = parser.parse()
    assert ast is not None


def test_parser_handles_long_input():
    """Test parser handles long EPL chains"""
    long_chain = "→".join(["🌳"] * 20)  # 20 emojis chained
    ast = parse(long_chain)

    # Should parse successfully
    assert ast.node_type == ASTNodeType.PROGRAM


# ============================================================================
# SUMMARY
# ============================================================================

"""
Test Coverage Summary:

1. AST Node Structure (3 tests)
   - Node creation
   - Node with children
   - Node serialization

2. Parser Initialization (1 test)
   - Basic initialization

3. Simple EPL Parsing (3 tests)
   - Single emoji
   - Multiple emojis
   - Emoji sequence

4. Chain Parsing (3 tests)
   - Simple chain
   - Long chain
   - Chain with complex emojis

5. Agent Invocation (3 tests)
   - Simple invocation
   - Invocation with chain
   - Invocation with single action

6. Binary Operators (2 tests)
   - Plus operator
   - Or operator

7. Complex Grammar (2 tests)
   - Multiple statements
   - Nested structures

8. Mixed Input (1 test)
   - Natural language + EPL

9. Edge Cases (3 tests)
   - Empty string
   - Only operators
   - Incomplete chain

10. Parser Helpers (3 tests)
    - Current token
    - Advance
    - EOF detection

11. AST Utilities (1 test)
    - Print AST

12. Real-World Patterns (3 tests)
    - TDD workflow
    - Sophia ToT
    - Security analysis

13. Parser Robustness (2 tests)
    - Unknown tokens
    - Long input

Total: 30 scientific tests for EPL Parser
"""
