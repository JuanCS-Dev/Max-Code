"""
Token Manager with Auto-Refresh

Gerencia renovação automática de tokens OAuth em background thread.
Garante que access token esteja sempre válido sem interrupção do usuário.

Triggers de refresh:
1. Token expirado (checked a cada requisição)
2. HTTP 401 Unauthorized recebido
3. Periodic check (a cada 5 minutos)
"""

import threading
import time
from typing import Optional, Callable
from datetime import datetime, timedelta

from .config import AuthConfig
from .credentials import CredentialsManager, Credentials
from .oauth import OAuthFlow


class TokenManager:
    """
    Gerenciador de tokens com auto-refresh

    Features:
    - Auto-refresh de access token quando próximo de expirar
    - Background thread para periodic checks
    - Thread-safe (usa locks)
    - Callbacks para notificação de eventos
    """

    def __init__(
        self,
        credentials_manager: Optional[CredentialsManager] = None,
        on_refresh: Optional[Callable[[str], None]] = None,
        on_refresh_failed: Optional[Callable[[str], None]] = None
    ):
        """
        Inicializa TokenManager

        Args:
            credentials_manager: Manager de credenciais (default: cria novo)
            on_refresh: Callback chamado quando token é renovado (recebe novo access_token)
            on_refresh_failed: Callback chamado quando refresh falha (recebe error message)
        """
        self.credentials_manager = credentials_manager or CredentialsManager()
        self.oauth_flow = OAuthFlow()

        # Callbacks
        self.on_refresh = on_refresh
        self.on_refresh_failed = on_refresh_failed

        # Thread management
        self._refresh_thread: Optional[threading.Thread] = None
        self._stop_event = threading.Event()
        self._lock = threading.Lock()

        # Stats
        self.refresh_count = 0
        self.last_refresh: Optional[datetime] = None

    def start_auto_refresh(self, check_interval_seconds: int = 300):
        """
        Inicia background thread para auto-refresh

        Args:
            check_interval_seconds: Intervalo entre checks (default: 5 min)
        """
        if self._refresh_thread and self._refresh_thread.is_alive():
            return  # Já está rodando

        self._stop_event.clear()

        self._refresh_thread = threading.Thread(
            target=self._auto_refresh_loop,
            args=(check_interval_seconds,),
            daemon=True,
            name="TokenRefreshThread"
        )
        self._refresh_thread.start()

    def stop_auto_refresh(self):
        """Para background thread de auto-refresh"""
        if not self._refresh_thread or not self._refresh_thread.is_alive():
            return

        self._stop_event.set()
        self._refresh_thread.join(timeout=5)

    def _auto_refresh_loop(self, check_interval_seconds: int):
        """
        Loop de auto-refresh (roda em background thread)

        Args:
            check_interval_seconds: Intervalo entre checks
        """
        while not self._stop_event.is_set():
            try:
                # Verificar se token precisa refresh
                credentials = self.credentials_manager.load()

                if credentials and credentials.is_expired():
                    # Token expirado/próximo de expirar - refresh
                    print(AuthConfig.TOKEN_REFRESH_MESSAGE)
                    self.refresh_token_sync()

            except Exception as e:
                # Não quebrar thread em caso de erro
                if self.on_refresh_failed:
                    self.on_refresh_failed(str(e))

            # Sleep até próximo check (ou até stop_event ser setado)
            self._stop_event.wait(timeout=check_interval_seconds)

    def refresh_token_sync(self) -> bool:
        """
        Refresh síncrono de token (thread-safe)

        Returns:
            True se refresh bem-sucedido
        """
        with self._lock:
            return self._do_refresh()

    def _do_refresh(self) -> bool:
        """
        Executa refresh de token (sem lock - chamado por refresh_token_sync)

        Returns:
            True se sucesso
        """
        # Carregar credenciais atuais
        credentials = self.credentials_manager.load()

        if not credentials:
            if self.on_refresh_failed:
                self.on_refresh_failed("No credentials found")
            return False

        # Tentar refresh
        new_tokens = self.oauth_flow.refresh_access_token(credentials.refresh_token)

        if not new_tokens:
            if self.on_refresh_failed:
                self.on_refresh_failed("Token refresh failed")
            return False

        # Atualizar credenciais
        success = self.credentials_manager.update_access_token(
            new_access_token=new_tokens['access_token'],
            expires_in=new_tokens['expires_in']
        )

        if success:
            # Stats
            self.refresh_count += 1
            self.last_refresh = datetime.utcnow()

            # Callback
            if self.on_refresh:
                self.on_refresh(new_tokens['access_token'])

        return success

    def get_valid_token(self) -> Optional[str]:
        """
        Obtém access token válido (refresha se necessário)

        Returns:
            Access token válido ou None se não autenticado
        """
        credentials = self.credentials_manager.load()

        if not credentials:
            return None

        # Se expirado, tentar refresh
        if credentials.is_expired():
            success = self.refresh_token_sync()
            if not success:
                return None

            # Recarregar credenciais após refresh
            credentials = self.credentials_manager.load()

        return credentials.access_token if credentials else None

    def force_refresh(self) -> bool:
        """
        Força refresh imediato do token

        Returns:
            True se sucesso
        """
        return self.refresh_token_sync()

    def get_stats(self) -> dict:
        """
        Retorna estatísticas do token manager

        Returns:
            Dict com stats
        """
        return {
            'refresh_count': self.refresh_count,
            'last_refresh': self.last_refresh.isoformat() if self.last_refresh else None,
            'auto_refresh_active': self._refresh_thread and self._refresh_thread.is_alive(),
        }


# ==================== SINGLETON INSTANCE ====================

# Instância global para uso em toda a aplicação
_token_manager_instance: Optional[TokenManager] = None


def get_token_manager() -> TokenManager:
    """
    Obtém instância singleton do TokenManager

    Returns:
        TokenManager instance
    """
    global _token_manager_instance

    if _token_manager_instance is None:
        _token_manager_instance = TokenManager()
        # Iniciar auto-refresh por padrão
        _token_manager_instance.start_auto_refresh()

    return _token_manager_instance


def get_valid_token() -> Optional[str]:
    """
    Helper function para obter token válido

    Auto-refresh se necessário

    Returns:
        Access token válido ou None
    """
    manager = get_token_manager()
    return manager.get_valid_token()


def force_token_refresh() -> bool:
    """
    Helper function para forçar refresh de token

    Returns:
        True se sucesso
    """
    manager = get_token_manager()
    return manager.force_refresh()
