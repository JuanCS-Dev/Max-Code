"""
OAuth 2.0 + PKCE Flow Implementation

Implementa o fluxo completo de autenticação OAuth com PKCE (Proof Key for Code Exchange)
para Max-Code CLI, replicando o sistema usado pelo Claude Code.

Flow:
1. Gerar PKCE code_verifier + code_challenge
2. Abrir browser em authorization URL
3. User faz login em Claude.ai
4. Browser redireciona para localhost callback
5. Interceptar código de autorização
6. Trocar código por access_token + refresh_token
7. Armazenar tokens de forma segura
"""

import base64
import hashlib
import secrets
import urllib.parse
import webbrowser
from http.server import HTTPServer, BaseHTTPRequestHandler
from typing import Optional, Dict, Tuple
from dataclasses import dataclass
import requests
import threading

from .config import AuthConfig


# ==================== PKCE GENERATOR ====================

class PKCEGenerator:
    """Gera code_verifier e code_challenge para PKCE"""

    @staticmethod
    def generate_code_verifier() -> str:
        """
        Gera code_verifier aleatório

        Spec: 43-128 caracteres usando [A-Z a-z 0-9 - . _ ~]

        Returns:
            Code verifier (64 caracteres)
        """
        verifier_bytes = secrets.token_bytes(AuthConfig.PKCE_VERIFIER_LENGTH)
        code_verifier = base64.urlsafe_b64encode(verifier_bytes).decode('utf-8')
        # Remove padding '='
        return code_verifier.rstrip('=')

    @staticmethod
    def generate_code_challenge(code_verifier: str) -> str:
        """
        Gera code_challenge a partir do code_verifier

        Method: S256 (SHA256)
        Formula: BASE64URL(SHA256(code_verifier))

        Args:
            code_verifier: Code verifier gerado

        Returns:
            Code challenge (SHA256 hash, base64url encoded)
        """
        # SHA256 hash
        digest = hashlib.sha256(code_verifier.encode('utf-8')).digest()
        # Base64 URL-safe encode
        challenge = base64.urlsafe_b64encode(digest).decode('utf-8')
        # Remove padding '='
        return challenge.rstrip('=')

    @staticmethod
    def generate_pkce_pair() -> Tuple[str, str]:
        """
        Gera par (code_verifier, code_challenge)

        Returns:
            Tuple (code_verifier, code_challenge)
        """
        verifier = PKCEGenerator.generate_code_verifier()
        challenge = PKCEGenerator.generate_code_challenge(verifier)
        return verifier, challenge


# ==================== OAUTH CALLBACK HANDLER ====================

@dataclass
class OAuthCallbackResult:
    """Resultado do callback OAuth"""
    success: bool
    authorization_code: Optional[str] = None
    state: Optional[str] = None
    error: Optional[str] = None
    error_description: Optional[str] = None


class OAuthCallbackHandler(BaseHTTPRequestHandler):
    """
    Handler HTTP para callback OAuth

    Intercepta redirect do browser após login
    """

    # Variável compartilhada entre threads para armazenar resultado
    callback_result: Optional[OAuthCallbackResult] = None

    def do_GET(self):
        """Handle GET request do redirect OAuth"""
        # Parse query parameters
        parsed_path = urllib.parse.urlparse(self.path)
        params = urllib.parse.parse_qs(parsed_path.query)

        # Verificar se há erro
        if 'error' in params:
            OAuthCallbackHandler.callback_result = OAuthCallbackResult(
                success=False,
                error=params['error'][0],
                error_description=params.get('error_description', ['Unknown error'])[0]
            )
            self._send_error_response()
            return

        # Extrair authorization code e state
        code = params.get('code', [None])[0]
        state = params.get('state', [None])[0]

        if not code:
            OAuthCallbackHandler.callback_result = OAuthCallbackResult(
                success=False,
                error='missing_code',
                error_description='No authorization code received'
            )
            self._send_error_response()
            return

        # Sucesso!
        OAuthCallbackHandler.callback_result = OAuthCallbackResult(
            success=True,
            authorization_code=code,
            state=state
        )
        self._send_success_response()

    def _send_success_response(self):
        """Envia resposta de sucesso ao browser"""
        html = """
<!DOCTYPE html>
<html>
<head>
    <title>Max-Code Authentication Successful</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
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
        h1 {
            color: #667eea;
            margin-bottom: 1rem;
        }
        .checkmark {
            font-size: 4rem;
            color: #10b981;
            margin-bottom: 1rem;
        }
        p {
            color: #6b7280;
            line-height: 1.6;
        }
        .code {
            background: #f3f4f6;
            padding: 0.5rem 1rem;
            border-radius: 0.5rem;
            font-family: monospace;
            margin-top: 1rem;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="checkmark">✓</div>
        <h1>Authentication Successful!</h1>
        <p>You have successfully authenticated with Claude.ai</p>
        <p>You can now close this window and return to your terminal.</p>
        <div class="code">max-code CLI is ready to use 🚀</div>
    </div>
</body>
</html>
"""
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(html.encode())

    def _send_error_response(self):
        """Envia resposta de erro ao browser"""
        error = OAuthCallbackHandler.callback_result.error or 'unknown_error'
        error_desc = OAuthCallbackHandler.callback_result.error_description or 'An unknown error occurred'

        html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Max-Code Authentication Failed</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        }}
        .container {{
            background: white;
            padding: 3rem;
            border-radius: 1rem;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            text-align: center;
            max-width: 500px;
        }}
        h1 {{
            color: #ef4444;
            margin-bottom: 1rem;
        }}
        .error-icon {{
            font-size: 4rem;
            color: #ef4444;
            margin-bottom: 1rem;
        }}
        p {{
            color: #6b7280;
            line-height: 1.6;
        }}
        .error-details {{
            background: #fef2f2;
            padding: 1rem;
            border-radius: 0.5rem;
            border-left: 4px solid #ef4444;
            margin-top: 1rem;
            text-align: left;
        }}
        .error-code {{
            font-family: monospace;
            color: #991b1b;
            font-weight: bold;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="error-icon">✗</div>
        <h1>Authentication Failed</h1>
        <p>We encountered an error during authentication.</p>
        <div class="error-details">
            <div class="error-code">{error}</div>
            <div>{error_desc}</div>
        </div>
        <p style="margin-top: 1.5rem;">Please try again or check the terminal for more details.</p>
    </div>
</body>
</html>
"""
        self.send_response(400)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(html.encode())

    def log_message(self, format, *args):
        """Suprimir logs HTTP (menos verboso)"""
        pass


# ==================== OAUTH FLOW ====================

class OAuthFlow:
    """
    Fluxo completo OAuth 2.0 + PKCE

    Implementa:
    1. Authorization request (abre browser)
    2. Callback handling (servidor local)
    3. Token exchange (código → tokens)
    4. Token refresh (renovação automática)
    """

    def __init__(self):
        self.config = AuthConfig()

    def start_authorization_flow(self) -> Optional[Dict[str, str]]:
        """
        Inicia fluxo de autorização OAuth completo

        Returns:
            Dict com access_token, refresh_token, expires_in
            ou None se falhar
        """
        print("🔐 Starting Max-Code authentication...")

        # 1. Gerar PKCE
        code_verifier, code_challenge = PKCEGenerator.generate_pkce_pair()
        print("✓ Generated PKCE challenge")

        # 2. Gerar state (proteção CSRF)
        state = secrets.token_urlsafe(32)

        # 3. Construir authorization URL
        auth_url = self._build_authorization_url(code_challenge, state)
        print(f"✓ Opening browser for authentication...")
        print(f"   URL: {auth_url[:80]}...")

        # 4. Abrir browser
        webbrowser.open(auth_url)

        # 5. Iniciar servidor callback
        print(f"✓ Waiting for callback on http://localhost:{AuthConfig.CALLBACK_SERVER_PORT}/callback")
        callback_result = self._start_callback_server()

        if not callback_result or not callback_result.success:
            error_msg = callback_result.error_description if callback_result else 'Unknown error'
            print(f"✗ Authentication failed: {error_msg}")
            return None

        # 6. Verificar state (proteção CSRF)
        if callback_result.state != state:
            print("✗ Authentication failed: State mismatch (possible CSRF attack)")
            return None

        print("✓ Received authorization code")

        # 7. Trocar código por tokens
        tokens = self._exchange_code_for_tokens(
            callback_result.authorization_code,
            code_verifier
        )

        if not tokens:
            print("✗ Failed to exchange code for tokens")
            return None

        print("✓ Received tokens successfully")
        return tokens

    def _build_authorization_url(self, code_challenge: str, state: str) -> str:
        """
        Constrói URL de autorização

        Args:
            code_challenge: PKCE challenge
            state: State para proteção CSRF

        Returns:
            URL completa de autorização
        """
        params = {
            'client_id': AuthConfig.CLIENT_ID,
            'response_type': 'code',
            'redirect_uri': AuthConfig.REDIRECT_URI,
            'scope': ' '.join(AuthConfig.SCOPES),
            'state': state,
            'code_challenge': code_challenge,
            'code_challenge_method': AuthConfig.PKCE_CHALLENGE_METHOD,
        }

        query_string = urllib.parse.urlencode(params)
        return f"{AuthConfig.AUTHORIZATION_URL}?{query_string}"

    def _start_callback_server(self) -> Optional[OAuthCallbackResult]:
        """
        Inicia servidor HTTP local para callback

        Returns:
            OAuthCallbackResult com código de autorização ou None
        """
        # Reset callback result
        OAuthCallbackHandler.callback_result = None

        # Criar servidor HTTP
        server = HTTPServer(
            ('localhost', AuthConfig.CALLBACK_SERVER_PORT),
            OAuthCallbackHandler
        )

        # Timeout configurável
        server.timeout = AuthConfig.CALLBACK_TIMEOUT

        # Handle uma única request (callback)
        server.handle_request()

        return OAuthCallbackHandler.callback_result

    def _exchange_code_for_tokens(
        self,
        authorization_code: str,
        code_verifier: str
    ) -> Optional[Dict[str, str]]:
        """
        Troca código de autorização por access/refresh tokens

        Args:
            authorization_code: Código recebido no callback
            code_verifier: PKCE verifier gerado anteriormente

        Returns:
            Dict com tokens ou None se falhar
        """
        payload = {
            'grant_type': 'authorization_code',
            'code': authorization_code,
            'redirect_uri': AuthConfig.REDIRECT_URI,
            'client_id': AuthConfig.CLIENT_ID,
            'code_verifier': code_verifier,
        }

        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'User-Agent': AuthConfig.USER_AGENT,
        }

        try:
            response = requests.post(
                AuthConfig.TOKEN_URL,
                data=payload,
                headers=headers,
                timeout=AuthConfig.HTTP_REQUEST_TIMEOUT
            )

            if response.status_code != 200:
                print(f"✗ Token exchange failed: HTTP {response.status_code}")
                print(f"   Response: {response.text}")
                return None

            tokens = response.json()

            # Validar resposta
            required_fields = ['access_token', 'refresh_token', 'expires_in']
            if not all(field in tokens for field in required_fields):
                print(f"✗ Invalid token response: missing required fields")
                return None

            return tokens

        except requests.RequestException as e:
            print(f"✗ Token exchange failed: {e}")
            return None

    def refresh_access_token(self, refresh_token: str) -> Optional[Dict[str, str]]:
        """
        Renova access token usando refresh token

        Args:
            refresh_token: Refresh token válido

        Returns:
            Dict com novo access_token e expires_in ou None
        """
        payload = {
            'grant_type': 'refresh_token',
            'refresh_token': refresh_token,
            'client_id': AuthConfig.CLIENT_ID,
        }

        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'User-Agent': AuthConfig.USER_AGENT,
        }

        try:
            response = requests.post(
                AuthConfig.TOKEN_URL,
                data=payload,
                headers=headers,
                timeout=AuthConfig.HTTP_REQUEST_TIMEOUT
            )

            if response.status_code != 200:
                print(f"⚠️  Token refresh failed: HTTP {response.status_code}")
                return None

            tokens = response.json()

            # Validar resposta
            if 'access_token' not in tokens or 'expires_in' not in tokens:
                print(f"⚠️  Invalid token refresh response")
                return None

            return tokens

        except requests.RequestException as e:
            print(f"⚠️  Token refresh failed: {e}")
            return None


# ==================== HELPER FUNCTIONS ====================

def initiate_oauth_login() -> Optional[Dict[str, str]]:
    """
    Helper function para iniciar login OAuth

    Returns:
        Dict com tokens ou None se falhar
    """
    oauth_flow = OAuthFlow()
    return oauth_flow.start_authorization_flow()


def refresh_token(refresh_token: str) -> Optional[Dict[str, str]]:
    """
    Helper function para refresh de token

    Args:
        refresh_token: Refresh token válido

    Returns:
        Dict com novo access_token ou None
    """
    oauth_flow = OAuthFlow()
    return oauth_flow.refresh_access_token(refresh_token)
