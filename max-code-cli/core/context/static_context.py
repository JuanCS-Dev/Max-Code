"""
Static Context Collector - Pilar I (RAG)

Memória de Longo Prazo do Projeto via Retrieval-Augmented Generation.

Biblical Foundation:
"Que não se aparte da tua boca o livro desta lei; antes medita nele dia e noite"
(Josué 1:8) - Maintain continuous access to knowledge.

Architecture:
- Semantic chunking via tree-sitter (AST-aware)
- Local embeddings (no network dependency)
- Hybrid search (dense + sparse BM25)
- Incremental indexing (only changed files)

Philosophy:
Context is NOT static text - it's living knowledge that adapts.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from pathlib import Path
import json
import subprocess
from datetime import datetime
import hashlib

# Lazy imports for optional dependencies
try:
    from sentence_transformers import SentenceTransformer
    HAS_EMBEDDINGS = True
except ImportError:
    HAS_EMBEDDINGS = False

try:
    import tree_sitter_python as tspython
    from tree_sitter import Language, Parser
    HAS_TREE_SITTER = True
except ImportError:
    HAS_TREE_SITTER = False


@dataclass
class CodeChunk:
    """
    Semantic code chunk (function, class, or logical block)

    Preserves:
    - Source location (file, line range)
    - Semantic meaning (function/class name)
    - Context (surrounding code)
    - Metadata (git history, dependencies)
    """
    file_path: str
    chunk_type: str  # "function", "class", "module"
    name: str
    code: str
    line_start: int
    line_end: int

    # Metadata
    language: str = "python"
    dependencies: List[str] = field(default_factory=list)
    docstring: Optional[str] = None

    # Search metadata
    embedding: Optional[List[float]] = None
    bm25_score: float = 0.0
    last_modified: Optional[datetime] = None

    @property
    def token_count(self) -> int:
        """Estimate token count (4 chars per token)"""
        return len(self.code) // 4

    def to_dict(self) -> Dict[str, Any]:
        """Serialize for storage"""
        return {
            'file_path': self.file_path,
            'chunk_type': self.chunk_type,
            'name': self.name,
            'code': self.code,
            'line_start': self.line_start,
            'line_end': self.line_end,
            'language': self.language,
            'dependencies': self.dependencies,
            'docstring': self.docstring,
            'last_modified': self.last_modified.isoformat() if self.last_modified else None,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'CodeChunk':
        """Deserialize from storage"""
        if data.get('last_modified'):
            data['last_modified'] = datetime.fromisoformat(data['last_modified'])
        return cls(**data)


@dataclass
class SearchResult:
    """Search result with relevance score"""
    chunk: CodeChunk
    score: float
    match_type: str  # "semantic", "lexical", "hybrid"

    def __repr__(self) -> str:
        return f"<SearchResult {self.chunk.name} score={self.score:.3f} type={self.match_type}>"


class StaticContextCollector:
    """
    Pilar I: Static Context via RAG

    Maintains indexed knowledge of codebase for efficient retrieval.

    Features:
    - Semantic search (embeddings)
    - Lexical search (BM25)
    - Hybrid fusion (best of both)
    - Incremental updates (only changed files)
    - Local-first (no network calls)

    Storage:
    - Index: ~/.max-code/rag_index.json
    - Embeddings: ~/.max-code/rag_embeddings.npy
    """

    def __init__(
        self,
        project_root: Optional[Path] = None,
        index_dir: Optional[Path] = None,
        use_embeddings: bool = True,
    ):
        self.project_root = Path(project_root or Path.cwd())
        self.index_dir = Path(index_dir or Path.home() / ".max-code")
        self.index_dir.mkdir(parents=True, exist_ok=True)

        self.index_file = self.index_dir / "rag_index.json"
        self.embeddings_file = self.index_dir / "rag_embeddings.json"

        # Index state
        self.chunks: List[CodeChunk] = []
        self.file_hashes: Dict[str, str] = {}

        # Embeddings model (lazy load)
        self.use_embeddings = use_embeddings and HAS_EMBEDDINGS
        self._embedder = None

        # Tree-sitter parser (lazy load)
        self._parser = None

        # Load existing index
        self._load_index()

    @property
    def embedder(self) -> Optional[Any]:
        """Lazy load embeddings model"""
        if not self.use_embeddings:
            return None

        if self._embedder is None and HAS_EMBEDDINGS:
            # Use lightweight code embeddings model
            # Alternative: "sentence-transformers/all-MiniLM-L6-v2" (22MB)
            self._embedder = SentenceTransformer('all-MiniLM-L6-v2')

        return self._embedder

    @property
    def parser(self) -> Optional[Any]:
        """Lazy load tree-sitter parser"""
        if self._parser is None and HAS_TREE_SITTER:
            PY_LANGUAGE = Language(tspython.language())
            self._parser = Parser(PY_LANGUAGE)

        return self._parser

    def index_codebase(self, force: bool = False) -> Dict[str, int]:
        """
        Index the codebase (incremental by default)

        Args:
            force: Re-index all files even if unchanged

        Returns:
            Stats: {indexed: N, skipped: M, errors: K}
        """
        stats = {'indexed': 0, 'skipped': 0, 'errors': 0}

        # Get tracked files from git
        files = self._get_tracked_files()

        for file_path in files:
            # Skip non-Python files for now
            if not file_path.endswith('.py'):
                stats['skipped'] += 1
                continue

            # Check if file changed (unless force)
            current_hash = self._hash_file(file_path)
            if not force and file_path in self.file_hashes:
                if self.file_hashes[file_path] == current_hash:
                    stats['skipped'] += 1
                    continue

            # Index this file
            try:
                chunks = self._index_file(file_path)
                stats['indexed'] += len(chunks)
                self.file_hashes[file_path] = current_hash
            except Exception as e:
                print(f"Error indexing {file_path}: {e}")
                stats['errors'] += 1

        # Generate embeddings for new chunks
        if self.use_embeddings:
            self._generate_embeddings()

        # Save index
        self._save_index()

        return stats

    def retrieve_relevant(
        self,
        query: str,
        n: int = 5,
        strategy: str = "hybrid"
    ) -> List[SearchResult]:
        """
        Retrieve relevant code chunks

        Args:
            query: Natural language query or code snippet
            n: Number of results
            strategy: "semantic", "lexical", or "hybrid"

        Returns:
            Top N most relevant chunks
        """
        if not self.chunks:
            return []

        if strategy == "semantic" and self.use_embeddings:
            return self._semantic_search(query, n)
        elif strategy == "lexical":
            return self._lexical_search(query, n)
        else:  # hybrid
            return self._hybrid_search(query, n)

    def _get_tracked_files(self) -> List[str]:
        """Get git-tracked files"""
        try:
            result = subprocess.run(
                ['git', 'ls-files'],
                cwd=self.project_root,
                capture_output=True,
                text=True,
                check=True
            )
            return [
                str(self.project_root / line.strip())
                for line in result.stdout.split('\n')
                if line.strip()
            ]
        except subprocess.CalledProcessError:
            # Fallback: all Python files
            return [
                str(p) for p in self.project_root.rglob('*.py')
                if '.git' not in str(p) and 'venv' not in str(p)
            ]

    def _hash_file(self, file_path: str) -> str:
        """Hash file contents for change detection"""
        try:
            with open(file_path, 'rb') as f:
                return hashlib.md5(f.read()).hexdigest()
        except Exception:
            return ""

    def _index_file(self, file_path: str) -> List[CodeChunk]:
        """
        Index a single file using tree-sitter

        Extracts functions and classes as semantic chunks
        """
        chunks = []

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                code = f.read()
        except Exception as e:
            print(f"Cannot read {file_path}: {e}")
            return chunks

        # Try tree-sitter parsing
        if self.parser:
            chunks.extend(self._parse_with_treesitter(file_path, code))
        else:
            # Fallback: simple regex-based chunking
            chunks.extend(self._parse_simple(file_path, code))

        # Remove old chunks for this file
        self.chunks = [c for c in self.chunks if c.file_path != file_path]

        # Add new chunks
        self.chunks.extend(chunks)

        return chunks

    def _parse_with_treesitter(self, file_path: str, code: str) -> List[CodeChunk]:
        """Parse using tree-sitter (AST-aware)"""
        chunks = []

        tree = self.parser.parse(bytes(code, 'utf8'))
        root = tree.root_node

        # Extract functions and classes
        for node in root.children:
            if node.type == 'function_definition':
                chunk = self._node_to_chunk(file_path, code, node, 'function')
                if chunk:
                    chunks.append(chunk)
            elif node.type == 'class_definition':
                chunk = self._node_to_chunk(file_path, code, node, 'class')
                if chunk:
                    chunks.append(chunk)

        return chunks

    def _node_to_chunk(
        self,
        file_path: str,
        code: str,
        node: Any,
        chunk_type: str
    ) -> Optional[CodeChunk]:
        """Convert tree-sitter node to CodeChunk"""
        try:
            # Extract name
            name_node = node.child_by_field_name('name')
            if not name_node:
                return None

            name = code[name_node.start_byte:name_node.end_byte]

            # Extract code
            chunk_code = code[node.start_byte:node.end_byte]

            # Extract docstring
            docstring = None
            body = node.child_by_field_name('body')
            if body and body.children:
                first_stmt = body.children[0]
                if first_stmt.type == 'expression_statement':
                    expr = first_stmt.children[0]
                    if expr.type == 'string':
                        docstring = code[expr.start_byte:expr.end_byte].strip('"\' ')

            return CodeChunk(
                file_path=file_path,
                chunk_type=chunk_type,
                name=name,
                code=chunk_code,
                line_start=node.start_point[0] + 1,
                line_end=node.end_point[0] + 1,
                docstring=docstring,
                last_modified=datetime.now()
            )
        except Exception as e:
            print(f"Error parsing node: {e}")
            return None

    def _parse_simple(self, file_path: str, code: str) -> List[CodeChunk]:
        """Simple regex-based parsing (fallback)"""
        import re
        chunks = []

        # Find functions
        for match in re.finditer(r'^def (\w+)\(', code, re.MULTILINE):
            name = match.group(1)
            start_line = code[:match.start()].count('\n') + 1

            # Simple heuristic: next def/class or end of file
            next_def = re.search(r'\n(def |class )', code[match.end():])
            end_pos = match.end() + next_def.start() if next_def else len(code)
            chunk_code = code[match.start():end_pos].strip()
            end_line = start_line + chunk_code.count('\n')

            chunks.append(CodeChunk(
                file_path=file_path,
                chunk_type='function',
                name=name,
                code=chunk_code,
                line_start=start_line,
                line_end=end_line,
                last_modified=datetime.now()
            ))

        return chunks

    def _generate_embeddings(self):
        """Generate embeddings for chunks without them"""
        if not self.embedder:
            return

        # Find chunks needing embeddings
        chunks_to_embed = [c for c in self.chunks if c.embedding is None]
        if not chunks_to_embed:
            return

        # Generate embeddings in batch
        texts = [
            f"{c.name}\n{c.docstring or ''}\n{c.code[:500]}"
            for c in chunks_to_embed
        ]

        embeddings = self.embedder.encode(texts, show_progress_bar=False)

        # Assign embeddings
        for chunk, embedding in zip(chunks_to_embed, embeddings):
            chunk.embedding = embedding.tolist()

    def _semantic_search(self, query: str, n: int) -> List[SearchResult]:
        """Semantic search using embeddings"""
        if not self.embedder:
            return []

        # Embed query
        query_embedding = self.embedder.encode([query])[0]

        # Compute cosine similarity
        results = []
        for chunk in self.chunks:
            if chunk.embedding is None:
                continue

            # Cosine similarity
            import numpy as np
            score = np.dot(query_embedding, chunk.embedding) / (
                np.linalg.norm(query_embedding) * np.linalg.norm(chunk.embedding)
            )

            results.append(SearchResult(
                chunk=chunk,
                score=float(score),
                match_type="semantic"
            ))

        # Sort by score
        results.sort(key=lambda r: r.score, reverse=True)
        return results[:n]

    def _lexical_search(self, query: str, n: int) -> List[SearchResult]:
        """Simple lexical search (keyword matching)"""
        query_lower = query.lower()
        query_words = set(query_lower.split())

        results = []
        for chunk in self.chunks:
            # Simple BM25-like scoring
            text = f"{chunk.name} {chunk.docstring or ''} {chunk.code}".lower()

            # Count matching words
            matches = sum(1 for word in query_words if word in text)
            score = matches / len(query_words) if query_words else 0

            if score > 0:
                results.append(SearchResult(
                    chunk=chunk,
                    score=score,
                    match_type="lexical"
                ))

        results.sort(key=lambda r: r.score, reverse=True)
        return results[:n]

    def _hybrid_search(self, query: str, n: int) -> List[SearchResult]:
        """Hybrid search combining semantic + lexical"""
        # Get results from both
        semantic_results = self._semantic_search(query, n * 2) if self.use_embeddings else []
        lexical_results = self._lexical_search(query, n * 2)

        # Combine with reciprocal rank fusion
        combined = {}

        for rank, result in enumerate(semantic_results):
            key = (result.chunk.file_path, result.chunk.name)
            combined[key] = combined.get(key, 0) + 1 / (rank + 60)

        for rank, result in enumerate(lexical_results):
            key = (result.chunk.file_path, result.chunk.name)
            combined[key] = combined.get(key, 0) + 1 / (rank + 60)

        # Sort by combined score
        sorted_results = sorted(combined.items(), key=lambda x: x[1], reverse=True)

        # Map back to chunks
        chunk_map = {
            (c.file_path, c.name): c
            for r in semantic_results + lexical_results
            for c in [r.chunk]
        }

        results = [
            SearchResult(
                chunk=chunk_map[key],
                score=score,
                match_type="hybrid"
            )
            for key, score in sorted_results[:n]
            if key in chunk_map
        ]

        return results

    def _load_index(self):
        """Load index from disk"""
        if not self.index_file.exists():
            return

        try:
            with open(self.index_file, 'r') as f:
                data = json.load(f)

            self.chunks = [CodeChunk.from_dict(c) for c in data.get('chunks', [])]
            self.file_hashes = data.get('file_hashes', {})

            # Load embeddings
            if self.embeddings_file.exists():
                with open(self.embeddings_file, 'r') as f:
                    embeddings_data = json.load(f)

                for chunk in self.chunks:
                    key = f"{chunk.file_path}:{chunk.name}"
                    if key in embeddings_data:
                        chunk.embedding = embeddings_data[key]

        except Exception as e:
            print(f"Error loading index: {e}")

    def _save_index(self):
        """Save index to disk"""
        try:
            data = {
                'chunks': [c.to_dict() for c in self.chunks],
                'file_hashes': self.file_hashes,
                'indexed_at': datetime.now().isoformat(),
                'num_chunks': len(self.chunks),
            }

            with open(self.index_file, 'w') as f:
                json.dump(data, f, indent=2)

            # Save embeddings separately (can be large)
            if self.use_embeddings:
                embeddings_data = {
                    f"{c.file_path}:{c.name}": c.embedding
                    for c in self.chunks
                    if c.embedding is not None
                }

                with open(self.embeddings_file, 'w') as f:
                    json.dump(embeddings_data, f)

        except Exception as e:
            print(f"Error saving index: {e}")

    def get_stats(self) -> Dict[str, Any]:
        """Get indexing statistics"""
        return {
            'num_files': len(self.file_hashes),
            'num_chunks': len(self.chunks),
            'num_functions': sum(1 for c in self.chunks if c.chunk_type == 'function'),
            'num_classes': sum(1 for c in self.chunks if c.chunk_type == 'class'),
            'has_embeddings': self.use_embeddings and any(c.embedding for c in self.chunks),
            'index_size_mb': self.index_file.stat().st_size / 1024 / 1024 if self.index_file.exists() else 0,
        }


# Singleton instance
_collector: Optional[StaticContextCollector] = None


def get_static_collector() -> StaticContextCollector:
    """Get or create singleton static context collector"""
    global _collector
    if _collector is None:
        _collector = StaticContextCollector()
    return _collector
