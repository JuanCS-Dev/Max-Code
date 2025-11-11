---
name: deploy
description: Deploy application to production or staging
args: [environment]
---

Deploy the MAX-CODE application to {{ environment }} environment.

**Deployment Checklist:**

1. **Pre-deployment validation:**
   - Run all tests (pytest tests/ -v)
   - Check code quality (linting, type checking)
   - Review recent commits
   - Verify environment configuration

2. **Build and package:**
   - Build Docker image if needed
   - Tag release version
   - Update CHANGELOG.md

3. **Deploy to {{ environment }}:**
   - Push Docker image to registry
   - Update Kubernetes manifests
   - Apply deployment
   - Verify pods are running

4. **Post-deployment verification:**
   - Health check endpoints
   - Run smoke tests
   - Monitor logs for errors
   - Update deployment documentation

Please execute these deployment steps carefully and report any issues.

**Target Environment:** {{ environment }}
**Deployment Type:** Automated with safety checks

Soli Deo Gloria 🙏
