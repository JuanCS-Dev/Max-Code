#!/bin/bash
# MAXIMUS AI - Test All Services
# Runs complete test suite

set -e

PROJECT_ROOT="/media/juan/DATA1/projects/MAXIMUS AI"
cd "$PROJECT_ROOT"

echo "🧪 MAXIMUS AI - Complete Test Suite"
echo "================================================"
echo ""

SERVICES=("core" "penelope" "maba" "nis" "orchestrator" "eureka" "oraculo" "dlq_monitor")

total_passed=0
total_failed=0
total_services=0

for service in "${SERVICES[@]}"; do
    service_dir="services/$service"

    if [ ! -d "$service_dir" ]; then
        echo "⚠️  Service directory not found: $service_dir"
        continue
    fi

    if [ ! -f "$service_dir/requirements.txt" ]; then
        echo "⚠️  No requirements.txt found for $service, skipping..."
        continue
    fi

    echo "================================================"
    echo "Testing: $service"
    echo "================================================"
    echo ""

    cd "$service_dir"

    # Check if tests directory exists
    if [ ! -d "tests" ]; then
        echo "⚠️  No tests directory found for $service"
        cd "$PROJECT_ROOT"
        continue
    fi

    # Install dependencies in virtual environment
    if [ ! -d ".venv" ]; then
        echo "Creating virtual environment..."
        python3 -m venv .venv
    fi

    source .venv/bin/activate

    echo "Installing dependencies..."
    pip install -q --upgrade pip
    pip install -q -r requirements.txt
    pip install -q pytest pytest-cov pytest-asyncio

    # Set PYTHONPATH to include libs
    export PYTHONPATH="$PROJECT_ROOT:$PROJECT_ROOT/libs:$PYTHONPATH"

    # Run tests
    echo ""
    echo "Running tests..."
    if pytest -v --tb=short 2>&1 | tee test_output.log; then
        passed=$(grep -c "PASSED" test_output.log || echo "0")
        total_passed=$((total_passed + passed))
        echo "✅ $service: $passed tests passed"
    else
        failed=$(grep -c "FAILED" test_output.log || echo "0")
        total_failed=$((total_failed + failed))
        echo "❌ $service: $failed tests failed"
    fi

    deactivate
    cd "$PROJECT_ROOT"
    echo ""

    total_services=$((total_services + 1))
done

echo "================================================"
echo "📊 Test Summary"
echo "================================================"
echo ""
echo "Services tested: $total_services"
echo "Total passed: $total_passed"
echo "Total failed: $total_failed"
echo ""

if [ $total_failed -eq 0 ]; then
    echo "✅ ALL TESTS PASSED!"
    exit 0
else
    echo "❌ SOME TESTS FAILED"
    exit 1
fi
