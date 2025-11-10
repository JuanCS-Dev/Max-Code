"""
Context Manager with Smart Retrieval & Token Optimization

RESEARCH SYNTHESIS:
- Anthropic: 200k context window, auto-prune stale data
- OpenAI: 128k-1M tokens (tier-dependent)
- Target: 8K tokens per task (reserve 25k for output)
- Strategy: Semantic retrieval + relevance pruning

BEST PRACTICES APPLIED:
✅ Anthropic prompt caching for repeated context
✅ OpenAI embeddings for semantic search
✅ Token-aware context pruning
✅ Relevance scoring (cosine similarity)
"""
import logging
from typing import List, Dict, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime
import tiktoken

from .vector_store import VectorStore, VectorDocument

logger = logging.getLogger(__name__)


@dataclass
class ContextItem:
    """Single context item with metadata"""
    content: str
    type: str  # 'code', 'doc', 'conversation', 'tool_result'
    timestamp: datetime
    relevance: float = 1.0
    token_count: int = 0
    metadata: Dict = field(default_factory=dict)
    
    def __post_init__(self):
        if self.token_count == 0:
            self.token_count = count_tokens(self.content)


@dataclass
class ContextWindow:
    """Optimized context window for a task"""
    items: List[ContextItem]
    total_tokens: int
    max_tokens: int
    relevance_threshold: float
    
    @property
    def utilization(self) -> float:
        """Context window utilization percentage"""
        return (self.total_tokens / self.max_tokens) * 100
    
    def is_full(self) -> bool:
        """Check if context window is near capacity"""
        return self.utilization > 90  # 90% threshold


def count_tokens(text: str, model: str = "cl100k_base") -> int:
    """
    Count tokens using tiktoken
    
    NOTE: OpenAI and Anthropic use similar tokenization
    cl100k_base is close enough for estimation
    """
    try:
        encoding = tiktoken.get_encoding(model)
        return len(encoding.encode(text))
    except Exception as e:
        logger.warning(f"Token counting failed: {e}, using char estimation")
        # Fallback: rough estimation (1 token ~= 4 chars)
        return len(text) // 4


class ContextManager:
    """
    Smart context manager with semantic retrieval
    
    Features:
    - Vector-based semantic search
    - Token-aware context pruning
    - Relevance scoring
    - Support for Anthropic prompt caching
    
    Token optimization (from research):
    - Max 8K tokens per task context
    - Reserve 25K for model output (reasoning tasks)
    - Prune irrelevant items below threshold
    """
    
    def __init__(
        self,
        vector_store: Optional[VectorStore] = None,
        max_tokens_per_task: int = 8000,
        relevance_threshold: float = 0.5,
        enable_caching: bool = True
    ):
        """
        Initialize context manager
        
        Args:
            vector_store: Vector store for semantic search
            max_tokens_per_task: Max tokens per task context
            relevance_threshold: Min relevance score (0-1)
            enable_caching: Enable Anthropic prompt caching
        """
        self.vector_store = vector_store or VectorStore()
        self.max_tokens_per_task = max_tokens_per_task
        self.relevance_threshold = relevance_threshold
        self.enable_caching = enable_caching
        
        # Cache for current context
        self._current_context: Dict[str, ContextWindow] = {}
        
        logger.info(f"ContextManager initialized:")
        logger.info(f"  Max tokens/task: {max_tokens_per_task}")
        logger.info(f"  Relevance threshold: {relevance_threshold}")
        logger.info(f"  Prompt caching: {enable_caching}")
    
    def get_relevant_context(
        self,
        task_description: str,
        task_id: str,
        k: int = 5,
        context_types: Optional[List[str]] = None
    ) -> ContextWindow:
        """
        Retrieve relevant context for a task using semantic search
        
        Strategy (from research):
        1. Semantic search with vector store (OpenAI embeddings)
        2. Filter by relevance threshold
        3. Prune to fit token budget
        4. Return optimized context window
        
        Args:
            task_description: Task description for semantic search
            task_id: Task ID for caching
            k: Number of results to retrieve
            context_types: Filter by context types
            
        Returns:
            Optimized context window
        """
        logger.info(f"Retrieving context for task: {task_id}")
        logger.info(f"  Query: {task_description[:100]}...")
        
        # Build metadata filter
        filter_metadata = None
        if context_types:
            filter_metadata = {"type": {"$in": context_types}}
        
        # Semantic search
        results = self.vector_store.search(
            query=task_description,
            k=k,
            filter_metadata=filter_metadata
        )
        
        # Convert to ContextItems
        items = []
        for doc, similarity in results:
            if similarity < self.relevance_threshold:
                logger.debug(f"Skipping doc (relevance={similarity:.2f} < {self.relevance_threshold})")
                continue
            
            item = ContextItem(
                content=doc.content,
                type=doc.metadata.get('type', 'unknown'),
                timestamp=datetime.fromisoformat(doc.metadata.get('timestamp', datetime.now().isoformat())),
                relevance=similarity,
                metadata=doc.metadata
            )
            items.append(item)
        
        logger.info(f"  Found {len(items)} relevant items (filtered from {len(results)})")
        
        # Optimize token budget
        optimized_items = self.optimize_tokens(items)
        
        # Create context window
        total_tokens = sum(item.token_count for item in optimized_items)
        context = ContextWindow(
            items=optimized_items,
            total_tokens=total_tokens,
            max_tokens=self.max_tokens_per_task,
            relevance_threshold=self.relevance_threshold
        )
        
        # Cache context
        self._current_context[task_id] = context
        
        logger.info(f"  Context window: {total_tokens}/{self.max_tokens_per_task} tokens ({context.utilization:.1f}%)")
        
        return context
    
    def optimize_tokens(self, items: List[ContextItem]) -> List[ContextItem]:
        """
        Optimize context to fit token budget
        
        Strategy:
        1. Sort by relevance (descending)
        2. Add items until budget exhausted
        3. Truncate if needed
        
        Args:
            items: Context items
            
        Returns:
            Optimized items within token budget
        """
        if not items:
            return []
        
        # Sort by relevance
        sorted_items = sorted(items, key=lambda x: x.relevance, reverse=True)
        
        # Greedy selection
        selected = []
        total_tokens = 0
        
        for item in sorted_items:
            if total_tokens + item.token_count <= self.max_tokens_per_task:
                selected.append(item)
                total_tokens += item.token_count
            else:
                # Try to fit truncated version
                remaining_tokens = self.max_tokens_per_task - total_tokens
                if remaining_tokens > 100:  # Min viable chunk
                    truncated = self._truncate_item(item, remaining_tokens)
                    if truncated:
                        selected.append(truncated)
                        total_tokens += truncated.token_count
                break
        
        logger.debug(f"Token optimization: {len(items)} → {len(selected)} items ({total_tokens} tokens)")
        
        return selected
    
    def _truncate_item(self, item: ContextItem, max_tokens: int) -> Optional[ContextItem]:
        """Truncate item to fit token budget"""
        # Rough truncation (1 token ~= 4 chars)
        max_chars = max_tokens * 4
        if len(item.content) <= max_chars:
            return item
        
        truncated_content = item.content[:max_chars] + "... [truncated]"
        
        return ContextItem(
            content=truncated_content,
            type=item.type,
            timestamp=item.timestamp,
            relevance=item.relevance * 0.9,  # Penalize truncation
            token_count=count_tokens(truncated_content),
            metadata={**item.metadata, 'truncated': True}
        )
    
    def prune_irrelevant(self, task_id: str, threshold: Optional[float] = None) -> int:
        """
        Prune irrelevant items from current context
        
        Args:
            task_id: Task ID
            threshold: Relevance threshold (default: use manager threshold)
            
        Returns:
            Number of items pruned
        """
        if task_id not in self._current_context:
            return 0
        
        threshold = threshold or self.relevance_threshold
        context = self._current_context[task_id]
        
        before_count = len(context.items)
        context.items = [item for item in context.items if item.relevance >= threshold]
        after_count = len(context.items)
        
        pruned = before_count - after_count
        if pruned > 0:
            # Recalculate total tokens
            context.total_tokens = sum(item.token_count for item in context.items)
            logger.info(f"Pruned {pruned} items from task {task_id}")
        
        return pruned
    
    def add_context(
        self,
        content: str,
        context_type: str,
        metadata: Optional[Dict] = None,
        doc_id: Optional[str] = None
    ) -> str:
        """
        Add new context to vector store
        
        Args:
            content: Context content
            context_type: Type ('code', 'doc', 'conversation', 'tool_result')
            metadata: Additional metadata
            doc_id: Optional document ID
            
        Returns:
            Document ID
        """
        import uuid
        
        doc_id = doc_id or str(uuid.uuid4())
        
        metadata = metadata or {}
        metadata.update({
            'type': context_type,
            'timestamp': datetime.now().isoformat(),
            'token_count': count_tokens(content)
        })
        
        doc = VectorDocument(
            id=doc_id,
            content=content,
            metadata=metadata
        )
        
        self.vector_store.store([doc])
        logger.info(f"Added context: {context_type} ({metadata['token_count']} tokens)")
        
        return doc_id
    
    def get_cache_control(self, context: ContextWindow) -> Dict:
        """
        Generate Anthropic cache_control for context
        
        From research:
        - Mark large context blocks for caching
        - 25% more cost for writes, 90% savings on hits
        - Cache duration: 5min-1h
        
        Args:
            context: Context window
            
        Returns:
            cache_control dict for Anthropic API
        """
        if not self.enable_caching:
            return {}
        
        # Cache if context is large (>4K tokens)
        if context.total_tokens > 4000:
            return {"type": "ephemeral"}
        
        return {}
    
    def format_for_anthropic(self, context: ContextWindow) -> Dict:
        """
        Format context for Anthropic API with caching
        
        Returns system message with cache_control
        """
        # Concatenate context items
        context_text = "\n\n---\n\n".join([
            f"[{item.type.upper()}] (relevance: {item.relevance:.2f})\n{item.content}"
            for item in context.items
        ])
        
        cache_control = self.get_cache_control(context)
        
        system_message = {
            "type": "text",
            "text": context_text
        }
        
        if cache_control:
            system_message["cache_control"] = cache_control
        
        return system_message
    
    def clear_cache(self, task_id: Optional[str] = None) -> None:
        """Clear cached context"""
        if task_id:
            self._current_context.pop(task_id, None)
            logger.info(f"Cleared cache for task: {task_id}")
        else:
            self._current_context.clear()
            logger.info("Cleared all cached contexts")
    
    def __repr__(self) -> str:
        return (
            f"ContextManager(max_tokens={self.max_tokens_per_task}, "
            f"threshold={self.relevance_threshold}, "
            f"cached_contexts={len(self._current_context)})"
        )


# Convenience function
def get_context_manager(
    max_tokens_per_task: int = 8000,
    relevance_threshold: float = 0.5
) -> ContextManager:
    """Get context manager singleton"""
    return ContextManager(
        max_tokens_per_task=max_tokens_per_task,
        relevance_threshold=relevance_threshold
    )
