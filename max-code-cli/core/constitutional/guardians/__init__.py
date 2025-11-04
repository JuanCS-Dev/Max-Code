"""
Guardian Agents - 24/7 Constitutional Enforcement

Os Guardians são agentes especializados que GARANTEM conformidade constitucional
em TODAS as fases do ciclo de vida de geração de código.

Arquitetura:
-----------
1. PreExecutionGuardian: Valida ANTES de executar
2. RuntimeGuardian: Monitora DURANTE execução
3. PostExecutionGuardian: Valida DEPOIS de executar

Enforcement Layers:
-----------------
- Layer 1: PRE-EXECUTION (blocking)
  └─ Bloqueia ações não-constitucionais ANTES de começar

- Layer 2: RUNTIME (monitoring)
  └─ Monitora conformidade DURANTE execução
  └─ Pode INTERROMPER se violação detectada

- Layer 3: POST-EXECUTION (verification)
  └─ Valida resultado final
  └─ Pode REJEITAR output não-constitucional

"The Guardians never sleep. Constitutional compliance is non-negotiable."
"""

from .pre_execution_guardian import PreExecutionGuardian
from .runtime_guardian import RuntimeGuardian
from .post_execution_guardian import PostExecutionGuardian
from .guardian_coordinator import GuardianCoordinator
from .auto_protection import (
    AutoProtectionSystem,
    AutoProtectionMode,
    AutoCorrectionStrategy,
    get_auto_protection,
    enable_auto_protection,
    disable_auto_protection,
)

__all__ = [
    'PreExecutionGuardian',
    'RuntimeGuardian',
    'PostExecutionGuardian',
    'GuardianCoordinator',
    'AutoProtectionSystem',
    'AutoProtectionMode',
    'AutoCorrectionStrategy',
    'get_auto_protection',
    'enable_auto_protection',
    'disable_auto_protection',
]
