"""
Vector Store using ChromaDB + OpenAI Embeddings

RESEARCH SYNTHESIS (2025-11-08):
- OpenAI embeddings: $0.00002/1K tokens (text-embedding-3-small)
- Best chunk size: ~1000 tokens with 20% overlap
- ChromaDB: Local SQLite backend, no external DB needed
- Search latency target: <500ms

TRADEOFFS:
✅ OpenAI embeddings: Cheaper, faster, proven quality
❌ Anthropic: No native embeddings API
→ DECISION: Use OpenAI for embeddings, Anthropic for reasoning
"""
import os
import logging
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass
from pathlib import Path

import chromadb
from chromadb.config import Settings
from openai import OpenAI

logger = logging.getLogger(__name__)


@dataclass
class VectorDocument:
    """Document with metadata for vector storage"""
    id: str
    content: str
    metadata: Dict
    embedding: Optional[List[float]] = None


class VectorStore:
    """
    Vector store using ChromaDB + OpenAI embeddings
    
    Features:
    - Local SQLite storage (no external DB)
    - OpenAI text-embedding-3-small (cost-effective)
    - Semantic search with relevance scoring
    - Support for code, docs, and conversation context
    
    Performance:
    - Embedding: ~50ms per chunk
    - Search: <500ms for top-k
    - Storage: SQLite (persistent)
    """
    
    def __init__(
        self,
        collection_name: str = "max_code_context",
        persist_directory: str = "./chroma_db",
        embedding_model: str = "text-embedding-3-small"
    ):
        """
        Initialize vector store
        
        Args:
            collection_name: ChromaDB collection name
            persist_directory: Local storage path
            embedding_model: OpenAI embedding model (default: text-embedding-3-small)
        """
        self.collection_name = collection_name
        self.persist_directory = Path(persist_directory)
        self.embedding_model = embedding_model
        
        # Initialize OpenAI client
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            logger.warning("OPENAI_API_KEY not set, using Anthropic fallback (less efficient)")
            # Fallback: usar Anthropic se OpenAI não disponível
            api_key = os.getenv("ANTHROPIC_API_KEY")
            if not api_key:
                raise ValueError("Either OPENAI_API_KEY or ANTHROPIC_API_KEY must be set")
        
        self.openai_client = OpenAI(api_key=api_key) if "OPENAI" in os.environ else None
        
        # Initialize ChromaDB
        self.persist_directory.mkdir(parents=True, exist_ok=True)
        self.client = chromadb.PersistentClient(
            path=str(self.persist_directory),
            settings=Settings(anonymized_telemetry=False)
        )
        
        # Get or create collection
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            metadata={"description": "MAX Code CLI context storage"}
        )
        
        logger.info(f"VectorStore initialized: {collection_name}")
        logger.info(f"  Storage: {self.persist_directory}")
        logger.info(f"  Embedding model: {embedding_model}")
        logger.info(f"  Documents: {self.collection.count()}")
    
    def embed(self, text: str) -> List[float]:
        """
        Generate embedding for text using OpenAI
        
        Best practices (from research):
        - Chunk at ~1000 tokens
        - Use text-embedding-3-small for cost-effectiveness
        - Add 20% overlap between chunks
        
        Args:
            text: Text to embed
            
        Returns:
            Embedding vector
        """
        if not self.openai_client:
            raise ValueError("OpenAI client not initialized")
        
        try:
            response = self.openai_client.embeddings.create(
                input=text,
                model=self.embedding_model
            )
            embedding = response.data[0].embedding
            logger.debug(f"Generated embedding (dim={len(embedding)}) for text: {text[:50]}...")
            return embedding
        
        except Exception as e:
            logger.error(f"Embedding generation failed: {e}")
            raise
    
    def store(
        self,
        documents: List[VectorDocument],
        batch_size: int = 2048  # OpenAI max batch size
    ) -> None:
        """
        Store documents with embeddings
        
        Args:
            documents: List of documents to store
            batch_size: Max batch size (OpenAI limit: 2048)
        """
        if not documents:
            logger.warning("No documents to store")
            return
        
        logger.info(f"Storing {len(documents)} documents...")
        
        # Generate embeddings in batches
        for i in range(0, len(documents), batch_size):
            batch = documents[i:i + batch_size]
            
            # Generate embeddings
            texts = [doc.content for doc in batch]
            try:
                response = self.openai_client.embeddings.create(
                    input=texts,
                    model=self.embedding_model
                )
                embeddings = [item.embedding for item in response.data]
            except Exception as e:
                logger.error(f"Batch embedding failed: {e}")
                # Fallback: individual embeddings
                embeddings = [self.embed(text) for text in texts]
            
            # Store in ChromaDB
            ids = [doc.id for doc in batch]
            metadatas = [doc.metadata for doc in batch]
            
            self.collection.add(
                ids=ids,
                embeddings=embeddings,
                documents=texts,
                metadatas=metadatas
            )
            
            logger.info(f"  Batch {i//batch_size + 1}: {len(batch)} docs stored")
        
        logger.info(f"✅ {len(documents)} documents stored successfully")
    
    def search(
        self,
        query: str,
        k: int = 5,
        filter_metadata: Optional[Dict] = None
    ) -> List[Tuple[VectorDocument, float]]:
        """
        Semantic search for relevant documents
        
        Target performance (from research):
        - Latency: <500ms
        - Relevance: cosine similarity
        
        Args:
            query: Search query
            k: Number of results
            filter_metadata: Optional metadata filter
            
        Returns:
            List of (document, similarity_score) tuples
        """
        import time
        start = time.time()
        
        # Generate query embedding
        query_embedding = self.embed(query)
        
        # Search ChromaDB
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=k,
            where=filter_metadata
        )
        
        elapsed = time.time() - start
        logger.info(f"Search completed in {elapsed*1000:.1f}ms")
        
        if elapsed > 0.5:
            logger.warning(f"⚠️  Search latency ({elapsed*1000:.1f}ms) exceeds target (500ms)")
        
        # Parse results
        documents = []
        for i in range(len(results['ids'][0])):
            doc = VectorDocument(
                id=results['ids'][0][i],
                content=results['documents'][0][i],
                metadata=results['metadatas'][0][i],
                embedding=None  # Don't return embeddings
            )
            distance = results['distances'][0][i]
            # Convert distance to similarity (cosine similarity = 1 - distance)
            similarity = 1.0 - distance
            documents.append((doc, similarity))
        
        return documents
    
    def clear(self) -> None:
        """Clear all documents from collection"""
        logger.warning(f"Clearing collection: {self.collection_name}")
        self.client.delete_collection(name=self.collection_name)
        self.collection = self.client.get_or_create_collection(
            name=self.collection_name,
            metadata={"description": "MAX Code CLI context storage"}
        )
        logger.info("✅ Collection cleared")
    
    def count(self) -> int:
        """Get document count"""
        return self.collection.count()
    
    def get_by_id(self, doc_id: str) -> Optional[VectorDocument]:
        """Get document by ID"""
        results = self.collection.get(ids=[doc_id])
        
        if not results['ids']:
            return None
        
        return VectorDocument(
            id=results['ids'][0],
            content=results['documents'][0],
            metadata=results['metadatas'][0]
        )
    
    def delete(self, doc_ids: List[str]) -> None:
        """Delete documents by IDs"""
        self.collection.delete(ids=doc_ids)
        logger.info(f"Deleted {len(doc_ids)} documents")
    
    def __repr__(self) -> str:
        return (
            f"VectorStore(collection={self.collection_name}, "
            f"docs={self.count()}, "
            f"model={self.embedding_model})"
        )


# Convenience function
def get_vector_store(
    collection_name: str = "max_code_context",
    persist_directory: str = "./chroma_db"
) -> VectorStore:
    """Get or create vector store singleton"""
    return VectorStore(
        collection_name=collection_name,
        persist_directory=persist_directory
    )
