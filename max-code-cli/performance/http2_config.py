"""
HTTP/2 configuration for MAXIMUS services.
Improves performance with multiplexing and header compression.
"""

import httpx
from typing import Optional


def create_http2_client(
    base_url: str,
    timeout: float = 30.0,
    verify: bool = True,
    http2: bool = True,
) -> httpx.AsyncClient:
    """
    Create HTTP/2 enabled client for better performance.

    Benefits:
    - Multiplexing: Multiple requests over single connection
    - Header compression (HPACK)
    - Server push (if backend supports)
    - Binary protocol (faster than HTTP/1.1)
    """
    return httpx.AsyncClient(
        base_url=base_url,
        timeout=httpx.Timeout(timeout),
        limits=httpx.Limits(
            max_connections=200,
            max_keepalive_connections=50,
            keepalive_expiry=30.0,
        ),
        verify=verify,
        http2=http2,  # Enable HTTP/2
    )


# Uvicorn HTTP/2 support (requires h2 package)
UVICORN_HTTP2_CMD = """
# Install dependencies
pip install httpx[http2] uvicorn[standard] h2

# Run with HTTP/2
uvicorn app:app \\
  --host 0.0.0.0 \\
  --port 8100 \\
  --workers 4 \\
  --http h2 \\
  --ssl-keyfile=certs/server-key.pem \\
  --ssl-certfile=certs/server-cert.pem
"""
