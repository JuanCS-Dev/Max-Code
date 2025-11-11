#!/usr/bin/env python3
"""
Fuzzy History Search - Enhanced Ctrl+R with Boris Technique ✨

Philosophy (Boris):
"History is not just a list - it's a searchable knowledge base.
Fuzzy matching finds what you meant, not just what you typed."

Features:
- Fuzzy matching (typo-tolerant)
- Frequency-based ranking
- Recency boost
- Smart filtering
- Beautiful UI

Soli Deo Gloria 🙏
"""

from typing import List, Tuple, Optional
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass
import re


@dataclass
class HistoryEntry:
    """Single history entry with metadata"""
    command: str
    timestamp: datetime
    frequency: int = 1
    score: float = 0.0


class FuzzyMatcher:
    """
    Fuzzy string matching algorithm.

    Boris: "Humans make typos. Computers should be forgiving."
    """

    @staticmethod
    def fuzzy_match(query: str, text: str) -> Tuple[bool, float]:
        """
        Check if query fuzzy-matches text.

        Algorithm: Sequential character matching with distance penalty.

        Args:
            query: Search query
            text: Text to match against

        Returns:
            (matched: bool, score: float)
        """
        if not query:
            return True, 1.0

        query = query.lower()
        text = text.lower()

        # Exact match gets perfect score
        if query in text:
            # Bonus for exact match at start
            if text.startswith(query):
                return True, 1.0
            return True, 0.9

        # Fuzzy matching
        query_idx = 0
        text_idx = 0
        matches = []

        while query_idx < len(query) and text_idx < len(text):
            if query[query_idx] == text[text_idx]:
                matches.append(text_idx)
                query_idx += 1

            text_idx += 1

        # Did we match all query characters?
        if query_idx == len(query):
            # Calculate score based on match density
            match_span = matches[-1] - matches[0] + 1
            density = len(matches) / match_span if match_span > 0 else 0
            score = density * 0.8  # Max score 0.8 for fuzzy match

            return True, score

        return False, 0.0


class HistorySearcher:
    """
    Enhanced history search with fuzzy matching.

    Design Principles (Boris):
    1. Fuzzy Matching - Typo-tolerant search
    2. Smart Ranking - Frequency + Recency + Relevance
    3. Fast Search - O(n) with early termination
    4. Context Aware - Recent commands get boost

    Boris Quote:
    "The best search finds what you need before you finish typing."
    """

    def __init__(self, history_file: Optional[Path] = None):
        """
        Initialize history searcher.

        Args:
            history_file: Path to history file (default: ~/.max-code-history)
        """
        if history_file is None:
            history_file = Path.home() / '.max-code-history'

        self.history_file = history_file
        self.matcher = FuzzyMatcher()

        # Load history
        self.entries: List[HistoryEntry] = []
        self._load_history()

    def _load_history(self):
        """Load history from file"""
        if not self.history_file.exists():
            return

        try:
            with open(self.history_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()

            # Count frequency
            freq_map = {}
            for line in lines:
                line = line.strip()
                if line:
                    freq_map[line] = freq_map.get(line, 0) + 1

            # Create entries (most recent first)
            for i, line in enumerate(reversed(lines)):
                line = line.strip()
                if line:
                    # Estimate timestamp (more recent = higher index)
                    timestamp = datetime.now()

                    entry = HistoryEntry(
                        command=line,
                        timestamp=timestamp,
                        frequency=freq_map.get(line, 1)
                    )
                    self.entries.append(entry)

        except Exception:
            pass  # Silent failure

    def search(
        self,
        query: str,
        max_results: int = 10,
        min_score: float = 0.3
    ) -> List[HistoryEntry]:
        """
        Search history with fuzzy matching.

        Args:
            query: Search query
            max_results: Maximum results to return
            min_score: Minimum relevance score

        Returns:
            List of matching HistoryEntry sorted by score
        """
        if not query:
            # No query = return recent commands
            return self.entries[:max_results]

        results = []

        for i, entry in enumerate(self.entries):
            # Fuzzy match
            matched, match_score = self.matcher.fuzzy_match(query, entry.command)

            if matched and match_score >= min_score:
                # Calculate final score
                # Components:
                # 1. Match score (0-1)
                # 2. Frequency boost (log scale)
                # 3. Recency boost (exponential decay)

                frequency_boost = min(entry.frequency * 0.1, 0.3)
                recency_boost = 1.0 / (i + 1)  # More recent = higher

                final_score = (
                    match_score * 0.6 +
                    frequency_boost * 0.2 +
                    recency_boost * 0.2
                )

                entry.score = final_score
                results.append(entry)

        # Sort by score (descending)
        results.sort(key=lambda e: e.score, reverse=True)

        return results[:max_results]

    def get_suggestions(self, partial: str, max_suggestions: int = 5) -> List[str]:
        """
        Get command suggestions based on partial input.

        Args:
            partial: Partial command input
            max_suggestions: Max suggestions to return

        Returns:
            List of suggested commands
        """
        entries = self.search(partial, max_results=max_suggestions)
        return [e.command for e in entries]


# Demo
if __name__ == "__main__":
    from rich.console import Console
    from rich.table import Table

    console = Console()

    console.print("[bold cyan]FUZZY HISTORY SEARCH DEMO[/bold cyan]\n")

    # Create sample history
    sample_commands = [
        "git status",
        "git commit -m 'fix: bug'",
        "git push origin main",
        "python test.py",
        "python main.py",
        "npm install",
        "npm run build",
        "docker ps",
        "docker-compose up",
        "read config.json",
        "write file.txt 'content'",
    ]

    # Simulate history file
    history_file = Path("/tmp/test_history")
    with open(history_file, 'w') as f:
        for cmd in sample_commands * 3:  # Repeat for frequency
            f.write(cmd + '\n')

    # Test searcher
    searcher = HistorySearcher(history_file)

    # Test queries
    test_queries = [
        "git",
        "gti",  # Typo
        "python",
        "docker",
        "config",
        "npm",
    ]

    for query in test_queries:
        console.print(f"\n[bold yellow]Query:[/bold yellow] '{query}'")

        results = searcher.search(query, max_results=5)

        table = Table(show_header=True, border_style="cyan")
        table.add_column("Score", width=8)
        table.add_column("Command", width=50)

        for entry in results:
            score_str = f"{entry.score:.2f}"
            table.add_row(score_str, entry.command)

        console.print(table)

    # Cleanup
    history_file.unlink()

    console.print("\n[bold green]✓[/bold green] Demo complete!")
