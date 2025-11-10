"""
Comprehensive tests for context management system

TEST COVERAGE TARGET: 100%
PERFORMANCE TARGET: <500ms retrieval
"""
import pytest
import os
import tempfile
import time
from pathlib import Path
from datetime import datetime

from src.context import (
    VectorStore,
    VectorDocument,
    ContextManager,
    ContextItem,
    ContextWindow,
    SemanticSearcher,
    SimilarityResult,
    count_tokens
)
from core.task_models import Task, TaskType


# ============================================================================
# FIXTURES
# ============================================================================

@pytest.fixture
def temp_db_path():
    """Temporary database path"""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield tmpdir


@pytest.fixture
def vector_store(temp_db_path):
    """Fresh vector store for each test"""
    # Set OpenAI API key for tests
    if not os.getenv("OPENAI_API_KEY"):
        os.environ["OPENAI_API_KEY"] = os.getenv("ANTHROPIC_API_KEY", "test-key")
    
    store = VectorStore(
        collection_name="test_collection",
        persist_directory=temp_db_path
    )
    yield store
    store.clear()


@pytest.fixture
def context_manager(vector_store):
    """Context manager with test vector store"""
    return ContextManager(vector_store=vector_store)


@pytest.fixture
def semantic_searcher(vector_store):
    """Semantic searcher with test vector store"""
    return SemanticSearcher(vector_store=vector_store)


@pytest.fixture
def sample_documents():
    """Sample documents for testing"""
    return [
        VectorDocument(
            id="doc1",
            content="Python function to calculate fibonacci numbers recursively",
            metadata={"type": "code", "language": "python"}
        ),
        VectorDocument(
            id="doc2",
            content="JavaScript implementation of binary search algorithm",
            metadata={"type": "code", "language": "javascript"}
        ),
        VectorDocument(
            id="doc3",
            content="Documentation for REST API endpoints and authentication",
            metadata={"type": "doc"}
        ),
        VectorDocument(
            id="doc4",
            content="Python code for sorting arrays using quicksort",
            metadata={"type": "code", "language": "python"}
        ),
        VectorDocument(
            id="doc5",
            content="User guide for command line interface options",
            metadata={"type": "doc"}
        ),
    ]


@pytest.fixture
def sample_tasks():
    """Sample tasks for testing"""
    return [
        Task(
            id="task1",
            description="Implement fibonacci function in Python",
            type=TaskType.THINK
        ),
        Task(
            id="task2",
            description="Write tests for authentication module",
            type=TaskType.THINK
        ),
        Task(
            id="task3",
            description="Create API documentation for user endpoints",
            type=TaskType.THINK
        ),
    ]


# ============================================================================
# VECTOR STORE TESTS
# ============================================================================

class TestVectorStore:
    """Test vector store operations"""
    
    def test_initialization(self, vector_store, temp_db_path):
        """Test vector store initialization"""
        assert vector_store.collection_name == "test_collection"
        assert vector_store.persist_directory == Path(temp_db_path)
        assert vector_store.count() == 0
    
    @pytest.mark.skipif(not os.getenv("OPENAI_API_KEY"), reason="Requires OpenAI API key")
    def test_embed_generation(self, vector_store):
        """Test embedding generation"""
        text = "Hello, world!"
        embedding = vector_store.embed(text)
        
        assert isinstance(embedding, list)
        assert len(embedding) > 0  # Should have dimensions
        assert all(isinstance(x, float) for x in embedding)
    
    @pytest.mark.skipif(not os.getenv("OPENAI_API_KEY"), reason="Requires OpenAI API key")
    def test_store_documents(self, vector_store, sample_documents):
        """Test storing documents"""
        vector_store.store(sample_documents)
        
        assert vector_store.count() == len(sample_documents)
    
    @pytest.mark.skipif(not os.getenv("OPENAI_API_KEY"), reason="Requires OpenAI API key")
    def test_search_basic(self, vector_store, sample_documents):
        """Test basic semantic search"""
        vector_store.store(sample_documents)
        
        # Search for Python code
        results = vector_store.search("python sorting algorithm", k=2)
        
        assert len(results) <= 2
        assert all(isinstance(r, tuple) for r in results)
        assert all(isinstance(r[0], VectorDocument) for r in results)
        assert all(isinstance(r[1], float) for r in results)
        
        # Check relevance
        best_match = results[0]
        assert best_match[1] > 0.5  # Should have decent similarity
    
    @pytest.mark.skipif(not os.getenv("OPENAI_API_KEY"), reason="Requires OpenAI API key")
    def test_search_with_filter(self, vector_store, sample_documents):
        """Test search with metadata filter"""
        vector_store.store(sample_documents)
        
        # Search only Python code
        results = vector_store.search(
            "sorting algorithm",
            k=5,
            filter_metadata={"language": "python"}
        )
        
        # Should only return Python documents
        for doc, similarity in results:
            assert doc.metadata.get("language") == "python"
    
    @pytest.mark.skipif(not os.getenv("OPENAI_API_KEY"), reason="Requires OpenAI API key")
    def test_search_performance(self, vector_store, sample_documents):
        """Test search latency < 500ms"""
        vector_store.store(sample_documents)
        
        start = time.time()
        results = vector_store.search("code example", k=3)
        elapsed = time.time() - start
        
        assert elapsed < 0.5, f"Search took {elapsed*1000:.1f}ms (target: <500ms)"
    
    def test_get_by_id(self, vector_store, sample_documents):
        """Test retrieving document by ID"""
        # Skip if no API key (needs embeddings)
        if not os.getenv("OPENAI_API_KEY"):
            pytest.skip("Requires OpenAI API key")
        
        vector_store.store(sample_documents)
        
        doc = vector_store.get_by_id("doc1")
        assert doc is not None
        assert doc.id == "doc1"
        assert "fibonacci" in doc.content.lower()
    
    def test_delete_documents(self, vector_store, sample_documents):
        """Test deleting documents"""
        # Skip if no API key (needs embeddings)
        if not os.getenv("OPENAI_API_KEY"):
            pytest.skip("Requires OpenAI API key")
        
        vector_store.store(sample_documents)
        initial_count = vector_store.count()
        
        vector_store.delete(["doc1", "doc2"])
        
        assert vector_store.count() == initial_count - 2
        assert vector_store.get_by_id("doc1") is None
    
    def test_clear_collection(self, vector_store, sample_documents):
        """Test clearing all documents"""
        # Skip if no API key (needs embeddings)
        if not os.getenv("OPENAI_API_KEY"):
            pytest.skip("Requires OpenAI API key")
        
        vector_store.store(sample_documents)
        assert vector_store.count() > 0
        
        vector_store.clear()
        assert vector_store.count() == 0


# ============================================================================
# CONTEXT MANAGER TESTS
# ============================================================================

class TestContextManager:
    """Test context manager with smart retrieval"""
    
    def test_initialization(self, context_manager):
        """Test context manager initialization"""
        assert context_manager.max_tokens_per_task == 8000
        assert context_manager.relevance_threshold == 0.5
    
    @pytest.mark.skipif(not os.getenv("OPENAI_API_KEY"), reason="Requires OpenAI API key")
    def test_add_context(self, context_manager):
        """Test adding context to vector store"""
        doc_id = context_manager.add_context(
            content="Example Python function",
            context_type="code",
            metadata={"language": "python"}
        )
        
        assert doc_id is not None
        assert context_manager.vector_store.count() == 1
    
    @pytest.mark.skipif(not os.getenv("OPENAI_API_KEY"), reason="Requires OpenAI API key")
    def test_get_relevant_context(self, context_manager, sample_documents):
        """Test retrieving relevant context"""
        # Store documents
        context_manager.vector_store.store(sample_documents)
        
        # Get context for Python sorting task
        context = context_manager.get_relevant_context(
            task_description="implement sorting algorithm",
            task_id="task1",
            k=3
        )
        
        assert isinstance(context, ContextWindow)
        assert len(context.items) <= 3
        assert context.total_tokens <= context.max_tokens
    
    def test_optimize_tokens(self, context_manager):
        """Test token optimization"""
        # Create items that exceed budget
        items = [
            ContextItem(
                content="x" * 500,  # ~125 tokens
                type="code",
                timestamp=datetime.now(),
                relevance=0.9
            ),
            ContextItem(
                content="y" * 500,  # ~125 tokens
                type="code",
                timestamp=datetime.now(),
                relevance=0.8
            ),
            ContextItem(
                content="z" * 50000,  # Large (exceeds budget)
                type="code",
                timestamp=datetime.now(),
                relevance=0.7
            ),
        ]
        
        optimized = context_manager.optimize_tokens(items)
        
        # Should select highest relevance within budget
        total_tokens = sum(item.token_count for item in optimized)
        assert total_tokens <= context_manager.max_tokens_per_task, f"Total tokens ({total_tokens}) exceeds budget ({context_manager.max_tokens_per_task})"
        
        # Should prefer high relevance
        if len(optimized) > 0:
            assert optimized[0].relevance >= optimized[-1].relevance
    
    def test_prune_irrelevant(self, context_manager):
        """Test pruning irrelevant context"""
        # Create context with low relevance items
        items = [
            ContextItem(content="relevant", type="code", timestamp=datetime.now(), relevance=0.9),
            ContextItem(content="somewhat", type="code", timestamp=datetime.now(), relevance=0.6),
            ContextItem(content="irrelevant", type="code", timestamp=datetime.now(), relevance=0.3),
        ]
        
        context = ContextWindow(
            items=items,
            total_tokens=sum(item.token_count for item in items),
            max_tokens=8000,
            relevance_threshold=0.5
        )
        
        context_manager._current_context["test_task"] = context
        
        pruned = context_manager.prune_irrelevant("test_task", threshold=0.5)
        
        assert pruned == 1  # Should prune 1 item (relevance 0.3)
        assert len(context.items) == 2
    
    def test_cache_control(self, context_manager):
        """Test Anthropic cache_control generation"""
        # Small context (no caching)
        small_context = ContextWindow(
            items=[],
            total_tokens=1000,
            max_tokens=8000,
            relevance_threshold=0.5
        )
        cache_control = context_manager.get_cache_control(small_context)
        assert cache_control == {}
        
        # Large context (should cache)
        large_context = ContextWindow(
            items=[],
            total_tokens=5000,
            max_tokens=8000,
            relevance_threshold=0.5
        )
        cache_control = context_manager.get_cache_control(large_context)
        assert cache_control == {"type": "ephemeral"}
    
    def test_format_for_anthropic(self, context_manager):
        """Test formatting context for Anthropic API"""
        items = [
            ContextItem(content="code1", type="code", timestamp=datetime.now(), relevance=0.9),
            ContextItem(content="doc1", type="doc", timestamp=datetime.now(), relevance=0.8),
        ]
        
        context = ContextWindow(
            items=items,
            total_tokens=100,
            max_tokens=8000,
            relevance_threshold=0.5
        )
        
        formatted = context_manager.format_for_anthropic(context)
        
        assert "type" in formatted
        assert "text" in formatted
        assert "code1" in formatted["text"]
        assert "doc1" in formatted["text"]


# ============================================================================
# SEMANTIC SEARCH TESTS
# ============================================================================

class TestSemanticSearcher:
    """Test semantic search functionality"""
    
    def test_initialization(self, semantic_searcher):
        """Test semantic searcher initialization"""
        assert semantic_searcher.similarity_threshold == 0.7
    
    @pytest.mark.skipif(not os.getenv("OPENAI_API_KEY"), reason="Requires OpenAI API key")
    def test_find_similar_tasks(self, semantic_searcher, sample_tasks):
        """Test finding similar tasks"""
        # Store tasks as documents
        for task in sample_tasks:
            doc = VectorDocument(
                id=task.id,
                content=task.description,
                metadata={
                    "type": "task",
                    "task_data": {
                        "type": task.type.value
                    }
                }
            )
            semantic_searcher.vector_store.store([doc])
        
        # Find similar to fibonacci task
        similar = semantic_searcher.find_similar_tasks(sample_tasks[0], k=2)
        
        assert len(similar) <= 2
        assert all(isinstance(r, SimilarityResult) for r in similar)
        assert all(isinstance(r.item, Task) for r in similar)
    
    @pytest.mark.skipif(not os.getenv("OPENAI_API_KEY"), reason="Requires OpenAI API key")
    def test_find_related_code(self, semantic_searcher, sample_documents):
        """Test finding related code"""
        semantic_searcher.vector_store.store(sample_documents)
        
        related = semantic_searcher.find_related_code(
            query="array sorting",
            k=3,
            language="python"
        )
        
        assert len(related) <= 3
        assert all(isinstance(r, SimilarityResult) for r in related)
        assert all(r.metadata.get("language") == "python" for r in related)
    
    @pytest.mark.skipif(not os.getenv("OPENAI_API_KEY"), reason="Requires OpenAI API key")
    def test_cluster_tasks(self, semantic_searcher, sample_tasks):
        """Test clustering similar tasks"""
        # Store tasks
        for task in sample_tasks:
            doc = VectorDocument(
                id=task.id,
                content=task.description,
                metadata={"type": "task"}
            )
            semantic_searcher.vector_store.store([doc])
        
        clusters = semantic_searcher.cluster_tasks(sample_tasks, similarity_threshold=0.8)
        
        assert isinstance(clusters, dict)
        assert len(clusters) > 0
    
    def test_explain_similarity(self, semantic_searcher, sample_tasks):
        """Test similarity explanation"""
        result = SimilarityResult(
            item=sample_tasks[0],
            similarity=0.95,
            metadata={}
        )
        
        explanation = semantic_searcher.explain_similarity(
            query="fibonacci implementation",
            result=result
        )
        
        assert "very high" in explanation.lower()
        assert "0.95" in explanation or "95" in explanation


# ============================================================================
# UTILITY TESTS
# ============================================================================

class TestUtilities:
    """Test utility functions"""
    
    def test_count_tokens(self):
        """Test token counting"""
        text = "Hello, world! This is a test."
        tokens = count_tokens(text)
        
        assert tokens > 0
        assert isinstance(tokens, int)
        
        # Longer text should have more tokens
        long_text = text * 10
        long_tokens = count_tokens(long_text)
        assert long_tokens > tokens
    
    def test_context_item_auto_token_count(self):
        """Test ContextItem auto-counts tokens"""
        item = ContextItem(
            content="Test content",
            type="test",
            timestamp=datetime.now()
        )
        
        assert item.token_count > 0
    
    def test_context_window_utilization(self):
        """Test context window utilization calculation"""
        items = [
            ContextItem(content="x" * 100, type="test", timestamp=datetime.now())
        ]
        
        context = ContextWindow(
            items=items,
            total_tokens=sum(i.token_count for i in items),
            max_tokens=1000,
            relevance_threshold=0.5
        )
        
        assert 0 <= context.utilization <= 100
        assert not context.is_full()  # Should not be full


# ============================================================================
# INTEGRATION TESTS
# ============================================================================

class TestIntegration:
    """Test full integration scenarios"""
    
    @pytest.mark.skipif(not os.getenv("OPENAI_API_KEY"), reason="Requires OpenAI API key")
    def test_end_to_end_workflow(self, context_manager, sample_documents):
        """Test complete workflow: store → retrieve → optimize"""
        # 1. Store documents
        context_manager.vector_store.store(sample_documents)
        
        # 2. Retrieve relevant context
        context = context_manager.get_relevant_context(
            task_description="implement Python algorithm",
            task_id="e2e_task",
            k=3
        )
        
        # 3. Verify context quality
        assert len(context.items) > 0
        assert context.total_tokens <= context.max_tokens
        assert all(item.relevance >= context.relevance_threshold for item in context.items)
        
        # 4. Format for Anthropic
        formatted = context_manager.format_for_anthropic(context)
        assert "text" in formatted
    
    @pytest.mark.skipif(not os.getenv("OPENAI_API_KEY"), reason="Requires OpenAI API key")
    def test_performance_with_large_dataset(self, vector_store):
        """Test performance with 100+ documents"""
        # Create 100 documents
        docs = [
            VectorDocument(
                id=f"perf_doc_{i}",
                content=f"Document {i} about {'Python' if i % 2 == 0 else 'JavaScript'} programming",
                metadata={"type": "code", "index": i}
            )
            for i in range(100)
        ]
        
        # Store (batched)
        start = time.time()
        vector_store.store(docs)
        store_time = time.time() - start
        
        # Search
        start = time.time()
        results = vector_store.search("Python programming", k=10)
        search_time = time.time() - start
        
        # Verify performance
        assert search_time < 0.5, f"Search took {search_time*1000:.1f}ms (target: <500ms)"
        assert len(results) == 10
        
        print(f"\n📊 Performance:")
        print(f"  Store 100 docs: {store_time:.2f}s")
        print(f"  Search top-10: {search_time*1000:.1f}ms")


# ============================================================================
# RUN TESTS
# ============================================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
