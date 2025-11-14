# Technical Debt Management

Welcome to the Max-Code Technical Debt Management System.

---

## Quick Start

### Viewing Current Debt

📊 **[View Debt Registry →](./DEBT_REGISTRY.md)**

See all active, resolved, and deferred technical debt items.

### Creating a New Debt Item

1. **Copy the template:**
   ```bash
   # Get next available number (e.g., 001)
   cp docs/debt-management/templates/DEBT_ITEM_TEMPLATE.md \
      docs/debt-management/items/DEBT-2025-11-001.md
   ```

2. **Fill in all sections** in the debt item file

3. **Add entry to registry:**
   - Edit `DEBT_REGISTRY.md`
   - Add item under appropriate severity section
   - Update quick stats

4. **Commit changes:**
   ```bash
   git add docs/debt-management/
   git commit -m "docs(debt): Add DEBT-2025-11-001 - [short description]"
   git push
   ```

### Understanding the System

📖 **[Read Full Documentation →](./DEBT_TRACKING.md)**

Comprehensive guide covering:
- Debt classification and prioritization
- Resolution workflows and SLAs
- Metrics and reporting
- Best practices

---

## Directory Structure

```
docs/debt-management/
├── README.md                    # This file - Quick start guide
├── DEBT_TRACKING.md            # Complete system documentation
├── DEBT_REGISTRY.md            # Central registry of all debt items
│
├── templates/                  # Templates for creating new items
│   └── DEBT_ITEM_TEMPLATE.md  # Template for debt items
│
├── items/                      # Individual debt item files
│   ├── DEBT-2025-11-EXAMPLE.md # Example debt item (reference)
│   └── DEBT-YYYY-MM-NNN.md    # Real debt items go here
│
└── archive/                    # Resolved items (optional)
    └── YYYY/                   # Organized by year
        └── MM/                 # Organized by month
```

---

## Quick Reference

### Severity Levels

| Severity | Resolution Time | Criteria |
|----------|----------------|----------|
| 🔴 **P0 - Critical** | 0-7 days | Security vulnerabilities, production blockers, data loss risks |
| 🟠 **P1 - High** | 2-4 weeks | Performance degradation >30%, significant duplication, missing critical tests |
| 🟡 **P2 - Medium** | 1-3 months | Code smells, moderate duplication, missing docs, refactoring opportunities |
| 🟢 **P3 - Low** | 3-6 months | Minor improvements, optimizations, nice-to-have refactoring |

### Debt States

- 📋 **Registered** - Item created and documented
- 🎯 **Prioritized** - Severity assessed, in backlog
- 📅 **Scheduled** - Added to sprint/iteration
- 🔄 **In Progress** - Active work happening
- 👀 **In Review** - PR created, awaiting approval
- ✅ **Resolved** - Changes merged
- ✔️ **Verified** - Validated in production
- ⏸️ **Deferred** - Postponed
- ❌ **Won't Fix** - Consciously not addressing

### Common Commands

```bash
# View all active debt items
cat docs/debt-management/DEBT_REGISTRY.md

# Search for debt items by keyword
grep -i "performance" docs/debt-management/items/*.md

# Count debt items by severity
grep -c "🔴 P0" docs/debt-management/DEBT_REGISTRY.md
grep -c "🟠 P1" docs/debt-management/DEBT_REGISTRY.md
grep -c "🟡 P2" docs/debt-management/DEBT_REGISTRY.md
grep -c "🟢 P3" docs/debt-management/DEBT_REGISTRY.md

# Find oldest debt items
ls -lt docs/debt-management/items/
```

---

## Workflow Summary

### 1. Identify Debt

Debt can be identified from:
- Code reviews
- Automated tools (linters, security scanners)
- Incident post-mortems
- Architecture reviews
- Developer feedback
- Metrics monitoring

### 2. Create Debt Item

Use the template and fill in:
- Clear description
- Impact assessment
- Root cause
- Proposed resolution
- Success criteria

### 3. Prioritize

Assess severity using:
- Impact score matrix
- Decision tree
- Team discussion

### 4. Schedule

Add to:
- Sprint backlog (P0-P1)
- Product backlog (P2-P3)
- Technical debt allocation (~20% capacity)

### 5. Resolve

Follow the resolution workflow:
1. Implement solution
2. Write/update tests
3. Code review
4. Deploy to staging
5. Validate
6. Deploy to production
7. Monitor

### 6. Verify

Ensure:
- Tests pass
- Metrics improve
- No regressions
- Documentation updated

---

## Key Metrics

Track these metrics regularly:

1. **Debt Inventory** - Total count by severity
2. **Debt Age** - Average age by severity
3. **Resolution Velocity** - Items resolved per sprint
4. **SLA Compliance** - % resolved within SLA
5. **Debt Ratio** - % of engineering time on debt

**Target:** Resolution rate > Creation rate

---

## Integration Points

### CI/CD Pipeline

```yaml
# Automated debt detection
- Linting violations → Create debt item (if threshold exceeded)
- Security vulnerabilities → Auto-create P0 debt item
- Coverage drops → Create debt item
```

### Code Review

```markdown
## PR Checklist
- [ ] No new technical debt introduced
- [ ] Related debt items updated
- [ ] Debt resolved (if applicable)
```

### Monitoring

```javascript
// Auto-create debt items for production issues
if (errorRate > threshold) {
  createDebtItem({ severity: 'P0', ... })
}
```

---

## Best Practices

### DO ✅

- **Be specific:** Use metrics, percentages, concrete examples
- **Quantify impact:** Show user/business/technical impact
- **Document context:** Why does this debt exist?
- **Link evidence:** Screenshots, logs, profiler reports
- **Update regularly:** Status changes, new findings
- **Celebrate resolution:** Document success stories

### DON'T ❌

- Create debt items for features (use feature requests)
- Use vague descriptions ("code is messy")
- Skip impact assessment
- Leave debt items without owners
- Forget to update status
- Let debt items go stale

---

## Examples

### Good Debt Item Title

✅ "Synchronous database queries in UserService causing 40% performance degradation"

### Bad Debt Item Title

❌ "Fix user service"

### Good Impact Description

✅ "Response time averages 800ms (target: 200ms) under load. Affects 10K+ daily users. Blocks horizontal scaling."

### Bad Impact Description

❌ "It's slow"

---

## Review Schedule

- **Daily:** P0 status updates (if any)
- **Weekly:** Debt triage meeting (30 min)
- **Monthly:** Comprehensive debt review (60 min)
- **Quarterly:** Strategic debt planning (90 min)

---

## Resources

### Documentation

- **[DEBT_TRACKING.md](./DEBT_TRACKING.md)** - Complete system documentation
- **[DEBT_REGISTRY.md](./DEBT_REGISTRY.md)** - Central debt registry
- **[Constitution Vértice v3.0](../governance/CONSTITUTION_VERTICE_v3.0.md)** - Governing principles

### Templates

- **[DEBT_ITEM_TEMPLATE.md](./templates/DEBT_ITEM_TEMPLATE.md)** - Template for creating debt items

### Examples

- **[DEBT-2025-11-EXAMPLE.md](./items/DEBT-2025-11-EXAMPLE.md)** - Example debt item

---

## Support

### Questions?

1. Check the [DEBT_TRACKING.md](./DEBT_TRACKING.md) documentation
2. Review the [example debt item](./items/DEBT-2025-11-EXAMPLE.md)
3. Ask in team chat or engineering meeting
4. Submit a GitHub issue

### Suggestions?

We welcome improvements to this system:

1. Submit a PR with your proposed changes
2. Discuss in the monthly debt review
3. Create a GitHub issue for discussion

---

## Philosophy

> "Debt acknowledged is debt that can be resolved. Debt ignored is debt that accumulates interest."
>
> — Max-Code Engineering Philosophy

Technical debt is not a failure. It's a conscious trade-off that must be:
- **Tracked** - We know it exists
- **Understood** - We know why and the impact
- **Prioritized** - We know when to address it
- **Resolved** - We systematically eliminate it

---

## Current Status

**As of 2025-11-14:**

- 🔴 **P0:** 0 items
- 🟠 **P1:** 0 items
- 🟡 **P2:** 0 items
- 🟢 **P3:** 0 items

**Total:** 0 active debt items

**Status:** 🟢 Excellent - Clean slate!

*Let's keep it that way by identifying and resolving debt proactively.*

---

## Quick Links

- [View All Debt Items →](./DEBT_REGISTRY.md)
- [Create New Debt Item →](./templates/DEBT_ITEM_TEMPLATE.md)
- [Full Documentation →](./DEBT_TRACKING.md)
- [Example Debt Item →](./items/DEBT-2025-11-EXAMPLE.md)

---

**Last Updated:** 2025-11-14
**Version:** 1.0.0
