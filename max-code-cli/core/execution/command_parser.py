#!/usr/bin/env python3
"""
Command Parser - Parse Complex Execution Commands com Boris Technique ✨

Philosophy (Boris):
"Natural language is powerful. Parse it intelligently,
execute it correctly."

Examples:
- "run agents code test review in parallel"
- "execute read config.json then write output.txt sequentially"
- "chain grep 'TODO' | filter .py files | count lines"

Grammar:
PARALLEL: "run agents <agent1> <agent2> ... in parallel"
SEQUENTIAL: "execute <cmd1> then <cmd2> then <cmd3> sequentially"
CHAIN: "chain <tool1> | <tool2> | <tool3>"

Soli Deo Gloria 🙏
"""

import re
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass
from enum import Enum


class ExecutionMode(Enum):
    """Execution mode"""
    PARALLEL = "parallel"
    SEQUENTIAL = "sequential"
    CHAIN = "chain"
    SINGLE = "single"


@dataclass
class ParsedCommand:
    """Parsed execution command"""
    mode: ExecutionMode
    commands: List[str]
    options: Dict[str, any]
    raw_input: str


class CommandParser:
    """
    Parse complex execution commands.

    Boris: "Grammar is structure. Parse the structure,
    understand the intent."
    """

    # Patterns
    PARALLEL_PATTERN = r'run\s+agents?\s+([\w\s]+)\s+in\s+parallel'
    SEQUENTIAL_PATTERN = r'execute\s+(.*?)\s+sequentially'
    CHAIN_PATTERN = r'chain\s+(.*)'

    # Keywords (English + Portuguese)
    PARALLEL_KEYWORDS = [
        'parallel', 'concurrent', 'simultaneously', 'together',
        'paralelo', 'simultaneo', 'junto', 'juntos', 'lança', 'lanca'
    ]
    SEQUENTIAL_KEYWORDS = [
        'sequential', 'sequentially', 'then', 'after', 'pipeline',
        'sequencial', 'depois', 'então', 'entao'
    ]
    CHAIN_KEYWORDS = ['chain', 'pipe', '|', 'cadeia']

    @classmethod
    def parse(cls, command: str) -> Optional[ParsedCommand]:
        """
        Parse command to determine execution mode.

        Args:
            command: User command string

        Returns:
            ParsedCommand or None if not parseable
        """
        command = command.strip()

        # Try parallel pattern
        if any(kw in command.lower() for kw in cls.PARALLEL_KEYWORDS):
            return cls._parse_parallel(command)

        # Try sequential pattern
        if any(kw in command.lower() for kw in cls.SEQUENTIAL_KEYWORDS):
            return cls._parse_sequential(command)

        # Try chain pattern
        if '|' in command or any(kw in command.lower() for kw in cls.CHAIN_KEYWORDS):
            return cls._parse_chain(command)

        # Single command (default)
        return ParsedCommand(
            mode=ExecutionMode.SINGLE,
            commands=[command],
            options={},
            raw_input=command
        )

    @classmethod
    def _parse_parallel(cls, command: str) -> ParsedCommand:
        """
        Parse parallel execution command.

        Examples:
        - "run agents code test review in parallel"
        - "execute code and test agents concurrently"

        Args:
            command: Command string

        Returns:
            ParsedCommand with PARALLEL mode
        """
        # Extract agent names
        match = re.search(cls.PARALLEL_PATTERN, command, re.IGNORECASE)

        if match:
            agents_str = match.group(1)
            # Split by spaces/commas
            agents = re.split(r'[\s,]+', agents_str.strip())
            agents = [a for a in agents if a and a not in ['and', 'with']]

            return ParsedCommand(
                mode=ExecutionMode.PARALLEL,
                commands=agents,
                options={'max_parallel': len(agents)},
                raw_input=command
            )

        # Fallback: split by "and"
        parts = re.split(r'\s+and\s+', command, flags=re.IGNORECASE)
        commands = [p.strip() for p in parts if p.strip()]

        return ParsedCommand(
            mode=ExecutionMode.PARALLEL,
            commands=commands,
            options={},
            raw_input=command
        )

    @classmethod
    def _parse_sequential(cls, command: str) -> ParsedCommand:
        """
        Parse sequential execution command.

        Examples:
        - "execute read config.json then write output.txt sequentially"
        - "run step1 then step2 then step3"

        Args:
            command: Command string

        Returns:
            ParsedCommand with SEQUENTIAL mode
        """
        # Remove "execute" and "sequentially" keywords
        cleaned = re.sub(r'(execute|sequentially)', '', command, flags=re.IGNORECASE)

        # Split by "then"
        parts = re.split(r'\s+then\s+', cleaned, flags=re.IGNORECASE)
        commands = [p.strip() for p in parts if p.strip()]

        return ParsedCommand(
            mode=ExecutionMode.SEQUENTIAL,
            commands=commands,
            options={'fail_fast': True},
            raw_input=command
        )

    @classmethod
    def _parse_chain(cls, command: str) -> ParsedCommand:
        """
        Parse tool chain command.

        Examples:
        - "chain grep 'TODO' | filter .py | count"
        - "read file.txt | parse json | extract field"

        Args:
            command: Command string

        Returns:
            ParsedCommand with CHAIN mode
        """
        # Remove "chain" keyword
        cleaned = re.sub(r'^chain\s+', '', command, flags=re.IGNORECASE)

        # Split by pipe
        parts = cleaned.split('|')
        commands = [p.strip() for p in parts if p.strip()]

        return ParsedCommand(
            mode=ExecutionMode.CHAIN,
            commands=commands,
            options={},
            raw_input=command
        )

    @classmethod
    def is_complex_command(cls, command: str) -> bool:
        """
        Check if command requires complex execution.

        Args:
            command: Command string

        Returns:
            True if parallel/sequential/chain command
        """
        keywords = (
            cls.PARALLEL_KEYWORDS +
            cls.SEQUENTIAL_KEYWORDS +
            cls.CHAIN_KEYWORDS
        )

        return any(kw in command.lower() for kw in keywords) or '|' in command


# Demo
if __name__ == "__main__":
    from rich.console import Console
    from rich.table import Table

    console = Console()

    console.print("[bold cyan]COMMAND PARSER DEMO[/bold cyan]\n")

    # Test commands
    test_commands = [
        "run agents code test review in parallel",
        "execute code and test agents concurrently",
        "execute read config.json then process data then write output sequentially",
        "run step1 then step2 then step3",
        "chain grep 'TODO' | filter .py | count lines",
        "read file.txt | parse json | extract field",
        "regular single command",
    ]

    table = Table(show_header=True, border_style="cyan")
    table.add_column("Command", width=50)
    table.add_column("Mode", width=15)
    table.add_column("Parts", width=30)

    for cmd in test_commands:
        parsed = CommandParser.parse(cmd)

        mode_color = {
            ExecutionMode.PARALLEL: "yellow",
            ExecutionMode.SEQUENTIAL: "blue",
            ExecutionMode.CHAIN: "magenta",
            ExecutionMode.SINGLE: "white"
        }[parsed.mode]

        table.add_row(
            cmd,
            f"[{mode_color}]{parsed.mode.value}[/{mode_color}]",
            f"{len(parsed.commands)} parts"
        )

    console.print(table)

    # Detailed example
    console.print("\n[bold]Detailed Parse Example:[/bold]")
    example = "run agents code test review in parallel"
    parsed = CommandParser.parse(example)

    console.print(f"Input: [cyan]{example}[/cyan]")
    console.print(f"Mode: [yellow]{parsed.mode.value}[/yellow]")
    console.print(f"Commands: {parsed.commands}")
    console.print(f"Options: {parsed.options}")

    console.print("\n[bold green]✓ Demo complete![/bold green]")
