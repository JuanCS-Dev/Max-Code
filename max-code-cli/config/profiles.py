"""
Max-Code CLI Configuration Profiles

Manages configuration profiles for different environments:
- development: Local development with all features enabled
- production: Production deployment with optimizations
- local: Standalone mode without MAXIMUS backend
"""

from enum import Enum
from pathlib import Path
from typing import Dict, Any, Optional
from dataclasses import dataclass, asdict
import json


class Profile(str, Enum):
    """Configuration profiles."""
    DEVELOPMENT = "development"
    PRODUCTION = "production"
    LOCAL = "local"


@dataclass
class ProfileConfig:
    """Configuration for a specific profile."""
    name: str
    description: str
    settings: Dict[str, Any]


# Profile definitions
PROFILES: Dict[Profile, ProfileConfig] = {
    Profile.DEVELOPMENT: ProfileConfig(
        name="development",
        description="Local development with all features enabled",
        settings={
            # Environment
            "MAX_CODE_ENV": "development",

            # MAXIMUS Services (localhost)
            "MAXIMUS_CORE_URL": "http://localhost:8100",  # FIXED: Was 8150, actual backend is 8100
            "MAXIMUS_PENELOPE_URL": "http://localhost:8154",  # Correct
            "MAXIMUS_ORCHESTRATOR_URL": "http://localhost:8027",
            "MAXIMUS_ORACULO_URL": "http://localhost:8026",
            "MAXIMUS_ATLAS_URL": "http://localhost:8007",

            # Service config
            "MAXIMUS_TIMEOUT": "30",
            "MAXIMUS_MAX_RETRIES": "3",

            # Features (all enabled)
            "MAXIMUS_ENABLE_CONSCIOUSNESS": "true",
            "MAXIMUS_ENABLE_PREDICTION": "true",
            "MAXIMUS_ENABLE_NEUROMODULATION": "true",
            "MAX_CODE_ENABLE_CONSTITUTIONAL": "true",
            "MAX_CODE_ENABLE_MULTI_AGENT": "true",
            "MAX_CODE_ENABLE_TOT": "true",

            # UI (all enabled, verbose)
            "MAX_CODE_BANNER_STYLE": "default",
            "MAX_CODE_NO_BANNER": "false",
            "NO_COLOR": "false",
            "MAX_CODE_QUIET": "false",
            "MAX_CODE_VERBOSE": "true",
            "MAX_CODE_SHOW_PROGRESS": "true",
            "MAX_CODE_SHOW_AGENTS": "true",
            "MAX_CODE_SHOW_CONSCIOUSNESS": "true",

            # Logging (verbose)
            "LOG_LEVEL": "DEBUG",
            "MAX_CODE_LOG_FORMAT": "text",
            "MAX_CODE_ENABLE_TRACING": "true",

            # Claude (requires API key from user)
            "CLAUDE_MODEL": "claude-sonnet-4-5-20250929",
            "CLAUDE_TEMPERATURE": "0.7",
            "CLAUDE_MAX_TOKENS": "4096",
        }
    ),

    Profile.PRODUCTION: ProfileConfig(
        name="production",
        description="Production deployment with optimizations",
        settings={
            # Environment
            "MAX_CODE_ENV": "production",

            # MAXIMUS Services (production URLs - to be configured)
            "MAXIMUS_CORE_URL": "http://maximus-core:8150",
            "MAXIMUS_PENELOPE_URL": "http://penelope:8154",
            "MAXIMUS_ORCHESTRATOR_URL": "http://orchestrator:8027",
            "MAXIMUS_ORACULO_URL": "http://oraculo:8026",
            "MAXIMUS_ATLAS_URL": "http://atlas:8007",

            # Service config (production timeouts)
            "MAXIMUS_TIMEOUT": "60",
            "MAXIMUS_MAX_RETRIES": "5",

            # Features (all enabled)
            "MAXIMUS_ENABLE_CONSCIOUSNESS": "true",
            "MAXIMUS_ENABLE_PREDICTION": "true",
            "MAXIMUS_ENABLE_NEUROMODULATION": "true",
            "MAX_CODE_ENABLE_CONSTITUTIONAL": "true",
            "MAX_CODE_ENABLE_MULTI_AGENT": "true",
            "MAX_CODE_ENABLE_TOT": "true",

            # UI (minimal output)
            "MAX_CODE_BANNER_STYLE": "default",
            "MAX_CODE_NO_BANNER": "false",
            "NO_COLOR": "false",
            "MAX_CODE_QUIET": "false",
            "MAX_CODE_VERBOSE": "false",
            "MAX_CODE_SHOW_PROGRESS": "true",
            "MAX_CODE_SHOW_AGENTS": "true",
            "MAX_CODE_SHOW_CONSCIOUSNESS": "false",  # Less verbose in prod

            # Logging (info level)
            "LOG_LEVEL": "INFO",
            "MAX_CODE_LOG_FORMAT": "json",  # Structured logs for prod
            "MAX_CODE_ENABLE_TRACING": "true",

            # Claude (requires API key from user)
            "CLAUDE_MODEL": "claude-sonnet-4-5-20250929",
            "CLAUDE_TEMPERATURE": "0.7",
            "CLAUDE_MAX_TOKENS": "4096",
        }
    ),

    Profile.LOCAL: ProfileConfig(
        name="local",
        description="Standalone mode without MAXIMUS backend",
        settings={
            # Environment
            "MAX_CODE_ENV": "local",

            # MAXIMUS Services (disabled)
            "MAXIMUS_ENABLE_CONSCIOUSNESS": "false",
            "MAXIMUS_ENABLE_PREDICTION": "false",
            "MAXIMUS_ENABLE_NEUROMODULATION": "false",

            # Features (limited)
            "MAX_CODE_ENABLE_CONSTITUTIONAL": "true",  # Local constitutional AI
            "MAX_CODE_ENABLE_MULTI_AGENT": "true",    # Direct Claude API
            "MAX_CODE_ENABLE_TOT": "true",            # Local ToT

            # UI (all enabled)
            "MAX_CODE_BANNER_STYLE": "default",
            "MAX_CODE_NO_BANNER": "false",
            "NO_COLOR": "false",
            "MAX_CODE_QUIET": "false",
            "MAX_CODE_VERBOSE": "false",
            "MAX_CODE_SHOW_PROGRESS": "true",
            "MAX_CODE_SHOW_AGENTS": "true",
            "MAX_CODE_SHOW_CONSCIOUSNESS": "false",  # No MAXIMUS backend

            # Logging
            "LOG_LEVEL": "INFO",
            "MAX_CODE_LOG_FORMAT": "text",
            "MAX_CODE_ENABLE_TRACING": "false",

            # Claude (requires API key from user)
            "CLAUDE_MODEL": "claude-sonnet-4-5-20250929",
            "CLAUDE_TEMPERATURE": "0.7",
            "CLAUDE_MAX_TOKENS": "4096",
        }
    ),
}


class ProfileManager:
    """Manages configuration profiles."""

    def __init__(self, config_dir: Optional[Path] = None):
        """
        Initialize profile manager.

        Args:
            config_dir: Configuration directory (default: ~/.max-code)
        """
        self.config_dir = config_dir or Path.home() / ".max-code"
        self.config_dir.mkdir(parents=True, exist_ok=True)
        self.profile_file = self.config_dir / "profile.json"
        self.env_file = self.config_dir / ".env"

    def get_current_profile(self) -> Profile:
        """
        Get currently active profile.

        Returns:
            Active profile (default: DEVELOPMENT)
        """
        if self.profile_file.exists():
            try:
                with open(self.profile_file, 'r') as f:
                    data = json.load(f)
                    return Profile(data.get('profile', Profile.DEVELOPMENT))
            except Exception:
                pass
        return Profile.DEVELOPMENT

    def set_profile(self, profile: Profile) -> None:
        """
        Set active profile.

        Args:
            profile: Profile to activate
        """
        # Save profile selection
        with open(self.profile_file, 'w') as f:
            json.dump({'profile': profile.value}, f, indent=2)

        # Write profile settings to .env
        self._write_env_file(profile)

    def _write_env_file(self, profile: Profile) -> None:
        """
        Write profile settings to .env file.

        Args:
            profile: Profile to write
        """
        config = PROFILES[profile]
        lines = [
            f"# Max-Code CLI Configuration",
            f"# Profile: {config.name}",
            f"# {config.description}",
            f"",
        ]

        for key, value in config.settings.items():
            lines.append(f"{key}={value}")

        lines.append("")
        lines.append("# Add your API keys below:")
        lines.append("# ANTHROPIC_API_KEY=your_key_here")
        lines.append("")

        with open(self.env_file, 'w') as f:
            f.write('\n'.join(lines))

    def list_profiles(self) -> Dict[Profile, ProfileConfig]:
        """
        List all available profiles.

        Returns:
            Dictionary of profiles
        """
        return PROFILES.copy()

    def get_profile_config(self, profile: Profile) -> ProfileConfig:
        """
        Get configuration for specific profile.

        Args:
            profile: Profile to get

        Returns:
            Profile configuration
        """
        return PROFILES[profile]

    def profile_exists(self) -> bool:
        """
        Check if profile configuration exists.

        Returns:
            True if profile configured
        """
        return self.profile_file.exists()

    def env_file_exists(self) -> bool:
        """
        Check if .env file exists.

        Returns:
            True if .env exists
        """
        return self.env_file.exists()

    def initialize_profile(self, profile: Profile = Profile.DEVELOPMENT) -> None:
        """
        Initialize configuration with given profile.

        Args:
            profile: Profile to initialize (default: DEVELOPMENT)
        """
        self.set_profile(profile)

    def get_env_file_path(self) -> Path:
        """
        Get path to .env file.

        Returns:
            Path to .env
        """
        return self.env_file


def init_profile_wizard() -> Profile:
    """
    Interactive profile selection wizard.

    Returns:
        Selected profile
    """
    from rich.console import Console
    from rich.prompt import Prompt
    from rich.table import Table

    console = Console()

    console.print("\n[bold cyan]Max-Code CLI - Profile Selection[/bold cyan]\n")

    # Show available profiles
    table = Table(show_header=True, header_style="bold cyan")
    table.add_column("Profile", style="cyan", width=15)
    table.add_column("Description", style="white", width=50)

    for profile, config in PROFILES.items():
        table.add_row(profile.value, config.description)

    console.print(table)
    console.print()

    # Prompt for selection
    choices = [p.value for p in Profile]
    choice = Prompt.ask(
        "Select profile",
        choices=choices,
        default=Profile.DEVELOPMENT.value
    )

    return Profile(choice)
