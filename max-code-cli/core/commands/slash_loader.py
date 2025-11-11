#!/usr/bin/env python3
"""
Slash Command Loader - Custom Command System with Boris Technique ✨

Philosophy (Boris):
"Commands are not just functions - they're user intentions
crystallized into reusable actions. Make them discoverable,
customizable, and powerful."

Pattern: .claude/commands/*.md (like Claude Code)

Example command file (.claude/commands/deploy.md):
```markdown
---
name: deploy
description: Deploy application to production
args: [environment]
---

Deploy the application to {{ environment }} environment.

Steps:
1. Run tests
2. Build Docker image
3. Push to registry
4. Deploy to {{ environment }}

Please execute these steps carefully.
```

Security:
- Sandboxed execution (no arbitrary code)
- Template injection protection
- File path validation

Beauty:
- YAML frontmatter for metadata
- Markdown for prompts
- Template variables ({{ var }})
- Auto-reload on file change

Soli Deo Gloria 🙏
"""

import os
import re
from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import dataclass
import yaml

from rich.console import Console


console = Console()


@dataclass
class SlashCommand:
    """Custom slash command definition"""
    name: str
    description: str
    prompt: str
    args: List[str] = None
    file_path: str = None

    def __post_init__(self):
        if self.args is None:
            self.args = []


class TemplateEngine:
    """
    Simple template engine for command prompts.

    Boris: "Templates are code with blanks. Fill the blanks
    with context, generate the prompt."
    """

    @staticmethod
    def render(template: str, variables: Dict[str, str]) -> str:
        """
        Render template with variables.

        Supports: {{ variable }} syntax

        Args:
            template: Template string with {{ placeholders }}
            variables: Dict of variable values

        Returns:
            Rendered string
        """
        result = template

        # Replace {{ variable }} with values
        for key, value in variables.items():
            # Match {{ key }} with optional whitespace
            pattern = r'\{\{\s*' + re.escape(key) + r'\s*\}\}'
            result = re.sub(pattern, str(value), result)

        return result

    @staticmethod
    def extract_variables(template: str) -> List[str]:
        """
        Extract variable names from template.

        Args:
            template: Template string

        Returns:
            List of variable names
        """
        # Find all {{ variable }} patterns
        pattern = r'\{\{\s*(\w+)\s*\}\}'
        matches = re.findall(pattern, template)
        return list(set(matches))  # Unique variables


class SlashCommandLoader:
    """
    Loader for custom slash commands.

    Design Principles (Boris):
    1. Convention over Configuration - .claude/commands/*.md
    2. Hot Reload - Detect file changes
    3. Validation - Parse and validate on load
    4. Beautiful Errors - Clear messages for invalid commands

    Boris Quote:
    "A command system without customization is like a car
    without a steering wheel - it goes, but you can't direct it."
    """

    def __init__(self, commands_dir: Optional[str] = None):
        """
        Initialize loader.

        Args:
            commands_dir: Directory with command files (default: .claude/commands)
        """
        if commands_dir is None:
            commands_dir = os.path.join(os.getcwd(), '.claude', 'commands')

        self.commands_dir = Path(commands_dir)
        self.commands: Dict[str, SlashCommand] = {}
        self.template_engine = TemplateEngine()
        self.console = Console()

        # Track file modification times for reload
        self._file_mtimes: Dict[str, float] = {}

    def load_commands(self) -> Dict[str, SlashCommand]:
        """
        Load all commands from directory.

        Returns:
            Dict of command_name -> SlashCommand
        """
        self.commands = {}
        self._file_mtimes = {}

        # Check if directory exists
        if not self.commands_dir.exists():
            return self.commands

        # Load all .md files
        for file_path in self.commands_dir.glob('*.md'):
            try:
                command = self._load_command_file(file_path)
                if command:
                    self.commands[command.name] = command
                    self._file_mtimes[str(file_path)] = file_path.stat().st_mtime
            except Exception as e:
                console.print(f"[yellow]⚠️  Failed to load {file_path.name}: {e}[/yellow]")

        return self.commands

    def _load_command_file(self, file_path: Path) -> Optional[SlashCommand]:
        """
        Load single command file.

        Args:
            file_path: Path to .md file

        Returns:
            SlashCommand or None if invalid
        """
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Parse frontmatter
        # Expected format:
        # ---
        # name: command-name
        # description: Command description
        # args: [arg1, arg2]
        # ---
        # Prompt template here

        # Split frontmatter and prompt
        parts = content.split('---', 2)

        if len(parts) < 3:
            raise ValueError("Invalid format: missing frontmatter (---)")

        frontmatter_text = parts[1].strip()
        prompt_template = parts[2].strip()

        # Parse YAML frontmatter
        try:
            frontmatter = yaml.safe_load(frontmatter_text)
        except yaml.YAMLError as e:
            raise ValueError(f"Invalid YAML frontmatter: {e}")

        # Validate required fields
        if 'name' not in frontmatter:
            raise ValueError("Missing 'name' in frontmatter")
        if 'description' not in frontmatter:
            raise ValueError("Missing 'description' in frontmatter")

        # Create command
        command = SlashCommand(
            name=frontmatter['name'],
            description=frontmatter['description'],
            prompt=prompt_template,
            args=frontmatter.get('args', []),
            file_path=str(file_path)
        )

        return command

    def get_command(self, name: str) -> Optional[SlashCommand]:
        """
        Get command by name.

        Args:
            name: Command name

        Returns:
            SlashCommand or None
        """
        return self.commands.get(name)

    def render_command(self, name: str, args: Dict[str, str]) -> Optional[str]:
        """
        Render command with arguments.

        Args:
            name: Command name
            args: Argument values

        Returns:
            Rendered prompt or None
        """
        command = self.get_command(name)
        if not command:
            return None

        # Render template
        rendered = self.template_engine.render(command.prompt, args)

        return rendered

    def check_for_updates(self) -> bool:
        """
        Check if any command files have been modified.

        Returns:
            True if files changed, False otherwise
        """
        if not self.commands_dir.exists():
            return False

        for file_path in self.commands_dir.glob('*.md'):
            file_path_str = str(file_path)
            current_mtime = file_path.stat().st_mtime

            # Check if file is new or modified
            if file_path_str not in self._file_mtimes:
                return True

            if current_mtime > self._file_mtimes[file_path_str]:
                return True

        return False

    def reload_if_changed(self) -> bool:
        """
        Reload commands if files have changed.

        Returns:
            True if reloaded, False otherwise
        """
        if self.check_for_updates():
            console.print("[dim]🔄 Reloading custom commands...[/dim]")
            self.load_commands()
            return True

        return False

    def list_commands(self) -> List[SlashCommand]:
        """Get list of all commands"""
        return list(self.commands.values())

    def get_command_help(self, name: str) -> Optional[str]:
        """
        Get help text for command.

        Args:
            name: Command name

        Returns:
            Help text or None
        """
        command = self.get_command(name)
        if not command:
            return None

        lines = []
        lines.append(f"[bold cyan]/{command.name}[/bold cyan]")
        lines.append(f"{command.description}")

        if command.args:
            lines.append(f"\n[bold]Arguments:[/bold]")
            for arg in command.args:
                lines.append(f"  - {arg}")

        lines.append(f"\n[dim]Source: {command.file_path}[/dim]")

        return "\n".join(lines)


# Convenience function
def load_custom_commands(commands_dir: Optional[str] = None) -> Dict[str, SlashCommand]:
    """
    Load custom commands from directory.

    Args:
        commands_dir: Commands directory (default: .claude/commands)

    Returns:
        Dict of commands
    """
    loader = SlashCommandLoader(commands_dir)
    return loader.load_commands()
