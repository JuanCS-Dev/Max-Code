# Maximus AI - Shared Libraries

Complete set of production-ready libraries for Maximus AI services.

**Day 2 Delivery:** Security & Stability Infrastructure ✅

---

## 📚 Available Libraries

### 1. 🔐 **libs/auth** - JWT Authentication
Complete JWT-based authentication for API endpoints.

**Features:**
- JWT token creation & verification
- API key support (service-to-service)
- FastAPI integration (Security dependencies)
- Token expiration management
- Role-based access control helpers

**Quick Start:**
```python
from libs.auth import verify_token, create_access_token
from fastapi import Depends

@app.post("/protected")
async def protected_route(token_data: dict = Depends(verify_token)):
    return {"user_id": token_data.get("sub")}
```

📖 **[Full Documentation](./auth/INTEGRATION_GUIDE.md)**

---

### 2. ✅ **libs/validation** - Pydantic Schemas
Input validation schemas for all API requests.

**Features:**
- Type validation
- Range & size limits
- Pattern matching (regex)
- Payload size protection
- Action whitelisting
- Custom validators

**Quick Start:**
```python
from libs.validation import BrowserActionRequest

@app.post("/browser/action")
async def browser_action(request: BrowserActionRequest):
    # Request is automatically validated
    url = request.url  # HttpUrl type
    action = request.action  # Whitelisted enum
    return {"status": "ok"}
```

**Available Schemas:**
- `HealthResponse` - Standard health check format
- `BrowserActionRequest/Response` - MABA browser automation
- `NarrativeRequest/Response` - NIS narrative generation
- `ConsciousnessRequest/Response` - Core consciousness processing
- `ErrorResponse/SuccessResponse` - Generic responses
- `PaginationParams/PaginatedResponse` - Pagination support

---

### 3. 🏥 **libs/health** - Health Checks
Comprehensive health checks with dependency testing.

**Features:**
- PostgreSQL connectivity check
- Redis connectivity check
- Neo4j connectivity check
- HTTP service health check
- Aggregated health status
- Timeout controls
- Concurrent checking

**Quick Start:**
```python
from libs.health import HealthChecker

health_checker = HealthChecker(
    service_name="maximus-core",
    version="1.0.0"
)

# Register dependency checks
health_checker.add_postgres_check()
health_checker.add_redis_check()

@app.get("/health")
async def health():
    return await health_checker.check_all()
```

**Response Format:**
```json
{
  "status": "healthy",
  "service": "maximus-core",
  "version": "1.0.0",
  "timestamp": "2024-01-15T10:30:00Z",
  "dependencies": {
    "postgres": "healthy",
    "redis": "healthy"
  }
}
```

---

## 🚀 Complete Integration Example

Here's a complete FastAPI service using all three libraries:

```python
from fastapi import FastAPI, Depends, HTTPException
from libs.auth import verify_token, create_access_token
from libs.validation import BrowserActionRequest, HealthResponse
from libs.health import HealthChecker

app = FastAPI(title="My Maximus Service")

# Initialize health checker
health_checker = HealthChecker(service_name="my-service", version="1.0.0")
health_checker.add_postgres_check()
health_checker.add_redis_check()

# PUBLIC ENDPOINT - No auth, simple response
@app.get("/health", response_model=HealthResponse)
async def health():
    """Public health check endpoint (no authentication required)."""
    return await health_checker.check_all()

# PROTECTED ENDPOINT - Requires JWT auth, validated request
@app.post("/browser/action")
async def browser_action(
    request: BrowserActionRequest,  # ← Automatic validation
    token_data: dict = Depends(verify_token)  # ← Requires auth
):
    """Protected endpoint with auth and validation."""
    user_id = token_data.get("sub")

    # Process request (already validated)
    result = await process_browser_action(
        url=request.url,
        action=request.action,
        parameters=request.parameters
    )

    return {
        "success": True,
        "user_id": user_id,
        "result": result
    }

# LOGIN ENDPOINT - Create tokens
@app.post("/auth/login")
async def login(username: str, password: str):
    """Create JWT token after validating credentials."""
    if validate_credentials(username, password):
        token = create_access_token({
            "sub": username,
            "role": "user"
        })
        return {"access_token": token, "token_type": "bearer"}
    raise HTTPException(status_code=401, detail="Invalid credentials")
```

---

## 📦 Dependencies

Add to your `requirements.txt`:

```txt
# JWT Authentication
pyjwt>=2.8.0
python-multipart>=0.0.6

# Validation (FastAPI includes Pydantic)
pydantic>=2.0.0

# Health Checks - Database clients
asyncpg>=0.29.0          # PostgreSQL
redis[asyncio]>=5.0.0    # Redis
neo4j>=5.14.0            # Neo4j
httpx>=0.25.0            # HTTP health checks
```

---

## 🔧 Environment Variables

Required for all services:

```bash
# JWT Authentication
JWT_SECRET=your_super_secret_random_string_min_32_chars
JWT_EXPIRE_MINUTES=60
INTERNAL_API_KEYS=key1,key2,key3  # Optional

# Database connections (for health checks)
POSTGRES_HOST=postgres
POSTGRES_PORT=5432
POSTGRES_USER=maximus
POSTGRES_PASSWORD=your_password
POSTGRES_DB=maximus

REDIS_HOST=redis
REDIS_PORT=6379
REDIS_PASSWORD=your_password  # Optional

NEO4J_URI=bolt://neo4j:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=your_password
```

---

## ✅ Service Integration Checklist

For each service (Core, MABA, NIS, PENELOPE):

### Phase 1: Dependencies
- [ ] Add `pyjwt`, `asyncpg`, `redis`, `httpx` to requirements.txt
- [ ] Run `pip install -r requirements.txt`

### Phase 2: Health Checks
- [ ] Import `HealthChecker` from `libs.health`
- [ ] Initialize checker with service name and version
- [ ] Add relevant dependency checks (postgres, redis, neo4j)
- [ ] Update `/health` endpoint to use checker
- [ ] Test: `curl http://localhost:PORT/health`

### Phase 3: Authentication
- [ ] Import `verify_token` from `libs.auth`
- [ ] Add `token_data: dict = Depends(verify_token)` to protected endpoints
- [ ] Keep `/health` endpoint public (no auth)
- [ ] Create test token for development
- [ ] Test with valid/invalid tokens

### Phase 4: Validation
- [ ] Import relevant schemas from `libs.validation`
- [ ] Replace `dict` parameters with Pydantic models
- [ ] Update endpoint signatures
- [ ] Test with valid/invalid payloads
- [ ] Verify error responses (422 for validation errors)

### Phase 5: Testing
- [ ] Health check returns 200 with dependency status
- [ ] Protected endpoints return 401 without token
- [ ] Protected endpoints return 200 with valid token
- [ ] Invalid requests return 422 with validation errors
- [ ] Load testing (optional)

---

## 📊 Testing Examples

### 1. Test Health Check
```bash
curl http://localhost:8150/health

# Expected response:
{
  "status": "healthy",
  "service": "maximus-core",
  "version": "1.0.0",
  "timestamp": "2024-01-15T10:30:00Z",
  "dependencies": {
    "postgres": "healthy",
    "redis": "healthy"
  }
}
```

### 2. Test Authentication
```bash
# Without token (should fail with 401)
curl http://localhost:8150/protected

# With token (should succeed)
TOKEN="your_jwt_token_here"
curl http://localhost:8150/protected \
  -H "Authorization: Bearer $TOKEN"
```

### 3. Test Validation
```bash
# Invalid request (should fail with 422)
curl -X POST http://localhost:8152/browser/action \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"url": "not-a-valid-url", "action": "hack"}'

# Valid request (should succeed)
curl -X POST http://localhost:8152/browser/action \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "url": "https://example.com",
    "action": "navigate",
    "timeout_seconds": 30
  }'
```

---

## 🛡️ Security Best Practices

### JWT_SECRET
- ⚠️ **CRITICAL**: Change default JWT_SECRET in production
- Use at least 32 random characters
- Never commit secrets to git
- Rotate regularly (every 90 days)

### API Keys
- Use different keys per environment (dev/staging/prod)
- Rotate after any potential compromise
- Limit scope (one key per service if possible)

### Validation
- Never trust user input
- Always use Pydantic schemas for validation
- Set reasonable size limits (prevent DoS)
- Whitelist actions/enums (don't use arbitrary strings)

### Health Checks
- Keep `/health` endpoint public (for monitoring)
- Don't expose sensitive info in health responses
- Set reasonable timeouts (5s recommended)
- Monitor health check failures

---

## 🐛 Troubleshooting

### "PyJWT not installed"
```bash
pip install pyjwt
```

### "Token expired"
Tokens expire after `JWT_EXPIRE_MINUTES` (default 60).
- Create new token
- Or increase expiration time

### "Invalid token"
- Check JWT_SECRET matches
- Verify token format: `Bearer <token>`
- Check token hasn't expired

### "Validation error: field required"
- Check request body matches schema
- All required fields must be present
- Check field types match

### "Health check timeout"
- Check dependency services are running
- Verify network connectivity
- Increase timeout if needed

---

## 📖 Additional Documentation

- **[JWT Auth Integration Guide](./auth/INTEGRATION_GUIDE.md)** - Detailed auth setup
- **[BRUTAL_AUDIT_FIX_PLAN.md](../BRUTAL_AUDIT_FIX_PLAN.md)** - Complete 4-day plan

---

## 🎯 Constitution Compliance

**P1 (Completude):** ✅ All libraries fully implemented, no placeholders
**P2 (Validação):** ✅ All inputs validated before processing
**P3 (Ceticismo):** ✅ Critical validation of all user inputs
**P4 (Rastreabilidade):** ✅ All code documented with examples
**P5 (Consciência Sistêmica):** ✅ System-wide health awareness

---

**Built with ❤️ under Constitutional Governance**

*Day 2 Complete: Security & Stability Infrastructure Ready for Integration*
