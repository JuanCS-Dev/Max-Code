"""
State Management Layer - DETER-AGENT Layer 3

OBJETIVO: Gerenciar contexto, memória e estado do agente de forma eficiente.

MANDATO CONSTITUCIONAL:
- P6: Context Retention Score (CRS) ≥95%
- P6: Token efficiency (evitar redundância, usar compressão)

COMPONENTES:
1. Context Compression: Comprime contexto para maximizar token usage
2. Progressive Disclosure: Revela informação gradualmente (só o necessário)
3. Memory Manager: Gerencia memória de curto e longo prazo
4. Sub-agent Isolation: Isola contexto de sub-agents

"Põe-me como selo sobre o teu coração... porque o amor é forte como a morte"
(Cantares 8:6)
"""

from .context_compression import ContextCompressor, CompressionResult
from .progressive_disclosure import ProgressiveDisclosure, DisclosureLevel
from .memory_manager import MemoryManager, MemoryEntry, MemoryType
from .sub_agent_isolation import SubAgentIsolation, IsolatedContext

__all__ = [
    # Context Compression
    'ContextCompressor',
    'CompressionResult',

    # Progressive Disclosure
    'ProgressiveDisclosure',
    'DisclosureLevel',

    # Memory Manager
    'MemoryManager',
    'MemoryEntry',
    'MemoryType',

    # Sub-agent Isolation
    'SubAgentIsolation',
    'IsolatedContext',
]
