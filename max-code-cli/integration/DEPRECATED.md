# ⚠️ DEPRECATED - Legacy Clients

**Status**: ❌ Obsolete - DO NOT USE
**Date**: 2025-11-11
**Replacement**: `core/maximus_integration/client_v2.py` and `core/maximus_integration/penelope_client_v2.py`

---

## 🚫 Deprecated Files

All clients in this folder are **LEGACY** and should NOT be used:

- ❌ `maximus_client.py` → Use `core/maximus_integration/client_v2.py`
- ❌ `penelope_client.py` → Use `core/maximus_integration/penelope_client_v2.py`
- ❌ `orchestrator_client.py` → Deprecated (not in backend schema)
- ❌ `oraculo_client.py` → Deprecated (not in backend schema)
- ❌ `atlas_client.py` → Deprecated (not in backend schema)
- ❌ `simple_clients.py` → Use v2 clients
- ❌ `base_client.py` → Use `core/maximus_integration/base_client.py`

---

## ✅ Use Instead

### For MAXIMUS Core

```python
from core.maximus_integration.client_v2 import MaximusClient

async with MaximusClient() as client:
    health = await client.health()
    response = await client.query("Analyze this code")
```

### For PENELOPE

```python
from core.maximus_integration.penelope_client_v2 import PENELOPEClient

async with PENELOPEClient() as client:
    health = await client.health()
    fruits = await client.fruits.get_all()
```

---

## 📊 Why Deprecated?

1. **API Incompatibility**: Legacy clients don't match actual backend API (0% compatibility)
2. **No Type Safety**: Missing Pydantic models
3. **Poor Error Handling**: Inconsistent retry logic
4. **Code Duplication**: Repeated `_request()` logic
5. **Not Tested**: No E2E tests

---

## 🗑️ Removal Timeline

- **Week 5** (Now): Marked as deprecated
- **Week 6**: Remove from imports
- **Week 7**: Delete files

---

## 📚 Migration Guide

See: `docs/docs-da-integracao/MIGRATION_GUIDE.md`

---

**Do NOT use these files. They will be deleted in Week 7.**
