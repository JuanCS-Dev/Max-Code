# DEBT-YYYY-MM-NNN: [Short Descriptive Title]

**ID:** DEBT-YYYY-MM-NNN
**Created:** YYYY-MM-DD
**Updated:** YYYY-MM-DD
**Status:** 📋 Registered
**Severity:** [🔴 P0 / 🟠 P1 / 🟡 P2 / 🟢 P3]

---

## Ownership & Tracking

| Field | Value |
|-------|-------|
| **Owner** | @username |
| **Service/Component** | services/[service-name] or max-code-cli/[component] |
| **Category** | [Code Quality / Architecture / Testing / Documentation / Performance / Security / Infrastructure] |
| **Estimated Effort** | X-Y days |
| **Actual Effort** | - (fill when resolved) |

---

## Description

### Problem Statement

Clear, concise description of the technical debt issue.

**Example:**
> The user authentication module uses synchronous database queries, causing the API to block on I/O operations. This results in poor performance under concurrent load and limits horizontal scalability.

### Current Behavior

What happens now (the problematic behavior):
- Describe current implementation
- Show code snippets if helpful
- Link to relevant files

### Desired Behavior

What should happen instead:
- Describe ideal implementation
- Reference best practices or patterns
- Link to examples in other services (if applicable)

---

## Impact Assessment

### User Impact
**Severity:** [None / Low / Medium / High / Critical]

Describe how this affects end users:
- Performance degradation?
- Feature limitations?
- Reliability issues?
- Security concerns?

### Business Impact
**Severity:** [None / Low / Medium / High / Critical]

Describe business consequences:
- Revenue impact?
- Compliance risks?
- Competitive disadvantage?
- Customer satisfaction?

### Technical Impact
**Severity:** [None / Low / Medium / High / Critical]

Describe technical consequences:
- Development velocity?
- Maintenance burden?
- Testing complexity?
- Deployment risks?

### Impact Score Matrix

| Factor | Weight | Score (1-5) | Weighted |
|--------|--------|-------------|----------|
| Security Impact | 30% | | |
| User/Business Impact | 25% | | |
| Technical Risk | 20% | | |
| Maintenance Burden | 15% | | |
| Team Velocity Impact | 10% | | |
| **TOTAL** | **100%** | | **X.XX** |

**Calculated Priority:** [Based on score]

---

## Root Cause Analysis

### Why This Debt Exists

Explain the context and reasons for the current situation:

**Common reasons:**
- [ ] Rapid prototyping / POC code that went to production
- [ ] Missing knowledge/expertise at implementation time
- [ ] Conscious trade-off for time-to-market
- [ ] Technology limitations at the time
- [ ] Evolving requirements made original design obsolete
- [ ] Inherited from legacy codebase
- [ ] Dependencies or third-party limitations
- [ ] Other: _______________

### Timeline

When was this code written and why?

```
YYYY-MM-DD: Original implementation (PR #XXX)
YYYY-MM-DD: First reported issue (#XXX)
YYYY-MM-DD: Debt item created
```

### Related Issues

- GitHub Issue: #XXX
- Related Debt: DEBT-YYYY-MM-XXX
- Original PR: #XXX
- Incident: INC-XXX (if applicable)

---

## Proposed Resolution

### Approach

Describe the recommended solution approach:

1. **Step 1:** [First step]
   - Details and considerations
   - Files affected: `path/to/file.py`

2. **Step 2:** [Second step]
   - Details and considerations
   - Dependencies on step 1

3. **Step 3:** [Third step]
   - Details and considerations

### Alternative Solutions Considered

**Option 1:** [Alternative approach]
- **Pros:** ...
- **Cons:** ...
- **Rejected because:** ...

**Option 2:** [Another alternative]
- **Pros:** ...
- **Cons:** ...
- **Rejected because:** ...

### Dependencies & Blockers

- [ ] Requires completion of DEBT-YYYY-MM-XXX
- [ ] Needs approval from [team/person]
- [ ] Waiting for library/framework update
- [ ] Requires infrastructure changes
- [ ] Other: _______________

### Risk Assessment

**Implementation Risks:**
- Risk 1: [Description] - Mitigation: [How to address]
- Risk 2: [Description] - Mitigation: [How to address]

**Rollback Plan:**
- How to revert if issues occur
- Rollback complexity: [Low / Medium / High]

---

## Success Criteria

### Functional Requirements

- [ ] Requirement 1
- [ ] Requirement 2
- [ ] Requirement 3

### Non-Functional Requirements

- [ ] Performance: [Specific metric, e.g., "Response time < 200ms"]
- [ ] Reliability: [Specific metric, e.g., "99.9% uptime"]
- [ ] Security: [Specific requirement]
- [ ] Scalability: [Specific requirement]

### Quality Gates

- [ ] All existing tests passing
- [ ] New tests added (coverage maintained/improved)
- [ ] Code review approved
- [ ] Linting passes with no new warnings
- [ ] Documentation updated
- [ ] Performance benchmarks meet targets
- [ ] Security scan passes
- [ ] Deployed to staging and validated
- [ ] Deployed to production successfully

### Acceptance Criteria

How will we know this is truly resolved?

```
GIVEN [context]
WHEN [action]
THEN [expected outcome]
```

---

## Implementation Progress

### Status History

| Date | Status | Notes |
|------|--------|-------|
| YYYY-MM-DD | 📋 Registered | Initial creation |
| | | |
| | | |

### Status Legend

- 📋 **Registered**: Debt item created
- 🎯 **Prioritized**: Severity assessed, added to backlog
- 📅 **Scheduled**: Added to sprint/iteration
- 🔄 **In Progress**: Active work happening
- 👀 **In Review**: PR created, awaiting approval
- ✅ **Resolved**: Merged to main
- ✔️ **Verified**: Validated in production
- ⏸️ **Deferred**: Postponed to future iteration
- ❌ **Won't Fix**: Consciously not addressing

### Current Status: [Status Icon] [Status Name]

**Details:**
- Last Updated: YYYY-MM-DD
- Current Owner: @username
- Blocker (if any): None / [Description]

---

## Work Log

### YYYY-MM-DD - @username

**Time Spent:** X hours

**Progress:**
- Completed: [What was done]
- In Progress: [What's being worked on]
- Next Steps: [What's coming next]

**Blockers:**
- None / [Description of blockers]

**Notes:**
- Any important observations or decisions

---

## Testing Plan

### Test Strategy

Describe how this will be tested:

1. **Unit Tests**
   - New tests to add
   - Existing tests to update
   - Coverage target: X%

2. **Integration Tests**
   - Scenarios to test
   - Services involved

3. **Performance Tests**
   - Benchmarks to run
   - Target metrics

4. **Manual Testing**
   - Steps to verify manually
   - Edge cases to check

### Test Cases

```markdown
**Test Case 1: [Description]**
- Given: [Preconditions]
- When: [Action]
- Then: [Expected result]

**Test Case 2: [Description]**
- Given: [Preconditions]
- When: [Action]
- Then: [Expected result]
```

---

## Documentation Updates

### Files to Update

- [ ] `README.md` - [What needs updating]
- [ ] `docs/architecture/[file].md` - [What needs updating]
- [ ] `docs/api-reference/[file].md` - [What needs updating]
- [ ] Code comments - [Where and what]
- [ ] Other: _______________

### New Documentation Needed

- [ ] Architecture decision record (ADR)
- [ ] Migration guide (if breaking change)
- [ ] Runbook updates
- [ ] Other: _______________

---

## Performance Metrics

### Before Resolution

```
Metric 1: [Value]
Metric 2: [Value]
Metric 3: [Value]
```

**Baseline Established:** YYYY-MM-DD
**Method:** [How measured]

### After Resolution

```
Metric 1: [Value] ([% change])
Metric 2: [Value] ([% change])
Metric 3: [Value] ([% change])
```

**Measured:** YYYY-MM-DD
**Method:** [How measured]

### Performance Comparison

| Metric | Before | After | Improvement |
|--------|--------|-------|-------------|
| Response Time | Xms | Yms | Z% |
| Throughput | X req/s | Y req/s | Z% |
| Memory Usage | X MB | Y MB | Z% |

---

## Resolution Summary

> **Note:** Fill this section when debt is resolved

### What Was Done

Brief summary of the resolution:
- Key changes made
- Approach used
- Surprises or deviations from plan

### Pull Requests

- PR #XXX: [Title] (merged YYYY-MM-DD)
- PR #XXX: [Title] (merged YYYY-MM-DD)

### Lessons Learned

**What Went Well:**
1. [Success 1]
2. [Success 2]

**What Could Be Improved:**
1. [Improvement 1]
2. [Improvement 2]

**Key Takeaways:**
1. [Lesson 1]
2. [Lesson 2]

### Recommendations

Based on this experience, recommend:
1. [Recommendation 1]
2. [Recommendation 2]

---

## Verification Checklist

- [ ] Code changes merged to main branch
- [ ] All tests passing in CI/CD
- [ ] Code coverage maintained/improved
- [ ] Performance benchmarks met
- [ ] Security scan passed
- [ ] Documentation updated
- [ ] Deployed to staging
- [ ] Validated in staging (X days)
- [ ] Deployed to production
- [ ] Monitored in production (X days)
- [ ] Metrics confirm resolution
- [ ] No regression issues reported
- [ ] Debt registry updated
- [ ] Success story documented (optional)

---

## References

### Code References

- File: `path/to/file.py:123` - [Description]
- File: `path/to/file.py:456` - [Description]

### Documentation

- [Related Architecture Doc](../path/to/doc.md)
- [Constitution Vértice v3.0](../governance/CONSTITUTION_VERTICE_v3.0.md)
- [Testing Strategy](../development/TESTING.md)

### External Resources

- [Article/Blog](https://example.com) - [Relevance]
- [Documentation](https://docs.example.com) - [Relevance]

---

## Comments & Discussion

### YYYY-MM-DD - @username

> Comment or question about the debt item

**Response (@another-user):**
> Response to comment

---

**Template Version:** 1.0.0
**Last Updated:** 2025-11-14
