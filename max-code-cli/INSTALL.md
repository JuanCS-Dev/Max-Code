# MAX-CODE CLI - Installation Guide

## Quick Install

```bash
# Clone repository
git clone https://github.com/yourusername/max-code-cli
cd max-code-cli

# Run installer
./install.sh

# Set API key
export ANTHROPIC_API_KEY="your-key-here"

# Use it!
max-code
```

## What the Installer Does

1. Copies MAX-CODE to `~/.max-code/`
2. Installs Python dependencies
3. Creates symlink in `~/.local/bin/max-code`
4. Adds `~/.local/bin` to your PATH

## Manual Installation

```bash
# 1. Copy to home directory
cp -r max-code-cli ~/.max-code

# 2. Install dependencies
cd ~/.max-code
pip install -r requirements.txt

# 3. Create symlink
mkdir -p ~/.local/bin
ln -s ~/.max-code/bin/max-code ~/.local/bin/max-code

# 4. Add to PATH
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

## Requirements

- Python 3.11+
- pip
- Anthropic API Key

## Verify Installation

```bash
# Check if installed
which max-code

# Should output: /home/your-username/.local/bin/max-code

# Test it
max-code --help
```

## Uninstall

```bash
# Remove files
rm -rf ~/.max-code

# Remove symlink
rm ~/.local/bin/max-code

# Remove from PATH (edit ~/.bashrc manually)
```

## Troubleshooting

### Command not found

```bash
# Reload your shell
source ~/.bashrc  # or source ~/.zshrc

# Or open a new terminal
```

### Python version error

```bash
# Check Python version
python3 --version

# Must be 3.11 or higher
```

### API Key not set

```bash
# Get key from: https://console.anthropic.com/settings/keys

# Set it
export ANTHROPIC_API_KEY="your-key-here"

# Make it permanent (add to ~/.bashrc)
echo 'export ANTHROPIC_API_KEY="your-key-here"' >> ~/.bashrc
```

---

**Ready!** Now you can use `max-code` from anywhere! 🚀

*Soli Deo Gloria* 🙏
