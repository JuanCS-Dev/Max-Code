# Max-Code Integration Guide

**Building a Personalized CLI with Maximus AI as Core**

---

## 🎯 Vision

**Max-Code** is a personalized CLI tool (similar to Claude Code) that leverages **Maximus AI** as its intelligence core. Unlike generic tools, Max-Code is tailored to your specific workflows, preferences, and needs.

---

## 🏗️ Architecture Overview

```
┌─────────────────────────────────────┐
│         Max-Code CLI                │
│  ┌─────────────────────────────┐   │
│  │  Command Parser & Router    │   │
│  └──────────┬──────────────────┘   │
│             │                       │
│  ┌──────────▼──────────────────┐   │
│  │   Maximus Client Library    │   │
│  └──────────┬──────────────────┘   │
└─────────────┼───────────────────────┘
              │
              │ HTTP/REST
              │
┌─────────────▼───────────────────────┐
│         MAXIMUS AI CORE             │
│  ┌────────┬────────┬────────┬────┐ │
│  │  Core  │PENELOPE│  MABA  │NIS │ │
│  └────────┴────────┴────────┴────┘ │
└─────────────────────────────────────┘
```

---

## 📦 Project Structure (Proposed)

```
max-code/
├── src/
│   ├── cli/
│   │   ├── __init__.py
│   │   ├── main.py              # Entry point
│   │   ├── commands/            # Command implementations
│   │   │   ├── ask.py          # max-code ask
│   │   │   ├── fix.py          # max-code fix
│   │   │   ├── commit.py       # max-code commit
│   │   │   ├── docs.py         # max-code docs
│   │   │   └── ...
│   │   ├── parser.py            # Argument parsing
│   │   └── formatter.py         # Output formatting
│   │
│   ├── maximus_client/          # Maximus AI client library
│   │   ├── __init__.py
│   │   ├── base.py             # Base client
│   │   ├── core.py             # Core service client
│   │   ├── penelope.py         # PENELOPE client
│   │   ├── maba.py             # MABA client
│   │   ├── nis.py              # NIS client
│   │   ├── orchestrator.py     # Orchestrator client
│   │   └── exceptions.py       # Custom exceptions
│   │
│   ├── config/
│   │   ├── __init__.py
│   │   ├── loader.py           # Config loader
│   │   └── defaults.yaml       # Default configuration
│   │
│   └── utils/
│       ├── __init__.py
│       ├── git.py              # Git utilities
│       ├── file.py             # File utilities
│       └── terminal.py         # Terminal utilities
│
├── tests/
│   ├── unit/
│   ├── integration/
│   └── e2e/
│
├── docs/
│   ├── GETTING_STARTED.md
│   ├── COMMANDS.md
│   └── CONFIGURATION.md
│
├── config/
│   └── default.yaml            # Default config
│
├── .maxcoderc.example          # User config template
├── pyproject.toml              # Python project config
├── setup.py                    # Installation script
├── requirements.txt
├── README.md
└── LICENSE
```

---

## 🚀 Phase 1: Core Setup (Week 1)

### Step 1.1: Project Initialization

```bash
mkdir max-code
cd max-code

# Create virtual environment
python3.11 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install click httpx pydantic pyyaml rich asyncio
```

### Step 1.2: Create Entry Point

**`src/cli/main.py`:**

```python
#!/usr/bin/env python3
"""Max-Code CLI - Personalized development assistant powered by Maximus AI"""

import click
from rich.console import Console

console = Console()

@click.group()
@click.version_option(version='1.0.0')
@click.option('--config', default='~/.maxcoderc', help='Config file path')
@click.pass_context
def cli(ctx, config):
    """Max-Code: Your personalized AI-powered development CLI"""
    ctx.ensure_object(dict)
    ctx.obj['config'] = config
    console.print("[bold cyan]Max-Code CLI v1.0.0[/bold cyan]")
    console.print("Powered by Maximus AI\n")

@cli.command()
@click.argument('question')
@click.pass_context
def ask(ctx, question):
    """Ask Maximus AI a question"""
    console.print(f"[yellow]Question:[/yellow] {question}")
    # TODO: Implement Maximus Core integration
    console.print("[green]Answer:[/green] (Coming soon)")

@cli.command()
@click.argument('file')
@click.pass_context
def fix(ctx, file):
    """Auto-fix issues in a file using PENELOPE"""
    console.print(f"[yellow]Fixing:[/yellow] {file}")
    # TODO: Implement PENELOPE integration
    console.print("[green]Fixed![/green] (Coming soon)")

@cli.command()
@click.pass_context
def commit(ctx):
    """Generate intelligent commit message"""
    console.print("[yellow]Generating commit message...[/yellow]")
    # TODO: Implement NIS integration
    console.print("[green]Commit message generated![/green] (Coming soon)")

if __name__ == '__main__':
    cli(obj={})
```

### Step 1.3: Create Maximus Client Base

**`src/maximus_client/base.py`:**

```python
"""Base client for Maximus AI services"""

import httpx
from typing import Optional, Dict, Any
import logging

logger = logging.getLogger(__name__)

class MaximusBaseClient:
    """Base client for all Maximus AI services"""

    def __init__(
        self,
        base_url: str = "http://localhost:8150",
        timeout: int = 30,
        api_key: Optional[str] = None
    ):
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.api_key = api_key

        # Create httpx client
        headers = {}
        if api_key:
            headers['Authorization'] = f'Bearer {api_key}'

        self.client = httpx.AsyncClient(
            base_url=self.base_url,
            timeout=timeout,
            headers=headers
        )

    async def _request(
        self,
        method: str,
        endpoint: str,
        **kwargs
    ) -> Dict[str, Any]:
        """Make HTTP request to Maximus service"""
        try:
            response = await self.client.request(
                method=method,
                url=endpoint,
                **kwargs
            )
            response.raise_for_status()
            return response.json()

        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error: {e.response.status_code}")
            raise
        except httpx.RequestError as e:
            logger.error(f"Request error: {e}")
            raise

    async def get(self, endpoint: str, **kwargs) -> Dict[str, Any]:
        """GET request"""
        return await self._request('GET', endpoint, **kwargs)

    async def post(self, endpoint: str, **kwargs) -> Dict[str, Any]:
        """POST request"""
        return await self._request('POST', endpoint, **kwargs)

    async def health_check(self) -> bool:
        """Check if service is healthy"""
        try:
            response = await self.get('/health')
            return response.get('status') == 'healthy'
        except Exception as e:
            logger.error(f"Health check failed: {e}")
            return False

    async def close(self):
        """Close HTTP client"""
        await self.client.aclose()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()
```

### Step 1.4: Create Core Service Client

**`src/maximus_client/core.py`:**

```python
"""Maximus Core service client"""

from .base import MaximusBaseClient
from typing import Dict, Any, Optional

class MaximusCore(MaximusBaseClient):
    """Client for Maximus Core consciousness system"""

    def __init__(self, base_url: str = "http://localhost:8150", **kwargs):
        super().__init__(base_url, **kwargs)

    async def ask(
        self,
        question: str,
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Ask Maximus Core a question.

        Args:
            question: The question to ask
            context: Optional context for the question

        Returns:
            Answer from Maximus Core
        """
        payload = {
            "question": question,
            "context": context or {}
        }

        return await self.post('/api/v1/consciousness/ask', json=payload)

    async def predict(
        self,
        context: Dict[str, Any],
        task: str
    ) -> Dict[str, Any]:
        """
        Use predictive coding to make decision.

        Args:
            context: Current context
            task: Task to perform

        Returns:
            Prediction result
        """
        payload = {
            "context": context,
            "task": task
        }

        return await self.post('/api/v1/consciousness/predict', json=payload)

    async def validate_ethics(
        self,
        action: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Validate action against ethical framework.

        Args:
            action: Action to validate

        Returns:
            Validation result
        """
        return await self.post('/api/v1/ethics/validate', json=action)

    async def check_governance(
        self,
        operation: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Check constitutional compliance.

        Args:
            operation: Operation to check

        Returns:
            Compliance result
        """
        return await self.post('/api/v1/governance/check', json=operation)
```

### Step 1.5: Configuration Management

**`~/.maxcoderc` (User Configuration):**

```yaml
# Max-Code Configuration

# Maximus AI Services
maximus:
  base_url: "http://localhost:8150"
  timeout: 30
  api_key: null  # Optional: for production deployment

# Service-specific settings
services:
  core:
    enabled: true
    port: 8150

  penelope:
    enabled: true
    port: 8151
    sabbath_respect: true
    auto_fix: false  # Require confirmation

  maba:
    enabled: true
    port: 8152
    headless: true
    max_sessions: 5

  nis:
    enabled: true
    port: 8153
    cache: true
    narrative_style: "concise"  # concise, detailed, technical

  orchestrator:
    enabled: true
    port: 8154

# CLI Behavior
cli:
  interactive_mode: false
  auto_commit: false
  confirm_destructive: true
  verbose: false
  color: true

# Git Integration
git:
  auto_commit_message: true
  sign_commits: false
  push_after_commit: false

# Personalization
preferences:
  language: "en"
  timezone: "America/Sao_Paulo"
  working_hours:
    start: "09:00"
    end: "18:00"
  respect_sabbath: true  # Align with PENELOPE
```

**`src/config/loader.py`:**

```python
"""Configuration loader for Max-Code"""

import yaml
from pathlib import Path
from typing import Dict, Any
import os

class Config:
    """Configuration manager"""

    def __init__(self, config_path: str = None):
        if config_path is None:
            config_path = os.path.expanduser('~/.maxcoderc')

        self.config_path = Path(config_path)
        self.config = self._load()

    def _load(self) -> Dict[str, Any]:
        """Load configuration from file"""
        if not self.config_path.exists():
            return self._get_defaults()

        with open(self.config_path) as f:
            return yaml.safe_load(f)

    def _get_defaults(self) -> Dict[str, Any]:
        """Get default configuration"""
        return {
            'maximus': {
                'base_url': 'http://localhost:8150',
                'timeout': 30,
                'api_key': None
            },
            'services': {
                'core': {'enabled': True, 'port': 8150},
                'penelope': {'enabled': True, 'port': 8151},
                'maba': {'enabled': True, 'port': 8152},
                'nis': {'enabled': True, 'port': 8153}
            },
            'cli': {
                'interactive_mode': False,
                'verbose': False,
                'color': True
            }
        }

    def get(self, key: str, default=None) -> Any:
        """Get configuration value by dot-notation key"""
        keys = key.split('.')
        value = self.config

        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default

        return value

    def save(self):
        """Save configuration to file"""
        with open(self.config_path, 'w') as f:
            yaml.dump(self.config, f, default_flow_style=False)
```

---

## 🎨 Phase 2: Implement Commands (Week 2)

### Command: `max-code ask`

**`src/cli/commands/ask.py`:**

```python
"""Ask command implementation"""

import click
import asyncio
from rich.console import Console
from rich.markdown import Markdown

from src.maximus_client import MaximusCore
from src.config import Config

console = Console()

@click.command()
@click.argument('question')
@click.option('--context', '-c', help='Additional context')
@click.pass_context
def ask(ctx, question, context):
    """Ask Maximus AI a question"""
    config = Config(ctx.obj.get('config'))

    asyncio.run(ask_async(question, context, config))

async def ask_async(question: str, context: str, config: Config):
    """Async implementation of ask"""
    base_url = f"http://localhost:{config.get('services.core.port')}"

    async with MaximusCore(base_url=base_url) as core:
        console.print(f"[yellow]Question:[/yellow] {question}\n")

        # Check health
        if not await core.health_check():
            console.print("[red]Error:[/red] Maximus Core is not responding")
            return

        # Ask question
        try:
            result = await core.ask(
                question=question,
                context={"additional": context} if context else None
            )

            # Display answer
            answer = result.get('answer', 'No answer provided')
            console.print(Markdown(f"**Answer:**\n\n{answer}"))

            # Display metadata
            if config.get('cli.verbose'):
                console.print(f"\n[dim]Confidence: {result.get('confidence', 'N/A')}[/dim]")
                console.print(f"[dim]Processing time: {result.get('processing_time', 'N/A')}ms[/dim]")

        except Exception as e:
            console.print(f"[red]Error:[/red] {e}")
```

### Command: `max-code fix`

**`src/cli/commands/fix.py`:**

```python
"""Fix command implementation"""

import click
import asyncio
from rich.console import Console
from rich.syntax import Syntax
from pathlib import Path

from src.maximus_client import PENELOPE
from src.config import Config

console = Console()

@click.command()
@click.argument('file', type=click.Path(exists=True))
@click.option('--auto', is_flag=True, help='Auto-apply fix without confirmation')
@click.option('--severity', type=click.Choice(['SURGICAL', 'MODERATE']), default='SURGICAL')
@click.pass_context
def fix(ctx, file, auto, severity):
    """Auto-fix issues in a file using PENELOPE"""
    config = Config(ctx.obj.get('config'))

    asyncio.run(fix_async(file, auto, severity, config))

async def fix_async(file: str, auto: bool, severity: str, config: Config):
    """Async implementation of fix"""
    base_url = f"http://localhost:{config.get('services.penelope.port')}"

    async with PENELOPE(base_url=base_url) as penelope:
        console.print(f"[yellow]Analyzing:[/yellow] {file}\n")

        # Read file
        file_path = Path(file)
        code = file_path.read_text()

        # Request healing
        try:
            result = await penelope.heal(
                code=code,
                file_path=str(file_path),
                severity=severity
            )

            if not result.get('needs_fix'):
                console.print("[green]✓[/green] File looks good, no fixes needed")
                return

            # Display suggested patch
            patch = result.get('patch')
            console.print("[yellow]Suggested fix:[/yellow]\n")
            console.print(Syntax(patch, "diff", theme="monokai"))

            # Check sabbath
            if result.get('sabbath_active'):
                console.print("\n[yellow]Note:[/yellow] It's Sabbath. PENELOPE suggests deferring fixes.")

            # Confirm or auto-apply
            if auto or config.get('services.penelope.auto_fix'):
                apply = True
            else:
                apply = click.confirm('\nApply this fix?')

            if apply:
                file_path.write_text(result.get('fixed_code'))
                console.print(f"[green]✓[/green] Fixed {file}")
            else:
                console.print("[yellow]Fix not applied[/yellow]")

        except Exception as e:
            console.print(f"[red]Error:[/red] {e}")
```

### Command: `max-code commit`

**`src/cli/commands/commit.py`:**

```python
"""Commit command implementation"""

import click
import asyncio
import subprocess
from rich.console import Console

from src.maximus_client import NIS
from src.config import Config
from src.utils.git import get_git_diff, get_changed_files

console = Console()

@click.command()
@click.option('--push', is_flag=True, help='Push after commit')
@click.pass_context
def commit(ctx, push):
    """Generate intelligent commit message and commit"""
    config = Config(ctx.obj.get('config'))

    asyncio.run(commit_async(push, config))

async def commit_async(push: bool, config: Config):
    """Async implementation of commit"""
    base_url = f"http://localhost:{config.get('services.nis.port')}"

    # Get git status
    try:
        diff = get_git_diff()
        files = get_changed_files()
    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")
        return

    if not files:
        console.print("[yellow]No changes to commit[/yellow]")
        return

    console.print(f"[yellow]Changed files:[/yellow]")
    for f in files:
        console.print(f"  - {f}")
    console.print()

    # Generate commit message
    async with NIS(base_url=base_url) as nis:
        try:
            result = await nis.generate(
                narrative_type="commit_message",
                context={
                    "files_changed": files,
                    "diff": diff,
                    "style": config.get('services.nis.narrative_style', 'concise')
                }
            )

            message = result.get('message')
            console.print("[yellow]Generated commit message:[/yellow]\n")
            console.print(f"  {message}\n")

            if click.confirm('Use this message?'):
                # Perform commit
                subprocess.run(['git', 'commit', '-m', message], check=True)
                console.print("[green]✓[/green] Committed")

                if push and config.get('git.push_after_commit'):
                    subprocess.run(['git', 'push'], check=True)
                    console.print("[green]✓[/green] Pushed")

        except Exception as e:
            console.print(f"[red]Error:[/red] {e}")
```

---

## 🧪 Phase 3: Testing (Week 3)

### Unit Tests

**`tests/unit/test_maximus_client.py`:**

```python
import pytest
from src.maximus_client import MaximusCore

@pytest.mark.asyncio
async def test_core_health_check():
    async with MaximusCore() as core:
        health = await core.health_check()
        assert health is True

@pytest.mark.asyncio
async def test_core_ask():
    async with MaximusCore() as core:
        result = await core.ask("What is 2+2?")
        assert 'answer' in result
```

### Integration Tests

**`tests/integration/test_commands.py`:**

```python
from click.testing import CliRunner
from src.cli.main import cli

def test_ask_command():
    runner = CliRunner()
    result = runner.invoke(cli, ['ask', 'test question'])
    assert result.exit_code == 0
```

---

## 📚 Phase 4: Documentation & Polish (Week 4)

1. Complete README.md
2. Command reference
3. Configuration guide
4. Troubleshooting guide
5. Examples and tutorials

---

## 🚀 Installation & Distribution

### PyPI Package

**`setup.py`:**

```python
from setuptools import setup, find_packages

setup(
    name='max-code',
    version='1.0.0',
    description='Personalized AI-powered development CLI',
    author='Your Name',
    packages=find_packages(),
    install_requires=[
        'click>=8.0',
        'httpx>=0.24',
        'pydantic>=2.0',
        'pyyaml>=6.0',
        'rich>=13.0',
    ],
    entry_points={
        'console_scripts': [
            'max-code=src.cli.main:cli',
        ],
    },
)
```

### Installation

```bash
# From PyPI (once published)
pip install max-code

# From source
git clone <repo>
cd max-code
pip install -e .
```

---

## 📖 Next Steps

1. **Implement remaining commands:** `docs`, `explain`, `suggest`
2. **Add interactive mode:** REPL-style interaction
3. **Create plugins system:** Allow extending with custom commands
4. **Build CI/CD pipeline:** Automated testing and releases
5. **Create web dashboard:** Visual interface for Maximus AI

---

**Ready to build Max-Code!**

*For questions or support, refer to the main Maximus AI documentation.*
