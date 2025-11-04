"""
Progressive Disclosure Implementation

OBJETIVO: Revelar informação gradualmente (só o necessário).

IDEIA CENTRAL:
- Não jogar TUDO no contexto de uma vez
- Revelar informação em camadas (progressive disclosure)
- Começar com overview, revelar detalhes sob demanda
- Reduzir cognitive load + token usage

BENEFÍCIOS:
- Token efficiency (P6)
- Cognitive load reduzido
- Contexto mais focado
- Melhor compreensão

NÍVEIS DE DISCLOSURE:
1. OVERVIEW: Apenas visão geral (nomes, tipos)
2. SUMMARY: Resumo (1-2 sentences)
3. DETAILED: Detalhes completos
4. FULL: Tudo (incluindo implementação)

"Ainda tenho muito que vos dizer, mas vós não o podeis suportar agora."
(João 16:12)
"""

from typing import List, Dict, Optional, Any
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime


class DisclosureLevel(Enum):
    """Nível de disclosure"""
    OVERVIEW = "overview"    # Apenas nomes/tipos
    SUMMARY = "summary"      # Resumo (1-2 sentences)
    DETAILED = "detailed"    # Detalhes (sem implementação)
    FULL = "full"           # Tudo


@dataclass
class DisclosableItem:
    """Item que pode ser revelado progressivamente"""
    id: str
    name: str
    type: str  # 'function', 'class', 'file', 'module', etc
    overview: str  # Nome + tipo
    summary: str  # 1-2 sentences
    detailed: str  # Detalhes (assinaturas, docstrings)
    full: str  # Implementação completa
    metadata: Dict[str, Any] = field(default_factory=dict)
    current_level: DisclosureLevel = DisclosureLevel.OVERVIEW

    def reveal_at_level(self, level: DisclosureLevel) -> str:
        """Revela item no nível especificado"""
        self.current_level = level

        if level == DisclosureLevel.OVERVIEW:
            return self.overview
        elif level == DisclosureLevel.SUMMARY:
            return self.summary
        elif level == DisclosureLevel.DETAILED:
            return self.detailed
        elif level == DisclosureLevel.FULL:
            return self.full

    def reveal_next_level(self) -> str:
        """Revela próximo nível"""
        levels = list(DisclosureLevel)
        current_idx = levels.index(self.current_level)

        if current_idx < len(levels) - 1:
            next_level = levels[current_idx + 1]
            return self.reveal_at_level(next_level)
        else:
            return self.full  # Já no máximo


@dataclass
class DisclosureContext:
    """Contexto com progressive disclosure"""
    items: List[DisclosableItem]
    current_level: DisclosureLevel
    revealed_items: List[str] = field(default_factory=list)  # IDs revelados em FULL
    metadata: Dict[str, Any] = field(default_factory=dict)


class ProgressiveDisclosure:
    """
    Progressive Disclosure Engine

    PROCESSO:
    1. START: Começa com OVERVIEW (só nomes)
    2. QUERY: User pergunta sobre algo específico
    3. REVEAL: Revela detalhes SOMENTE do que foi perguntado
    4. ITERATE: Repete até user ter informação suficiente

    BENEFÍCIOS:
    - Token efficiency (P6)
    - Focused context (só o relevante)
    - Melhor compreensão (passo-a-passo)
    - Reduz cognitive load

    EXEMPLO:
    ```
    # Fase 1: OVERVIEW
    User: "Mostre arquivos"
    Agent: "3 arquivos: auth.py, db.py, api.py"

    # Fase 2: SUMMARY
    User: "O que faz auth.py?"
    Agent: "auth.py: Autenticação JWT com refresh tokens"

    # Fase 3: DETAILED
    User: "Quais funções em auth.py?"
    Agent: "auth.py tem 5 funções: login(), logout(), refresh_token(), ..."

    # Fase 4: FULL
    User: "Mostre implementação de login()"
    Agent: [implementação completa]
    ```

    "Põe, SENHOR, uma guarda à minha boca; guarda a porta dos meus lábios."
    (Salmos 141:3)
    """

    def __init__(self, starting_level: DisclosureLevel = DisclosureLevel.OVERVIEW):
        """
        Inicializa Progressive Disclosure

        Args:
            starting_level: Nível inicial de disclosure
        """
        self.starting_level = starting_level

        # Stats
        self.stats = {
            'total_contexts_created': 0,
            'total_revelations': 0,
            'revelations_by_level': {level: 0 for level in DisclosureLevel},
        }

    def create_context(self, items: List[DisclosableItem]) -> DisclosureContext:
        """
        Cria contexto com progressive disclosure

        Args:
            items: Itens a revelar progressivamente

        Returns:
            DisclosureContext
        """
        self.stats['total_contexts_created'] += 1

        print(f"📖 Progressive Disclosure: Created context with {len(items)} items at {self.starting_level.value} level")

        return DisclosureContext(
            items=items,
            current_level=self.starting_level,
        )

    def reveal_items(
        self,
        context: DisclosureContext,
        item_ids: Optional[List[str]] = None,
        level: Optional[DisclosureLevel] = None
    ) -> Dict[str, str]:
        """
        Revela itens específicos

        Args:
            context: Contexto
            item_ids: IDs dos itens a revelar (None = todos)
            level: Nível de disclosure (None = próximo nível)

        Returns:
            Dict de {item_id: revealed_content}
        """
        self.stats['total_revelations'] += 1

        # Se level não especificado, usar próximo nível
        if level is None:
            levels = list(DisclosureLevel)
            current_idx = levels.index(context.current_level)
            level = levels[min(current_idx + 1, len(levels) - 1)]

        # Se item_ids não especificado, revelar todos
        if item_ids is None:
            items_to_reveal = context.items
        else:
            items_to_reveal = [
                item for item in context.items
                if item.id in item_ids
            ]

        # Revelar itens
        revealed = {}
        for item in items_to_reveal:
            content = item.reveal_at_level(level)
            revealed[item.id] = content

            # Track revelations
            if level == DisclosureLevel.FULL and item.id not in context.revealed_items:
                context.revealed_items.append(item.id)

        # Update stats
        self.stats['revelations_by_level'][level] += len(items_to_reveal)

        # Update context level
        context.current_level = level

        print(f"   ✓ Revealed {len(revealed)} items at {level.value} level")

        return revealed

    def reveal_by_query(
        self,
        context: DisclosureContext,
        query: str
    ) -> Dict[str, str]:
        """
        Revela itens relevantes para query

        Em produção, isso usaria:
        - Semantic search (embeddings)
        - Keyword matching
        - LLM para entender intent

        Args:
            context: Contexto
            query: Query do user

        Returns:
            Dict de {item_id: revealed_content}
        """
        # Placeholder: em produção, usar embeddings + semantic search
        # Por enquanto, simples keyword matching
        relevant_items = []

        query_lower = query.lower()

        for item in context.items:
            # Check if query matches name or summary
            if (
                query_lower in item.name.lower() or
                query_lower in item.summary.lower()
            ):
                relevant_items.append(item.id)

        if not relevant_items:
            print(f"   ⚠️  No items matched query: '{query}'")
            return {}

        print(f"   ✓ Found {len(relevant_items)} items matching query: '{query}'")

        # Revelar próximo nível dos itens relevantes
        return self.reveal_items(context, item_ids=relevant_items)

    def get_overview(self, context: DisclosureContext) -> str:
        """
        Retorna overview do contexto (lista de nomes)

        Útil para dar ao user uma visão geral antes de pedir detalhes.
        """
        overview_parts = []

        for item in context.items:
            overview_parts.append(f"- {item.overview}")

        overview = "\n".join(overview_parts)

        return f"Overview ({len(context.items)} items):\n{overview}"

    def get_fully_revealed(self, context: DisclosureContext) -> List[DisclosableItem]:
        """Retorna itens revelados em FULL"""
        return [
            item for item in context.items
            if item.id in context.revealed_items
        ]

    def get_stats(self) -> Dict:
        """Retorna estatísticas"""
        return {
            **self.stats,
        }

    def print_stats(self):
        """Imprime estatísticas"""
        stats = self.get_stats()

        print("\n" + "="*60)
        print("  PROGRESSIVE DISCLOSURE - STATISTICS")
        print("="*60)
        print(f"Total contexts created:    {stats['total_contexts_created']}")
        print(f"Total revelations:         {stats['total_revelations']}")
        print("Revelations by level:")
        for level, count in stats['revelations_by_level'].items():
            print(f"  {level.value:12s}  {count}")
        print("="*60 + "\n")


# ==================== HELPER FUNCTIONS ====================

def create_disclosable_from_file(file_path: str) -> DisclosableItem:
    """
    Cria DisclosableItem a partir de arquivo

    Em produção, isso analisaria o arquivo e extrairia:
    - Overview: Nome do arquivo
    - Summary: Docstring/comentário de topo
    - Detailed: Lista de funções/classes com assinaturas
    - Full: Conteúdo completo

    Args:
        file_path: Caminho do arquivo

    Returns:
        DisclosableItem
    """
    import os

    # Placeholder: em produção, analisar arquivo real
    file_name = os.path.basename(file_path)

    return DisclosableItem(
        id=file_path,
        name=file_name,
        type='file',
        overview=f"{file_name} (file)",
        summary=f"{file_name}: [Would extract docstring/top comment]",
        detailed=f"{file_name}: [Would list functions/classes with signatures]",
        full=f"{file_name}: [Would show full file content]",
    )
