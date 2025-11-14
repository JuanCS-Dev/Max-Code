#!/bin/bash
# Max-Code CLI - Development Environment Setup
# Boris Cherny Standard: Make setup effortless
# "If it's hard to set up, you won't do it" - Boris Cherny

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

echo -e "${CYAN}╔══════════════════════════════════════════════════════════╗${NC}"
echo -e "${CYAN}║   MAX-CODE CLI - DEVELOPMENT ENVIRONMENT SETUP          ║${NC}"
echo -e "${CYAN}╚══════════════════════════════════════════════════════════╝${NC}"
echo ""

# Function to print status
print_status() {
    echo -e "${GREEN}✓${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC}  $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

print_step() {
    echo -e "\n${CYAN}→${NC} $1"
}

# Check Python version
print_step "Checking Python version..."
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
REQUIRED_VERSION="3.11"

if [[ "$(printf '%s\n' "$REQUIRED_VERSION" "$PYTHON_VERSION" | sort -V | head -n1)" == "$REQUIRED_VERSION" ]]; then
    print_status "Python $PYTHON_VERSION (>= $REQUIRED_VERSION required)"
else
    print_error "Python $PYTHON_VERSION is too old. Python >= $REQUIRED_VERSION required."
    exit 1
fi

# Upgrade pip
print_step "Upgrading pip..."
python3 -m pip install --upgrade pip --quiet

# Install production dependencies
print_step "Installing production dependencies..."
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt --quiet
    print_status "Production dependencies installed"
else
    print_warning "requirements.txt not found, skipping"
fi

# Install development dependencies
print_step "Installing development dependencies..."
if [ -f "requirements-dev.txt" ]; then
    pip install -r requirements-dev.txt --quiet
    print_status "Development dependencies installed"
else
    print_warning "requirements-dev.txt not found, skipping"
fi

# Install secure dependencies (optional)
print_step "Installing secure dependencies..."
if [ -f "requirements.secure.txt" ]; then
    echo -e "${YELLOW}Would you like to install security-hardened dependencies? (y/N)${NC}"
    read -r response
    if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
        pip install -r requirements.secure.txt --quiet
        print_status "Secure dependencies installed"
    else
        print_warning "Skipped secure dependencies (recommended for production)"
    fi
else
    print_warning "requirements.secure.txt not found, skipping"
fi

# Install pre-commit hooks
print_step "Installing pre-commit hooks..."
pip install pre-commit --quiet
cd .. && pre-commit install && cd max-code-cli || exit
print_status "Pre-commit hooks installed"

# Create necessary directories
print_step "Creating project directories..."
mkdir -p htmlcov
mkdir -p .pytest_cache
mkdir -p .mypy_cache
print_status "Directories created"

# Run initial tests to verify setup
print_step "Running initial tests..."
if pytest tests/ --tb=short -q 2>/dev/null; then
    print_status "Tests passed - setup verified!"
else
    print_warning "Some tests failed - check test output above"
fi

# Summary
echo ""
echo -e "${CYAN}╔══════════════════════════════════════════════════════════╗${NC}"
echo -e "${CYAN}║   SETUP COMPLETE!                                        ║${NC}"
echo -e "${CYAN}╚══════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${GREEN}✅ Development environment ready!${NC}"
echo ""
echo -e "${YELLOW}Quick Start:${NC}"
echo -e "  ${CYAN}make test${NC}          - Run tests"
echo -e "  ${CYAN}make lint${NC}          - Check code quality"
echo -e "  ${CYAN}make format${NC}        - Format code"
echo -e "  ${CYAN}make ci${NC}            - Run CI checks locally"
echo -e "  ${CYAN}make pre-push${NC}      - Validate before pushing"
echo ""
echo -e "${YELLOW}Or use the CLI:${NC}"
echo -e "  ${CYAN}max-code dev test${NC}       - Run tests"
echo -e "  ${CYAN}max-code dev lint${NC}       - Check code quality"
echo -e "  ${CYAN}max-code dev ci${NC}         - Run CI checks"
echo -e "  ${CYAN}max-code dev help-dev${NC}   - Show all dev commands"
echo ""
echo -e "${YELLOW}Documentation:${NC}"
echo -e "  ${CYAN}PHASE_4_SUMMARY.md${NC}  - CI/CD setup details"
echo -e "  ${CYAN}PHASE_3_SUMMARY.md${NC}  - Documentation standards"
echo -e "  ${CYAN}PHASE_2_SUMMARY.md${NC}  - Testing infrastructure"
echo ""
echo -e "${GREEN}Happy coding!${NC} 🚀"
echo ""
