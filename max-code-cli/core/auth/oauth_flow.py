"""
Browser-based OAuth 2.0 flow com PKCE para Claude API.
Implementa o mesmo flow que claude-code CLI usa.
"""

import secrets
import hashlib
import base64
import webbrowser
import time
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlencode, parse_qs
from typing import Optional, Dict
from pathlib import Path
import json


class OAuthCallbackHandler(BaseHTTPRequestHandler):
    """Handler para capturar callback do OAuth"""

    authorization_code: Optional[str] = None

    def do_GET(self):
        """Processar GET request do callback"""
        # Parse query params
        query = parse_qs(self.path.split('?')[1] if '?' in self.path else '')

        if 'code' in query:
            OAuthCallbackHandler.authorization_code = query['code'][0]

            # Responder com página de sucesso
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            success_html = """
            <!DOCTYPE html>
            <html>
            <head>
                <title>MAX-CODE Authentication</title>
                <style>
                    body {
                        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
                        display: flex;
                        justify-content: center;
                        align-items: center;
                        height: 100vh;
                        margin: 0;
                        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    }
                    .container {
                        background: white;
                        padding: 3rem;
                        border-radius: 1rem;
                        box-shadow: 0 20px 60px rgba(0,0,0,0.3);
                        text-align: center;
                        max-width: 500px;
                    }
                    h1 { color: #667eea; margin-bottom: 1rem; }
                    p { color: #666; line-height: 1.6; }
                    .checkmark { font-size: 4rem; color: #10b981; }
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="checkmark">✓</div>
                    <h1>Authentication Successful!</h1>
                    <p>You can close this window and return to your terminal.</p>
                    <p style="font-size: 0.9rem; color: #999; margin-top: 2rem;">
                        MAX-CODE CLI is now connected to your Claude account.
                    </p>
                </div>
            </body>
            </html>
            """
            self.wfile.write(success_html.encode())
        else:
            # Error
            self.send_response(400)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            error_html = """
            <!DOCTYPE html>
            <html>
            <head><title>MAX-CODE Authentication Error</title></head>
            <body style="font-family: sans-serif; text-align: center; padding-top: 50px;">
                <h1 style="color: #ef4444;">Error: No authorization code received</h1>
                <p>Please close this window and try again in your terminal.</p>
            </body>
            </html>
            """
            self.wfile.write(error_html.encode())

    def log_message(self, format, *args):
        """Suprimir logs do servidor HTTP"""
        pass


class OAuthFlow:
    """
    Gerencia OAuth 2.0 flow via browser.
    Implementa PKCE para segurança adicional.
    """

    # NOTE: Estes endpoints são placeholders. Os endpoints reais do Anthropic
    # precisam ser verificados na documentação oficial.
    AUTHORIZE_URL = "https://console.anthropic.com/api/auth/authorize"
    TOKEN_URL = "https://api.anthropic.com/v1/oauth/token"
    CLIENT_ID = "max-code-cli"
    REDIRECT_URI = "http://localhost:8765/callback"
    SCOPES = ["user", "api"]

    def __init__(self):
        self.code_verifier: Optional[str] = None
        self.code_challenge: Optional[str] = None

    def _generate_pkce_pair(self) -> tuple[str, str]:
        """
        Gerar par PKCE (code_verifier, code_challenge).

        PKCE (Proof Key for Code Exchange) previne ataques de interceptação.
        """
        # Gerar code_verifier (43-128 caracteres)
        code_verifier = base64.urlsafe_b64encode(
            secrets.token_bytes(32)
        ).decode('utf-8').rstrip('=')

        # Gerar code_challenge (SHA256 do verifier)
        challenge_bytes = hashlib.sha256(code_verifier.encode('utf-8')).digest()
        code_challenge = base64.urlsafe_b64encode(challenge_bytes).decode('utf-8').rstrip('=')

        return code_verifier, code_challenge

    def initiate_flow(self) -> bool:
        """
        Iniciar OAuth flow via browser.

        Returns:
            True se autenticação bem-sucedida, False caso contrário
        """
        # Gerar PKCE
        self.code_verifier, self.code_challenge = self._generate_pkce_pair()

        # Construir authorization URL
        params = {
            'response_type': 'code',
            'client_id': self.CLIENT_ID,
            'redirect_uri': self.REDIRECT_URI,
            'scope': ' '.join(self.SCOPES),
            'code_challenge': self.code_challenge,
            'code_challenge_method': 'S256',
        }
        auth_url = f"{self.AUTHORIZE_URL}?{urlencode(params)}"

        # Iniciar servidor callback
        server = HTTPServer(('localhost', 8765), OAuthCallbackHandler)

        # Abrir browser
        print("\n🔐 Opening browser for authentication...")
        print(f"📍 If browser doesn't open, visit: {auth_url}\n")
        webbrowser.open(auth_url)

        # Aguardar callback (timeout 2 minutos)
        print("⏳ Waiting for authentication...")
        server.timeout = 120
        server.handle_request()

        # Verificar se recebeu código
        if not OAuthCallbackHandler.authorization_code:
            print("❌ Authentication failed: No authorization code received")
            return False

        # Trocar code por token
        token_data = self._exchange_code_for_token(
            OAuthCallbackHandler.authorization_code
        )

        if not token_data:
            print("❌ Authentication failed: Could not exchange code for token")
            return False

        # Salvar token
        self._save_token(token_data)

        print("✅ Authentication successful!")
        return True

    def _exchange_code_for_token(self, code: str) -> Optional[Dict]:
        """
        Trocar authorization code por access token.

        Args:
            code: Authorization code do callback

        Returns:
            Dict com token data ou None se falhou
        """
        try:
            import httpx
        except ImportError:
            print("⚠️  Warning: httpx not installed. Install with: pip install httpx")
            return None

        payload = {
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': self.REDIRECT_URI,
            'client_id': self.CLIENT_ID,
            'code_verifier': self.code_verifier,
        }

        try:
            response = httpx.post(
                self.TOKEN_URL,
                data=payload,
                timeout=30.0
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error exchanging code: {e}")
            return None

    def _save_token(self, token_data: Dict) -> None:
        """
        Salvar token no formato compatível com claude-code.

        Args:
            token_data: Dict com access_token, refresh_token, etc.
        """
        credentials_dir = Path.home() / '.claude'
        credentials_dir.mkdir(exist_ok=True)

        credentials_file = credentials_dir / '.credentials.json'

        # Calcular expires_at (timestamp UNIX)
        expires_in = token_data.get('expires_in', 3600)  # Default 1 hora
        expires_at = int(time.time()) + expires_in

        # Formato compatível com claude-code
        credentials = {
            'token': token_data.get('access_token'),
            'refresh_token': token_data.get('refresh_token'),
            'expires_at': expires_at,
            'token_type': 'Bearer',
        }

        with open(credentials_file, 'w') as f:
            json.dump(credentials, f, indent=2)

        print(f"💾 Token saved to {credentials_file}")

        # Também salvar em .env para compatibilidade com outras ferramentas
        env_file = Path.cwd() / '.env'
        try:
            # Ler .env existente se houver
            existing_lines = []
            if env_file.exists():
                with open(env_file, 'r') as f:
                    existing_lines = [line for line in f.readlines()
                                     if not line.startswith('CLAUDE_CODE_OAUTH_TOKEN=')]

            # Adicionar novo token
            with open(env_file, 'w') as f:
                f.writelines(existing_lines)
                f.write(f"\nCLAUDE_CODE_OAUTH_TOKEN={credentials['token']}\n")

            print(f"💾 Token also saved to {env_file}")
        except Exception as e:
            print(f"⚠️  Warning: Could not update .env file: {e}")
