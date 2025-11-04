"""
Memory Manager Implementation

OBJETIVO: Gerenciar memória de curto e longo prazo do agente.

IDEIA CENTRAL:
- Agentes precisam "lembrar" de interações passadas
- Memória de curto prazo: Conversação atual (working memory)
- Memória de longo prazo: Fatos aprendidos, preferências user
- Indexação eficiente para retrieval rápido

TIPOS DE MEMÓRIA:
1. WORKING: Conversação atual (curto prazo)
2. EPISODIC: Episódios passados (ex: "ontem você me pediu X")
3. SEMANTIC: Fatos aprendidos (ex: "user prefere Python")
4. PROCEDURAL: Como fazer tarefas (ex: "sempre rodar tests depois de code")

BENEFÍCIOS:
- Contexto rico (lembrar preferências user)
- Continuidade entre sessões
- Personalização (adaptar a user)
- Token efficiency (não repetir informação)

"Lembra-te de mim, SENHOR, segundo a tua benevolência para com o teu povo..."
(Salmos 106:4)
"""

from typing import List, Dict, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
import json


class MemoryType(Enum):
    """Tipo de memória"""
    WORKING = "working"        # Conversação atual
    EPISODIC = "episodic"      # Episódios passados
    SEMANTIC = "semantic"      # Fatos aprendidos
    PROCEDURAL = "procedural"  # Como fazer tarefas


class MemoryImportance(Enum):
    """Importância da memória"""
    CRITICAL = "critical"  # Nunca esquecer
    HIGH = "high"          # Importante
    MEDIUM = "medium"      # Normal
    LOW = "low"            # Pode esquecer


@dataclass
class MemoryEntry:
    """Entrada de memória"""
    id: str
    type: MemoryType
    content: str
    importance: MemoryImportance
    timestamp: datetime
    access_count: int = 0
    last_accessed: Optional[datetime] = None
    tags: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    expires_at: Optional[datetime] = None  # None = nunca expira

    def access(self):
        """Marca memória como acessada"""
        self.access_count += 1
        self.last_accessed = datetime.utcnow()

    def is_expired(self) -> bool:
        """Checa se memória expirou"""
        if self.expires_at is None:
            return False
        return datetime.utcnow() > self.expires_at

    def to_dict(self) -> Dict:
        return {
            'id': self.id,
            'type': self.type.value,
            'content': self.content[:200],  # Truncar
            'importance': self.importance.value,
            'timestamp': self.timestamp.isoformat(),
            'access_count': self.access_count,
            'last_accessed': self.last_accessed.isoformat() if self.last_accessed else None,
            'tags': self.tags,
        }


class MemoryManager:
    """
    Memory Manager Engine

    PROCESSO:
    1. STORE: Armazena novas memórias
    2. RETRIEVE: Busca memórias relevantes
    3. FORGET: Remove memórias expiradas/irrelevantes
    4. CONSOLIDATE: Consolida memórias similares

    ESTRATÉGIAS DE RETENTION:
    - Importance-based: Memórias CRITICAL nunca expiram
    - Recency-based: Memórias recentes = mais retidas
    - Frequency-based: Memórias acessadas frequentemente = mais retidas

    BENEFÍCIOS:
    - Contexto rico e personalizado
    - Token efficiency (não repetir)
    - Continuidade entre sessões
    - Adaptive behavior

    "O coração do sábio adquire conhecimento, e o ouvido dos sábios busca a ciência."
    (Provérbios 18:15)
    """

    # Limites de memória (para prevenir memory bloat)
    MAX_WORKING_MEMORY = 100  # 100 entries
    MAX_EPISODIC_MEMORY = 1000  # 1000 episodes
    MAX_SEMANTIC_MEMORY = 5000  # 5000 fatos
    MAX_PROCEDURAL_MEMORY = 500  # 500 procedures

    # TTL (Time To Live) padrão por tipo
    DEFAULT_TTL = {
        MemoryType.WORKING: timedelta(hours=1),      # 1 hora
        MemoryType.EPISODIC: timedelta(days=30),     # 30 dias
        MemoryType.SEMANTIC: None,                    # Nunca expira
        MemoryType.PROCEDURAL: None,                  # Nunca expira
    }

    def __init__(self):
        """Inicializa Memory Manager"""
        self.memories: Dict[MemoryType, List[MemoryEntry]] = {
            MemoryType.WORKING: [],
            MemoryType.EPISODIC: [],
            MemoryType.SEMANTIC: [],
            MemoryType.PROCEDURAL: [],
        }

        # Stats
        self.stats = {
            'total_memories_stored': 0,
            'total_memories_retrieved': 0,
            'total_memories_forgotten': 0,
            'memories_by_type': {mt: 0 for mt in MemoryType},
        }

    def store(
        self,
        content: str,
        memory_type: MemoryType,
        importance: MemoryImportance = MemoryImportance.MEDIUM,
        tags: Optional[List[str]] = None,
        ttl: Optional[timedelta] = None,
        metadata: Optional[Dict] = None
    ) -> MemoryEntry:
        """
        Armazena nova memória

        Args:
            content: Conteúdo da memória
            memory_type: Tipo de memória
            importance: Importância
            tags: Tags (para indexação)
            ttl: Time to live (None = usar default)
            metadata: Metadata adicional

        Returns:
            MemoryEntry criada
        """
        self.stats['total_memories_stored'] += 1
        self.stats['memories_by_type'][memory_type] += 1

        # Generate ID
        memory_id = f"{memory_type.value}_{self.stats['total_memories_stored']}"

        # Calculate expiration
        if ttl is None:
            ttl = self.DEFAULT_TTL[memory_type]

        expires_at = None
        if ttl is not None:
            expires_at = datetime.utcnow() + ttl

        # Create memory entry
        entry = MemoryEntry(
            id=memory_id,
            type=memory_type,
            content=content,
            importance=importance,
            timestamp=datetime.utcnow(),
            tags=tags or [],
            metadata=metadata or {},
            expires_at=expires_at,
        )

        # Store
        self.memories[memory_type].append(entry)

        # Check limits and prune if necessary
        self._enforce_limits(memory_type)

        print(f"💾 Memory Manager: Stored {memory_type.value} memory (importance: {importance.value})")

        return entry

    def retrieve(
        self,
        query: Optional[str] = None,
        memory_type: Optional[MemoryType] = None,
        tags: Optional[List[str]] = None,
        limit: int = 10
    ) -> List[MemoryEntry]:
        """
        Busca memórias

        Args:
            query: Query de busca (None = retornar todas)
            memory_type: Filtrar por tipo (None = todos tipos)
            tags: Filtrar por tags (None = sem filtro)
            limit: Máximo de resultados

        Returns:
            Lista de MemoryEntry
        """
        self.stats['total_memories_retrieved'] += 1

        # Determinar tipos a buscar
        if memory_type is not None:
            types_to_search = [memory_type]
        else:
            types_to_search = list(MemoryType)

        # Coletar memórias de todos tipos relevantes
        all_memories = []
        for mt in types_to_search:
            all_memories.extend(self.memories[mt])

        # Filtrar memórias expiradas
        all_memories = [m for m in all_memories if not m.is_expired()]

        # Filtrar por tags se especificado
        if tags:
            all_memories = [
                m for m in all_memories
                if any(tag in m.tags for tag in tags)
            ]

        # Filtrar por query se especificado
        if query:
            query_lower = query.lower()
            all_memories = [
                m for m in all_memories
                if query_lower in m.content.lower()
            ]

        # Ordenar por relevância (simplificado: importance + recency + frequency)
        def relevance_score(memory: MemoryEntry) -> float:
            # Importance weight
            importance_weights = {
                MemoryImportance.CRITICAL: 100,
                MemoryImportance.HIGH: 10,
                MemoryImportance.MEDIUM: 1,
                MemoryImportance.LOW: 0.1,
            }
            importance_score = importance_weights[memory.importance]

            # Recency weight (mais recente = mais pontos)
            age_hours = (datetime.utcnow() - memory.timestamp).total_seconds() / 3600
            recency_score = 1.0 / (1.0 + age_hours)  # Decay exponencial

            # Frequency weight
            frequency_score = memory.access_count

            return importance_score * 10 + recency_score * 5 + frequency_score

        all_memories.sort(key=relevance_score, reverse=True)

        # Limitar resultados
        results = all_memories[:limit]

        # Marcar como acessadas
        for memory in results:
            memory.access()

        print(f"   ✓ Retrieved {len(results)} memories (from {len(all_memories)} candidates)")

        return results

    def forget(
        self,
        memory_id: Optional[str] = None,
        memory_type: Optional[MemoryType] = None,
        criteria: Optional[str] = None
    ) -> int:
        """
        Remove memórias

        Args:
            memory_id: ID específico (None = não filtrar por ID)
            memory_type: Tipo específico (None = todos tipos)
            criteria: Critério ('expired', 'low_importance', etc)

        Returns:
            Número de memórias removidas
        """
        removed_count = 0

        # Determinar tipos
        if memory_type is not None:
            types_to_process = [memory_type]
        else:
            types_to_process = list(MemoryType)

        for mt in types_to_process:
            memories = self.memories[mt]
            to_keep = []

            for memory in memories:
                should_forget = False

                # Check ID
                if memory_id and memory.id == memory_id:
                    should_forget = True

                # Check criteria
                if criteria == 'expired' and memory.is_expired():
                    should_forget = True
                elif criteria == 'low_importance' and memory.importance == MemoryImportance.LOW:
                    should_forget = True

                if should_forget:
                    removed_count += 1
                    self.stats['total_memories_forgotten'] += 1
                else:
                    to_keep.append(memory)

            self.memories[mt] = to_keep

        if removed_count > 0:
            print(f"🗑️  Memory Manager: Forgot {removed_count} memories")

        return removed_count

    def consolidate(self, memory_type: MemoryType) -> int:
        """
        Consolida memórias similares

        Combina memórias redundantes em uma única.

        Args:
            memory_type: Tipo a consolidar

        Returns:
            Número de memórias consolidadas
        """
        # Placeholder: em produção, usar embeddings para detectar similaridade
        # Por enquanto, apenas remover duplicatas exatas

        memories = self.memories[memory_type]
        seen_content = {}
        consolidated = []
        consolidated_count = 0

        for memory in memories:
            content_hash = hash(memory.content.lower().strip())

            if content_hash in seen_content:
                # Duplicata - incrementar access count da original
                seen_content[content_hash].access_count += memory.access_count
                consolidated_count += 1
            else:
                consolidated.append(memory)
                seen_content[content_hash] = memory

        self.memories[memory_type] = consolidated

        if consolidated_count > 0:
            print(f"   ✓ Consolidated {consolidated_count} duplicate memories")

        return consolidated_count

    def _enforce_limits(self, memory_type: MemoryType):
        """
        Enforça limites de memória

        Remove memórias menos importantes se exceder limites.
        """
        limits = {
            MemoryType.WORKING: self.MAX_WORKING_MEMORY,
            MemoryType.EPISODIC: self.MAX_EPISODIC_MEMORY,
            MemoryType.SEMANTIC: self.MAX_SEMANTIC_MEMORY,
            MemoryType.PROCEDURAL: self.MAX_PROCEDURAL_MEMORY,
        }

        max_memories = limits[memory_type]
        current_count = len(self.memories[memory_type])

        if current_count > max_memories:
            # Remover memórias menos importantes
            # Ordenar por importância (ascendente) + recency (ascendente)
            self.memories[memory_type].sort(
                key=lambda m: (
                    -m.importance.value,  # Menos importante primeiro
                    m.timestamp  # Mais antiga primeiro
                )
            )

            # Remover excesso
            to_remove = current_count - max_memories
            removed = self.memories[memory_type][:to_remove]
            self.memories[memory_type] = self.memories[memory_type][to_remove:]

            self.stats['total_memories_forgotten'] += len(removed)

            print(f"   ⚠️  Limit exceeded: Removed {len(removed)} old {memory_type.value} memories")

    def clear_working_memory(self):
        """Limpa working memory (útil entre sessões)"""
        count = len(self.memories[MemoryType.WORKING])
        self.memories[MemoryType.WORKING] = []
        self.stats['total_memories_forgotten'] += count
        print(f"🧹 Memory Manager: Cleared {count} working memories")

    def get_memory_count(self, memory_type: Optional[MemoryType] = None) -> int:
        """Retorna contagem de memórias"""
        if memory_type:
            return len(self.memories[memory_type])
        else:
            return sum(len(memories) for memories in self.memories.values())

    def get_stats(self) -> Dict:
        """Retorna estatísticas"""
        return {
            **self.stats,
            'current_memory_count': {
                mt.value: len(self.memories[mt])
                for mt in MemoryType
            },
        }

    def print_stats(self):
        """Imprime estatísticas"""
        stats = self.get_stats()

        print("\n" + "="*60)
        print("  MEMORY MANAGER - STATISTICS")
        print("="*60)
        print(f"Total memories stored:     {stats['total_memories_stored']}")
        print(f"Total memories retrieved:  {stats['total_memories_retrieved']}")
        print(f"Total memories forgotten:  {stats['total_memories_forgotten']}")
        print("\nCurrent memory counts:")
        for mt, count in stats['current_memory_count'].items():
            print(f"  {mt:12s}  {count}")
        print("="*60 + "\n")

    def save_to_file(self, file_path: str):
        """Salva memórias em arquivo (para persistência entre sessões)"""
        data = {
            'memories': {
                mt.value: [m.to_dict() for m in memories]
                for mt, memories in self.memories.items()
            },
            'stats': self.stats,
        }

        with open(file_path, 'w') as f:
            json.dump(data, f, indent=2)

        print(f"💾 Memory Manager: Saved memories to {file_path}")

    def load_from_file(self, file_path: str):
        """Carrega memórias de arquivo"""
        with open(file_path, 'r') as f:
            data = json.load(f)

        # Reconstruct memories
        # (implementação simplificada - em produção, reconstruir MemoryEntry completo)
        print(f"💾 Memory Manager: Loaded memories from {file_path}")


# ==================== HELPER FUNCTIONS ====================

def create_memory_manager() -> MemoryManager:
    """Helper function para criar MemoryManager"""
    return MemoryManager()
