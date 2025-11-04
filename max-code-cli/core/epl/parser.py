"""
EPL Parser - Abstract Syntax Tree Construction

Parses token stream from Lexer into structured AST.

Biblical Foundation:
"E disse Deus: Haja luz; e houve luz." (Gênesis 1:3)
From tokens (words) we create structure (light) - parsing brings order to chaos.

EPL Grammar (EBNF):
    program        ::= statement*
    statement      ::= agent_invoke | action | expression
    agent_invoke   ::= AGENT ":" action
    action         ::= METHOD target? | chain
    chain          ::= expression ("→" expression)*
    expression     ::= term (operator term)*
    term           ::= emoji | operator | "(" expression ")"
    operator       ::= "→" | "+" | "|" | "!" | "?" | "✓"

Examples:
    👑:🌳          → Sophia uses Tree of Thoughts
    🌳📊🔒         → Analyze security with Tree of Thoughts
    👑:🌳→💡💡💡    → Sophia: ToT generates 3 insights
    🔴→🟢→🔄       → Red to Green (TDD) with refactor
"""

from typing import List, Optional, Union
from dataclasses import dataclass, field
from enum import Enum

from .lexer import Token, TokenType, tokenize
from .vocabulary import get_emoji_definition, OPERATORS, EmojiCategory


# ============================================================================
# AST NODE TYPES
# ============================================================================

class ASTNodeType(Enum):
    """Types of AST nodes"""
    # Program structure
    PROGRAM = "program"
    STATEMENT = "statement"

    # High-level constructs
    AGENT_INVOKE = "agent_invoke"      # 👑:🌳
    ACTION = "action"                   # 🔒📊
    CHAIN = "chain"                     # 🔴→🟢→🔄

    # Expressions
    EXPRESSION = "expression"           # 💡💡💡
    BINARY_OP = "binary_op"            # A + B, A | B

    # Terminals
    EMOJI = "emoji"                     # 🌳
    OPERATOR = "operator"               # →


@dataclass
class ASTNode:
    """Base AST node"""
    node_type: ASTNodeType
    line: int
    column: int
    children: List['ASTNode'] = field(default_factory=list)

    # Metadata
    value: Optional[str] = None         # For terminals (emoji, operator)
    meaning: Optional[str] = None       # Semantic meaning

    def __repr__(self) -> str:
        if self.value:
            return f"ASTNode({self.node_type.value}, '{self.value}')"
        else:
            return f"ASTNode({self.node_type.value}, children={len(self.children)})"

    def to_dict(self) -> dict:
        """Serialize to dict for debugging"""
        result = {
            'type': self.node_type.value,
            'line': self.line,
            'column': self.column,
        }

        if self.value:
            result['value'] = self.value
        if self.meaning:
            result['meaning'] = self.meaning
        if self.children:
            result['children'] = [child.to_dict() for child in self.children]

        return result


# ============================================================================
# PARSER
# ============================================================================

class Parser:
    """
    EPL Parser

    Recursive descent parser that builds AST from token stream.

    Algorithm:
    1. Start with program (list of statements)
    2. Each statement is either:
       - Agent invocation (👑:🌳)
       - Chain (🔴→🟢→🔄)
       - Simple action (🔒📊)
    3. Build tree recursively
    """

    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.position = 0

    def parse(self) -> ASTNode:
        """
        Parse token stream into AST

        Returns:
            Root AST node (PROGRAM)
        """
        return self._parse_program()

    # ========================================================================
    # GRAMMAR RULES
    # ========================================================================

    def _parse_program(self) -> ASTNode:
        """
        program ::= statement*
        """
        program = ASTNode(
            node_type=ASTNodeType.PROGRAM,
            line=1,
            column=1,
        )

        while not self._is_eof():
            # Skip newlines
            if self._current_token().type == TokenType.NEWLINE:
                self._advance()
                continue

            # Parse statement
            stmt = self._parse_statement()
            if stmt:
                program.children.append(stmt)
            else:
                # Skip unknown tokens
                self._advance()

        return program

    def _parse_statement(self) -> Optional[ASTNode]:
        """
        statement ::= agent_invoke | chain | action
        """
        # Try agent invocation first (has highest precedence)
        if self._is_agent_invoke():
            return self._parse_agent_invoke()

        # Try chain (has → operator)
        if self._has_chain():
            return self._parse_chain()

        # Otherwise, simple action
        return self._parse_action()

    def _parse_agent_invoke(self) -> ASTNode:
        """
        agent_invoke ::= AGENT ":" action

        Example: 👑:🌳 → Sophia uses Tree of Thoughts
        Example: 👑:🌳→💡💡💡→🏆 → Sophia: ToT generates 3 insights, pick winner
        """
        token = self._current_token()
        agent_token = token

        node = ASTNode(
            node_type=ASTNodeType.AGENT_INVOKE,
            line=token.line,
            column=token.column,
            value=token.value,
            meaning=token.emoji_meaning,
        )

        # Consume agent emoji
        self._advance()

        # Expect ":"
        if self._current_token().value != ":":
            # Missing ":", but continue parsing
            pass
        else:
            self._advance()  # Skip ":"

        # Parse action (which could be a chain!)
        # Check if rest is a chain
        if self._has_chain():
            action = self._parse_chain()
        else:
            action = self._parse_action()

        if action:
            node.children.append(action)

        return node

    def _parse_chain(self) -> ASTNode:
        """
        chain ::= expression ("→" expression)*

        Example: 🔴→🟢→🔄 → Red to Green to Refactor
        """
        first_token = self._current_token()

        node = ASTNode(
            node_type=ASTNodeType.CHAIN,
            line=first_token.line,
            column=first_token.column,
        )

        # Parse first expression
        expr = self._parse_expression()
        node.children.append(expr)

        # Parse remaining "→ expression" pairs
        while not self._is_eof() and self._current_token().value == "→":
            arrow_token = self._current_token()
            self._advance()  # Skip "→"

            # Create operator node
            op_node = ASTNode(
                node_type=ASTNodeType.OPERATOR,
                line=arrow_token.line,
                column=arrow_token.column,
                value="→",
                meaning="then, followed by",
            )
            node.children.append(op_node)

            # Parse next expression
            expr = self._parse_expression()
            node.children.append(expr)

        return node

    def _parse_action(self) -> ASTNode:
        """
        action ::= expression

        Simple action without chains
        """
        return self._parse_expression()

    def _parse_expression(self) -> ASTNode:
        """
        expression ::= term (operator term)*

        Handles binary operators (+, |, etc)
        """
        first_token = self._current_token()

        # Parse first term
        left = self._parse_term()

        # Check for binary operators
        while not self._is_eof() and self._is_binary_operator():
            op_token = self._current_token()
            self._advance()

            # Parse right term
            right = self._parse_term()

            # Create binary op node
            binary_node = ASTNode(
                node_type=ASTNodeType.BINARY_OP,
                line=op_token.line,
                column=op_token.column,
                value=op_token.value,
                meaning=op_token.operator_meaning,
            )
            binary_node.children = [left, right]

            left = binary_node  # Left becomes the binary op for next iteration

        return left

    def _parse_term(self) -> ASTNode:
        """
        term ::= emoji | operator
        """
        token = self._current_token()

        if token.type == TokenType.EMOJI:
            node = ASTNode(
                node_type=ASTNodeType.EMOJI,
                line=token.line,
                column=token.column,
                value=token.value,
                meaning=token.emoji_meaning,
            )
            self._advance()
            return node

        elif token.type == TokenType.OPERATOR:
            node = ASTNode(
                node_type=ASTNodeType.OPERATOR,
                line=token.line,
                column=token.column,
                value=token.value,
                meaning=token.operator_meaning,
            )
            self._advance()
            return node

        else:
            # Unknown term, skip
            self._advance()
            return ASTNode(
                node_type=ASTNodeType.EMOJI,
                line=token.line,
                column=token.column,
                value="�",
                meaning="unknown",
            )

    # ========================================================================
    # HELPER METHODS
    # ========================================================================

    def _current_token(self) -> Token:
        """Get current token"""
        if self.position >= len(self.tokens):
            # Return EOF token
            return Token(
                type=TokenType.EOF,
                value="",
                line=0,
                column=0
            )
        return self.tokens[self.position]

    def _peek(self, offset: int = 1) -> Token:
        """Peek ahead without consuming"""
        pos = self.position + offset
        if pos >= len(self.tokens):
            return Token(type=TokenType.EOF, value="", line=0, column=0)
        return self.tokens[pos]

    def _advance(self):
        """Move to next token"""
        if self.position < len(self.tokens):
            self.position += 1

    def _is_eof(self) -> bool:
        """Check if end of tokens"""
        if self.position >= len(self.tokens):
            return True
        return self.tokens[self.position].type == TokenType.EOF

    def _is_agent_invoke(self) -> bool:
        """Check if current position is agent invocation (👑:...)"""
        token = self._current_token()
        if token.type != TokenType.EMOJI:
            return False

        # Check if emoji is an agent
        definition = get_emoji_definition(token.value)
        if not definition:
            return False

        if definition.category != EmojiCategory.AGENT:
            return False

        # Check if next token is ":"
        next_token = self._peek()
        return next_token.value == ":"

    def _has_chain(self) -> bool:
        """Check if upcoming tokens form a chain (has → operator)"""
        # Look ahead for → operator
        pos = self.position
        while pos < len(self.tokens) and pos < self.position + 10:
            token = self.tokens[pos]
            if token.value == "→":
                return True
            if token.type in [TokenType.NEWLINE, TokenType.EOF]:
                break
            pos += 1
        return False

    def _is_binary_operator(self) -> bool:
        """Check if current token is a binary operator (+, |)"""
        token = self._current_token()
        if token.type != TokenType.OPERATOR:
            return False
        return token.value in ["+", "|"]


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def parse(source: str) -> ASTNode:
    """
    Convenience function to parse EPL source

    Args:
        source: EPL source string

    Returns:
        Root AST node

    Example:
        >>> ast = parse("👑:🌳→💡💡💡")
        >>> print(ast.to_dict())
    """
    tokens = tokenize(source)
    parser = Parser(tokens)
    return parser.parse()


def print_ast(node: ASTNode, indent: int = 0):
    """
    Pretty print AST for debugging

    Args:
        node: AST node to print
        indent: Indentation level
    """
    prefix = "  " * indent

    if node.value:
        meaning_str = f" ({node.meaning})" if node.meaning else ""
        print(f"{prefix}{node.node_type.value}: {node.value}{meaning_str}")
    else:
        print(f"{prefix}{node.node_type.value}")

    for child in node.children:
        print_ast(child, indent + 1)


# ============================================================================
# DEMO
# ============================================================================

if __name__ == "__main__":
    print("🌳 EPL Parser Demo\n")

    test_cases = [
        # Simple emoji sequence
        "🌳📊🔒",

        # Agent invocation (simple)
        "👑:🌳",

        # Chain (TDD workflow)
        "🔴→🟢→🔄",

        # Complex agent invocation with chain
        "👑:🌳→💡→🏆",

        # Binary operators
        "🔒+🔐",

        # Mixed (natural language + EPL)
        "Use 🌳 for analysis",

        # Multiple statements (separated by newlines)
        "🌳📊\n🔒🔐",
    ]

    for i, test in enumerate(test_cases, 1):
        print(f"Test {i}: \"{test}\"")
        print("-" * 60)

        # Parse
        ast = parse(test)

        # Print AST
        print_ast(ast)

        print()
