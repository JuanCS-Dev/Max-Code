"""
User Confirmation UI - Interactive prompts for risky operations

Beautiful confirmation prompts with:
- Risk level visualization
- Diff preview
- Affected files list
- Color-coded warnings
- Keyboard shortcuts

Biblical Foundation:
"No coração do homem se projetam os seus planos, mas a resposta certa dos lábios vem do SENHOR" (Provérbios 16:1)
Human plans, divine guidance - ask before acting.

Soli Deo Gloria
"""

from rich.console import Console, Group
from rich.prompt import Confirm
from rich.panel import Panel
from rich.text import Text
from rich.table import Table
from rich.syntax import Syntax
from typing import Optional, List
import difflib

from core.risk_classifier import RiskAssessment, RiskLevel


class ConfirmationUI:
    """
    UI for user confirmations with rich visual feedback
    
    Features:
    - Color-coded risk warnings
    - Diff preview with syntax highlighting
    - Affected files table
    - Reversibility indicators
    - Backup notifications
    
    Examples:
        >>> ui = ConfirmationUI()
        >>> if ui.confirm_file_operation(risk_assessment, diff=diff_text):
        ...     proceed_with_operation()
    """
    
    # Risk level colors
    RISK_COLORS = {
        RiskLevel.SAFE: "green",
        RiskLevel.LOW: "blue",
        RiskLevel.MEDIUM: "yellow",
        RiskLevel.HIGH: "red",
        RiskLevel.CRITICAL: "bold red"
    }
    
    # Risk level icons
    RISK_ICONS = {
        RiskLevel.SAFE: "✓",
        RiskLevel.LOW: "ℹ",
        RiskLevel.MEDIUM: "⚠",
        RiskLevel.HIGH: "⚠️",
        RiskLevel.CRITICAL: "🚨"
    }
    
    def __init__(self, console: Optional[Console] = None):
        """
        Initialize confirmation UI
        
        Args:
            console: Rich console (created if None)
        """
        self.console = console or Console()
    
    def confirm_file_operation(
        self,
        risk: RiskAssessment,
        diff: Optional[str] = None,
        old_content: Optional[str] = None,
        new_content: Optional[str] = None,
        operation_name: str = "operation"
    ) -> bool:
        """
        Ask user to confirm file operation
        
        Args:
            risk: Risk assessment
            diff: Git-style diff (optional)
            old_content: Original content (optional)
            new_content: New content (optional)
            operation_name: Name of operation for display
        
        Returns:
            True if user confirms, False otherwise
        """
        # Skip confirmation for safe/low risk
        if not risk.requires_confirmation:
            return True
        
        # Display risk warning
        self._display_risk_warning(risk)
        
        # Show diff if available
        if diff:
            self._display_diff(diff)
        elif old_content is not None and new_content is not None:
            self._display_side_by_side(
                old_content,
                new_content,
                risk.affected_files[0] if risk.affected_files else "file"
            )
        
        # Show affected files (if multiple)
        if len(risk.affected_files) > 1:
            self._display_affected_files(risk.affected_files)
        
        # Show safety features
        if risk.backup_available:
            self.console.print(
                "[dim]ℹ️  A backup will be created before modification[/dim]\n"
            )
        
        if risk.reversible:
            self.console.print(
                "[dim green]✓ This operation is reversible (via backup or git)[/dim green]\n"
            )
        else:
            self.console.print(
                "[bold red]⚠️  This operation is NOT REVERSIBLE[/bold red]\n"
            )
        
        # Ask confirmation
        prompt_text = self._get_confirmation_prompt(risk, operation_name)
        
        try:
            return Confirm.ask(prompt_text, default=False)
        except KeyboardInterrupt:
            self.console.print("\n[yellow]⚠️  Operation cancelled by user[/yellow]")
            return False
    
    def confirm_batch_operation(
        self,
        risk: RiskAssessment,
        operations: List[tuple[str, str]],  # [(operation, filepath), ...]
    ) -> bool:
        """
        Confirm batch operation
        
        Args:
            risk: Risk assessment for batch
            operations: List of operations
        
        Returns:
            True if confirmed
        """
        self._display_risk_warning(risk)
        
        # Show operations table
        self._display_batch_operations(operations)
        
        prompt_text = self._get_confirmation_prompt(risk, "batch operation")
        
        try:
            return Confirm.ask(prompt_text, default=False)
        except KeyboardInterrupt:
            self.console.print("\n[yellow]⚠️  Batch operation cancelled by user[/yellow]")
            return False
    
    def _display_risk_warning(self, risk: RiskAssessment):
        """Display risk warning banner"""
        color = self.RISK_COLORS[risk.level]
        icon = self.RISK_ICONS[risk.level]
        
        # Build warning content
        warning = Text()
        warning.append(f"{icon} ", style=color)
        warning.append(f"Risk Level: {risk.level.value.upper()}", style=f"bold {color}")
        warning.append("\n\n")
        warning.append(f"Reason: {risk.reason}", style=color)
        
        # Add reversibility warning if not reversible
        if not risk.reversible:
            warning.append("\n\n")
            warning.append("⚠️  This operation is NOT REVERSIBLE", style="bold red")
        
        # Create panel
        panel = Panel(
            warning,
            border_style=color,
            padding=(1, 2),
            title=f"[bold {color}]⚡ Confirmation Required"
        )
        
        self.console.print()
        self.console.print(panel)
        self.console.print()
    
    def _display_diff(self, diff: str):
        """Display git-style diff with syntax highlighting"""
        if not diff.strip():
            return
        
        syntax = Syntax(
            diff,
            "diff",
            theme="monokai",
            line_numbers=False,
            word_wrap=True
        )
        
        panel = Panel(
            syntax,
            title="[bold cyan]📝 Changes",
            border_style="cyan",
            padding=(1, 2)
        )
        
        self.console.print(panel)
        self.console.print()
    
    def _display_side_by_side(self, old: str, new: str, filename: str):
        """Display side-by-side comparison using diff"""
        # Generate unified diff
        old_lines = old.splitlines(keepends=True)
        new_lines = new.splitlines(keepends=True)
        
        diff = difflib.unified_diff(
            old_lines,
            new_lines,
            fromfile=f"{filename} (before)",
            tofile=f"{filename} (after)",
            lineterm=""
        )
        
        diff_text = "\n".join(diff)
        
        if diff_text.strip():
            self._display_diff(diff_text)
    
    def _display_affected_files(self, files: List[str]):
        """Display list of affected files"""
        table = Table(
            title="📁 Affected Files",
            border_style="cyan",
            show_header=True,
            header_style="bold cyan"
        )
        table.add_column("File Path", style="cyan")
        
        # Show first 20 files
        for f in files[:20]:
            table.add_row(f)
        
        # Add "more" indicator if truncated
        if len(files) > 20:
            table.add_row(f"[dim]... and {len(files) - 20} more files[/dim]")
        
        self.console.print(table)
        self.console.print()
    
    def _display_batch_operations(self, operations: List[tuple[str, str]]):
        """Display batch operations table"""
        table = Table(
            title="📋 Operations",
            border_style="cyan",
            show_header=True,
            header_style="bold cyan"
        )
        table.add_column("Operation", style="yellow", width=12)
        table.add_column("File", style="white")
        
        # Show first 15 operations
        for op, filepath in operations[:15]:
            # Color code operation
            op_colors = {
                "read": "green",
                "write": "blue",
                "edit": "yellow",
                "delete": "red"
            }
            op_color = op_colors.get(op.lower(), "white")
            
            table.add_row(
                f"[{op_color}]{op.upper()}[/{op_color}]",
                filepath
            )
        
        # Add "more" indicator if truncated
        if len(operations) > 15:
            table.add_row(
                "[dim]...[/dim]",
                f"[dim]and {len(operations) - 15} more[/dim]"
            )
        
        self.console.print(table)
        self.console.print()
    
    def _get_confirmation_prompt(self, risk: RiskAssessment, operation_name: str) -> str:
        """Get confirmation prompt text"""
        if risk.level == RiskLevel.CRITICAL:
            return f"[bold red]🚨 CRITICAL: Proceed with {operation_name}?[/bold red]"
        elif risk.level == RiskLevel.HIGH:
            return f"[bold yellow]⚠️  HIGH RISK: Continue with {operation_name}?[/bold yellow]"
        elif risk.level == RiskLevel.MEDIUM:
            return f"[yellow]Proceed with {operation_name}?[/yellow]"
        else:
            return f"Continue with {operation_name}?"


class QuietConfirmationUI(ConfirmationUI):
    """
    Minimal confirmation UI (for --yes flag or CI/CD)
    
    Always returns True without prompting.
    Use with caution!
    """
    
    def __init__(self, console: Optional[Console] = None):
        """Initialize quiet UI"""
        super().__init__(console)
    
    def confirm_file_operation(self, *args, **kwargs) -> bool:
        """Always confirm without prompting"""
        return True
    
    def confirm_batch_operation(self, *args, **kwargs) -> bool:
        """Always confirm without prompting"""
        return True


# Convenience functions
def confirm_operation(
    risk: RiskAssessment,
    diff: Optional[str] = None,
    quiet: bool = False,
    **kwargs
) -> bool:
    """
    Convenience function to get confirmation
    
    Args:
        risk: Risk assessment
        diff: Optional diff to display
        quiet: Skip prompts (--yes mode)
        **kwargs: Additional arguments for confirm_file_operation
    
    Returns:
        True if confirmed
    """
    if quiet:
        ui = QuietConfirmationUI()
    else:
        ui = ConfirmationUI()
    
    return ui.confirm_file_operation(risk, diff=diff, **kwargs)


# Export
__all__ = [
    'ConfirmationUI',
    'QuietConfirmationUI',
    'confirm_operation',
]
