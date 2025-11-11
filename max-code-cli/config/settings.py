"""
Max-Code CLI Settings

Type-safe configuration using Pydantic with environment variable support.
Validates configuration on startup and provides sensible defaults.
"""

import os
from pathlib import Path
from typing import Optional, Literal
from pydantic_settings import BaseSettings
from pydantic import Field, validator
from functools import lru_cache


class MaximusServiceConfig(BaseSettings):
    """MAXIMUS backend services configuration."""

    # MAXIMUS Core Service (consciousness, predictive coding, neuromodulation)
    core_url: str = Field(
        default="http://localhost:8100",  # FIXED: Was 8153, actual backend is 8100
        env="MAXIMUS_CORE_URL",
        description="MAXIMUS Core Service URL"
    )

    # Penelope Service (NLP, healing, 7 Biblical Articles)
    penelope_url: str = Field(
        default="http://localhost:8154",  # FIXED: Was 8150, actual backend is 8154
        env="MAXIMUS_PENELOPE_URL",
        description="Penelope NLP Service URL"
    )

    # NIS Service (Narrative Intelligence System)
    nis_url: str = Field(
        default="http://localhost:8152",
        env="MAXIMUS_NIS_URL",
        description="NIS Narrative Intelligence Service URL"
    )

    # MABA Service (Multi-Agent Browser Assistant)
    maba_url: str = Field(
        default="http://localhost:8151",
        env="MAXIMUS_MABA_URL",
        description="MABA Browser Assistant Service URL"
    )

    # Orchestrator Service (workflow coordination)
    orchestrator_url: str = Field(
        default="http://localhost:8027",
        env="MAXIMUS_ORCHESTRATOR_URL",
        description="Orchestrator Service URL"
    )

    # Oraculo Service (prediction, forecasting)
    oraculo_url: str = Field(
        default="http://localhost:8026",
        env="MAXIMUS_ORACULO_URL",
        description="Oraculo Prediction Service URL"
    )

    # Atlas Service (context, environment)
    atlas_url: str = Field(
        default="http://localhost:8007",
        env="MAXIMUS_ATLAS_URL",
        description="Atlas Context Service URL"
    )

    # Service timeouts
    timeout_seconds: int = Field(
        default=30,
        env="MAXIMUS_TIMEOUT",
        description="Request timeout in seconds"
    )

    # Retry configuration
    max_retries: int = Field(
        default=3,
        env="MAXIMUS_MAX_RETRIES",
        description="Maximum retry attempts"
    )

    # Enable/disable services
    enable_consciousness: bool = Field(
        default=True,
        env="MAXIMUS_ENABLE_CONSCIOUSNESS",
        description="Enable ESGT consciousness integration"
    )

    enable_prediction: bool = Field(
        default=True,
        env="MAXIMUS_ENABLE_PREDICTION",
        description="Enable predictive coding"
    )

    enable_neuromodulation: bool = Field(
        default=True,
        env="MAXIMUS_ENABLE_NEUROMODULATION",
        description="Enable neuromodulation system"
    )

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"  # Allow other env vars in .env
        extra = "ignore"  # Allow ANTHROPIC_API_KEY in .env without error


class ClaudeConfig(BaseSettings):
    """
    Claude API configuration.

    Uses ANTHROPIC_API_KEY for authentication.
    """

    api_key: Optional[str] = Field(
        default=None,
        env="ANTHROPIC_API_KEY",
        description="Anthropic API key for Claude"
    )

    model: str = Field(
        default="claude-3-5-haiku-20241022",  # Haiku 4.5 - Cost-effective for tests
        env="CLAUDE_MODEL",
        description="Claude model to use"
    )

    temperature: float = Field(
        default=0.7,
        env="CLAUDE_TEMPERATURE",
        description="Sampling temperature (0-1)"
    )

    max_tokens: int = Field(
        default=4096,
        env="CLAUDE_MAX_TOKENS",
        description="Maximum tokens per response"
    )

    @validator('temperature')
    def validate_temperature(cls, v):
        if not 0 <= v <= 1:
            raise ValueError("Temperature must be between 0 and 1")
        return v

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"  # Allow other env vars in .env


class GeminiConfig(BaseSettings):
    """
    Google Gemini API configuration for P.P.B.P.R research.

    Uses GEMINI_API_KEY for authentication.
    """

    api_key: Optional[str] = Field(
        default=None,
        env="GEMINI_API_KEY",
        description="Google Gemini API key"
    )

    model: str = Field(
        default="gemini-2.5-flash",  # Cost-effective and latest
        env="GEMINI_MODEL",
        description="Gemini model (2.5-flash/2.5-pro/2.0-flash)"
    )

    model_pro: str = Field(
        default="gemini-2.5-pro",  # For deep research
        env="GEMINI_MODEL_PRO",
        description="Gemini Pro model for comprehensive research"
    )

    enable_grounding: bool = Field(
        default=True,
        env="GEMINI_ENABLE_GROUNDING",
        description="Enable Google Search grounding"
    )

    temperature: float = Field(
        default=0.7,
        env="GEMINI_TEMPERATURE",
        description="Sampling temperature (0-1)"
    )

    max_tokens: int = Field(
        default=10_000,
        env="GEMINI_MAX_TOKENS",
        description="Maximum tokens per response"
    )

    @validator('temperature')
    def validate_temperature(cls, v):
        if not 0 <= v <= 1:
            raise ValueError("Temperature must be between 0 and 1")
        return v

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"


class PPBPRConfig(BaseSettings):
    """
    P.P.B.P.R Methodology configuration.

    Prompt → Paper → Blueprint → Plan → Refine
    """

    # Quality gates
    enable_quality_gates: bool = Field(
        default=True,
        env="PPBPR_ENABLE_QUALITY_GATES",
        description="Enable quality validation at each step (QG1-QG5)"
    )

    enable_constitutional_validation: bool = Field(
        default=True,
        env="PPBPR_ENABLE_CONSTITUTIONAL",
        description="Enable Constitutional AI validation (P1-P6)"
    )

    # Retry configuration
    retry_on_failure: bool = Field(
        default=True,
        env="PPBPR_RETRY_ON_FAILURE",
        description="Retry failed steps"
    )

    max_retries: int = Field(
        default=2,
        env="PPBPR_MAX_RETRIES",
        description="Maximum retry attempts per step"
    )

    # Research configuration
    research_depth: Literal['basic', 'moderate', 'comprehensive'] = Field(
        default='comprehensive',
        env="PPBPR_RESEARCH_DEPTH",
        description="Research depth level"
    )

    # Output configuration
    output_format: Literal['markdown', 'json', 'html'] = Field(
        default='markdown',
        env="PPBPR_OUTPUT_FORMAT",
        description="Deliverable output format"
    )

    output_dir: Path = Field(
        default_factory=lambda: Path("./outputs/ppbpr"),
        env="PPBPR_OUTPUT_DIR",
        description="Output directory for deliverables"
    )

    # Quality thresholds
    min_research_words: int = Field(
        default=500,
        env="PPBPR_MIN_RESEARCH_WORDS",
        description="Minimum words for research quality gate"
    )

    min_research_sources: int = Field(
        default=3,
        env="PPBPR_MIN_RESEARCH_SOURCES",
        description="Minimum sources for research quality gate"
    )

    min_quality_score: float = Field(
        default=0.5,
        env="PPBPR_MIN_QUALITY_SCORE",
        description="Minimum overall quality score (0-1)"
    )

    @validator('output_dir')
    def create_output_dir(cls, v):
        """Ensure output directory exists."""
        v.mkdir(parents=True, exist_ok=True)
        return v

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"


class UIConfig(BaseSettings):
    """UI/UX configuration."""

    banner_style: Literal['default', 'isometric', 'banner', 'bold', 'tech', 'cyber'] = Field(
        default='default',
        env="MAX_CODE_BANNER_STYLE",
        description="Banner ASCII art style"
    )

    no_banner: bool = Field(
        default=False,
        env="MAX_CODE_NO_BANNER",
        description="Disable banner display"
    )

    no_color: bool = Field(
        default=False,
        env="NO_COLOR",
        description="Disable colored output"
    )

    quiet: bool = Field(
        default=False,
        env="MAX_CODE_QUIET",
        description="Minimal output mode"
    )

    verbose: bool = Field(
        default=False,
        env="MAX_CODE_VERBOSE",
        description="Detailed output mode"
    )

    # Progress indicators
    show_progress: bool = Field(
        default=True,
        env="MAX_CODE_SHOW_PROGRESS",
        description="Show progress indicators"
    )

    # Sabbath mode (runtime state, not persisted)
    sabbath_mode: bool = Field(
        default=False,
        description="Sabbath mode active (runtime state)"
    )

    # Agent display
    show_agent_activity: bool = Field(
        default=True,
        env="MAX_CODE_SHOW_AGENTS",
        description="Show agent activity dashboard"
    )

    # Consciousness visualization
    show_consciousness: bool = Field(
        default=True,
        env="MAX_CODE_SHOW_CONSCIOUSNESS",
        description="Show consciousness state (ESGT ignitions)"
    )

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"  # Allow other env vars in .env


class LoggingConfig(BaseSettings):
    """Logging configuration."""

    log_level: Literal['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'] = Field(
        default='INFO',
        env="LOG_LEVEL",
        description="Logging level"
    )

    log_file: Optional[Path] = Field(
        default=None,
        env="MAX_CODE_LOG_FILE",
        description="Log file path (None = stdout only)"
    )

    log_format: Literal['text', 'json'] = Field(
        default='text',
        env="MAX_CODE_LOG_FORMAT",
        description="Log format (text or JSON)"
    )

    enable_tracing: bool = Field(
        default=False,
        env="MAX_CODE_ENABLE_TRACING",
        description="Enable OpenTelemetry tracing"
    )

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"  # Allow other env vars in .env


class Settings(BaseSettings):
    """
    Max-Code CLI Settings (Root Configuration)

    Aggregates all configuration sections with type safety and validation.
    Loads from environment variables and .env file.
    """

    # Application metadata
    app_name: str = "Max-Code CLI"
    version: str = "1.0.0"
    environment: Literal['development', 'production', 'local'] = Field(
        default='development',
        env="MAX_CODE_ENV",
        description="Runtime environment"
    )

    # Configuration sections
    maximus: MaximusServiceConfig = Field(default_factory=MaximusServiceConfig)
    claude: ClaudeConfig = Field(default_factory=ClaudeConfig)
    gemini: GeminiConfig = Field(default_factory=GeminiConfig)
    ppbpr: PPBPRConfig = Field(default_factory=PPBPRConfig)
    ui: UIConfig = Field(default_factory=UIConfig)
    logging: LoggingConfig = Field(default_factory=LoggingConfig)

    # Project paths
    project_root: Path = Field(
        default_factory=lambda: Path(__file__).parent.parent,
        description="Project root directory"
    )

    config_dir: Path = Field(
        default_factory=lambda: Path.home() / ".max-code",
        env="MAX_CODE_CONFIG_DIR",
        description="User configuration directory"
    )

    # Feature flags
    enable_constitutional_ai: bool = Field(
        default=True,
        env="MAX_CODE_ENABLE_CONSTITUTIONAL",
        description="Enable Constitutional AI v3.0 framework"
    )

    enable_multi_agent: bool = Field(
        default=True,
        env="MAX_CODE_ENABLE_MULTI_AGENT",
        description="Enable multi-agent system"
    )

    enable_tree_of_thoughts: bool = Field(
        default=True,
        env="MAX_CODE_ENABLE_TOT",
        description="Enable Tree of Thoughts visualization"
    )

    # Truth Engine + Vital System (Always-On by default)
    enable_truth_audit: bool = Field(
        default=True,
        env="MAX_CODE_ENABLE_AUDIT",
        description="Enable Truth Engine + Vital System verification (always-on)"
    )

    audit_plan_level: bool = Field(
        default=True,
        env="MAX_CODE_AUDIT_PLAN_LEVEL",
        description="Audit at plan level (final outcome) vs per-task"
    )

    @validator('config_dir')
    def create_config_dir(cls, v):
        """Ensure config directory exists."""
        v.mkdir(parents=True, exist_ok=True)
        return v

    def validate_configuration(self) -> tuple[bool, list[str]]:
        """
        Validate complete configuration.

        Returns:
            (is_valid, errors): Tuple of validation status and error list
        """
        errors = []
        warnings = []

        # Check Claude API key if multi-agent enabled
        if self.enable_multi_agent and not self.claude.api_key:
            errors.append("Claude API key required for multi-agent system (set ANTHROPIC_API_KEY)")

        # Check Gemini API key (warning, not error - P.P.B.P.R is optional)
        if not self.gemini.api_key:
            warnings.append("Gemini API key not set - P.P.B.P.R research will be unavailable (set GEMINI_API_KEY)")

        # Check MAXIMUS services accessibility (could add health checks here)
        # For now, just validate URLs are set
        if not self.maximus.core_url:
            errors.append("MAXIMUS Core URL not configured")

        if not self.maximus.penelope_url:
            errors.append("Penelope URL not configured")

        if not self.maximus.nis_url:
            errors.append("NIS URL not configured")

        if not self.maximus.maba_url:
            errors.append("MABA URL not configured")

        # Log warnings if any
        if warnings:
            from config.logging_config import get_logger
            logger = get_logger(__name__)
            for warning in warnings:
                logger.warning(f"⚠️  {warning}")

        return (len(errors) == 0, errors)

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"  # Allow other env vars in .env
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    """
    Get singleton Settings instance.

    Uses LRU cache to ensure single instance across application.
    Loads from environment variables and .env file.

    Returns:
        Settings instance
    """
    return Settings()


def load_settings_from_file(file_path: Path) -> Settings:
    """
    Load settings from specific file.

    Args:
        file_path: Path to .env file

    Returns:
        Settings instance
    """
    return Settings(_env_file=file_path)


# Export for convenience
settings = get_settings()
