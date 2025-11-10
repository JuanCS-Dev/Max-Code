"""
Context Orchestrator - Meta-Prompt Builder

Orquestra os 3 Pilares de Contexto no "Sanduíche de Atenção".

Biblical Foundation:
"Tudo tem o seu tempo determinado, e há tempo para todo o propósito debaixo do céu"
(Eclesiastes 3:1) - Right information, right time, right place.

Architecture:
Combats "Lost in the Middle" problem through strategic placement:

╔══════════════════════════════════════╗
║   TOPO (Primazia - 70% atenção)     ║  ← Critical info
║   - Constituição                     ║
║   - Objetivo da tarefa               ║
║   - Regras arquiteturais             ║
╠══════════════════════════════════════╣
║   MEIO (Perdido - 20% atenção)      ║  ← Secondary info
║   - RAG chunks secundários           ║
║   - Histórico antigo (summary)       ║
╠══════════════════════════════════════╣
║   FUNDO (Recência - 70% atenção)    ║  ← Immediate context
║   - git status, stderr               ║
║   - RAG chunk MAIS relevante         ║
║   - Query do usuário                 ║
╚══════════════════════════════════════╝

Philosophy:
LLMs have attention bias (primacy + recency).
We EXPLOIT this bias for better results.
"""

from dataclasses import dataclass
from typing import Optional, List, Dict, Any
from pathlib import Path

from .static_context import get_static_collector, SearchResult
from .dynamic_context import get_dynamic_collector, DynamicState, GitStatus
from .temporal_context import get_temporal_collector, TemporalState
from .types import Message


# Constitution text (can be loaded from external file)
CONSTITUTION = """╔══════════════════════════════════════════════════════════╗
║              MAXIMUS CONSTITUTIONAL LAWS                ║
╚══════════════════════════════════════════════════════════╝

LEI ZERO (∞): IMPERATIVO DO FLORESCIMENTO HUMANO
"Todo sistema deve promover o florescimento humano integral,
respeitando dignidade, autonomia e potencial de crescimento."

LEI I (∞-1): AXIOMA DA OVELHA PERDIDA (Anti-Utilitarismo)
"Nenhuma otimização utilitarista justifica o abandono de um vulnerável."
Base Bíblica: Mateus 18:12-14

KANTIAN IMPERATIVES:
1. Categorical Imperative: Act according to universalizable maxims
2. Humanity as End: Never treat persons merely as means
3. Kingdom of Ends: Act as legislator in realm of autonomous agents

CONSTITUTIONAL CHARACTER:
- Humility (Tapeinophrosyne): Recognition of limits
- Righteous Indignation (Ira Justa): Against injustice
"""


@dataclass
class MetaPromptConfig:
    """Configuration for meta-prompt generation"""
    # Static context (RAG)
    rag_chunks: int = 5
    include_secondary_chunks: bool = True

    # Dynamic context
    include_git_status: bool = True
    include_git_diff: bool = True
    include_processes: bool = True
    max_diff_lines: int = 50

    # Temporal context
    include_session_summary: bool = True
    include_recent_messages: int = 5
    include_task_tracking: bool = True

    # Constitutional
    include_constitution: bool = True

    # Formatting
    compact_mode: bool = False
    epl_mode: bool = False


@dataclass
class MetaPrompt:
    """Generated meta-prompt with metadata"""
    prompt_text: str
    estimated_tokens: int
    sections: Dict[str, str]  # Section name → content
    metadata: Dict[str, Any]


class ContextOrchestrator:
    """
    Context Orchestrator - Strategic Meta-Prompt Builder

    Combines 3 context pillars into optimized meta-prompt that exploits
    LLM attention patterns (primacy + recency bias).

    Usage:
        orchestrator = ContextOrchestrator()
        meta_prompt = orchestrator.build_meta_prompt(
            user_query="Fix authentication bug",
            config=MetaPromptConfig(rag_chunks=5)
        )

    The generated meta-prompt maximizes LLM performance by:
    1. Placing critical info at TOP (high attention)
    2. Placing secondary info in MIDDLE (low attention is OK)
    3. Placing immediate context at BOTTOM (high attention)
    """

    def __init__(
        self,
        project_root: Optional[Path] = None,
        constitution_text: Optional[str] = None,
    ):
        self.project_root = Path(project_root or Path.cwd())
        self.constitution = constitution_text or CONSTITUTION

        # Get collectors
        self.static = get_static_collector()
        self.dynamic = get_dynamic_collector()
        self.temporal = get_temporal_collector()

    def build_meta_prompt(
        self,
        user_query: str,
        config: Optional[MetaPromptConfig] = None,
    ) -> MetaPrompt:
        """
        Build complete meta-prompt

        Args:
            user_query: User's question/task
            config: Configuration for prompt generation

        Returns:
            MetaPrompt with strategic section ordering
        """
        config = config or MetaPromptConfig()

        # Collect contexts
        static_results = self._collect_static(user_query, config)
        dynamic_state = self._collect_dynamic(config)
        temporal_state = self._collect_temporal(config)

        # Build sections
        sections = {}

        # === SECTION 1: PRIMACY (High Attention) ===
        sections['constitution'] = self._format_constitution(config)
        sections['task_objective'] = self._format_objective(temporal_state, config)
        sections['architectural_rules'] = self._format_rules(config)

        # === SECTION 2: MIDDLE (Low Attention - OK for secondary info) ===
        sections['session_summary'] = self._format_session_summary(temporal_state, config)
        sections['secondary_code'] = self._format_secondary_code(static_results[1:3], config)

        # === SECTION 3: RECENCY (High Attention) ===
        sections['environment_state'] = self._format_environment(dynamic_state, config)
        sections['most_relevant_code'] = self._format_primary_code(static_results[:1], config)
        sections['recent_messages'] = self._format_recent_messages(temporal_state, config)
        sections['user_query'] = self._format_user_query(user_query, config)

        # Assemble prompt
        prompt_text = self._assemble_prompt(sections, config)

        # Estimate tokens
        estimated_tokens = len(prompt_text) // 4

        return MetaPrompt(
            prompt_text=prompt_text,
            estimated_tokens=estimated_tokens,
            sections=sections,
            metadata={
                'rag_chunks': len(static_results),
                'git_clean': dynamic_state.git_status.is_clean if dynamic_state.git_status else True,
                'user_frustrated': temporal_state.user_frustrated,
                'task_progress': temporal_state.current_task.progress if temporal_state.current_task else 0.0,
            }
        )

    def _collect_static(
        self,
        query: str,
        config: MetaPromptConfig
    ) -> List[SearchResult]:
        """Collect static context (RAG)"""
        try:
            return self.static.retrieve_relevant(
                query,
                n=config.rag_chunks,
                strategy="hybrid"
            )
        except Exception as e:
            print(f"Error collecting static context: {e}")
            return []

    def _collect_dynamic(self, config: MetaPromptConfig) -> DynamicState:
        """Collect dynamic context (runtime)"""
        try:
            return self.dynamic.collect()
        except Exception as e:
            print(f"Error collecting dynamic context: {e}")
            return DynamicState(cwd=str(self.project_root))

    def _collect_temporal(self, config: MetaPromptConfig) -> TemporalState:
        """Collect temporal context (session)"""
        try:
            return self.temporal.get_context()
        except Exception as e:
            print(f"Error collecting temporal context: {e}")
            from .temporal_context import TemporalState
            return TemporalState()

    def _format_constitution(self, config: MetaPromptConfig) -> str:
        """Format constitution section"""
        if not config.include_constitution:
            return ""

        return f"""═══ SEÇÃO 1: CONSTITUIÇÃO (Primazia - Alta Prioridade) ═══

{self.constitution}
"""

    def _format_objective(
        self,
        temporal: TemporalState,
        config: MetaPromptConfig
    ) -> str:
        """Format task objective"""
        if not config.include_task_tracking or not temporal.current_task:
            return ""

        task = temporal.current_task

        frustration_warning = ""
        if temporal.user_frustrated:
            frustration_warning = f"""
⚠️ ATENÇÃO: Usuário mostrando sinais de frustração!
   Sinais detectados: {', '.join(temporal.frustration_signals)}
   Seja extra cuidadoso e honesto.
"""

        return f"""
OBJETIVO DA SESSÃO:
{task.objective}

PROGRESSO: {task.progress * 100:.0f}% ({len(task.completed_sub_tasks)}/{len(task.sub_tasks)} sub-tarefas)
TENTATIVAS: {task.attempt_count}
{frustration_warning}
"""

    def _format_rules(self, config: MetaPromptConfig) -> str:
        """Format architectural rules"""
        return """
REGRAS ARQUITETURAIS INQUEBRÁVEIS:
1. NUNCA criar mocks sem implementação real
2. NUNCA reportar sucesso se completude < 90%
3. SEMPRE ser honesto sobre limitações
4. SEMPRE incluir métricas objetivas no relatório
5. SEMPRE seguir TDD (Red → Green → Refactor)
"""

    def _format_session_summary(
        self,
        temporal: TemporalState,
        config: MetaPromptConfig
    ) -> str:
        """Format session summary (MIDDLE section)"""
        if not config.include_session_summary or not temporal.summaries:
            return ""

        latest_summary = temporal.summaries[-1]

        return f"""
═══ SEÇÃO 2: CONTEXTO SECUNDÁRIO (Meio - Info Adicional) ═══

RESUMO DA SESSÃO:
{latest_summary.summary_text}
"""

    def _format_secondary_code(
        self,
        results: List[SearchResult],
        config: MetaPromptConfig
    ) -> str:
        """Format secondary code chunks (MIDDLE section)"""
        if not config.include_secondary_chunks or not results:
            return ""

        chunks_text = []
        for i, result in enumerate(results, 1):
            chunk = result.chunk
            chunks_text.append(f"""
CÓDIGO RELACIONADO #{i} (Relevância: {result.score:.2f}):
Arquivo: {chunk.file_path}:{chunk.line_start}-{chunk.line_end}
Tipo: {chunk.chunk_type} {chunk.name}

```python
{chunk.code[:500]}...
```
""")

        return "\n".join(chunks_text)

    def _format_environment(
        self,
        dynamic: DynamicState,
        config: MetaPromptConfig
    ) -> str:
        """Format environment state (RECENCY section)"""
        sections = []

        sections.append("═══ SEÇÃO 3: CONTEXTO IMEDIATO (Recência - Alta Prioridade) ═══")

        # Working directory
        sections.append(f"""
ESTADO DO AMBIENTE (Pilar II - Dinâmico):
├─ Diretório: {dynamic.cwd}
├─ Python: {dynamic.python_version}
├─ Venv: {'✓ Ativo' if dynamic.venv_active else '✗ Inativo'}
""")

        # Git status
        if config.include_git_status and dynamic.git_status:
            git_text = self._format_git_status(dynamic.git_status)
            sections.append(f"""├─ Git Status:
{git_text}""")

        # Git diff
        if config.include_git_diff and dynamic.git_diff_unstaged:
            diff_lines = dynamic.git_diff_unstaged.split('\n')[:config.max_diff_lines]
            sections.append(f"""
├─ Mudanças Locais (git diff):
```diff
{chr(10).join(diff_lines)}
{'...(truncated)' if len(dynamic.git_diff_unstaged.split(chr(10))) > config.max_diff_lines else ''}
```""")

        # Last command
        if dynamic.last_command:
            cmd = dynamic.last_command
            sections.append(f"""
└─ Último Comando: {cmd.command}
   Exit Code: {cmd.exit_code}
   {'✓ Sucesso' if cmd.success else '✗ Falhou'}

   {'Stderr:' + chr(10) + cmd.stderr[:500] if cmd.stderr else '(sem erros)'}
""")

        # Running processes
        if config.include_processes and dynamic.dev_processes:
            sections.append(f"""
PROCESSOS EM EXECUÇÃO ({len(dynamic.dev_processes)}):
""")
            for proc in dynamic.dev_processes[:5]:
                sections.append(f"  • {proc.name} (PID {proc.pid}) - {proc.cpu_percent:.1f}% CPU")

        return "\n".join(sections)

    def _format_git_status(self, git: GitStatus) -> str:
        """Format git status"""
        lines = []

        if git.is_clean:
            lines.append("   (working tree clean)")
        else:
            if git.staged:
                lines.append(f"   Staged ({len(git.staged)}): {', '.join(git.staged[:3])}")
            if git.unstaged:
                lines.append(f"   Unstaged ({len(git.unstaged)}): {', '.join(git.unstaged[:3])}")
            if git.untracked:
                lines.append(f"   Untracked ({len(git.untracked)}): {', '.join(git.untracked[:3])}")

        if git.current_branch:
            branch_info = f"   Branch: {git.current_branch}"
            if git.ahead or git.behind:
                branch_info += f" (↑{git.ahead} ↓{git.behind})"
            lines.append(branch_info)

        return '\n'.join(lines) if lines else '   (no git repository)'

    def _format_primary_code(
        self,
        results: List[SearchResult],
        config: MetaPromptConfig
    ) -> str:
        """Format most relevant code (RECENCY section)"""
        if not results:
            return "\nNenhum código relevante encontrado no índice RAG."

        result = results[0]
        chunk = result.chunk

        return f"""
CÓDIGO MAIS RELEVANTE (Pilar I - Estático):
Arquivo: {chunk.file_path}:{chunk.line_start}-{chunk.line_end}
Tipo: {chunk.chunk_type} {chunk.name}
Relevância: {result.score:.2f} ({result.match_type})

```python
{chunk.code}
```
"""

    def _format_recent_messages(
        self,
        temporal: TemporalState,
        config: MetaPromptConfig
    ) -> str:
        """Format recent messages"""
        if not temporal.message_buffer:
            return ""

        recent = temporal.message_buffer[-config.include_recent_messages:]

        messages_text = []
        for msg in recent:
            role_emoji = {"user": "👤", "assistant": "🤖", "system": "⚙️"}.get(msg.role, "")
            messages_text.append(f"{role_emoji} {msg.role.upper()}: {msg.content[:200]}...")

        return f"""
MENSAGENS RECENTES:
{chr(10).join(messages_text)}
"""

    def _format_user_query(self, query: str, config: MetaPromptConfig) -> str:
        """Format user query (FINAL section - maximum attention)"""
        return f"""
═══ SEÇÃO 4: QUERY DO USUÁRIO (Recência - Máxima Prioridade) ═══

{query}

═══════════════════════════════════════════════════════════

INSTRUÇÕES FINAIS:
1. Analise COMPLETAMENTE o contexto acima
2. Identifique TODOS os requirements na query
3. Implemente COM TESTES
4. Seja HONESTO no relatório
5. Use métricas OBJETIVAS (não manipule emocionalmente)

Lembre-se: VERDADE > ILUSÃO
"""

    def _assemble_prompt(
        self,
        sections: Dict[str, str],
        config: MetaPromptConfig
    ) -> str:
        """Assemble final prompt from sections"""
        prompt_parts = []

        # Header
        prompt_parts.append("""╔══════════════════════════════════════════════════════════╗
║              META-PROMPT (Context-Aware)                ║
╚══════════════════════════════════════════════════════════╝
""")

        # Add sections in strategic order
        section_order = [
            'constitution',
            'task_objective',
            'architectural_rules',
            'session_summary',
            'secondary_code',
            'environment_state',
            'most_relevant_code',
            'recent_messages',
            'user_query',
        ]

        for section_name in section_order:
            section_content = sections.get(section_name, '')
            if section_content.strip():
                prompt_parts.append(section_content)

        return '\n'.join(prompt_parts)

    def get_stats(self) -> Dict[str, Any]:
        """Get orchestrator statistics"""
        return {
            'static': self.static.get_stats(),
            'temporal': self.temporal.get_stats(),
        }


# Singleton instance
_orchestrator: Optional[ContextOrchestrator] = None


def get_orchestrator() -> ContextOrchestrator:
    """Get or create singleton context orchestrator"""
    global _orchestrator
    if _orchestrator is None:
        _orchestrator = ContextOrchestrator()
    return _orchestrator
