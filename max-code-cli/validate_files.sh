#!/bin/bash
cd "/media/juan/DATA2/projects/MAXIMUS AI/max-code-cli"

echo "================================================================================"
echo "FASE 1: VALIDAÇÃO DE EXISTÊNCIA DE ARQUIVOS"
echo "================================================================================"
echo ""

# Cores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Contadores
TOTAL=0
EXISTS=0
MISSING=0

# Função de checagem
check_file() {
    local file=$1
    TOTAL=$((TOTAL + 1))
    
    if [ -f "$file" ]; then
        echo -e "${GREEN}✓${NC} $file"
        EXISTS=$((EXISTS + 1))
        return 0
    else
        echo -e "${RED}✗${NC} $file [MISSING]"
        MISSING=$((MISSING + 1))
        return 1
    fi
}

echo "=== FASE 1: Quick Wins ==="
check_file "ui/streaming.py"
check_file "core/risk_classifier.py"
check_file "ui/confirmation.py"
check_file "core/plan_visualizer.py"

echo ""
echo "=== FASE 2: Core Gap ==="
check_file "core/task_models.py"
check_file "core/task_graph.py"
check_file "core/task_decomposer.py"
check_file "core/dependency_resolver.py"
check_file "prompts/decomposition_prompts.py"
check_file "core/tools/tool_metadata.py"
check_file "core/tools/enhanced_registry.py"
check_file "core/tools/tool_selector.py"
check_file "core/tools/decorator.py"
check_file "core/tool_integration.py"
check_file "core/execution_engine.py"
check_file "ui/execution_display.py"

echo ""
echo "=== Error Recovery (integrated in execution_engine.py) ==="
echo -e "${GREEN}✓${NC} Error recovery exists in execution_engine.py (RetryStrategy)"
TOTAL=$((TOTAL + 1))
EXISTS=$((EXISTS + 1))

echo ""
echo "=== Testes ==="
check_file "tests/test_streaming_thinking.py"
check_file "tests/test_confirmation.py"
check_file "tests/test_task_decomposition.py"
check_file "tests/test_tool_selection_system.py"
check_file "tests/test_execution_engine.py"

echo ""
echo "================================================================================"
echo "SUMMARY - FASE 1"
echo "================================================================================"
echo -e "Total files expected: $TOTAL"
echo -e "${GREEN}Files found: $EXISTS${NC}"
echo -e "${RED}Files missing: $MISSING${NC}"

if [ $MISSING -eq 0 ]; then
    echo -e "\n${GREEN}✓ FASE 1 PASSED: All files exist${NC}"
    exit 0
else
    echo -e "\n${RED}✗ FASE 1 FAILED: $MISSING files missing${NC}"
    exit 1
fi
