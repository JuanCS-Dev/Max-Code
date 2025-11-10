# MAX-CODE-CLI - CLI Reference

**Generated:** 2025-11-07 21:30:00

---

## 1. Main Entry Point

### `cli/main.py`

**Lines:** 581

## 2. Available Commands

- 20:@click.group(invoke_without_command=True)
- 21:@click.option('--version', is_flag=True, help='Show version information')
- 22:@click.option('--no-banner', is_flag=True, help='Disable banner display')
- 23:@click.pass_context
- 24:def cli(ctx, version, no_banner):
- 41:            style=settings.ui.banner_style if hasattr(settings.ui, 'banner_style') else 'default',
- 59:@cli.command()
- 60:@click.option('--profile', type=click.Choice(['development', 'production', 'local']),
- 62:@click.option('--interactive', is_flag=True, help='Interactive profile selection')
- 63:def init(profile, interactive):
- 99:@cli.command()
- 100:def setup():
- 163:@cli.command()
- 164:def config():
- 236:@cli.command()
- 237:@click.argument('profile', type=click.Choice(['development', 'production', 'local']))
- 238:def profile(profile):
- 263:@cli.command()
- 264:def profiles():
- 288:@cli.command()


## 3. REPL (Interactive Shell)

### Overview

**File:** `cli/repl_enhanced.py`
**Lines:** 716

### Slash Commands

- `/help`
- `/exit`
- `/quit`
- `/clear`
- `/sophia`
- `/code`
- `/test`
- `/review`
- `/fix`
- `/docs`
- `/explore`
- `/plan`
- `/sofia`
- `/dream`
- `/dashboard`
- `/theme`

## 4. CLI Modules

| Module | Lines | Purpose |
|--------|-------|---------|
| `auth_command.py` | 303 | CLI module |
| `health_command.py` | 145 | CLI module |
| `learn_command.py` | 377 | CLI module |
| `main.py` | 581 | CLI module |
| `predict_command.py` | 224 | CLI module |
| `repl_enhanced.py` | 716 | CLI module |
| `sabbath_command.py` | 259 | CLI module |
| `task_command.py` | 563 | CLI module |

---

**Generated:** 2025-11-07 21:31:24
