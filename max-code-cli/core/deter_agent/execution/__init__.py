"""
Execution Layer - DETER-AGENT Layer 4

OBJETIVO: Executar ações de forma estruturada, segura e TDD-first.

MANDATO CONSTITUCIONAL:
- P1: Completude (nunca placeholders, stubs)
- P2: API validation (validar antes de usar)
- P6: FPC ≥80% (First-Pass Correctness)

COMPONENTES:
1. Tool Executor: Executa ferramentas (bash, file ops, API calls)
2. TDD Enforcer: Força test-driven development (tests BEFORE code)
3. Action Validator: Valida ações antes de executar
4. Structured Actions: Ações estruturadas (não ad-hoc)

FILOSOFIA:
- Tests FIRST, code SECOND (TDD)
- Validar BEFORE executar (fail-fast)
- Structured (não ad-hoc)
- Auditable (P4 - rastrear cada ação)

"Tudo quanto fizerdes, fazei-o de todo o coração, como ao Senhor..."
(Colossenses 3:23)
"""

from .tool_executor import ToolExecutor, Tool, ToolResult
from .tdd_enforcer import TDDEnforcer, TestStatus, TDDViolation
from .action_validator import ActionValidator, Action, ActionType
from .structured_actions import StructuredAction, ActionPlan, ActionStep

__all__ = [
    # Tool Executor
    'ToolExecutor',
    'Tool',
    'ToolResult',

    # TDD Enforcer
    'TDDEnforcer',
    'TestStatus',
    'TDDViolation',

    # Action Validator
    'ActionValidator',
    'Action',
    'ActionType',

    # Structured Actions
    'StructuredAction',
    'ActionPlan',
    'ActionStep',
]
