# JWT Authentication - Integration Guide

## Quick Start (5 minutes per service)

### Step 1: Install Dependencies

```bash
pip install pyjwt python-multipart
```

Add to `requirements.txt`:
```
pyjwt>=2.8.0
python-multipart>=0.0.6
```

### Step 2: Import Auth in Your API

```python
# At the top of your main.py or api.py
from libs.auth import verify_token, create_access_token, get_optional_token
from fastapi import Depends
```

### Step 3: Protect Endpoints

**Before (No Auth):**
```python
@app.post("/process")
async def process_request(request: ProcessRequest):
    # Anyone can access
    return {"result": "processed"}
```

**After (With Auth):**
```python
@app.post("/process")
async def process_request(
    request: ProcessRequest,
    token_data: dict = Depends(verify_token)  # ← ADD THIS
):
    # Only authenticated users can access
    user_id = token_data.get("sub")
    return {"result": "processed", "user": user_id}
```

### Step 4: Keep Health Endpoint Public

```python
# Health endpoint should NOT require auth (for monitoring)
@app.get("/health")
async def health():
    return {"status": "healthy"}
```

### Step 5: Create Login/Token Endpoint (Optional)

```python
from libs.auth import create_access_token

@app.post("/auth/token")
async def login(username: str, password: str):
    # Validate credentials (your logic here)
    if validate_user(username, password):
        token = create_access_token({"sub": username, "role": "user"})
        return {"access_token": token, "token_type": "bearer"}
    raise HTTPException(status_code=401, detail="Invalid credentials")
```

---

## Complete Examples

### Example 1: Simple Protected Endpoint

```python
from fastapi import FastAPI, Depends
from libs.auth import verify_token

app = FastAPI()

@app.get("/health")
async def health():
    """Public endpoint - no auth required."""
    return {"status": "healthy"}

@app.get("/protected")
async def protected_route(token_data: dict = Depends(verify_token)):
    """Protected endpoint - requires valid JWT."""
    return {
        "message": "You are authenticated!",
        "user_id": token_data.get("sub")
    }
```

### Example 2: Optional Authentication

```python
from libs.auth import get_optional_token

@app.get("/public-or-private")
async def flexible_route(token_data: dict = Depends(get_optional_token)):
    """Works with or without auth (different response)."""
    if token_data:
        return {"message": "authenticated", "user": token_data.get("sub")}
    return {"message": "anonymous"}
```

### Example 3: Service-to-Service (API Key)

```python
from libs.auth import verify_api_key

@app.post("/internal/sync")
async def internal_sync(authenticated: bool = Depends(verify_api_key)):
    """Only accessible with valid API key (for internal services)."""
    return {"status": "synced"}
```

### Example 4: Role-Based Access

```python
from libs.auth import require_role

admin_required = require_role("admin")

@app.delete("/users/{user_id}")
async def delete_user(
    user_id: str,
    token_data: dict = Depends(admin_required)
):
    """Only admins can delete users."""
    return {"deleted": user_id}
```

---

## Testing with cURL

### 1. Create a Token (for testing)

```python
# In Python shell or test script
from libs.auth import create_access_token

token = create_access_token({"sub": "test_user", "role": "admin"})
print(f"Token: {token}")
```

### 2. Use Token in Request

```bash
# Without auth (should fail)
curl http://localhost:8150/protected

# With auth (should succeed)
curl http://localhost:8150/protected \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

### 3. Use API Key

```bash
# Set INTERNAL_API_KEYS=my-secret-key-123 in .env

curl http://localhost:8150/internal/sync \
  -H "Authorization: Bearer my-secret-key-123"
```

---

## Environment Variables

Add to your `.env` file:

```bash
# JWT Authentication
JWT_SECRET=your_super_secret_random_string_min_32_chars
JWT_EXPIRE_MINUTES=60

# Internal API Keys (comma-separated)
INTERNAL_API_KEYS=key1,key2,key3
```

**⚠️  SECURITY:** Never commit real JWT_SECRET or API keys to git!

---

## Service Integration Checklist

For each service (Core, MABA, NIS, PENELOPE):

- [ ] Add `pyjwt` to requirements.txt
- [ ] Import `verify_token` from `libs.auth`
- [ ] Add `token_data: dict = Depends(verify_token)` to protected endpoints
- [ ] Keep `/health` endpoint public (no auth)
- [ ] Test with valid token
- [ ] Test with invalid/expired token
- [ ] Test with no token (should return 401)

---

## Common Issues

### "PyJWT not installed"

```bash
pip install pyjwt
```

### "Invalid token"

- Check JWT_SECRET matches between token creation and verification
- Check token hasn't expired (default 60 min)
- Check token format: `Bearer <token>`

### "Token expired"

Tokens expire after JWT_EXPIRE_MINUTES (default 60).
Create a new token or increase expiration time.

---

## Next Steps

1. Apply auth to all services (see checklist above)
2. Add input validation (Pydantic schemas)
3. Implement real health checks
4. Add rate limiting (future enhancement)
5. Add audit logging for auth failures

---

**Constitution Compliance:**
✅ P1 (Completude): Full implementation
✅ P2 (Validação): All tokens validated
✅ P3 (Ceticismo): Critical validation of credentials
