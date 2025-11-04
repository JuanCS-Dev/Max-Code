# Max-Code CLI - Quick Start Guide

**Status:** ✅ OAuth Module Complete - Ready for Testing!

---

## 🚀 Installation

### 1. Prerequisites

- Python 3.11+
- pip
- Your **Claude Max x20** subscription (paid plan)

### 2. Install Dependencies

```bash
cd "/media/juan/DATA1/projects/Max-Code/max-code-cli"

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Install in development mode
pip install -e .
```

### 3. Verify Installation

```bash
# Check if max-code command is available
max-code --version

# Output: max-code, version 1.0.0-alpha
```

---

## 🔐 Authentication (OAuth with Your Claude Max x20)

### Method 1: Interactive Login (RECOMMENDED)

This uses **your paid Claude Max x20 subscription** without consuming API credits.

```bash
# Start OAuth login flow
max-code login

# What happens:
# 1. Opens browser to Claude.ai
# 2. You login with your account (the one with Max x20 plan)
# 3. Browser redirects back to CLI
# 4. Tokens saved in ~/.max-code/.credentials.json
# 5. Auto-refresh enabled
```

**Expected Output:**
```
🔐 Starting Max-Code authentication...
✓ Generated PKCE challenge
✓ Opening browser for authentication...
✓ Waiting for callback on http://localhost:5678/callback
✓ Received authorization code
✓ Received tokens successfully

═══════════════════════════════════════════════════════════════
  ✅ AUTHENTICATION SUCCESSFUL!
═══════════════════════════════════════════════════════════════

✓ Tokens stored in: /home/juan/.max-code/.credentials.json
✓ Access token valid for: ~12 hours
✓ Auto-refresh: ENABLED
```

### Method 2: Setup Token (for CI/CD)

```bash
# Generate long-lived token (valid ~1 year)
claude setup-token

# Copy the token (sk-ant-oat01-...)
export CLAUDE_CODE_OAUTH_TOKEN="sk-ant-oat01-..."

# Max-Code will use it automatically
max-code status
```

### Method 3: API Key (FALLBACK - consumes credits)

```bash
# Get API key from https://console.anthropic.com/settings/keys
export ANTHROPIC_API_KEY="sk-ant-api..."

# Max-Code will use it (but consumes API credits)
```

---

## ✅ Test OAuth Authentication

### Check Status

```bash
max-code status
```

**Expected Output:**
```
============================================================
MAX-CODE AUTHENTICATION STATUS
============================================================
✅ Authenticated

Credentials file: /home/juan/.max-code/.credentials.json
Created at: 2025-11-04T12:34:56.789Z

✓ Access token valid
  Time until expiration: 11:45:32
============================================================
```

### Test Claude API Call

```bash
# Ask Claude a simple question (uses your Max x20 plan, NO API credits)
max-code ask "What is the capital of France?"
```

**Expected Output:**
```
🤔 Asking Claude (model: claude-sonnet-4-5-20250929)...

╭────────────────── Claude's Response ───────────────────╮
│                                                         │
│ The capital of France is Paris. Paris is not only the │
│ capital but also the largest city in France and is     │
│ known for its art, fashion, culture, and iconic        │
│ landmarks like the Eiffel Tower, Louvre Museum, and    │
│ Notre-Dame Cathedral.                                   │
│                                                         │
╰─────────────────────────────────────────────────────────╯

📊 Tokens used: 15 input + 67 output
```

---

## 🎯 Available Commands (Current)

### Authentication

```bash
# Login with OAuth (opens browser)
max-code login

# Check authentication status
max-code status

# Logout (delete stored tokens)
max-code logout
```

### Testing

```bash
# Ask Claude a question (uses OAuth token from your Max x20 plan)
max-code ask "Your question here"

# Show constitutional compliance metrics (demo)
max-code constitutional
```

---

## 🔧 Troubleshooting

### Problem: "No authentication available"

**Solution:**
```bash
# Run login
max-code login

# Or use setup token
claude setup-token
export CLAUDE_CODE_OAUTH_TOKEN="sk-ant-oat01-..."
```

### Problem: "Token expired"

**Solution:**
Auto-refresh should handle this automatically. If not:
```bash
# Re-login
max-code logout
max-code login
```

### Problem: "Failed to save credentials"

**Solution:**
```bash
# Check directory permissions
ls -la ~/.max-code/

# Should be: drwx------ (700)
# If not:
chmod 700 ~/.max-code/
```

### Problem: Browser doesn't open during login

**Solution:**
```bash
# Manually copy URL from terminal and open in browser
# Or use setup token instead:
claude setup-token
```

---

## 📊 OAuth Implementation Status

| Component | Status | Description |
|-----------|--------|-------------|
| **config.py** | ✅ Complete | Constants, endpoints, priorities |
| **oauth.py** | ✅ Complete | PKCE generation, auth flow, token exchange |
| **credentials.py** | ✅ Complete | Secure token storage (~/.max-code/.credentials.json) |
| **token_manager.py** | ✅ Complete | Auto-refresh in background thread |
| **http_client.py** | ✅ Complete | HTTP client with Bearer token injection |
| **CLI commands** | ✅ Complete | login, logout, status, ask (test) |

---

## 🚀 Next Steps

### Short Term (This Week)

1. **Test OAuth flow end-to-end:**
   ```bash
   max-code login
   max-code ask "Test question"
   ```

2. **Verify auto-refresh:**
   - Wait ~11 hours
   - Run `max-code ask` again
   - Should auto-refresh without prompt

3. **Test with your Max x20 plan:**
   - Verify it uses your subscription
   - Check that API credits are NOT consumed

### Medium Term (Next 2 Weeks)

1. Implement Constitutional Core Engine (P1-P6 validators)
2. Implement DETER-AGENT Framework (5 layers)
3. Create `max-code fix` command (PENELOPE integration)
4. Create `max-code commit` command (NIS integration)

### Long Term (Next Month)

1. Full TRINITY integration (PENELOPE, MABA, NIS)
2. Plan Mode agent
3. Code Generator agent
4. Complete CLI with all commands

---

## 📞 Support

### If OAuth Doesn't Work

1. **Check logs:**
   ```bash
   # Enable debug mode
   export DEBUG=true
   max-code login
   ```

2. **Verify prerequisites:**
   - Python 3.11+
   - Network connectivity
   - Browser available
   - Claude.ai account with Max x20 plan

3. **Alternative: Use setup token:**
   ```bash
   claude setup-token
   export CLAUDE_CODE_OAUTH_TOKEN="..."
   ```

4. **Last resort: Use API key (consumes credits):**
   ```bash
   export ANTHROPIC_API_KEY="sk-ant-api..."
   ```

---

## 🎓 Documentation

- **OAuth Implementation:** [Investigation docs](../MAXIMUS\ AI/IMPLEMENTATION_GUIDE.md)
- **Architecture:** [Blueprint](./README.md)
- **Constitution:** `/home/juan/Downloads/CONSTITUIÇÃO_VÉRTICE_v3.0.md`
- **Research Paper:** `/media/juan/DATA1/projects/Max-Code/papers/MAX_CODE_PHD_PAPER.md`

---

## ✅ Testing Checklist

- [ ] Installation successful (`max-code --version`)
- [ ] OAuth login works (`max-code login`)
- [ ] Tokens saved (`max-code status` shows authenticated)
- [ ] Claude API call works (`max-code ask "test"`)
- [ ] Uses Max x20 plan (NO API credits consumed)
- [ ] Auto-refresh works (wait 11+ hours and test)
- [ ] Logout works (`max-code logout`)

---

**Built with ❤️ under Constitutional Governance**

*"Your Claude Max x20 plan, your code, no API credits wasted."*

---

**Ready to test? Run: `max-code login`** 🚀
