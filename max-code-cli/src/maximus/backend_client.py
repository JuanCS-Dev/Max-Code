"""MAXIMUS Backend Client - aiohttp + JWT + retry"""
import os, asyncio, jwt, time, logging
from typing import Dict, Optional
from enum import Enum
import aiohttp
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

logger = logging.getLogger(__name__)

class MaximusError(Exception): pass
class ServiceUnavailable(MaximusError): pass
class RateLimitError(MaximusError): pass

class MaximusClient:
    """Async HTTP client for MAXIMUS microservices (research-based: Jan 2025)"""
    def __init__(self, base_url=None, api_key=None, max_connections=100):
        self.base_url = base_url or os.getenv("MAXIMUS_BASE_URL", "http://localhost:8000")
        self.api_key = api_key or os.getenv("MAXIMUS_API_KEY", os.getenv("ANTHROPIC_API_KEY", "your-api-key-here"))
        connector = aiohttp.TCPConnector(limit=max_connections, limit_per_host=10, ttl_dns_cache=300)
        self.session = aiohttp.ClientSession(connector=connector)
        logger.info(f"MaximusClient initialized: {self.base_url}")
    
    def _create_jwt(self) -> str:
        payload = {"sub": "max-code-cli", "exp": int(time.time()) + 3600}
        return jwt.encode(payload, self.api_key, algorithm="HS256")
    
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10), retry=retry_if_exception_type(RateLimitError))
    async def call_service(self, service: str, data: Dict, timeout: int = 30) -> Dict:
        """Call MAXIMUS service with retry + backoff"""
        url = f"{self.base_url}/api/v1/{service}"
        headers = {"Authorization": f"Bearer {self._create_jwt()}", "Content-Type": "application/json"}
        try:
            async with self.session.post(url, json=data, headers=headers, timeout=aiohttp.ClientTimeout(total=timeout)) as resp:
                if resp.status == 429: raise RateLimitError("Rate limit exceeded")
                if resp.status >= 500: raise ServiceUnavailable(f"{service} unavailable")
                resp.raise_for_status()
                return await resp.json()
        except asyncio.TimeoutError: raise ServiceUnavailable(f"{service} timeout")
        except aiohttp.ClientError as e: raise MaximusError(f"{service} error: {e}")
    
    async def close(self): await self.session.close()
    async def __aenter__(self): return self
    async def __aexit__(self, *args): await self.close()
