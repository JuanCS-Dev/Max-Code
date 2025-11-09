"""
Context Compression Implementation

OBJETIVO: Comprimir contexto para maximizar token efficiency (P6).

IDEIA CENTRAL:
- LLMs tem limite de contexto (200k tokens para Claude)
- Não podemos jogar TUDO no contexto
- Precisamos comprimir de forma inteligente
- Preservar informação crítica, remover redundância

ESTRATÉGIAS:
1. Summarization: Resumir conversas longas
2. Deduplication: Remover informação duplicada
3. Relevance Filtering: Manter só o relevante
4. Hierarchical Storage: Armazenar hierarquicamente (hot/warm/cold)

MANDATO CONSTITUCIONAL:
- P6: Context Retention Score (CRS) ≥95%
- P6: Token efficiency maximizada

"Ajunta o meu vagar no teu odre; não estão elas no teu livro?" (Salmos 56:8)
"""

from typing import List, Dict, Optional, Any, Tuple
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import hashlib
from config.logging_config import get_logger

logger = get_logger(__name__)


class CompressionStrategy(Enum):
    """Estratégia de compressão"""
    SUMMARIZATION = "summarization"      # Resumir
    DEDUPLICATION = "deduplication"      # Remover duplicatas
    RELEVANCE_FILTER = "relevance_filter"  # Filtrar por relevância
    HIERARCHICAL = "hierarchical"        # Armazenamento hierárquico


class StorageTier(Enum):
    """Tier de armazenamento"""
    HOT = "hot"      # Acesso imediato (contexto atual)
    WARM = "warm"    # Acesso rápido (sessão recente)
    COLD = "cold"    # Acesso lento (arquivo)


@dataclass
class ContextItem:
    """Item de contexto"""
    id: str
    content: str
    timestamp: datetime
    token_count: int
    relevance_score: float = 1.0  # 0.0-1.0
    tier: StorageTier = StorageTier.HOT
    metadata: Dict[str, Any] = field(default_factory=dict)

    def hash(self) -> str:
        """Hash do conteúdo (para dedup)"""
        normalized = self.content.strip().lower()
        return hashlib.md5(normalized.encode(), usedforsecurity=False).hexdigest()


@dataclass
class CompressionResult:
    """Resultado da compressão"""
    original_token_count: int
    compressed_token_count: int
    compression_ratio: float  # compressed / original
    items_removed: int
    items_summarized: int
    items_kept: int
    crs: float  # Context Retention Score (0.0-1.0)
    compressed_context: List[ContextItem]

    def to_dict(self) -> Dict:
        return {
            'original_token_count': self.original_token_count,
            'compressed_token_count': self.compressed_token_count,
            'compression_ratio': self.compression_ratio,
            'items_removed': self.items_removed,
            'items_summarized': self.items_summarized,
            'items_kept': self.items_kept,
            'crs': self.crs,
        }


class ContextCompressor:
    """
    Context Compression Engine

    PROCESSO:
    1. ANALYZE: Analisa contexto atual (token count, relevance)
    2. DEDUPLICATE: Remove duplicatas
    3. FILTER: Filtra por relevância
    4. SUMMARIZE: Resume itens menos relevantes
    5. TIER: Move para storage tier apropriado
    6. VALIDATE: Valida CRS ≥95%

    BENEFÍCIOS:
    - Maximiza token efficiency (P6)
    - Mantém informação crítica (CRS ≥95%)
    - Permite conversas longas sem perder contexto
    - Reduz custos (menos tokens = menos $$$)

    "Não ajunteis tesouros na terra... mas ajuntai tesouros no céu..."
    (Mateus 6:19-20)
    """

    # Limites constitucionais
    TARGET_CRS = 0.95  # 95% minimum
    MAX_HOT_TOKENS = 100_000  # 100k tokens no tier HOT
    MAX_WARM_TOKENS = 500_000  # 500k tokens no tier WARM

    def __init__(
        self,
        target_token_count: Optional[int] = None,
        min_relevance: float = 0.3
    ):
        """
        Inicializa Context Compressor

        Args:
            target_token_count: Token count alvo (default: MAX_HOT_TOKENS)
            min_relevance: Relevance mínima para manter item (0.0-1.0)
        """
        self.target_token_count = target_token_count or self.MAX_HOT_TOKENS
        self.min_relevance = min_relevance

        # Stats
        self.stats = {
            'total_compressions': 0,
            'total_tokens_saved': 0,
            'avg_compression_ratio': [],
            'avg_crs': [],
        }

    def compress(
        self,
        context: List[ContextItem],
        strategies: Optional[List[CompressionStrategy]] = None
    ) -> CompressionResult:
        """
        Comprime contexto

        Args:
            context: Contexto a comprimir
            strategies: Estratégias a usar (default: todas)

        Returns:
            CompressionResult
        """
        self.stats['total_compressions'] += 1

        # Default strategies
        if strategies is None:
            strategies = [
                CompressionStrategy.DEDUPLICATION,
                CompressionStrategy.RELEVANCE_FILTER,
                CompressionStrategy.SUMMARIZATION,
            ]

        # Calculate original token count
        original_token_count = sum(item.token_count for item in context)

        logger.info(f"🗜️  Context Compression: Compressing {len(context)} items ({original_token_count:,} tokens)...")
        # FASE 1: DEDUPLICATION
        if CompressionStrategy.DEDUPLICATION in strategies:
            context = self._deduplicate(context)

        # FASE 2: RELEVANCE FILTERING
        if CompressionStrategy.RELEVANCE_FILTER in strategies:
            context, removed = self._filter_by_relevance(context)
        else:
            removed = 0

        # FASE 3: SUMMARIZATION
        if CompressionStrategy.SUMMARIZATION in strategies:
            context, summarized = self._summarize_low_relevance(context)
        else:
            summarized = 0

        # FASE 4: TIERING (move para storage tiers apropriados)
        context = self._apply_tiering(context)

        # Calculate metrics
        compressed_token_count = sum(item.token_count for item in context)
        compression_ratio = compressed_token_count / original_token_count if original_token_count > 0 else 1.0
        tokens_saved = original_token_count - compressed_token_count

        # Calculate CRS (Context Retention Score)
        # CRS = (informação preservada) / (informação original)
        # Simplificação: assumir que cada item tem peso igual
        crs = len(context) / (len(context) + removed) if (len(context) + removed) > 0 else 1.0

        # Update stats
        self.stats['total_tokens_saved'] += tokens_saved
        self.stats['avg_compression_ratio'].append(compression_ratio)
        self.stats['avg_crs'].append(crs)

        # Log resultado
        logger.info(f"   ✓ Compressed: {original_token_count:,} → {compressed_token_count:,} tokens")
        logger.info(f"   Compression ratio: {compression_ratio:.1%}")
        logger.info(f"   CRS: {crs:.1%} (target: {self.TARGET_CRS:.1%})")
        # VALIDAÇÃO CONSTITUCIONAL: CRS ≥95%
        if crs < self.TARGET_CRS:
            logger.warning(f"   ⚠️  WARNING: CRS ({crs:.1%}) below constitutional minimum ({self.TARGET_CRS:.1%})")
        result = CompressionResult(
            original_token_count=original_token_count,
            compressed_token_count=compressed_token_count,
            compression_ratio=compression_ratio,
            items_removed=removed,
            items_summarized=summarized,
            items_kept=len(context),
            crs=crs,
            compressed_context=context,
        )

        return result

    def _deduplicate(self, context: List[ContextItem]) -> List[ContextItem]:
        """
        Remove duplicatas

        Usa hash para identificar conteúdo idêntico.
        """
        seen_hashes = set()
        deduplicated = []

        for item in context:
            item_hash = item.hash()
            if item_hash not in seen_hashes:
                deduplicated.append(item)
                seen_hashes.add(item_hash)

        removed = len(context) - len(deduplicated)
        if removed > 0:
            logger.info(f"   ✓ Deduplication: Removed {removed} duplicates")
        return deduplicated

    def _filter_by_relevance(
        self,
        context: List[ContextItem]
    ) -> Tuple[List[ContextItem], int]:
        """
        Filtra por relevância

        Remove itens com relevance < min_relevance.
        """
        filtered = [
            item for item in context
            if item.relevance_score >= self.min_relevance
        ]

        removed = len(context) - len(filtered)
        if removed > 0:
            logger.info(f"   ✓ Relevance Filter: Removed {removed} low-relevance items")
        return filtered, removed

    def _summarize_low_relevance(
        self,
        context: List[ContextItem]
    ) -> Tuple[List[ContextItem], int]:
        """
        Resume itens de baixa relevância

        Itens com relevance entre min_relevance e 0.7 são resumidos.

        Em produção, isso usaria LLM:
        ```
        Summarize this text to 20% of its original length while preserving key information:

        {item.content}

        Summary:
        ```
        """
        summarized_count = 0

        for item in context:
            # Resumir se relevance entre min_relevance e 0.7
            if self.min_relevance <= item.relevance_score < 0.7:
                # Placeholder: em produção, chamar LLM para resumir
                original_length = len(item.content)
                item.content = f"[SUMMARY: {item.content[:100]}...]"
                item.token_count = int(item.token_count * 0.2)  # Assumir 20% do tamanho
                summarized_count += 1

        if summarized_count > 0:
            logger.info(f"   ✓ Summarization: Summarized {summarized_count} items")
        return context, summarized_count

    def _apply_tiering(self, context: List[ContextItem]) -> List[ContextItem]:
        """
        Aplica storage tiering

        Move itens para tiers apropriados baseado em relevância e timestamp.

        HOT:  Relevance ≥0.8, acessado recentemente
        WARM: Relevance 0.5-0.8, ou acessado há alguns dias
        COLD: Relevance <0.5, ou não acessado há muito tempo
        """
        for item in context:
            if item.relevance_score >= 0.8:
                item.tier = StorageTier.HOT
            elif item.relevance_score >= 0.5:
                item.tier = StorageTier.WARM
            else:
                item.tier = StorageTier.COLD

        # Log tier distribution
        hot_count = sum(1 for item in context if item.tier == StorageTier.HOT)
        warm_count = sum(1 for item in context if item.tier == StorageTier.WARM)
        cold_count = sum(1 for item in context if item.tier == StorageTier.COLD)

        logger.info(f"   ✓ Tiering: HOT={hot_count}, WARM={warm_count}, COLD={cold_count}")
        return context

    def get_hot_context(self, context: List[ContextItem]) -> List[ContextItem]:
        """Retorna apenas contexto HOT (para uso imediato)"""
        return [item for item in context if item.tier == StorageTier.HOT]

    def calculate_relevance(
        self,
        item: ContextItem,
        query: Optional[str] = None
    ) -> float:
        """
        Calcula relevância de um item

        Em produção, isso usaria:
        - Semantic similarity (embeddings)
        - Recency (itens recentes = mais relevantes)
        - Access frequency (itens acessados frequentemente = mais relevantes)

        Args:
            item: Item a avaliar
            query: Query atual (opcional)

        Returns:
            Relevance score (0.0-1.0)
        """
        # Placeholder: em produção, usar embeddings + heurísticas
        import random
        return random.uniform(0.3, 1.0)

    def get_stats(self) -> Dict:
        """Retorna estatísticas"""
        avg_compression_ratio = (
            sum(self.stats['avg_compression_ratio']) / len(self.stats['avg_compression_ratio'])
            if self.stats['avg_compression_ratio'] else 0.0
        )

        avg_crs = (
            sum(self.stats['avg_crs']) / len(self.stats['avg_crs'])
            if self.stats['avg_crs'] else 0.0
        )

        return {
            **self.stats,
            'avg_compression_ratio': round(avg_compression_ratio, 3),
            'avg_crs': round(avg_crs, 3),
        }

    def print_stats(self):
        """Imprime estatísticas"""
        stats = self.get_stats()

        print("\n" + "="*60)
        logger.info("  CONTEXT COMPRESSION - STATISTICS")
        print("="*60)
        logger.info(f"Total compressions:        {stats['total_compressions']}")
        logger.info(f"Total tokens saved:        {stats['total_tokens_saved']:,}")
        logger.info(f"Avg compression ratio:     {stats['avg_compression_ratio']:.1%}")
        logger.info(f"Avg CRS:                   {stats['avg_crs']:.1%}")
        print("="*60 + "\n")


# ==================== HELPER FUNCTIONS ====================

def compress_context(
    context: List[ContextItem],
    target_token_count: Optional[int] = None
) -> CompressionResult:
    """
    Helper function para comprimir contexto

    Args:
        context: Contexto a comprimir
        target_token_count: Token count alvo

    Returns:
        CompressionResult
    """
    compressor = ContextCompressor(target_token_count=target_token_count)
    return compressor.compress(context)
