"""
Plan Visualizer - Beautiful preview of execution plans

Displays ExecutionPlan from TaskPlanner with:
- SOFIA architectural analysis
- DREAM reality check
- Step-by-step breakdown
- Risk summary
- Time estimates
- Constitutional validation status

Biblical Foundation:
"Os planos bem elaborados levam à fartura" (Provérbios 21:5)
"Planejem cuidadosamente o que fazem" (Provérbios 4:26 NTLH)

Integration:
- Uses existing ExecutionPlan from core/task_planner.py
- Rich UI components
- Color-coded risk levels
- Constitutional compliance display

Soli Deo Gloria
"""

from rich.console import Console, Group
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.tree import Tree
from rich.syntax import Syntax
from typing import Optional, Dict, Any
from pathlib import Path

# Import existing models
from core.task_planner import ExecutionPlan, ToolStep, PlanStatus


class PlanVisualizer:
    """
    Visualize execution plans before execution
    
    Uses existing ExecutionPlan from TaskPlanner.
    Displays with beautiful Rich UI.
    
    Examples:
        >>> from core.task_planner import TaskPlanner
        >>> planner = TaskPlanner()
        >>> plan = await planner.plan_task("Create calculator")
        >>> 
        >>> visualizer = PlanVisualizer()
        >>> visualizer.show_plan(plan)
        >>> if visualizer.confirm_execution():
        ...     execute(plan)
    """
    
    # Risk level colors (matches confirmation system)
    RISK_COLORS = {
        "LOW": "green",
        "MEDIUM": "yellow",
        "HIGH": "red",
        "CRITICAL": "bold red"
    }
    
    # Risk level icons
    RISK_ICONS = {
        "LOW": "🟢",
        "MEDIUM": "🟡",
        "HIGH": "🔴",
        "CRITICAL": "🚨"
    }
    
    def __init__(self, console: Optional[Console] = None):
        """
        Initialize plan visualizer
        
        Args:
            console: Rich console (created if None)
        """
        self.console = console or Console()
    
    def show_plan(self, plan: ExecutionPlan, show_constitutional: bool = True):
        """
        Display complete execution plan
        
        Args:
            plan: ExecutionPlan from TaskPlanner
            show_constitutional: Show constitutional validation details
        """
        self.console.print()
        
        # 1. Header with task description
        self._display_header(plan)
        
        # 2. SOFIA architectural analysis
        if plan.architectural_vision:
            self._display_sofia_analysis(plan)
        
        # 3. DREAM reality check
        if plan.dream_analysis:
            self._display_dream_check(plan)
        
        # 4. Execution steps table
        self._display_steps_table(plan.steps)
        
        # 5. Constitutional validation (if enabled)
        if show_constitutional and plan.constitutional_approved:
            self._display_constitutional_status(plan)
        
        # 6. Summary
        self._display_summary(plan)
        
        self.console.print()
    
    def _display_header(self, plan: ExecutionPlan):
        """Display plan header"""
        # Create header text
        header = Text()
        header.append("🎯 ", style="cyan")
        header.append(plan.task_description, style="bold cyan")
        
        # Add task ID
        header.append("\n\n", style="dim")
        header.append(f"Plan ID: {plan.task_id}", style="dim cyan")
        
        # Add complexity estimate
        if plan.complexity_estimate:
            complexity_colors = {
                "LOW": "green",
                "MEDIUM": "yellow",
                "HIGH": "red",
                "VERY_HIGH": "bold red"
            }
            color = complexity_colors.get(plan.complexity_estimate, "white")
            header.append(f" • Complexity: {plan.complexity_estimate}", style=f"dim {color}")
        
        # Create panel
        panel = Panel(
            header,
            border_style="cyan",
            padding=(1, 2),
            title="[bold cyan]Execution Plan"
        )
        
        self.console.print(panel)
        self.console.print()
    
    def _display_sofia_analysis(self, plan: ExecutionPlan):
        """Display SOFIA architectural analysis"""
        # Create analysis text
        text = Text()
        text.append("🏗️ SOFIA Architectural Analysis\n\n", style="bold blue")
        text.append(plan.architectural_vision, style="white")
        
        # Add dependencies if any
        if plan.dependencies:
            text.append("\n\n📦 Dependencies:\n", style="bold blue")
            for dep in plan.dependencies:
                text.append(f"  • {dep}\n", style="cyan")
        
        # Add estimated time
        if plan.estimated_time:
            text.append(f"\n⏱️  Estimated time: {plan.estimated_time}", style="dim yellow")
        
        panel = Panel(
            text,
            border_style="blue",
            padding=(1, 2)
        )
        
        self.console.print(panel)
        self.console.print()
    
    def _display_dream_check(self, plan: ExecutionPlan):
        """Display DREAM reality check"""
        # Create reality check text
        text = Text()
        text.append("🤖 DREAM Reality Check\n\n", style="bold magenta")
        text.append(plan.dream_analysis, style="white")
        
        # Reality score with color
        score_percent = int(plan.reality_score * 100)
        if plan.reality_score >= 0.8:
            score_color = "green"
            score_icon = "✓"
        elif plan.reality_score >= 0.5:
            score_color = "yellow"
            score_icon = "⚠"
        else:
            score_color = "red"
            score_icon = "⚠️"
        
        text.append(f"\n\n{score_icon} Reality Score: {score_percent}%", style=f"bold {score_color}")
        
        # Alternative suggestions
        if plan.alternative_suggestions:
            text.append("\n\n💡 Suggestions:\n", style="bold magenta")
            for suggestion in plan.alternative_suggestions:
                text.append(f"  • {suggestion}\n", style="cyan")
        
        # Risks identified
        if plan.risks_identified:
            text.append("\n⚠️  Risks:\n", style="bold red")
            for risk in plan.risks_identified:
                text.append(f"  • {risk}\n", style="yellow")
        
        panel = Panel(
            text,
            border_style="magenta",
            padding=(1, 2)
        )
        
        self.console.print(panel)
        self.console.print()
    
    def _display_steps_table(self, steps: list[ToolStep]):
        """Display execution steps as table"""
        if not steps:
            self.console.print("[dim]No execution steps defined[/dim]")
            return
        
        # Create table
        table = Table(
            title="📋 Execution Steps",
            border_style="cyan",
            show_header=True,
            header_style="bold cyan",
            title_style="bold cyan"
        )
        
        table.add_column("#", style="dim", width=4, justify="right")
        table.add_column("Description", style="white", no_wrap=False)
        table.add_column("Tool", style="cyan", width=15)
        table.add_column("Risk", justify="center", width=6)
        table.add_column("Status", justify="center", width=8)
        
        # Add rows
        for step in steps:
            # Risk icon
            risk = step.constitutional_risk or "LOW"
            risk_icon = self.RISK_ICONS.get(risk, "🟢")
            
            # Status icon
            if step.executed:
                if step.error:
                    status = "❌"
                    status_style = "red"
                else:
                    status = "✅"
                    status_style = "green"
            else:
                status = "⏳"
                status_style = "dim"
            
            # Truncate description if too long
            desc = step.description
            if len(desc) > 50:
                desc = desc[:47] + "..."
            
            table.add_row(
                str(step.step_number),
                desc,
                step.tool_name,
                risk_icon,
                f"[{status_style}]{status}[/{status_style}]"
            )
        
        self.console.print(table)
        self.console.print()
    
    def _display_constitutional_status(self, plan: ExecutionPlan):
        """Display constitutional validation status"""
        text = Text()
        
        if plan.constitutional_approved:
            text.append("⚖️  Constitutional Validation: ", style="bold white")
            text.append("✅ APPROVED", style="bold green")
            
            # Score
            score_percent = int(plan.constitutional_score * 100)
            text.append(f" ({score_percent}%)", style="dim green")
            
            # Violations (if any)
            if plan.constitutional_violations:
                text.append("\n\n⚠️  Warnings:\n", style="bold yellow")
                for violation in plan.constitutional_violations:
                    text.append(f"  • {violation}\n", style="yellow")
        else:
            text.append("⚖️  Constitutional Validation: ", style="bold white")
            text.append("❌ REJECTED", style="bold red")
            
            # Violations
            if plan.constitutional_violations:
                text.append("\n\nViolations:\n", style="bold red")
                for violation in plan.constitutional_violations:
                    text.append(f"  • {violation}\n", style="red")
        
        panel = Panel(
            text,
            border_style="green" if plan.constitutional_approved else "red",
            padding=(1, 2)
        )
        
        self.console.print(panel)
        self.console.print()
    
    def _display_summary(self, plan: ExecutionPlan):
        """Display execution summary"""
        # Calculate stats
        total_steps = len(plan.steps)
        
        # Count risk levels
        risk_counts = {
            "LOW": 0,
            "MEDIUM": 0,
            "HIGH": 0,
            "CRITICAL": 0
        }
        
        for step in plan.steps:
            risk = step.constitutional_risk or "LOW"
            if risk in risk_counts:
                risk_counts[risk] += 1
        
        # Build summary text
        summary = Text()
        summary.append("📊 Summary\n\n", style="bold white")
        summary.append(f"Total steps:      {total_steps}\n")
        
        # Estimated time (parse if string, calculate if missing)
        if plan.estimated_time:
            summary.append(f"Estimated time:   {plan.estimated_time}\n")
        
        # Status
        status_colors = {
            "PENDING": "yellow",
            "PLANNING": "cyan",
            "APPROVED": "green",
            "EXECUTING": "blue",
            "COMPLETED": "green",
            "FAILED": "red"
        }
        status_color = status_colors.get(plan.status.value, "white")
        summary.append(f"Status:           ", style="white")
        summary.append(f"{plan.status.value.upper()}\n", style=f"bold {status_color}")
        
        # Risk breakdown
        summary.append("\nRisk levels:\n")
        summary.append(f"  🟢 Low:       {risk_counts['LOW']}\n")
        summary.append(f"  🟡 Medium:    {risk_counts['MEDIUM']}\n")
        summary.append(f"  🔴 High:      {risk_counts['HIGH']}\n")
        
        if risk_counts['CRITICAL'] > 0:
            summary.append(f"  🚨 Critical:  {risk_counts['CRITICAL']}\n", style="bold red")
        
        panel = Panel(
            summary,
            border_style="cyan",
            padding=(1, 2)
        )
        
        self.console.print(panel)
    
    def confirm_execution(self, plan: Optional[ExecutionPlan] = None) -> bool:
        """
        Ask user to confirm plan execution
        
        Args:
            plan: ExecutionPlan (optional, for additional checks)
        
        Returns:
            True if user confirms, False otherwise
        """
        from rich.prompt import Confirm
        
        self.console.print()
        
        # Check if plan has critical risks
        if plan:
            critical_steps = [
                s for s in plan.steps
                if s.constitutional_risk == "CRITICAL"
            ]
            
            if critical_steps:
                self.console.print(
                    "[bold red]⚠️  WARNING: This plan contains CRITICAL risk steps![/bold red]"
                )
                self.console.print()
        
        try:
            return Confirm.ask(
                "[bold cyan]Execute this plan?[/bold cyan]",
                default=True
            )
        except KeyboardInterrupt:
            self.console.print("\n[yellow]⚠️  Execution cancelled by user[/yellow]")
            return False


# Convenience function
def preview_and_confirm(plan: ExecutionPlan) -> bool:
    """
    Show plan preview and ask for confirmation
    
    Args:
        plan: ExecutionPlan to preview
    
    Returns:
        True if user confirms
    
    Example:
        >>> plan = await planner.plan_task("Create app")
        >>> if preview_and_confirm(plan):
        ...     execute(plan)
    """
    visualizer = PlanVisualizer()
    visualizer.show_plan(plan)
    return visualizer.confirm_execution(plan)


# Export
__all__ = [
    'PlanVisualizer',
    'preview_and_confirm',
]
