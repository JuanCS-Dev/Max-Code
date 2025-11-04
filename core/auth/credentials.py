"""
Credentials Management for Max-Code

Gerencia armazenamento seguro de tokens OAuth em ~/.max-code/.credentials.json
com permissões restritas (600 - apenas owner pode ler/escrever).

Baseado no sistema do Claude Code.
"""

import json
import os
from pathlib import Path
from typing import Optional, Dict
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta

from .config import AuthConfig


@dataclass
class Credentials:
    """
    Estrutura de credenciais OAuth

    Armazenadas em ~/.max-code/.credentials.json
    """
    access_token: str
    refresh_token: str
    expires_in: int  # Segundos até expiração
    token_type: str = "Bearer"
    created_at: Optional[str] = None  # ISO timestamp

    def __post_init__(self):
        """Inicializa created_at se não fornecido"""
        if self.created_at is None:
            self.created_at = datetime.utcnow().isoformat()

    def is_expired(self) -> bool:
        """
        Verifica se access token está expirado

        Considera margem de segurança de 5 minutos (300s)

        Returns:
            True se expirado ou perto de expirar
        """
        if not self.created_at:
            return True

        created = datetime.fromisoformat(self.created_at)
        expiration = created + timedelta(seconds=self.expires_in)

        # Margem de segurança: renovar 5 min antes
        expiration_with_margin = expiration - timedelta(
            seconds=AuthConfig.REFRESH_MARGIN_SECONDS
        )

        return datetime.utcnow() >= expiration_with_margin

    def time_until_expiration(self) -> Optional[timedelta]:
        """
        Calcula tempo até expiração

        Returns:
            timedelta ou None se não puder calcular
        """
        if not self.created_at:
            return None

        created = datetime.fromisoformat(self.created_at)
        expiration = created + timedelta(seconds=self.expires_in)
        return expiration - datetime.utcnow()

    def to_dict(self) -> Dict:
        """Converte para dicionário"""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict) -> 'Credentials':
        """Cria instância a partir de dicionário"""
        return cls(**data)


class CredentialsManager:
    """
    Gerenciador de credenciais OAuth

    Responsabilidades:
    - Salvar tokens em arquivo seguro (~/.max-code/.credentials.json)
    - Carregar tokens do arquivo
    - Verificar expiração
    - Deletar credenciais
    """

    def __init__(self, credentials_file: Optional[Path] = None):
        """
        Inicializa gerenciador

        Args:
            credentials_file: Caminho do arquivo (default: ~/.max-code/.credentials.json)
        """
        self.credentials_file = credentials_file or AuthConfig.CREDENTIALS_FILE
        self._ensure_config_dir()

    def _ensure_config_dir(self):
        """Garante que diretório de configuração existe com permissões corretas"""
        AuthConfig.ensure_config_dir()

    def save(self, credentials: Credentials) -> bool:
        """
        Salva credenciais em arquivo

        Args:
            credentials: Credenciais a salvar

        Returns:
            True se sucesso, False se erro
        """
        try:
            # Converter para JSON
            data = credentials.to_dict()

            # Escrever arquivo
            with open(self.credentials_file, 'w') as f:
                json.dump(data, f, indent=2)

            # Definir permissões: apenas owner pode ler/escrever (600)
            os.chmod(self.credentials_file, AuthConfig.CREDENTIALS_FILE_PERMISSIONS)

            return True

        except Exception as e:
            print(f"✗ Failed to save credentials: {e}")
            return False

    def load(self) -> Optional[Credentials]:
        """
        Carrega credenciais do arquivo

        Returns:
            Credentials ou None se não encontrado/inválido
        """
        if not self.credentials_file.exists():
            return None

        try:
            with open(self.credentials_file, 'r') as f:
                data = json.load(f)

            credentials = Credentials.from_dict(data)
            return credentials

        except Exception as e:
            print(f"⚠️  Failed to load credentials: {e}")
            return None

    def delete(self) -> bool:
        """
        Deleta arquivo de credenciais

        Returns:
            True se sucesso ou arquivo não existe
        """
        if not self.credentials_file.exists():
            return True

        try:
            self.credentials_file.unlink()
            return True

        except Exception as e:
            print(f"✗ Failed to delete credentials: {e}")
            return False

    def exists(self) -> bool:
        """
        Verifica se arquivo de credenciais existe

        Returns:
            True se existe
        """
        return self.credentials_file.exists()

    def get_access_token(self) -> Optional[str]:
        """
        Obtém access token (se válido)

        Returns:
            Access token ou None se não existe/expirado
        """
        credentials = self.load()
        if not credentials:
            return None

        if credentials.is_expired():
            return None

        return credentials.access_token

    def get_refresh_token(self) -> Optional[str]:
        """
        Obtém refresh token

        Returns:
            Refresh token ou None se não existe
        """
        credentials = self.load()
        if not credentials:
            return None

        return credentials.refresh_token

    def update_access_token(self, new_access_token: str, expires_in: int) -> bool:
        """
        Atualiza apenas access token (mantém refresh token)

        Usado após refresh de token

        Args:
            new_access_token: Novo access token
            expires_in: Tempo de expiração em segundos

        Returns:
            True se sucesso
        """
        credentials = self.load()
        if not credentials:
            print("✗ Cannot update token: no existing credentials")
            return False

        # Criar novas credenciais com access token atualizado
        updated_credentials = Credentials(
            access_token=new_access_token,
            refresh_token=credentials.refresh_token,
            expires_in=expires_in,
            token_type=credentials.token_type,
            created_at=datetime.utcnow().isoformat()  # Reset timestamp
        )

        return self.save(updated_credentials)

    def get_status(self) -> Dict:
        """
        Retorna status das credenciais

        Returns:
            Dict com informações de status
        """
        if not self.exists():
            return {
                'authenticated': False,
                'message': 'No credentials found'
            }

        credentials = self.load()
        if not credentials:
            return {
                'authenticated': False,
                'message': 'Invalid credentials file'
            }

        time_left = credentials.time_until_expiration()

        return {
            'authenticated': True,
            'access_token_expired': credentials.is_expired(),
            'time_until_expiration': str(time_left) if time_left else 'Unknown',
            'created_at': credentials.created_at,
            'credentials_file': str(self.credentials_file),
        }

    def print_status(self):
        """Imprime status das credenciais (formato amigável)"""
        status = self.get_status()

        print("\n" + "="*60)
        print("MAX-CODE AUTHENTICATION STATUS")
        print("="*60)

        if not status['authenticated']:
            print(f"❌ {status['message']}")
            print("\nRun 'max-code login' to authenticate")
        else:
            print("✅ Authenticated")
            print(f"\nCredentials file: {status['credentials_file']}")
            print(f"Created at: {status['created_at']}")

            if status['access_token_expired']:
                print("\n⚠️  Access token expired (will auto-refresh on next request)")
            else:
                print(f"\n✓ Access token valid")
                print(f"  Time until expiration: {status['time_until_expiration']}")

        print("="*60 + "\n")


# ==================== HELPER FUNCTIONS ====================

def save_credentials(access_token: str, refresh_token: str, expires_in: int) -> bool:
    """
    Helper function para salvar credenciais

    Args:
        access_token: Access token
        refresh_token: Refresh token
        expires_in: Tempo de expiração (segundos)

    Returns:
        True se sucesso
    """
    credentials = Credentials(
        access_token=access_token,
        refresh_token=refresh_token,
        expires_in=expires_in
    )

    manager = CredentialsManager()
    return manager.save(credentials)


def load_credentials() -> Optional[Credentials]:
    """
    Helper function para carregar credenciais

    Returns:
        Credentials ou None
    """
    manager = CredentialsManager()
    return manager.load()


def delete_credentials() -> bool:
    """
    Helper function para deletar credenciais

    Returns:
        True se sucesso
    """
    manager = CredentialsManager()
    return manager.delete()


def get_valid_access_token() -> Optional[str]:
    """
    Helper function para obter access token válido

    Returns:
        Access token ou None se não existe/expirado
    """
    manager = CredentialsManager()
    return manager.get_access_token()


def is_authenticated() -> bool:
    """
    Helper function para verificar se está autenticado

    Returns:
        True se credenciais válidas existem
    """
    manager = CredentialsManager()
    return manager.exists() and manager.load() is not None
