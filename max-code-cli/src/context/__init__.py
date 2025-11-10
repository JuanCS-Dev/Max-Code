"""
Context Management Package

Advanced context management with:
- Vector store (ChromaDB + OpenAI embeddings)
- Semantic search (task/code similarity)
- Smart retrieval with token optimization
- Anthropic prompt caching support

RESEARCH-BASED IMPLEMENTATION:
- OpenAI embeddings: Cost-effective, proven quality
- Anthropic caching: 90% cost reduction for repeated context
- Token optimization: Max 8K per task, reserve 25K for output
- Search latency: <500ms target

Usage:
    from src.context import VectorStore, ContextManager, SemanticSearcher
    
    # Initialize
    vector_store = VectorStore()
    context_manager = ContextManager(vector_store)
    
    # Add context
    context_manager.add_context("code snippet", "code")
    
    # Retrieve relevant context
    context = context_manager.get_relevant_context("task description", "task_id")
    
    # Semantic search
    searcher = SemanticSearcher(vector_store)
    similar_tasks = searcher.find_similar_tasks(task)
"""
from .vector_store import VectorStore, VectorDocument, get_vector_store
from .context_manager import (
    ContextManager,
    ContextItem,
    ContextWindow,
    count_tokens,
    get_context_manager
)
from .semantic_search import (
    SemanticSearcher,
    SimilarityResult,
    find_similar_tasks,
    find_related_code
)

__all__ = [
    # Vector Store
    "VectorStore",
    "VectorDocument",
    "get_vector_store",
    
    # Context Manager
    "ContextManager",
    "ContextItem",
    "ContextWindow",
    "count_tokens",
    "get_context_manager",
    
    # Semantic Search
    "SemanticSearcher",
    "SimilarityResult",
    "find_similar_tasks",
    "find_related_code",
]
