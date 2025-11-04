"""
Sub-Agent Isolation Implementation

OBJETIVO: Isolar contexto de sub-agents para prevenir vazamento de informação.

IDEIA CENTRAL:
- Quando spawnar sub-agent (ex: Agent Plan, Agent Explore)
- Sub-agent NÃO deve ter acesso a TODO contexto do parent
- Passar apenas o NECESSÁRIO (principle of least privilege)
- Prevenir information leakage + token waste

BENEFÍCIOS:
- Security (principle of least privilege)
- Token efficiency (sub-agent não vê contexto irrelevante)
- Clear boundaries (cada agent tem seu escopo)
- Prevents confusion (sub-agent não fica "distracted")

EXEMPLO:
```
Parent Agent: "Refatore função authenticate()"
  │
  ├─> Sub-agent (Code): Recebe APENAS:
  │     - Código de authenticate()
  │     - Requirements de refactoring
  │     - NÃO recebe: Histórico completo da conversa
  │
  └─> Sub-agent (Test): Recebe APENAS:
        - Código refatorado
        - Coverage requirements
        - NÃO recebe: Contexto de refactoring
```

"Cada um dê conforme determinou no seu coração, não com pesar ou por obrigação"
(2 Coríntios 9:7)
"""

from typing import List, Dict, Optional, Any
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime


class IsolationLevel(Enum):
    """Nível de isolamento"""
    FULL = "full"          # Sub-agent vê TUDO (não recomendado)
    PARTIAL = "partial"    # Sub-agent vê parte do contexto
    MINIMAL = "minimal"    # Sub-agent vê apenas o essencial (recomendado)
    NONE = "none"          # Sub-agent não vê nada do parent (para tasks independentes)


@dataclass
class IsolatedContext:
    """Contexto isolado para sub-agent"""
    agent_id: str
    agent_type: str  # 'plan', 'explore', 'code', 'test', etc
    isolation_level: IsolationLevel
    task: str  # Task específica do sub-agent
    allowed_context: Dict[str, Any]  # Contexto permitido
    forbidden_keys: List[str] = field(default_factory=list)  # Keys proibidas
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.utcnow)

    def has_access_to(self, key: str) -> bool:
        """Checa se sub-agent tem acesso a key"""
        if key in self.forbidden_keys:
            return False
        return key in self.allowed_context

    def get(self, key: str, default: Any = None) -> Any:
        """Pega valor do contexto (se permitido)"""
        if self.has_access_to(key):
            return self.allowed_context.get(key, default)
        else:
            # Log access denial (para auditoria)
            print(f"   🚫 Access denied: Sub-agent '{self.agent_id}' tried to access forbidden key '{key}'")
            return default


@dataclass
class SubAgentReport:
    """Relatório de execução do sub-agent"""
    agent_id: str
    agent_type: str
    task: str
    result: Any
    success: bool
    execution_time: float  # seconds
    tokens_used: int
    access_violations: int  # Quantas vezes tentou acessar contexto proibido
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict:
        return {
            'agent_id': self.agent_id,
            'agent_type': self.agent_type,
            'task': self.task[:100],
            'success': self.success,
            'execution_time': self.execution_time,
            'tokens_used': self.tokens_used,
            'access_violations': self.access_violations,
        }


class SubAgentIsolation:
    """
    Sub-Agent Isolation Engine

    PROCESSO:
    1. SPAWN: Parent agent spawna sub-agent
    2. ISOLATE: Cria IsolatedContext com apenas contexto necessário
    3. EXECUTE: Sub-agent executa com contexto isolado
    4. MERGE: Resultado do sub-agent é mergeado de volta ao parent
    5. AUDIT: Audita acessos (detectar access violations)

    BENEFÍCIOS:
    - Security (principle of least privilege)
    - Token efficiency (P6)
    - Clear boundaries
    - Auditability (P4 - rastrear o que sub-agent viu)

    MANDATO CONSTITUCIONAL:
    - P4: Rastreabilidade (auditar contexto passado para sub-agent)
    - P6: Token efficiency (não passar contexto desnecessário)

    "A cada um é dada a manifestação do Espírito para o proveito comum."
    (1 Coríntios 12:7)
    """

    def __init__(self, default_isolation_level: IsolationLevel = IsolationLevel.MINIMAL):
        """
        Inicializa Sub-Agent Isolation

        Args:
            default_isolation_level: Nível de isolamento padrão
        """
        self.default_isolation_level = default_isolation_level

        # Stats
        self.stats = {
            'total_sub_agents_spawned': 0,
            'access_violations': 0,
            'tokens_saved': 0,  # Tokens economizados por isolamento
        }

    def create_isolated_context(
        self,
        agent_type: str,
        task: str,
        full_context: Dict[str, Any],
        isolation_level: Optional[IsolationLevel] = None,
        whitelist: Optional[List[str]] = None,
        blacklist: Optional[List[str]] = None
    ) -> IsolatedContext:
        """
        Cria contexto isolado para sub-agent

        Args:
            agent_type: Tipo do sub-agent ('plan', 'explore', etc)
            task: Task específica
            full_context: Contexto completo do parent
            isolation_level: Nível de isolamento (None = usar default)
            whitelist: Keys permitidas (None = inferir do isolation_level)
            blacklist: Keys proibidas (None = vazio)

        Returns:
            IsolatedContext
        """
        self.stats['total_sub_agents_spawned'] += 1

        if isolation_level is None:
            isolation_level = self.default_isolation_level

        # Generate agent ID
        agent_id = f"{agent_type}_{self.stats['total_sub_agents_spawned']}"

        # Determinar contexto permitido
        if whitelist is not None:
            # Explicitamente especificado
            allowed_context = {
                key: full_context[key]
                for key in whitelist
                if key in full_context
            }
        else:
            # Inferir do isolation_level + agent_type
            allowed_context = self._infer_allowed_context(
                agent_type,
                full_context,
                isolation_level
            )

        # Forbidden keys
        forbidden_keys = blacklist or []

        # Calculate tokens saved
        full_context_size = sum(
            len(str(v)) for v in full_context.values()
        )
        allowed_context_size = sum(
            len(str(v)) for v in allowed_context.values()
        )
        tokens_saved = (full_context_size - allowed_context_size) // 4  # Rough estimate (4 chars = 1 token)
        self.stats['tokens_saved'] += tokens_saved

        print(f"🔒 Sub-Agent Isolation: Created isolated context for {agent_type}")
        print(f"   Isolation level: {isolation_level.value}")
        print(f"   Allowed keys: {len(allowed_context)} / {len(full_context)}")
        print(f"   Tokens saved: ~{tokens_saved}")

        return IsolatedContext(
            agent_id=agent_id,
            agent_type=agent_type,
            isolation_level=isolation_level,
            task=task,
            allowed_context=allowed_context,
            forbidden_keys=forbidden_keys,
        )

    def _infer_allowed_context(
        self,
        agent_type: str,
        full_context: Dict[str, Any],
        isolation_level: IsolationLevel
    ) -> Dict[str, Any]:
        """
        Infere contexto permitido baseado em agent_type e isolation_level

        Estratégia: Cada tipo de agent tem acesso a diferentes keys.

        Exemplos:
        - Agent Plan: Precisa ver requirements, constraints, mas não histórico completo
        - Agent Code: Precisa ver código existente, specifications, mas não logs de debug
        - Agent Test: Precisa ver código a testar, coverage requirements, mas não discussões de design
        """
        # Base keys (sempre permitidas)
        base_keys = ['task', 'requirements', 'constraints']

        # Agent-specific keys
        agent_specific_keys = {
            'plan': ['codebase_structure', 'existing_plans'],
            'explore': ['codebase_structure', 'search_patterns'],
            'code': ['existing_code', 'specifications', 'style_guide'],
            'test': ['code_to_test', 'coverage_requirements', 'test_framework'],
            'review': ['code_to_review', 'review_checklist'],
            'fix': ['error_logs', 'failing_tests', 'code_to_fix'],
            'docs': ['code_to_document', 'doc_style_guide'],
        }

        # Get allowed keys based on agent type
        allowed_keys = base_keys + agent_specific_keys.get(agent_type, [])

        # Apply isolation level
        if isolation_level == IsolationLevel.FULL:
            # Sub-agent vê TUDO
            return full_context.copy()
        elif isolation_level == IsolationLevel.PARTIAL:
            # Sub-agent vê agent-specific + alguns extras
            extra_keys = ['conversation_history', 'user_preferences']
            allowed_keys.extend(extra_keys)
        elif isolation_level == IsolationLevel.MINIMAL:
            # Sub-agent vê apenas agent-specific (default)
            pass
        elif isolation_level == IsolationLevel.NONE:
            # Sub-agent não vê nada do parent
            allowed_keys = []

        # Extract allowed context
        allowed_context = {
            key: full_context[key]
            for key in allowed_keys
            if key in full_context
        }

        return allowed_context

    def execute_sub_agent(
        self,
        isolated_context: IsolatedContext,
        execution_callback: Any  # Callable[[IsolatedContext], Any]
    ) -> SubAgentReport:
        """
        Executa sub-agent com contexto isolado

        Args:
            isolated_context: Contexto isolado
            execution_callback: Função que executa o sub-agent

        Returns:
            SubAgentReport
        """
        import time

        print(f"▶️  Executing sub-agent: {isolated_context.agent_id}")

        start_time = time.time()

        # Track access violations (via isolated_context)
        access_violations_before = self.stats['access_violations']

        try:
            # Execute sub-agent
            # Placeholder: em produção, isso chamaria o sub-agent real
            result = execution_callback(isolated_context)
            success = True
        except Exception as e:
            result = None
            success = False
            print(f"   ❌ Sub-agent failed: {e}")

        execution_time = time.time() - start_time

        # Calculate access violations during execution
        access_violations = self.stats['access_violations'] - access_violations_before

        # Placeholder: tokens_used (em produção, obter do LLM)
        tokens_used = 1000

        report = SubAgentReport(
            agent_id=isolated_context.agent_id,
            agent_type=isolated_context.agent_type,
            task=isolated_context.task,
            result=result,
            success=success,
            execution_time=execution_time,
            tokens_used=tokens_used,
            access_violations=access_violations,
        )

        print(f"   ✓ Sub-agent completed (success: {success}, time: {execution_time:.2f}s)")

        return report

    def merge_result(
        self,
        parent_context: Dict[str, Any],
        sub_agent_report: SubAgentReport,
        merge_key: str = 'sub_agent_results'
    ) -> Dict[str, Any]:
        """
        Merge resultado do sub-agent de volta ao parent context

        Args:
            parent_context: Contexto do parent
            sub_agent_report: Relatório do sub-agent
            merge_key: Key onde armazenar resultado

        Returns:
            Parent context atualizado
        """
        if merge_key not in parent_context:
            parent_context[merge_key] = []

        parent_context[merge_key].append(sub_agent_report.to_dict())

        print(f"   ✓ Merged sub-agent result into parent context")

        return parent_context

    def audit_access(self, isolated_context: IsolatedContext, attempted_key: str):
        """
        Audita tentativa de acesso (chamado quando sub-agent tenta acessar key proibida)

        Args:
            isolated_context: Contexto do sub-agent
            attempted_key: Key que tentou acessar
        """
        self.stats['access_violations'] += 1

        # Log para auditoria (P4 - rastreabilidade)
        print(f"   🚨 ACCESS VIOLATION: {isolated_context.agent_id} tried to access '{attempted_key}'")

    def get_stats(self) -> Dict:
        """Retorna estatísticas"""
        return {
            **self.stats,
        }

    def print_stats(self):
        """Imprime estatísticas"""
        stats = self.get_stats()

        print("\n" + "="*60)
        print("  SUB-AGENT ISOLATION - STATISTICS")
        print("="*60)
        print(f"Total sub-agents spawned:  {stats['total_sub_agents_spawned']}")
        print(f"Access violations:         {stats['access_violations']}")
        print(f"Tokens saved:              {stats['tokens_saved']:,}")
        print("="*60 + "\n")


# ==================== HELPER FUNCTIONS ====================

def spawn_isolated_sub_agent(
    agent_type: str,
    task: str,
    full_context: Dict[str, Any],
    execution_callback: Any
) -> SubAgentReport:
    """
    Helper function para spawnar sub-agent isolado

    Args:
        agent_type: Tipo do sub-agent
        task: Task
        full_context: Contexto completo
        execution_callback: Função de execução

    Returns:
        SubAgentReport
    """
    isolation = SubAgentIsolation()
    isolated_context = isolation.create_isolated_context(
        agent_type=agent_type,
        task=task,
        full_context=full_context,
    )
    return isolation.execute_sub_agent(isolated_context, execution_callback)
