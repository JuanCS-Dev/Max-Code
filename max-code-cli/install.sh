#!/usr/bin/env bash
#
# MAX-CODE CLI - Installer
# Install MAX-CODE globally on your system
#

set -e

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

echo -e "${CYAN}"
echo "╔═══════════════════════════════════════╗"
echo "║   MAX-CODE CLI - Global Installer    ║"
echo "║   Constitutional AI Assistant         ║"
echo "╚═══════════════════════════════════════╝"
echo -e "${NC}"

# Check if running as root (we don't want that)
if [ "$EUID" -eq 0 ]; then
    echo -e "${YELLOW}Warning: Don't run as root${NC}"
    echo "Run as regular user instead"
    exit 1
fi

# Get installation directory
INSTALL_DIR="${HOME}/.max-code"

echo -e "${CYAN}Installation directory: ${INSTALL_DIR}${NC}"

# Create directory
mkdir -p "$INSTALL_DIR"

# Copy files
echo "Copying files..."
cp -r cli core agents ui config bin requirements.txt README.md CLAUDE.md "$INSTALL_DIR/" 2>/dev/null || true

# Install Python dependencies
echo "Installing Python dependencies..."
cd "$INSTALL_DIR"
pip install -r requirements.txt --quiet

# Create symlink
SYMLINK_DIR="${HOME}/.local/bin"
mkdir -p "$SYMLINK_DIR"

if [ -L "${SYMLINK_DIR}/max-code" ]; then
    rm "${SYMLINK_DIR}/max-code"
fi

ln -s "${INSTALL_DIR}/bin/max-code" "${SYMLINK_DIR}/max-code"

# Add to PATH if not already there
SHELL_RC="${HOME}/.bashrc"
if [ -f "${HOME}/.zshrc" ]; then
    SHELL_RC="${HOME}/.zshrc"
fi

if ! grep -q "${SYMLINK_DIR}" "$SHELL_RC" 2>/dev/null; then
    echo "" >> "$SHELL_RC"
    echo "# MAX-CODE CLI" >> "$SHELL_RC"
    echo "export PATH=\"\${HOME}/.local/bin:\$PATH\"" >> "$SHELL_RC"
    echo -e "${YELLOW}Added to PATH in ${SHELL_RC}${NC}"
    echo -e "${YELLOW}Run: source ${SHELL_RC}${NC}"
fi

echo ""
echo -e "${GREEN}✓ MAX-CODE CLI installed successfully!${NC}"
echo ""
echo "Usage:"
echo "  max-code              # Start interactive shell"
echo "  max-code --help       # Show help"
echo "  max-code --version    # Show version"
echo ""
echo "Configuration:"
echo "  export ANTHROPIC_API_KEY='your-key-here'"
echo ""
echo -e "${CYAN}Happy coding! Soli Deo Gloria 🙏${NC}"
