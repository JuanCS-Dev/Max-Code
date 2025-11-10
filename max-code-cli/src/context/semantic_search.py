"""
Semantic Search for Tasks and Code

RESEARCH SYNTHESIS:
- Semantic similarity via cosine distance
- Task matching based on description embeddings
- Code similarity for related implementations

USE CASES:
✅ Find similar completed tasks (reuse context)
✅ Discover related code snippets
✅ Identify duplicate or overlapping work
"""
import logging
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass

from .vector_store import VectorStore, VectorDocument
from core.task_models import Task

logger = logging.getLogger(__name__)


@dataclass
class SimilarityResult:
    """Result with similarity score"""
    item: any  # Task or code snippet
    similarity: float
    metadata: Dict


class SemanticSearcher:
    """
    Semantic searcher for tasks and code
    
    Features:
    - Find similar tasks by description
    - Find related code by functionality
    - Configurable similarity thresholds
    """
    
    def __init__(
        self,
        vector_store: Optional[VectorStore] = None,
        similarity_threshold: float = 0.7
    ):
        """
        Initialize semantic searcher
        
        Args:
            vector_store: Vector store instance
            similarity_threshold: Min similarity for results (0-1)
        """
        self.vector_store = vector_store or VectorStore()
        self.similarity_threshold = similarity_threshold
        
        logger.info(f"SemanticSearcher initialized (threshold={similarity_threshold})")
    
    def find_similar_tasks(
        self,
        task: Task,
        k: int = 5,
        min_similarity: Optional[float] = None
    ) -> List[SimilarityResult]:
        """
        Find similar tasks based on description
        
        Use case:
        - Reuse context from similar completed tasks
        - Identify duplicate work
        - Learn from past approaches
        
        Args:
            task: Current task
            k: Number of results
            min_similarity: Min similarity score (default: use threshold)
            
        Returns:
            List of similar tasks with scores
        """
        min_similarity = min_similarity or self.similarity_threshold
        
        logger.info(f"Finding similar tasks for: {task.id}")
        logger.debug(f"  Query: {task.description[:100]}...")
        
        # Search by task description
        results = self.vector_store.search(
            query=task.description,
            k=k,
            filter_metadata={"type": "task"}  # Only search tasks
        )
        
        # Filter by similarity
        similar_tasks = []
        for doc, similarity in results:
            if similarity < min_similarity:
                continue
            
            # Reconstruct task from metadata
            task_data = doc.metadata.get('task_data', {})
            similar_task = Task(
                id=doc.id,
                description=doc.content,
                **task_data
            )
            
            similar_tasks.append(SimilarityResult(
                item=similar_task,
                similarity=similarity,
                metadata=doc.metadata
            ))
        
        logger.info(f"  Found {len(similar_tasks)} similar tasks (threshold={min_similarity})")
        
        return similar_tasks
    
    def find_related_code(
        self,
        query: str,
        k: int = 5,
        language: Optional[str] = None,
        min_similarity: Optional[float] = None
    ) -> List[SimilarityResult]:
        """
        Find related code snippets
        
        Use case:
        - Find similar implementations
        - Discover reusable patterns
        - Reference existing solutions
        
        Args:
            query: Functionality description
            k: Number of results
            language: Filter by language (e.g., 'python', 'javascript')
            min_similarity: Min similarity score
            
        Returns:
            List of code snippets with scores
        """
        min_similarity = min_similarity or self.similarity_threshold
        
        logger.info(f"Finding related code for: {query[:100]}...")
        
        # Build filter
        filter_metadata = {"type": "code"}
        if language:
            filter_metadata["language"] = language
        
        # Search
        results = self.vector_store.search(
            query=query,
            k=k,
            filter_metadata=filter_metadata
        )
        
        # Filter by similarity
        related_code = []
        for doc, similarity in results:
            if similarity < min_similarity:
                continue
            
            related_code.append(SimilarityResult(
                item=doc.content,  # Code snippet
                similarity=similarity,
                metadata=doc.metadata
            ))
        
        logger.info(f"  Found {len(related_code)} related code snippets")
        
        return related_code
    
    def find_similar_documents(
        self,
        query: str,
        doc_type: str = "doc",
        k: int = 5,
        min_similarity: Optional[float] = None
    ) -> List[SimilarityResult]:
        """
        Find similar documents (generic)
        
        Args:
            query: Search query
            doc_type: Document type filter
            k: Number of results
            min_similarity: Min similarity score
            
        Returns:
            List of documents with scores
        """
        min_similarity = min_similarity or self.similarity_threshold
        
        results = self.vector_store.search(
            query=query,
            k=k,
            filter_metadata={"type": doc_type}
        )
        
        similar_docs = []
        for doc, similarity in results:
            if similarity < min_similarity:
                continue
            
            similar_docs.append(SimilarityResult(
                item=doc.content,
                similarity=similarity,
                metadata=doc.metadata
            ))
        
        return similar_docs
    
    def cluster_tasks(
        self,
        tasks: List[Task],
        similarity_threshold: float = 0.8
    ) -> Dict[str, List[Task]]:
        """
        Cluster similar tasks together
        
        Use case:
        - Identify duplicate tasks
        - Group related work
        - Batch similar operations
        
        Args:
            tasks: List of tasks
            similarity_threshold: Min similarity for clustering
            
        Returns:
            Dict of cluster_id -> List[Task]
        """
        logger.info(f"Clustering {len(tasks)} tasks...")
        
        clusters: Dict[str, List[Task]] = {}
        processed = set()
        
        for task in tasks:
            if task.id in processed:
                continue
            
            # Find similar tasks
            similar = self.find_similar_tasks(
                task,
                k=len(tasks),
                min_similarity=similarity_threshold
            )
            
            # Create cluster
            cluster_id = f"cluster_{task.id}"
            cluster_tasks = [task] + [r.item for r in similar if r.item.id not in processed]
            clusters[cluster_id] = cluster_tasks
            
            # Mark as processed
            processed.update(t.id for t in cluster_tasks)
        
        logger.info(f"  Created {len(clusters)} clusters")
        for cluster_id, cluster_tasks in clusters.items():
            logger.debug(f"  {cluster_id}: {len(cluster_tasks)} tasks")
        
        return clusters
    
    def explain_similarity(
        self,
        query: str,
        result: SimilarityResult
    ) -> str:
        """
        Explain why two items are similar
        
        Args:
            query: Original query
            result: Similarity result
            
        Returns:
            Human-readable explanation
        """
        score = result.similarity
        
        if score > 0.9:
            confidence = "very high"
        elif score > 0.8:
            confidence = "high"
        elif score > 0.7:
            confidence = "moderate"
        else:
            confidence = "low"
        
        explanation = f"Similarity: {score:.2%} ({confidence} confidence)\n"
        explanation += f"Query: {query[:100]}...\n"
        
        if isinstance(result.item, Task):
            explanation += f"Task: {result.item.description[:100]}...\n"
        elif isinstance(result.item, str):
            explanation += f"Content: {result.item[:100]}...\n"
        
        return explanation
    
    def __repr__(self) -> str:
        return f"SemanticSearcher(threshold={self.similarity_threshold})"


# Convenience functions
def find_similar_tasks(task: Task, k: int = 5) -> List[SimilarityResult]:
    """Quick helper to find similar tasks"""
    searcher = SemanticSearcher()
    return searcher.find_similar_tasks(task, k=k)


def find_related_code(query: str, k: int = 5, language: Optional[str] = None) -> List[SimilarityResult]:
    """Quick helper to find related code"""
    searcher = SemanticSearcher()
    return searcher.find_related_code(query, k=k, language=language)
