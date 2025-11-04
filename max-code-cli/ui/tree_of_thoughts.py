"""
Max-Code CLI Tree of Thoughts Visualization

Beautiful ToT visualization with:
- Tree structure with branches
- Reasoning step-by-step display
- Constitutional principle analysis (P1-P6)
- Score visualization and path highlighting
- Perfect alignment (TOC-approved! 🎯)

Usage:
    from ui.tree_of_thoughts import ThoughtTree, ReasoningSteps, ConstitutionalAnalysis

    tree = ThoughtTree()
    tree.show_tree(root_node)
"""

from rich.console import Console
from rich.tree import Tree as RichTree
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich.progress import Progress, BarColumn, TextColumn
from typing import List, Dict, Optional, Any
from dataclasses import dataclass
from enum import Enum
import re


class BranchStatus(Enum):
    """Branch evaluation status."""
    ACTIVE = "active"
    BEST = "best"
    PRUNED = "pruned"
    PENDING = "pending"


@dataclass
class ThoughtNode:
    """Single thought/reasoning node."""
    id: str
    content: str
    score: float  # 0-10
    status: BranchStatus
    parent_id: Optional[str] = None
    depth: int = 0
    reasoning: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


@dataclass
class ReasoningStep:
    """Single reasoning step."""
    step_number: int
    description: str
    evaluation: str
    score: float  # 0-10
    decision: str  # continue/prune/select
    rationale: str


@dataclass
class ConstitutionalScore:
    """Constitutional principle evaluation."""
    principle: str  # P1-P6
    name: str
    score: float  # 0-10
    reasoning: str
    conflicts: List[str] = None
    color: str = "cyan"


class ThoughtTree:
    """
    Visualize Tree of Thoughts reasoning.

    Features:
    - Tree structure with branches
    - Node evaluation scores
    - Path highlighting (best/pruned)
    - Beautiful formatting
    """

    # Status colors and symbols
    STATUS_CONFIG = {
        BranchStatus.ACTIVE: ('cyan', '○', 'Active'),
        BranchStatus.BEST: ('green', '✓', 'BEST'),
        BranchStatus.PRUNED: ('red', '✗', 'PRUNED'),
        BranchStatus.PENDING: ('yellow', '⟳', 'Pending'),
    }

    def __init__(self, console: Optional[Console] = None):
        """Initialize thought tree visualizer."""
        self.console = console or Console()

    def show_tree(
        self,
        root: ThoughtNode,
        children: Dict[str, List[ThoughtNode]],
        title: str = "TREE OF THOUGHTS"
    ):
        """
        Display thought tree with branches.

        Args:
            root: Root thought node
            children: Dict mapping parent_id to list of children
            title: Tree title
        """
        # Build rich tree
        tree = RichTree(
            self._format_node(root),
            guide_style="cyan"
        )

        self._build_tree(tree, root.id, children)

        # Display in panel
        panel = Panel(
            tree,
            title=title,
            border_style="cyan",
            padding=(1, 2),
        )

        self.console.print(panel)

    def show_tree_table(
        self,
        nodes: List[ThoughtNode],
        title: str = "THOUGHT ANALYSIS"
    ):
        """
        Display thoughts in table format.

        Args:
            nodes: List of thought nodes
            title: Table title
        """
        table = Table(
            title=title,
            show_header=True,
            header_style="bold cyan",
            border_style="cyan",
            padding=(0, 1),
            expand=False,
        )

        table.add_column("Branch", style="white", width=25)
        table.add_column("Score", style="white", width=12, justify="center")
        table.add_column("Status", style="white", width=15, justify="center")
        table.add_column("Reasoning", style="dim", width=40)

        for node in nodes:
            # Branch content (truncate if needed)
            content = node.content[:23] + "..." if len(node.content) > 25 else node.content

            # Score with color
            score_color = self._get_score_color(node.score)
            score_display = f"[{score_color}]{node.score:.1f}/10[/{score_color}]"

            # Status with symbol
            status_color, status_symbol, status_text = self.STATUS_CONFIG[node.status]
            status_display = f"[{status_color}]{status_symbol} {status_text}[/{status_color}]"

            # Reasoning (truncate if needed)
            reasoning = node.reasoning or ""
            reasoning_display = reasoning[:38] + "..." if len(reasoning) > 40 else reasoning

            table.add_row(
                content,
                score_display,
                status_display,
                reasoning_display
            )

        self.console.print(table)

    def show_comparison(
        self,
        nodes: List[ThoughtNode],
        title: str = "BRANCH COMPARISON"
    ):
        """
        Compare multiple branches side-by-side.

        Args:
            nodes: List of nodes to compare
            title: Comparison title
        """
        table = Table(
            title=title,
            show_header=True,
            header_style="bold cyan",
            border_style="cyan",
            padding=(0, 1),
            expand=False,
        )

        table.add_column("Aspect", style="cyan", width=20)

        for i, node in enumerate(nodes, 1):
            status_color, _, _ = self.STATUS_CONFIG[node.status]
            table.add_column(f"Branch {i}", style=status_color, width=25, justify="center")

        # Add comparison rows
        # Approach
        table.add_row(
            "Approach",
            *[node.content[:23] + "..." if len(node.content) > 25 else node.content for node in nodes]
        )

        # Score
        table.add_row(
            "Score",
            *[f"{node.score:.1f}/10" for node in nodes]
        )

        # Status
        table.add_row(
            "Status",
            *[self.STATUS_CONFIG[node.status][2] for node in nodes]
        )

        # Complexity (from metadata)
        complexities = []
        for node in nodes:
            if node.metadata and 'complexity' in node.metadata:
                complexities.append(node.metadata['complexity'])
            else:
                complexities.append("N/A")
        table.add_row("Complexity", *complexities)

        self.console.print(table)

    def _build_tree(self, tree: RichTree, parent_id: str, children: Dict[str, List[ThoughtNode]]):
        """Recursively build tree structure."""
        if parent_id not in children:
            return

        for child in children[parent_id]:
            branch = tree.add(self._format_node(child))
            self._build_tree(branch, child.id, children)

    def _format_node(self, node: ThoughtNode) -> str:
        """Format node for display."""
        status_color, status_symbol, status_text = self.STATUS_CONFIG[node.status]
        score_color = self._get_score_color(node.score)

        return (
            f"{node.content} "
            f"[{score_color}][Score: {node.score:.1f}/10][/{score_color}] "
            f"[{status_color}]{status_symbol} {status_text}[/{status_color}]"
        )

    def _get_score_color(self, score: float) -> str:
        """Get color based on score."""
        if score >= 8.0:
            return "green"
        elif score >= 6.0:
            return "yellow"
        elif score >= 4.0:
            return "orange3"
        else:
            return "red"


class ReasoningSteps:
    """
    Display step-by-step reasoning process.

    Features:
    - Sequential steps with evaluation
    - Decision points
    - Score progression
    - Final conclusion
    """

    def __init__(self, console: Optional[Console] = None):
        """Initialize reasoning steps display."""
        self.console = console or Console()

    def show_steps(
        self,
        steps: List[ReasoningStep],
        title: str = "REASONING PROCESS",
        show_conclusion: bool = True
    ):
        """
        Display reasoning steps.

        Args:
            steps: List of reasoning steps
            title: Steps title
            show_conclusion: Show final conclusion
        """
        table = Table(
            title=title,
            show_header=True,
            header_style="bold cyan",
            border_style="cyan",
            padding=(0, 1),
            expand=False,
        )

        table.add_column("Step", style="cyan", width=6, justify="center")
        table.add_column("Description", style="white", width=30)
        table.add_column("Evaluation", style="white", width=25)
        table.add_column("Decision", style="white", width=12, justify="center")

        for step in steps:
            # Decision with color
            decision_color = self._get_decision_color(step.decision)
            decision_display = f"[{decision_color}]{step.decision.upper()}[/{decision_color}]"

            # Evaluation (truncate if needed)
            eval_display = step.evaluation[:23] + "..." if len(step.evaluation) > 25 else step.evaluation

            table.add_row(
                str(step.step_number),
                step.description,
                eval_display,
                decision_display
            )

        self.console.print(table)

        # Show conclusion
        if show_conclusion and steps:
            last_step = steps[-1]
            self.console.print()
            conclusion_panel = Panel(
                f"[bold cyan]Final Decision:[/bold cyan] {last_step.decision.upper()}\n\n"
                f"[dim]Rationale:[/dim] {last_step.rationale}",
                title="Conclusion",
                border_style="green" if last_step.decision == "select" else "yellow",
                padding=(1, 2),
            )
            self.console.print(conclusion_panel)

    def show_reasoning_flow(
        self,
        steps: List[ReasoningStep],
        title: str = "REASONING FLOW"
    ):
        """
        Display reasoning as flow diagram.

        Args:
            steps: List of reasoning steps
            title: Flow title
        """
        lines = []
        lines.append(f"[bold cyan]{title}[/bold cyan]")
        lines.append("")

        for i, step in enumerate(steps, 1):
            # Step number and description
            lines.append(f"[cyan]Step {step.step_number}:[/cyan] {step.description}")

            # Evaluation
            lines.append(f"  ├─ [dim]Evaluation:[/dim] {step.evaluation}")

            # Score
            score_color = self._get_score_color(step.score)
            lines.append(f"  ├─ [dim]Score:[/dim] [{score_color}]{step.score:.1f}/10[/{score_color}]")

            # Decision
            decision_color = self._get_decision_color(step.decision)
            lines.append(f"  └─ [dim]Decision:[/dim] [{decision_color}]{step.decision.upper()}[/{decision_color}]")

            # Arrow to next step (if not last)
            if i < len(steps):
                lines.append("      ↓")

            lines.append("")

        panel = Panel(
            "\n".join(lines),
            border_style="cyan",
            padding=(1, 2),
        )

        self.console.print(panel)

    def _get_decision_color(self, decision: str) -> str:
        """Get color based on decision."""
        decision_lower = decision.lower()
        if decision_lower == "select":
            return "green"
        elif decision_lower == "continue":
            return "cyan"
        elif decision_lower == "prune":
            return "red"
        else:
            return "yellow"

    def _get_score_color(self, score: float) -> str:
        """Get color based on score."""
        if score >= 8.0:
            return "green"
        elif score >= 6.0:
            return "yellow"
        elif score >= 4.0:
            return "orange3"
        else:
            return "red"


class ConstitutionalAnalysis:
    """
    Constitutional AI principle analysis (P1-P6).

    Features:
    - P1-P6 scores with reasoning
    - Conflict/tension visualization
    - Trade-off analysis
    - Recommendations
    """

    # Constitutional principles with colors
    PRINCIPLES = {
        'p1': ('Transcendence', 'violet', 'Higher purpose and meaning'),
        'p2': ('Reasoning', 'blue', 'Logic and critical thinking'),
        'p3': ('Care', 'green', 'Empathy and compassion'),
        'p4': ('Wisdom', 'yellow', 'Practical judgment and experience'),
        'p5': ('Beauty', 'magenta', 'Aesthetic and elegance'),
        'p6': ('Autonomy', 'cyan', 'Self-determination and agency'),
    }

    def __init__(self, console: Optional[Console] = None):
        """Initialize constitutional analysis display."""
        self.console = console or Console()

    def show_analysis(
        self,
        scores: List[ConstitutionalScore],
        title: str = "CONSTITUTIONAL ANALYSIS"
    ):
        """
        Display constitutional principle analysis.

        Args:
            scores: List of constitutional scores
            title: Analysis title
        """
        table = Table(
            title=title,
            show_header=True,
            header_style="bold cyan",
            border_style="cyan",
            padding=(0, 1),
            expand=False,
        )

        table.add_column("Principle", style="white", width=15)
        table.add_column("Score", style="white", width=20, justify="center")
        table.add_column("Reasoning", style="dim", width=45)

        for score in scores:
            # Principle with color
            principle_display = f"[{score.color}]{score.principle.upper()} - {score.name}[/{score.color}]"

            # Score bar
            score_bar = self._render_score_bar(score.score, color=score.color)
            score_display = f"{score_bar} {score.score:.1f}/10"

            # Reasoning (truncate if needed)
            reasoning_display = score.reasoning[:43] + "..." if len(score.reasoning) > 45 else score.reasoning

            table.add_row(
                principle_display,
                score_display,
                reasoning_display
            )

        self.console.print(table)

    def show_conflicts(
        self,
        scores: List[ConstitutionalScore],
        title: str = "PRINCIPLE CONFLICTS & TENSIONS"
    ):
        """
        Display conflicts between principles.

        Args:
            scores: List of constitutional scores with conflicts
            title: Conflicts title
        """
        # Find scores with conflicts
        conflicted = [s for s in scores if s.conflicts and len(s.conflicts) > 0]

        if not conflicted:
            self.console.print(f"[green]✓[/green] No principle conflicts detected")
            return

        lines = []
        lines.append(f"[bold yellow]{title}[/bold yellow]")
        lines.append("")

        for score in conflicted:
            lines.append(f"[{score.color}]{score.principle.upper()} - {score.name}[/{score.color}]")
            for conflict in score.conflicts:
                lines.append(f"  ⚠ {conflict}")
            lines.append("")

        panel = Panel(
            "\n".join(lines),
            border_style="yellow",
            padding=(1, 2),
        )

        self.console.print(panel)

    def show_radar_chart(
        self,
        scores: List[ConstitutionalScore],
        title: str = "CONSTITUTIONAL PROFILE"
    ):
        """
        Display constitutional scores as text-based radar chart.

        Args:
            scores: List of constitutional scores
            title: Chart title
        """
        table = Table(
            title=title,
            show_header=False,
            border_style="cyan",
            padding=(0, 2),
            expand=False,
        )

        table.add_column("Principle", style="white", width=25)
        table.add_column("Score", style="white", width=40)

        for score in scores:
            # Principle with color
            principle_display = f"[{score.color}]{score.principle.upper()} - {score.name}[/{score.color}]"

            # Horizontal bar
            bar = self._render_horizontal_bar(score.score, width=30, color=score.color)
            score_display = f"{bar} [{score.color}]{score.score:.1f}[/{score.color}]"

            table.add_row(principle_display, score_display)

        self.console.print(table)

    def show_recommendations(
        self,
        recommendations: List[str],
        title: str = "RECOMMENDATIONS"
    ):
        """
        Display recommendations based on constitutional analysis.

        Args:
            recommendations: List of recommendation strings
            title: Recommendations title
        """
        lines = []
        for i, rec in enumerate(recommendations, 1):
            lines.append(f"[cyan]{i}.[/cyan] {rec}")

        panel = Panel(
            "\n".join(lines),
            title=title,
            border_style="green",
            padding=(1, 2),
        )

        self.console.print(panel)

    def _render_score_bar(self, score: float, width: int = 10, color: str = 'cyan') -> str:
        """Render score progress bar."""
        filled = int((score / 10) * width)
        empty = width - filled
        bar = f"[{color}]{'█' * filled}[/{color}][dim]{'░' * empty}[/dim]"
        return bar

    def _render_horizontal_bar(self, score: float, width: int = 30, color: str = 'cyan') -> str:
        """Render horizontal bar chart."""
        filled = int((score / 10) * width)
        empty = width - filled
        bar = f"[{color}]{'━' * filled}[/{color}][dim]{'─' * empty}[/dim]"
        return bar


# Demo
if __name__ == "__main__":
    print("\n" + "=" * 80)
    print("MAX-CODE CLI TREE OF THOUGHTS VISUALIZATION DEMONSTRATION")
    print("=" * 80 + "\n")

    console = Console()

    # Demo 1: Thought Tree
    print("1. THOUGHT TREE STRUCTURE:")
    tree_viz = ThoughtTree(console)

    root = ThoughtNode(
        id="root",
        content="Implement user authentication",
        score=7.5,
        status=BranchStatus.ACTIVE,
        reasoning="Multiple viable approaches"
    )

    children = {
        "root": [
            ThoughtNode(
                id="oauth",
                content="OAuth 2.0 with Auth0",
                score=8.5,
                status=BranchStatus.BEST,
                parent_id="root",
                depth=1,
                reasoning="Industry standard, secure, easy integration"
            ),
            ThoughtNode(
                id="jwt",
                content="JWT with refresh tokens",
                score=7.5,
                status=BranchStatus.ACTIVE,
                parent_id="root",
                depth=1,
                reasoning="Stateless, good for microservices"
            ),
            ThoughtNode(
                id="sessions",
                content="Traditional sessions",
                score=6.0,
                status=BranchStatus.PRUNED,
                parent_id="root",
                depth=1,
                reasoning="Not scalable for distributed systems"
            ),
        ],
        "oauth": [
            ThoughtNode(
                id="oauth_auth0",
                content="Use Auth0 service",
                score=9.0,
                status=BranchStatus.BEST,
                parent_id="oauth",
                depth=2,
                reasoning="Fully managed, best practices built-in"
            ),
            ThoughtNode(
                id="oauth_custom",
                content="Custom OAuth implementation",
                score=7.0,
                status=BranchStatus.ACTIVE,
                parent_id="oauth",
                depth=2,
                reasoning="More control but higher maintenance"
            ),
        ],
    }

    tree_viz.show_tree(root, children)
    print()

    import time
    time.sleep(2)

    # Demo 2: Thought Table
    print("\n2. THOUGHT ANALYSIS TABLE:")
    all_nodes = [root] + children["root"] + children["oauth"]
    tree_viz.show_tree_table(all_nodes)
    print()

    time.sleep(2)

    # Demo 3: Branch Comparison
    print("\n3. BRANCH COMPARISON:")
    tree_viz.show_comparison(children["root"])
    print()

    time.sleep(2)

    # Demo 4: Reasoning Steps
    print("\n4. REASONING PROCESS:")
    reasoning_viz = ReasoningSteps(console)

    steps = [
        ReasoningStep(
            step_number=1,
            description="Analyze authentication requirements",
            evaluation="Need secure, scalable solution",
            score=8.0,
            decision="continue",
            rationale="Requirements are clear"
        ),
        ReasoningStep(
            step_number=2,
            description="Evaluate OAuth 2.0 approach",
            evaluation="Industry standard, well-supported",
            score=8.5,
            decision="continue",
            rationale="Strong candidate"
        ),
        ReasoningStep(
            step_number=3,
            description="Consider JWT alternative",
            evaluation="Good for microservices",
            score=7.5,
            decision="continue",
            rationale="Worth exploring"
        ),
        ReasoningStep(
            step_number=4,
            description="Compare OAuth vs JWT",
            evaluation="OAuth better for our use case",
            score=8.5,
            decision="select",
            rationale="OAuth 2.0 with Auth0 provides best security and developer experience"
        ),
    ]

    reasoning_viz.show_steps(steps)
    print()

    time.sleep(2)

    # Demo 5: Reasoning Flow
    print("\n5. REASONING FLOW DIAGRAM:")
    reasoning_viz.show_reasoning_flow(steps[:3])
    print()

    time.sleep(2)

    # Demo 6: Constitutional Analysis
    print("\n6. CONSTITUTIONAL ANALYSIS:")
    const_viz = ConstitutionalAnalysis(console)

    const_scores = [
        ConstitutionalScore(
            principle="P1",
            name="Transcendence",
            score=8.0,
            reasoning="Enables users to achieve their authentication goals seamlessly",
            color="violet"
        ),
        ConstitutionalScore(
            principle="P2",
            name="Reasoning",
            score=9.0,
            reasoning="OAuth 2.0 is a well-reasoned, industry-standard approach",
            color="blue"
        ),
        ConstitutionalScore(
            principle="P3",
            name="Care",
            score=8.5,
            reasoning="Protects user data and privacy with proven security measures",
            color="green"
        ),
        ConstitutionalScore(
            principle="P4",
            name="Wisdom",
            score=9.0,
            reasoning="Leverages battle-tested Auth0 platform instead of reinventing",
            color="yellow"
        ),
        ConstitutionalScore(
            principle="P5",
            name="Beauty",
            score=7.5,
            reasoning="Clean integration but could improve UX flows",
            color="magenta",
            conflicts=["Could simplify login UI"]
        ),
        ConstitutionalScore(
            principle="P6",
            name="Autonomy",
            score=8.0,
            reasoning="Users control their authentication preferences",
            color="cyan"
        ),
    ]

    const_viz.show_analysis(const_scores)
    print()

    time.sleep(2)

    # Demo 7: Constitutional Radar
    print("\n7. CONSTITUTIONAL PROFILE:")
    const_viz.show_radar_chart(const_scores)
    print()

    time.sleep(2)

    # Demo 8: Conflicts
    print("\n8. PRINCIPLE CONFLICTS:")
    const_viz.show_conflicts(const_scores)
    print()

    time.sleep(2)

    # Demo 9: Recommendations
    print("\n9. RECOMMENDATIONS:")
    recommendations = [
        "Implement OAuth 2.0 with Auth0 for primary authentication",
        "Add JWT refresh token mechanism for improved UX",
        "Design simplified login flows to enhance P5 (Beauty) score",
        "Implement comprehensive security audit logging",
        "Add user preference management for authentication methods",
    ]
    const_viz.show_recommendations(recommendations)
    print()

    print("=" * 80)
    print("TREE OF THOUGHTS VISUALIZATION DEMO COMPLETE - Perfect Alignment! 🎯")
    print("=" * 80 + "\n")
