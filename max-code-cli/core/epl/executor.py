"""
EPL Executor - Route EPL Commands to Agents

Executes parsed EPL by routing to appropriate Max-Code CLI agents.

Biblical Foundation:
"Portanto ide, fazei discípulos de todas as nações" (Mateus 28:19)
Go forth and execute - the EPL executor brings commands to life.

Execution Flow:
    1. Parse EPL → AST
    2. Analyze intent & agents
    3. Route to appropriate agent
    4. Return execution result
"""

from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass
from enum import Enum

from .parser import parse, ASTNode, ASTNodeType
from .translator import Translator, translate_to_nl
from .vocabulary import get_emoji_definition, EmojiCategory
from config.logging_config import get_logger

logger = get_logger(__name__)


class ExecutionStatus(Enum):
    """Status of EPL execution"""
    SUCCESS = "success"
    FAILED = "failed"
    PENDING = "pending"
    UNSUPPORTED = "unsupported"


@dataclass
class ExecutionResult:
    """Result of EPL execution"""
    status: ExecutionStatus
    message: str
    epl: str
    natural_language: str
    agent: Optional[str] = None      # Which agent was invoked
    output: Optional[Any] = None     # Agent output


class EPLExecutor:
    """
    EPL Executor

    Routes parsed EPL commands to Max-Code CLI agents.

    Integration with Max-Code:
    - 👑 (Sophia) → ArchitectAgent
    - 💻 (Code) → CodeAgent
    - 🧪 (Test) → TestAgent
    - 🐛 (Bug) → DebugAgent
    - 📚 (Docs) → DocsAgent
    - 📊 (Analysis) → AnalysisAgent
    """

    def __init__(self):
        self.translator = Translator()

        # Agent registry (to be populated by Max-Code CLI)
        self.agents: Dict[str, Callable] = {}

        # Agent emoji mappings
        self.agent_map = {
            "👑": "sophia",           # Sophia (Architect)
            "💻": "code",             # Code generation
            "🧪": "test",             # Testing
            "🐛": "debug",            # Debugging/fixing
            "📚": "docs",             # Documentation
            "📊": "analysis",         # Analysis
            "🔍": "explore",          # Code exploration
            "👀": "review",           # Code review
        }

    def register_agent(self, agent_id: str, handler: Callable):
        """
        Register an agent handler

        Args:
            agent_id: Agent identifier (e.g., "sophia", "code")
            handler: Callable that handles agent execution
        """
        self.agents[agent_id] = handler

    def execute(self, epl: str, context: Optional[Dict] = None) -> ExecutionResult:
        """
        Execute EPL command

        Args:
            epl: EPL input (emoji protocol)
            context: Optional execution context

        Returns:
            ExecutionResult

        Example:
            >>> executor = EPLExecutor()
            >>> executor.register_agent("sophia", sophia_handler)
            >>> result = executor.execute("👑:🌳")
            >>> print(result.message)
            "Sophia invoked with Tree of Thoughts"
        """
        context = context or {}

        # Translate to natural language for logging
        nl = translate_to_nl(epl)

        # Parse EPL
        try:
            ast = parse(epl)
        except Exception as e:
            return ExecutionResult(
                status=ExecutionStatus.FAILED,
                message=f"Failed to parse EPL: {e}",
                epl=epl,
                natural_language=nl,
            )

        # Execute AST
        try:
            return self._execute_ast(ast, epl, nl, context)
        except Exception as e:
            return ExecutionResult(
                status=ExecutionStatus.FAILED,
                message=f"Execution failed: {e}",
                epl=epl,
                natural_language=nl,
            )

    def _execute_ast(
        self,
        ast: ASTNode,
        epl: str,
        nl: str,
        context: Dict
    ) -> ExecutionResult:
        """
        Execute AST node

        Recursive execution of AST
        """
        if ast.node_type == ASTNodeType.PROGRAM:
            # Execute all statements
            results = []
            for child in ast.children:
                result = self._execute_ast(child, epl, nl, context)
                results.append(result)

            # Aggregate results
            if all(r.status == ExecutionStatus.SUCCESS for r in results):
                return ExecutionResult(
                    status=ExecutionStatus.SUCCESS,
                    message=f"Executed {len(results)} statement(s)",
                    epl=epl,
                    natural_language=nl,
                    output=results,
                )
            else:
                return ExecutionResult(
                    status=ExecutionStatus.FAILED,
                    message="Some statements failed",
                    epl=epl,
                    natural_language=nl,
                    output=results,
                )

        elif ast.node_type == ASTNodeType.AGENT_INVOKE:
            # Agent invocation: 👑:🌳
            agent_emoji = ast.value
            agent_id = self.agent_map.get(agent_emoji)

            if not agent_id:
                return ExecutionResult(
                    status=ExecutionStatus.UNSUPPORTED,
                    message=f"Unknown agent: {agent_emoji}",
                    epl=epl,
                    natural_language=nl,
                    agent=agent_emoji,
                )

            # Get action (what agent should do)
            action = None
            if ast.children:
                action = ast.children[0]

            # Check if agent is registered
            if agent_id not in self.agents:
                return ExecutionResult(
                    status=ExecutionStatus.UNSUPPORTED,
                    message=f"Agent '{agent_id}' not registered",
                    epl=epl,
                    natural_language=nl,
                    agent=agent_id,
                )

            # Invoke agent
            agent_handler = self.agents[agent_id]
            try:
                # Build agent context
                agent_context = {
                    **context,
                    "epl": epl,
                    "natural_language": nl,
                    "action": action,
                }

                output = agent_handler(agent_context)

                return ExecutionResult(
                    status=ExecutionStatus.SUCCESS,
                    message=f"Agent '{agent_id}' executed successfully",
                    epl=epl,
                    natural_language=nl,
                    agent=agent_id,
                    output=output,
                )

            except Exception as e:
                return ExecutionResult(
                    status=ExecutionStatus.FAILED,
                    message=f"Agent '{agent_id}' failed: {e}",
                    epl=epl,
                    natural_language=nl,
                    agent=agent_id,
                )

        elif ast.node_type == ASTNodeType.CHAIN:
            # Chain execution: A → B → C
            # Execute sequentially
            chain_results = []
            for child in ast.children:
                if child.node_type != ASTNodeType.OPERATOR:
                    result = self._execute_ast(child, epl, nl, context)
                    chain_results.append(result)

            return ExecutionResult(
                status=ExecutionStatus.SUCCESS,
                message=f"Chain executed ({len(chain_results)} steps)",
                epl=epl,
                natural_language=nl,
                output=chain_results,
            )

        elif ast.node_type == ASTNodeType.EMOJI:
            # Single emoji - interpret as intent
            emoji = ast.value
            definition = get_emoji_definition(emoji)

            if definition and definition.category == EmojiCategory.AGENT:
                # It's an agent, invoke it
                agent_id = self.agent_map.get(emoji)
                if agent_id and agent_id in self.agents:
                    agent_handler = self.agents[agent_id]
                    agent_context = {
                        **context,
                        "epl": epl,
                        "natural_language": nl,
                    }
                    output = agent_handler(agent_context)

                    return ExecutionResult(
                        status=ExecutionStatus.SUCCESS,
                        message=f"Agent '{agent_id}' executed",
                        epl=epl,
                        natural_language=nl,
                        agent=agent_id,
                        output=output,
                    )

            # Otherwise, just acknowledge
            return ExecutionResult(
                status=ExecutionStatus.SUCCESS,
                message=f"Acknowledged: {ast.meaning or emoji}",
                epl=epl,
                natural_language=nl,
            )

        else:
            # Other node types - acknowledge
            return ExecutionResult(
                status=ExecutionStatus.SUCCESS,
                message=f"Executed {ast.node_type.value}",
                epl=epl,
                natural_language=nl,
            )

    def get_registered_agents(self) -> List[str]:
        """Get list of registered agent IDs"""
        return list(self.agents.keys())


# ============================================================================
# DEMO
# ============================================================================

if __name__ == "__main__":
    logger.info("⚙️ EPL Executor Demo\n")
    # Create executor
    executor = EPLExecutor()

    # Mock agent handlers
    def sophia_handler(context: Dict) -> str:
        action = context.get("action")
        return f"Sophia executed with action: {action}"

    def code_handler(context: Dict) -> str:
        return "Code generation executed"

    def test_handler(context: Dict) -> str:
        return "Test generation executed"

    # Register agents
    executor.register_agent("sophia", sophia_handler)
    executor.register_agent("code", code_handler)
    executor.register_agent("test", test_handler)

    logger.info(f"Registered agents: {executor.get_registered_agents()}\n")
    # ========================================================================
    # TEST CASES
    # ========================================================================

    test_cases = [
        # Simple agent invocation
        ("👑:🌳", "Sophia with Tree of Thoughts"),

        # Chain
        ("🔴→🟢→🔄", "TDD workflow"),

        # Complex agent + chain
        ("👑:🌳→💡→🏆", "Sophia: ToT → Ideas → Winner"),

        # Code generation
        ("💻", "Code generation"),

        # Unknown agent
        ("🚀:🔥", "Unknown agent"),
    ]

    for i, (epl, description) in enumerate(test_cases, 1):
        logger.info(f"Test {i}: {description}")
        logger.info(f"  EPL: {epl}")
        result = executor.execute(epl)

        logger.info(f"  Status: {result.status.value}")
        logger.info(f"  Message: {result.message}")
        if result.agent:
            logger.info(f"  Agent: {result.agent}")
        if result.natural_language:
            logger.info(f"  NL: {result.natural_language}")
        print()
