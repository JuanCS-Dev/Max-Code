"""
Max-Code Config Override - Compatibilidade Claude Code

Override de configuração para usar paths compatíveis com Claude Code oficial.

PAI usa:
- ~/.max-code/.credentials.json

FILHO (max-code-cli) deve usar:
- ~/.claude/.credentials.json

Para compatibilidade total com Claude Code oficial.

Biblical Foundation:
"Não vos conformeis com este século" (Romanos 12:2)
Adaptação inteligente mantendo compatibilidade.
"""

from pathlib import Path
import sys

# Import base config from PAI
from core.auth.config import AuthConfig as BaseAuthConfig


class MaxCodeAuthConfig(BaseAuthConfig):
    """
    Max-Code Auth Config - Override para compatibilidade Claude Code

    Herda tudo do PAI mas ajusta paths para ~/.claude/
    """

    # ==================== STORAGE OVERRIDE ====================

    # Diretório compatível com Claude Code oficial
    CONFIG_DIR = Path.home() / ".claude"

    # Arquivo de credenciais (mesmo formato que Claude Code)
    CREDENTIALS_FILE = CONFIG_DIR / ".credentials.json"

    # Permissões do arquivo (apenas owner pode ler/escrever)
    CREDENTIALS_FILE_PERMISSIONS = 0o600


# Alias para facilitar imports
AuthConfig = MaxCodeAuthConfig


# ==================== HELPER FUNCTIONS ====================

def get_credentials_file_path() -> Path:
    """Retorna caminho do arquivo de credenciais (override)"""
    return MaxCodeAuthConfig.CREDENTIALS_FILE


def get_config_dir() -> Path:
    """Retorna diretório de configuração (override)"""
    return MaxCodeAuthConfig.CONFIG_DIR


def ensure_config_dir():
    """Garante que diretório ~/.claude/ existe com permissões corretas"""
    MaxCodeAuthConfig.CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    # Definir permissões: apenas owner pode acessar
    MaxCodeAuthConfig.CONFIG_DIR.chmod(0o700)


# ==================== VALIDATION ====================

if __name__ == "__main__":
    print("=== Max-Code Auth Config Override ===\n")
    print(f"CONFIG_DIR: {MaxCodeAuthConfig.CONFIG_DIR}")
    print(f"CREDENTIALS_FILE: {MaxCodeAuthConfig.CREDENTIALS_FILE}")
    print(f"REDIRECT_URI: {MaxCodeAuthConfig.REDIRECT_URI}")
    print(f"CLIENT_ID: {MaxCodeAuthConfig.CLIENT_ID}")
    print(f"CALLBACK_PORT: {MaxCodeAuthConfig.CALLBACK_SERVER_PORT}")
    print("\n✅ Config override loaded successfully")
    print("   Compatible with Claude Code official paths")
