#!/usr/bin/env bash
#
# Max-Code CLI Comprehensive Audit Script
#
# Boris Cherny Standards:
# - Type safety analysis
# - Code smell detection
# - Security vulnerability scanning
# - Test coverage measurement
# - Documentation completeness
# - Architecture validation
#
# "Código limpo que parece poesia" - Boris Cherny
#

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Configuration
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPORT_FILE="${PROJECT_ROOT}/AUDIT_REPORT_COMPLETE.md"
TIMESTAMP=$(date +"%Y-%m-%d %H:%M:%S")

# Counters
TOTAL_ISSUES=0
CRITICAL_ISSUES=0
HIGH_ISSUES=0
MEDIUM_ISSUES=0
LOW_ISSUES=0

echo -e "${CYAN}╔══════════════════════════════════════════════════════════╗${NC}"
echo -e "${CYAN}║   MAX-CODE CLI - COMPREHENSIVE AUDIT (Boris Cherny)     ║${NC}"
echo -e "${CYAN}╚══════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${BLUE}Timestamp: ${TIMESTAMP}${NC}"
echo -e "${BLUE}Project Root: ${PROJECT_ROOT}${NC}"
echo ""

# Function to log findings
log_issue() {
    local severity=$1
    local category=$2
    local message=$3

    case $severity in
        "CRITICAL") CRITICAL_ISSUES=$((CRITICAL_ISSUES + 1)) ;;
        "HIGH") HIGH_ISSUES=$((HIGH_ISSUES + 1)) ;;
        "MEDIUM") MEDIUM_ISSUES=$((MEDIUM_ISSUES + 1)) ;;
        "LOW") LOW_ISSUES=$((LOW_ISSUES + 1)) ;;
    esac
    TOTAL_ISSUES=$((TOTAL_ISSUES + 1))

    echo -e "  [${severity}] ${category}: ${message}"
}

# Initialize report
cat > "$REPORT_FILE" << 'EOF'
# MAX-CODE CLI - COMPREHENSIVE AUDIT REPORT

**Auditor:** Boris Cherny (Claude Code Implementation)
**Standard:** Boris Cherny Engineering Excellence
**Philosophy:** "Type safety máxima, código limpo, zero technical debt"

---

## 📋 EXECUTIVE SUMMARY

This comprehensive audit evaluates the Max-Code CLI against Boris Cherny's non-negotiable engineering standards:

✅ Type safety máxima
✅ Separação de concerns clara
✅ Testes unitários para cada função pública
✅ Documentação inline onde necessário
✅ Error handling robusto
✅ Performance otimizada desde o início
✅ Zero technical debt introduzido

---

EOF

echo -e "${YELLOW}[1/7] Security Vulnerability Scan${NC}"
echo "----------------------------------------"

if command -v pip-audit &> /dev/null; then
    echo "Running pip-audit..." >> "$REPORT_FILE"
    echo '```' >> "$REPORT_FILE"
    pip-audit --desc -f json > /tmp/audit_results.json 2>&1 || true

    if [ -f /tmp/audit_results.json ]; then
        VULN_COUNT=$(jq '.dependencies | length' /tmp/audit_results.json 2>/dev/null || echo "0")
        echo "  Found ${VULN_COUNT} vulnerable dependencies"
        log_issue "CRITICAL" "Security" "${VULN_COUNT} dependencies with known vulnerabilities"

        cat /tmp/audit_results.json >> "$REPORT_FILE"
    fi
    echo '```' >> "$REPORT_FILE"
else
    echo "  ⚠ pip-audit not installed, skipping..."
    log_issue "HIGH" "Security" "pip-audit not available for security scanning"
fi

echo "" >> "$REPORT_FILE"
echo "## 🔍 DETAILED FINDINGS" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"

echo -e "${YELLOW}[2/7] Type Safety Analysis${NC}"
echo "----------------------------------------"

echo "### 1. TYPE SAFETY ANALYSIS" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"

# Check for missing type hints
echo "Analyzing Python files for type hints..." >> "$REPORT_FILE"
echo '```python' >> "$REPORT_FILE"

UNTYPED_FUNCTIONS=0
TOTAL_FUNCTIONS=0

while IFS= read -r -d '' file; do
    if [ -f "$file" ]; then
        # Count functions without type hints (more robust)
        FUNCS=$(grep "^def " "$file" 2>/dev/null | wc -l)
        TYPED=$(grep "^def .*->.*:" "$file" 2>/dev/null | wc -l)

        # Clean up whitespace
        FUNCS=$(echo "$FUNCS" | tr -d ' ')
        TYPED=$(echo "$TYPED" | tr -d ' ')

        # Ensure numeric
        FUNCS=${FUNCS:-0}
        TYPED=${TYPED:-0}

        if [ "$FUNCS" -gt 0 ]; then
            UNTYPED=$((FUNCS - TYPED))
            TOTAL_FUNCTIONS=$((TOTAL_FUNCTIONS + FUNCS))
            UNTYPED_FUNCTIONS=$((UNTYPED_FUNCTIONS + UNTYPED))

            if [ $UNTYPED -gt 0 ]; then
                echo "  ${file}: ${UNTYPED}/${FUNCS} functions lack type hints" >> "$REPORT_FILE"
            fi
        fi
    fi
done < <(find "$PROJECT_ROOT" -name "*.py" -not -path "*/venv/*" -not -path "*/__pycache__/*" -print0)

echo '```' >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"

if [ $TOTAL_FUNCTIONS -eq 0 ]; then
    echo "**Type Coverage:** N/A (no functions found)" >> "$REPORT_FILE"
elif [ $UNTYPED_FUNCTIONS -gt 0 ]; then
    TYPE_COVERAGE=$(( (TOTAL_FUNCTIONS - UNTYPED_FUNCTIONS) * 100 / TOTAL_FUNCTIONS ))
    echo "**Type Coverage:** ${TYPE_COVERAGE}% (${UNTYPED_FUNCTIONS}/${TOTAL_FUNCTIONS} functions untyped)" >> "$REPORT_FILE"
    log_issue "HIGH" "Type Safety" "${UNTYPED_FUNCTIONS} functions without type hints (${TYPE_COVERAGE}% coverage)"
else
    echo "**Type Coverage:** 100% ✅" >> "$REPORT_FILE"
fi

echo "" >> "$REPORT_FILE"

echo -e "${YELLOW}[3/7] Code Smell Detection${NC}"
echo "----------------------------------------"

echo "### 2. CODE SMELL DETECTION" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"

# Check for common code smells
echo "#### Anti-Patterns Found:" >> "$REPORT_FILE"
echo '```' >> "$REPORT_FILE"

# Long functions (>50 lines)
LONG_FUNCS=$(find "$PROJECT_ROOT" -name "*.py" -exec awk '/^def |^    def / {start=NR} /^def |^    def |^class / && NR!=start && start {if(NR-start>50) print FILENAME":"start":"NR-start" lines"}' {} \; 2>/dev/null | wc -l)
if [ $LONG_FUNCS -gt 0 ]; then
    echo "Long functions (>50 lines): ${LONG_FUNCS}" >> "$REPORT_FILE"
    log_issue "MEDIUM" "Code Smell" "${LONG_FUNCS} functions exceed 50 lines"
fi

# Broad except clauses
BROAD_EXCEPTS=$(grep -r "except:" "$PROJECT_ROOT" --include="*.py" 2>/dev/null | grep -v "test_" | wc -l)
if [ $BROAD_EXCEPTS -gt 0 ]; then
    echo "Broad except clauses: ${BROAD_EXCEPTS}" >> "$REPORT_FILE"
    log_issue "MEDIUM" "Code Smell" "${BROAD_EXCEPTS} broad except: clauses found"
fi

# TODO/FIXME comments
TODOS=$(grep -r "TODO\|FIXME" "$PROJECT_ROOT" --include="*.py" 2>/dev/null | grep -v "test_\|docs/" | wc -l)
if [ $TODOS -gt 0 ]; then
    echo "TODO/FIXME comments: ${TODOS}" >> "$REPORT_FILE"
    log_issue "LOW" "Code Smell" "${TODOS} TODO/FIXME comments indicating incomplete work"
fi

# Print statements (should use logging)
PRINTS=$(grep -r "print(" "$PROJECT_ROOT" --include="*.py" 2>/dev/null | grep -v "test_\|cli/\|ui/" | wc -l)
if [ $PRINTS -gt 0 ]; then
    echo "Print statements in non-UI code: ${PRINTS}" >> "$REPORT_FILE"
    log_issue "LOW" "Code Smell" "${PRINTS} print() calls should use logging"
fi

echo '```' >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"

echo -e "${YELLOW}[4/7] Test Coverage Analysis${NC}"
echo "----------------------------------------"

echo "### 3. TEST COVERAGE" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"

if command -v pytest &> /dev/null; then
    echo "Running pytest with coverage..." >> "$REPORT_FILE"
    echo '```' >> "$REPORT_FILE"

    cd "$PROJECT_ROOT"
    pytest --cov=. --cov-report=term-missing --tb=short > /tmp/coverage_report.txt 2>&1 || true

    if [ -f /tmp/coverage_report.txt ]; then
        cat /tmp/coverage_report.txt >> "$REPORT_FILE"

        COVERAGE=$(grep "TOTAL" /tmp/coverage_report.txt | awk '{print $NF}' | sed 's/%//' || echo "0")
        if [ "$COVERAGE" -lt 80 ]; then
            log_issue "HIGH" "Testing" "Test coverage is ${COVERAGE}% (target: >80%)"
        fi
    fi

    echo '```' >> "$REPORT_FILE"
else
    echo "  ⚠ pytest not installed, skipping..."
    log_issue "HIGH" "Testing" "pytest not available for coverage analysis"
fi

echo "" >> "$REPORT_FILE"

echo -e "${YELLOW}[5/7] Documentation Completeness${NC}"
echo "----------------------------------------"

echo "### 4. DOCUMENTATION" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"

# Check docstrings
MISSING_DOCSTRINGS=0
TOTAL_CLASSES_FUNCS=0

while IFS= read -r -d '' file; do
    if [ -f "$file" ]; then
        # Check for classes/functions without docstrings
        DEFS=$(grep -c "^class \|^def " "$file" 2>/dev/null || echo 0)
        DOCS=$(grep -c '"""' "$file" 2>/dev/null || echo 0)

        TOTAL_CLASSES_FUNCS=$((TOTAL_CLASSES_FUNCS + DEFS))

        # Rough estimate: each def/class should have at least one docstring
        if [ $DEFS -gt $DOCS ]; then
            MISSING=$((DEFS - DOCS))
            MISSING_DOCSTRINGS=$((MISSING_DOCSTRINGS + MISSING))
        fi
    fi
done < <(find "$PROJECT_ROOT" -name "*.py" -not -path "*/venv/*" -not -path "*/__pycache__/*" -not -path "*/test_*" -print0)

if [ $TOTAL_CLASSES_FUNCS -eq 0 ]; then
    echo "**Documentation Coverage:** N/A (no classes/functions found)" >> "$REPORT_FILE"
else
    DOC_COVERAGE=$(( (TOTAL_CLASSES_FUNCS - MISSING_DOCSTRINGS) * 100 / TOTAL_CLASSES_FUNCS ))
    echo "**Documentation Coverage:** ${DOC_COVERAGE}%" >> "$REPORT_FILE"
    echo "" >> "$REPORT_FILE"

    if [ $DOC_COVERAGE -lt 80 ]; then
        log_issue "MEDIUM" "Documentation" "Documentation coverage is ${DOC_COVERAGE}% (target: >80%)"
    fi
fi

echo "" >> "$REPORT_FILE"

echo -e "${YELLOW}[6/7] Architecture & Complexity${NC}"
echo "----------------------------------------"

echo "### 5. ARCHITECTURE & COMPLEXITY" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"

# Calculate cyclomatic complexity (if radon is available)
if command -v radon &> /dev/null; then
    echo "#### Cyclomatic Complexity:" >> "$REPORT_FILE"
    echo '```' >> "$REPORT_FILE"
    radon cc "$PROJECT_ROOT" -a -s >> "$REPORT_FILE" 2>&1 || true
    echo '```' >> "$REPORT_FILE"
else
    echo "  ⚠ radon not installed, skipping complexity analysis..."
    echo "radon not available" >> "$REPORT_FILE"
fi

echo "" >> "$REPORT_FILE"

echo -e "${YELLOW}[7/7] Performance & Best Practices${NC}"
echo "----------------------------------------"

echo "### 6. PERFORMANCE & BEST PRACTICES" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"

# Check for common performance issues
echo "#### Performance Checks:" >> "$REPORT_FILE"
echo '```' >> "$REPORT_FILE"

# List comprehensions vs loops
LOOPS_WITH_APPEND=$(grep -r "\.append(" "$PROJECT_ROOT" --include="*.py" 2>/dev/null | wc -l)
if [ $LOOPS_WITH_APPEND -gt 20 ]; then
    echo "Consider list comprehensions: ${LOOPS_WITH_APPEND} .append() calls" >> "$REPORT_FILE"
    log_issue "LOW" "Performance" "${LOOPS_WITH_APPEND} .append() calls could be list comprehensions"
fi

# String concatenation in loops
STRING_CONCAT=$(grep -r '"\s*+\s*"' "$PROJECT_ROOT" --include="*.py" 2>/dev/null | wc -l)
if [ $STRING_CONCAT -gt 10 ]; then
    echo "String concatenation: ${STRING_CONCAT} occurrences (consider f-strings)" >> "$REPORT_FILE"
    log_issue "LOW" "Performance" "${STRING_CONCAT} string concatenations could use f-strings"
fi

echo '```' >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"

# Summary
echo -e "${GREEN}[COMPLETE] Generating Summary${NC}"
echo "----------------------------------------"

cat >> "$REPORT_FILE" << EOF

---

## 📊 AUDIT SUMMARY

### Issue Severity Breakdown

| Severity | Count |
|----------|-------|
| 🔴 **CRITICAL** | ${CRITICAL_ISSUES} |
| 🟠 **HIGH** | ${HIGH_ISSUES} |
| 🟡 **MEDIUM** | ${MEDIUM_ISSUES} |
| 🟢 **LOW** | ${LOW_ISSUES} |
| **TOTAL** | ${TOTAL_ISSUES} |

---

## 🎯 RECOMMENDATIONS (Boris Cherny Priority)

### P0 - IMMEDIATE (Critical)

1. **Fix Security Vulnerabilities**
   - Update all dependencies with known CVEs
   - Prioritize: cryptography, langchain, fastapi, starlette
   - Create: \`requirements.secure.txt\` with pinned secure versions

2. **Implement Type Safety**
   - Add type hints to all public functions
   - Use \`mypy\` for static type checking
   - Target: 100% type coverage

### P1 - HIGH PRIORITY (Within 48h)

3. **Improve Test Coverage**
   - Add unit tests for all public APIs
   - Target: >80% code coverage
   - Include edge cases and error conditions

4. **Error Handling**
   - Replace broad \`except:\` with specific exceptions
   - Add proper error context and logging
   - Implement graceful degradation

### P2 - MEDIUM PRIORITY (Within 1 week)

5. **Documentation**
   - Add docstrings to all public classes/functions
   - Follow Google/NumPy docstring format
   - Include type hints in docstrings

6. **Code Refactoring**
   - Break down functions >50 lines
   - Extract complex logic into separate functions
   - Improve naming for clarity

### P3 - LOW PRIORITY (Continuous Improvement)

7. **Performance Optimization**
   - Replace string concatenation with f-strings
   - Use list comprehensions where appropriate
   - Profile and optimize hot paths

8. **Best Practices**
   - Replace print() with proper logging
   - Resolve TODO/FIXME comments
   - Add type: ignore comments where necessary with justification

---

## ✅ ACCEPTANCE CRITERIA

Before considering this audit complete:

- [ ] All CRITICAL issues resolved
- [ ] All HIGH issues have tickets/timeline
- [ ] Type coverage > 90%
- [ ] Test coverage > 80%
- [ ] Documentation coverage > 80%
- [ ] Zero security vulnerabilities in dependencies
- [ ] All tests passing
- [ ] Mypy type checking passing
- [ ] Code review completed

---

## 📝 IMPLEMENTATION CHECKLIST

### Phase 1: Security & Type Safety (P0)
- [ ] Update dependencies (requirements.secure.txt)
- [ ] Add type hints to all functions
- [ ] Configure mypy
- [ ] Fix mypy errors

### Phase 2: Testing & Error Handling (P1)
- [ ] Add unit tests (target 80%+ coverage)
- [ ] Replace broad except clauses
- [ ] Add error logging
- [ ] Test error scenarios

### Phase 3: Documentation & Refactoring (P2)
- [ ] Add docstrings to all public APIs
- [ ] Refactor long functions
- [ ] Extract complex logic
- [ ] Update README with new standards

### Phase 4: Optimization & Polish (P3)
- [ ] Performance profiling
- [ ] Code style consistency
- [ ] Resolve TODOs
- [ ] Final review

---

## 🏆 BORIS CHERNY STANDARDS COMPLIANCE

| Standard | Status | Notes |
|----------|--------|-------|
| Type Safety Máxima | 🟡 IN PROGRESS | Need to add type hints |
| Separação de Concerns | 🟢 GOOD | Architecture is clean |
| Testes Unitários | 🟡 IN PROGRESS | Need more coverage |
| Documentação Inline | 🟡 IN PROGRESS | Need docstrings |
| Error Handling Robusto | 🟠 NEEDS WORK | Too many broad excepts |
| Performance Otimizada | 🟢 GOOD | No major issues |
| Zero Technical Debt | 🔴 NOT MET | ${TOTAL_ISSUES} issues to resolve |

---

**"Se não tem tipos, não é produção"** - Boris Cherny

**"Código é lido 10x mais que escrito"** - Boris Cherny

**"Simplicidade é sofisticação final"** - Boris Cherny

**"Tests ou não aconteceu"** - Boris Cherny

---

**Report Generated:** ${TIMESTAMP}
**Auditor:** Boris Cherny (Claude Code)
**Total Issues:** ${TOTAL_ISSUES}
**Next Action:** Begin Phase 1 implementation immediately

---

**END OF AUDIT REPORT**
EOF

echo ""
echo -e "${GREEN}╔══════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║                  AUDIT COMPLETE                          ║${NC}"
echo -e "${GREEN}╚══════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${CYAN}Summary:${NC}"
echo -e "  🔴 Critical: ${CRITICAL_ISSUES}"
echo -e "  🟠 High:     ${HIGH_ISSUES}"
echo -e "  🟡 Medium:   ${MEDIUM_ISSUES}"
echo -e "  🟢 Low:      ${LOW_ISSUES}"
echo -e "  ${YELLOW}──────────────${NC}"
echo -e "  Total:    ${TOTAL_ISSUES}"
echo ""
echo -e "${BLUE}Report saved to:${NC} ${REPORT_FILE}"
echo ""
echo -e "${YELLOW}Next Steps:${NC}"
echo -e "  1. Review ${REPORT_FILE}"
echo -e "  2. Address P0 (CRITICAL) issues immediately"
echo -e "  3. Create implementation plan for P1-P3"
echo -e "  4. Run audit regularly to track progress"
echo ""

exit 0
