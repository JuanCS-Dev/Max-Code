# Guia Prático de Implementação: OAuth 2.0 + PKCE para Max-Code

## 1. Overview da Arquitetura

```
┌─────────────────────────────────────────────┐
│          Max-Code CLI                       │
├─────────────────────────────────────────────┤
│                                             │
│  ┌──────────────┐  ┌──────────────────┐   │
│  │ OAuth Module │  │ Credential Store │   │
│  │              │  │                  │   │
│  │- PKCE        │  │- ~/.max-code/    │   │
│  │- Browser flow│  │  .credentials    │   │
│  │- Token exch. │  │- AES-256 enc?    │   │
│  └──────────────┘  └──────────────────┘   │
│         │                                  │
│  ┌──────▼──────────────────────┐          │
│  │  HTTP Request Interceptor    │          │
│  │                              │          │
│  │- Add Bearer token            │          │
│  │- Auto-refresh on 401         │          │
│  │- Retry logic                 │          │
│  └──────┬───────────────────────┘          │
│         │                                  │
└─────────┼──────────────────────────────────┘
          │
          ▼
    ┌──────────────────┐
    │ Anthropic API    │
    │ api.anthropic.com│
    └──────────────────┘
```

---

## 2. Estrutura de Arquivos Recomendada

```
max-code/
├── src/
│   ├── auth/
│   │   ├── __init__.py
│   │   ├── oauth.py          # OAuth 2.0 + PKCE implementation
│   │   ├── credentials.py     # Credential storage/retrieval
│   │   ├── token_manager.py   # Token refresh logic
│   │   └── crypto.py          # Encryption utilities (optional)
│   │
│   ├── client/
│   │   ├── __init__.py
│   │   ├── http_client.py     # HTTP wrapper with auth interceptor
│   │   └── api.py             # Anthropic API client
│   │
│   ├── cli/
│   │   ├── __init__.py
│   │   ├── commands/
│   │   │   ├── login.py       # /login command
│   │   │   ├── logout.py      # /logout command
│   │   │   └── auth_status.py # auth status command
│   │   └── main.py
│   │
│   └── config.py              # Configuration constants
│
├── tests/
│   ├── test_oauth.py
│   ├── test_credentials.py
│   └── test_http_client.py
│
├── requirements.txt
└── setup.py
```

---

## 3. Implementação Passo a Passo

### 3.1 Config Constants (config.py)

```python
import os

# OAuth Configuration
OAUTH_CLIENT_ID = "9d1c250a-e61b-44d9-88ed-5944d1962f5e"  # Claude Code's ID (temporary)
OAUTH_AUTHORIZE_URL = "https://claude.ai/oauth/authorize"
OAUTH_TOKEN_URL = "https://console.anthropic.com/v1/oauth/token"
OAUTH_REDIRECT_URI = "http://localhost:5678/callback"
OAUTH_CALLBACK_PORT = 5678

OAUTH_SCOPES = ["user:inference", "user:profile"]

# API Configuration
API_BASE_URL = "https://api.anthropic.com"
API_VERSION = "2023-06-01"

# Credential Storage
CREDENTIALS_DIR = os.path.expanduser("~/.max-code")
CREDENTIALS_FILE = os.path.join(CREDENTIALS_DIR, ".credentials.json")
CREDENTIALS_PERMISSIONS = 0o600

# Token Refresh
TOKEN_REFRESH_BUFFER = 300  # Refresh 5 minutes before expiration
TOKEN_REFRESH_CHECK_INTERVAL = 300  # Check every 5 minutes
```

### 3.2 OAuth Implementation (oauth.py)

```python
import json
import secrets
import hashlib
import base64
import webbrowser
import threading
import time
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlencode, parse_qs, urlparse
import requests
from datetime import datetime, timedelta
from typing import Dict, Optional, Tuple

from .credentials import CredentialManager
from .. import config


class PKCEGenerator:
    """Generates PKCE code challenge and verifier"""
    
    @staticmethod
    def generate_code_verifier(length: int = 128) -> str:
        """Generate random code verifier (128-128 chars)"""
        return base64.urlsafe_b64encode(
            secrets.token_bytes(int(length * 3 / 4))
        ).decode('utf-8').rstrip('=')
    
    @staticmethod
    def generate_code_challenge(code_verifier: str) -> str:
        """Generate code challenge from verifier using SHA256"""
        digest = hashlib.sha256(code_verifier.encode()).digest()
        return base64.urlsafe_b64encode(digest).decode('utf-8').rstrip('=')


class OAuthCallbackHandler(BaseHTTPRequestHandler):
    """HTTP request handler for OAuth callback"""
    
    # Class variable to store callback data
    callback_data: Dict = {}
    
    def do_GET(self):
        """Handle GET request from OAuth redirect"""
        try:
            # Parse query parameters
            parsed = urlparse(self.path)
            params = parse_qs(parsed.query)
            
            # Extract auth code and state
            auth_code = params.get('code', [None])[0]
            state = params.get('state', [None])[0]
            error = params.get('error', [None])[0]
            
            # Store callback data
            OAuthCallbackHandler.callback_data = {
                'code': auth_code,
                'state': state,
                'error': error
            }
            
            # Send response
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            
            if error:
                html = f"""
                <html>
                <body style="font-family: Arial">
                <h1>Authentication Failed</h1>
                <p>Error: {error}</p>
                <p>You can close this window.</p>
                </body>
                </html>
                """
            else:
                html = """
                <html>
                <body style="font-family: Arial">
                <h1>Authentication Successful!</h1>
                <p>You have successfully authenticated with Max-Code.</p>
                <p>You can close this window and return to your terminal.</p>
                </body>
                </html>
                """
            
            self.wfile.write(html.encode())
            
        except Exception as e:
            self.send_error(500, str(e))
    
    def log_message(self, format, *args):
        """Suppress default logging"""
        pass


class OAuthFlow:
    """OAuth 2.0 + PKCE flow implementation"""
    
    def __init__(self, credential_manager: CredentialManager):
        self.credential_manager = credential_manager
        self.code_verifier = None
        self.state = None
    
    def start_login(self) -> Optional[Dict]:
        """Start OAuth login flow
        
        Returns:
            Dict with access_token, refresh_token, and other data
            or None if login failed
        """
        try:
            # Generate PKCE
            self.code_verifier = PKCEGenerator.generate_code_verifier()
            code_challenge = PKCEGenerator.generate_code_challenge(self.code_verifier)
            self.state = secrets.token_urlsafe(32)
            
            # Start local callback server
            server = HTTPServer(
                ('localhost', config.OAUTH_CALLBACK_PORT),
                OAuthCallbackHandler
            )
            server_thread = threading.Thread(target=server.handle_request)
            server_thread.daemon = True
            server_thread.start()
            
            print(f"Opening browser for authentication...")
            print(f"If browser doesn't open, visit: {self._build_auth_url(code_challenge)}")
            
            # Open authorization URL in browser
            auth_url = self._build_auth_url(code_challenge)
            webbrowser.open(auth_url)
            
            # Wait for callback (with timeout)
            start_time = time.time()
            timeout = 600  # 10 minutes
            
            while time.time() - start_time < timeout:
                if OAuthCallbackHandler.callback_data:
                    callback_data = OAuthCallbackHandler.callback_data
                    OAuthCallbackHandler.callback_data = {}
                    
                    if callback_data.get('error'):
                        print(f"Error: {callback_data['error']}")
                        return None
                    
                    if callback_data.get('code'):
                        # Validate state
                        if callback_data.get('state') != self.state:
                            print("Error: State mismatch (CSRF protection)")
                            return None
                        
                        auth_code = callback_data['code']
                        
                        # Exchange code for tokens
                        tokens = self._exchange_code(auth_code)
                        
                        if tokens:
                            # Save credentials
                            self.credential_manager.save(tokens)
                            print("✓ Authentication successful!")
                            return tokens
                        else:
                            print("Error: Failed to exchange code for tokens")
                            return None
                
                time.sleep(0.1)
            
            print("Error: Authentication timeout")
            return None
        
        except Exception as e:
            print(f"Error during login: {e}")
            return None
        
        finally:
            server.server_close()
    
    def _build_auth_url(self, code_challenge: str) -> str:
        """Build OAuth authorization URL"""
        params = {
            'client_id': config.OAUTH_CLIENT_ID,
            'redirect_uri': config.OAUTH_REDIRECT_URI,
            'response_type': 'code',
            'scope': ' '.join(config.OAUTH_SCOPES),
            'code_challenge': code_challenge,
            'code_challenge_method': 'S256',
            'state': self.state
        }
        return f"{config.OAUTH_AUTHORIZE_URL}?{urlencode(params)}"
    
    def _exchange_code(self, auth_code: str) -> Optional[Dict]:
        """Exchange authorization code for tokens"""
        try:
            payload = {
                'grant_type': 'authorization_code',
                'code': auth_code,
                'client_id': config.OAUTH_CLIENT_ID,
                'code_verifier': self.code_verifier,
                'redirect_uri': config.OAUTH_REDIRECT_URI
            }
            
            response = requests.post(
                config.OAUTH_TOKEN_URL,
                json=payload,
                timeout=30
            )
            response.raise_for_status()
            
            tokens = response.json()
            
            # Add metadata
            tokens['expiresAt'] = int(
                (datetime.now() + timedelta(seconds=tokens.get('expires_in', 3600))).timestamp() * 1000
            )
            
            return tokens
        
        except Exception as e:
            print(f"Error exchanging code: {e}")
            return None
```

### 3.3 Credential Management (credentials.py)

```python
import json
import os
from typing import Optional, Dict
from datetime import datetime
from . import config


class CredentialManager:
    """Manages credential storage and retrieval"""
    
    def __init__(self):
        self._ensure_directory()
    
    def _ensure_directory(self):
        """Create credentials directory if it doesn't exist"""
        os.makedirs(config.CREDENTIALS_DIR, exist_ok=True)
    
    def save(self, tokens: Dict) -> bool:
        """Save credentials to file"""
        try:
            credentials = {
                'claudeAiOauth': {
                    'accessToken': tokens.get('access_token'),
                    'refreshToken': tokens.get('refresh_token'),
                    'expiresAt': tokens.get('expiresAt'),
                    'scopes': tokens.get('scope', '').split(),
                    'subscriptionType': tokens.get('subscriptionType', 'free'),
                    'tokenType': tokens.get('token_type', 'Bearer')
                }
            }
            
            # Write to file
            with open(config.CREDENTIALS_FILE, 'w') as f:
                json.dump(credentials, f, indent=2)
            
            # Set restrictive permissions
            os.chmod(config.CREDENTIALS_FILE, config.CREDENTIALS_PERMISSIONS)
            
            return True
        
        except Exception as e:
            print(f"Error saving credentials: {e}")
            return False
    
    def load(self) -> Optional[Dict]:
        """Load credentials from file"""
        try:
            if not os.path.exists(config.CREDENTIALS_FILE):
                return None
            
            with open(config.CREDENTIALS_FILE, 'r') as f:
                data = json.load(f)
            
            return data.get('claudeAiOauth')
        
        except Exception as e:
            print(f"Error loading credentials: {e}")
            return None
    
    def delete(self) -> bool:
        """Delete saved credentials"""
        try:
            if os.path.exists(config.CREDENTIALS_FILE):
                os.remove(config.CREDENTIALS_FILE)
            return True
        
        except Exception as e:
            print(f"Error deleting credentials: {e}")
            return False
    
    def is_expired(self, credentials: Dict) -> bool:
        """Check if credentials are expired"""
        if not credentials:
            return True
        
        expires_at = credentials.get('expiresAt', 0)
        if expires_at == 0:
            return True
        
        # Convert from milliseconds to seconds
        expires_at_seconds = expires_at / 1000
        current_time = datetime.now().timestamp()
        
        # Add buffer (refresh 5 minutes before expiration)
        buffer_seconds = config.TOKEN_REFRESH_BUFFER
        
        return current_time > (expires_at_seconds - buffer_seconds)
```

### 3.4 Token Manager (token_manager.py)

```python
import requests
from typing import Optional, Dict
import threading
import time
from datetime import datetime

from .credentials import CredentialManager
from . import config


class TokenManager:
    """Manages token refresh and lifecycle"""
    
    def __init__(self, credential_manager: CredentialManager):
        self.credential_manager = credential_manager
        self._refresh_thread = None
        self._stop_refresh = False
    
    def start_refresh_thread(self):
        """Start background token refresh thread"""
        if self._refresh_thread is None or not self._refresh_thread.is_alive():
            self._stop_refresh = False
            self._refresh_thread = threading.Thread(
                target=self._refresh_loop,
                daemon=True
            )
            self._refresh_thread.start()
    
    def stop_refresh_thread(self):
        """Stop background token refresh thread"""
        self._stop_refresh = True
        if self._refresh_thread:
            self._refresh_thread.join(timeout=5)
    
    def _refresh_loop(self):
        """Background loop that checks and refreshes tokens"""
        while not self._stop_refresh:
            try:
                credentials = self.credential_manager.load()
                
                if credentials and self.credential_manager.is_expired(credentials):
                    print("[Token Manager] Token expiring soon, refreshing...")
                    self.refresh_token(credentials)
                
                time.sleep(config.TOKEN_REFRESH_CHECK_INTERVAL)
            
            except Exception as e:
                print(f"[Token Manager] Error in refresh loop: {e}")
    
    def refresh_token(self, credentials: Dict) -> Optional[Dict]:
        """Refresh access token using refresh token"""
        try:
            refresh_token = credentials.get('refreshToken')
            
            if not refresh_token:
                print("No refresh token available")
                return None
            
            payload = {
                'grant_type': 'refresh_token',
                'refresh_token': refresh_token,
                'client_id': config.OAUTH_CLIENT_ID
            }
            
            response = requests.post(
                config.OAUTH_TOKEN_URL,
                json=payload,
                timeout=30
            )
            response.raise_for_status()
            
            tokens = response.json()
            
            # Add metadata
            tokens['expiresAt'] = int(
                (datetime.now().timestamp() + tokens.get('expires_in', 3600)) * 1000
            )
            
            # Save new credentials
            self.credential_manager.save(tokens)
            
            return tokens
        
        except Exception as e:
            print(f"Error refreshing token: {e}")
            return None
    
    def get_valid_token(self) -> Optional[str]:
        """Get a valid access token, refreshing if needed"""
        credentials = self.credential_manager.load()
        
        if not credentials:
            return None
        
        # Check if expired
        if self.credential_manager.is_expired(credentials):
            # Try to refresh
            new_credentials = self.refresh_token(credentials)
            if new_credentials:
                credentials = new_credentials
            else:
                return None
        
        return credentials.get('accessToken')
```

### 3.5 HTTP Client Interceptor (http_client.py)

```python
import requests
from typing import Optional, Dict, Any
from .token_manager import TokenManager
from . import config


class AuthenticatedHTTPClient:
    """HTTP client with automatic authentication and token refresh"""
    
    def __init__(self, token_manager: TokenManager):
        self.token_manager = token_manager
        self.session = requests.Session()
    
    def _get_headers(self) -> Dict[str, str]:
        """Get headers with authorization token"""
        token = self.token_manager.get_valid_token()
        
        if not token:
            raise RuntimeError("No valid authentication token available")
        
        return {
            'Authorization': f'Bearer {token}',
            'anthropic-version': config.API_VERSION,
            'content-type': 'application/json'
        }
    
    def post(
        self,
        endpoint: str,
        data: Dict[str, Any],
        timeout: int = 30,
        **kwargs
    ) -> requests.Response:
        """POST request with authentication"""
        url = f"{config.API_BASE_URL}{endpoint}"
        headers = self._get_headers()
        
        response = self.session.post(
            url,
            json=data,
            headers=headers,
            timeout=timeout,
            **kwargs
        )
        
        # Handle 401 - token might be revoked
        if response.status_code == 401:
            # Try to refresh and retry once
            if self.token_manager.refresh_token(
                self.token_manager.credential_manager.load()
            ):
                headers = self._get_headers()
                response = self.session.post(
                    url,
                    json=data,
                    headers=headers,
                    timeout=timeout,
                    **kwargs
                )
        
        return response
    
    def get(
        self,
        endpoint: str,
        timeout: int = 30,
        **kwargs
    ) -> requests.Response:
        """GET request with authentication"""
        url = f"{config.API_BASE_URL}{endpoint}"
        headers = self._get_headers()
        
        response = self.session.get(
            url,
            headers=headers,
            timeout=timeout,
            **kwargs
        )
        
        # Handle 401 - token might be revoked
        if response.status_code == 401:
            if self.token_manager.refresh_token(
                self.token_manager.credential_manager.load()
            ):
                headers = self._get_headers()
                response = self.session.get(
                    url,
                    headers=headers,
                    timeout=timeout,
                    **kwargs
                )
        
        return response
```

### 3.6 CLI Commands (commands/login.py)

```python
from ..auth.oauth import OAuthFlow
from ..auth.credentials import CredentialManager


def login_command():
    """Execute login command"""
    print("Starting Max-Code authentication...")
    print()
    
    credential_manager = CredentialManager()
    
    # Check if already logged in
    existing_credentials = credential_manager.load()
    if existing_credentials:
        print("You are already logged in.")
        response = input("Do you want to log in with a different account? (y/N): ")
        if response.lower() != 'y':
            return
        
        # Clear existing credentials
        credential_manager.delete()
    
    # Start OAuth flow
    oauth_flow = OAuthFlow(credential_manager)
    tokens = oauth_flow.start_login()
    
    if tokens:
        print()
        print("✓ You are now authenticated!")
        print("You can start using Max-Code with your Pro/Max subscription.")
    else:
        print()
        print("✗ Authentication failed. Please try again.")
```

---

## 4. Integração com Sistema Existente

### 4.1 Inicializar no Startup

```python
# main.py
from src.auth.credentials import CredentialManager
from src.auth.token_manager import TokenManager
from src.client.http_client import AuthenticatedHTTPClient

# Global instances
credential_manager = CredentialManager()
token_manager = TokenManager(credential_manager)
http_client = AuthenticatedHTTPClient(token_manager)

def initialize():
    """Initialize authentication system"""
    # Start background token refresh
    token_manager.start_refresh_thread()
    
    # Check authentication status
    credentials = credential_manager.load()
    if not credentials:
        print("Not authenticated. Run 'max-code /login' to authenticate.")
    else:
        print("✓ Authenticated")

def cleanup():
    """Cleanup on exit"""
    token_manager.stop_refresh_thread()
```

### 4.2 Fazer Requisições Autenticadas

```python
# Exemplo de uso
def send_message(prompt: str, model: str = "claude-3-5-sonnet-20241022"):
    """Send message using authenticated client"""
    try:
        response = http_client.post(
            "/v1/messages",
            data={
                "model": model,
                "max_tokens": 1024,
                "messages": [{"role": "user", "content": prompt}]
            }
        )
        
        response.raise_for_status()
        return response.json()
    
    except Exception as e:
        print(f"Error sending message: {e}")
        return None
```

---

## 5. Testing

```python
# tests/test_oauth.py
import pytest
from src.auth.oauth import PKCEGenerator


def test_pkce_generation():
    """Test PKCE generation"""
    code_verifier = PKCEGenerator.generate_code_verifier()
    code_challenge = PKCEGenerator.generate_code_challenge(code_verifier)
    
    assert len(code_verifier) > 0
    assert len(code_challenge) > 0
    assert code_verifier != code_challenge


def test_auth_url_building():
    """Test authorization URL generation"""
    from src.auth.credentials import CredentialManager
    from src.auth.oauth import OAuthFlow
    
    cred_mgr = CredentialManager()
    oauth = OAuthFlow(cred_mgr)
    
    code_verifier = PKCEGenerator.generate_code_verifier()
    code_challenge = PKCEGenerator.generate_code_challenge(code_verifier)
    oauth.state = "test_state"
    oauth.code_verifier = code_verifier
    
    url = oauth._build_auth_url(code_challenge)
    
    assert "client_id=" in url
    assert "code_challenge=" in url
    assert "code_challenge_method=S256" in url
```

---

## 6. Dependencies (requirements.txt)

```
requests>=2.31.0
```

---

## 7. Deployment Checklist

- [ ] OAuth client_id registrado com Anthropic (ou usar público temporariamente)
- [ ] Testes passando (unit + integration)
- [ ] Token refresh funcionando
- [ ] Tratamento de erros 401/403
- [ ] Suporte para múltiplas plataformas (Windows/Mac/Linux)
- [ ] Documentação de setup atualizada
- [ ] Segurança: credenciais com permissão 600
- [ ] Segurança: CSRF protection com state parameter
- [ ] Logging and monitoring
- [ ] Fallback para setup-token method

---

## 8. Troubleshooting

### Problema: "Authorization URL não abre no browser"
**Solução:** Exibir URL manualmente para user copiar/colar

### Problema: "Token refresh falha com 401"
**Solução:** Implementar fallback para re-autenticação manual (/login)

### Problema: "Port 5678 já está em uso"
**Solução:** Tentar portas alternativas ou usar device flow

### Problema: "macOS Keychain access denied"
**Solução:** Usar file-based storage com encryption (para consistência cross-platform)

