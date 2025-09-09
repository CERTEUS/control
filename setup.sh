#!/usr/bin/env bash
# +=====================================================================+
# |                          CERTEUS                                    |
# +=====================================================================+
# | FILE: setup.sh                                                     |
# | ROLE: Shell script for automation                                  |
# | PLIK: setup.sh                                                     |
# | ROLA: Skrypt shell do automatyzacji                                |
# +=====================================================================+

# PL: Moduł zapewniający funkcjonalność setup
# EN: Module providing setup functionality

set -Eeuo pipefail
trap 'echo "[ERR] $0 line:$LINENO status:$?" >&2' ERR

# Control Workspace Setup Script
# Automatically sets up the control workspace environment

set -e

echo "🚀 Control Workspace Setup"
echo "=========================="

# Check Python
if ! command -v python &> /dev/null; then
    echo "❌ Python not found. Please install Python 3.11+ first."
    exit 1
fi

PYTHON_VERSION=$(python --version 2>&1 | cut -d' ' -f2)
echo "✅ Python $PYTHON_VERSION found"

# Create virtual environment
if [ ! -d ".venv" ]; then
    echo "📦 Creating virtual environment..."
    python -m venv .venv
    echo "✅ Virtual environment created"
else
    echo "✅ Virtual environment already exists"
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source .venv/bin/activate

# Upgrade pip
echo "⬆️ Upgrading pip..."
python -m pip install --upgrade pip wheel setuptools

# Install control package
echo "📋 Installing control package..."
pip install -e .

# Install development tools
echo "🛠️ Installing development tools..."
pip install ruff pytest pre-commit mypy

# Run health check
echo "🔍 Running health check..."
python -m control.main health

# Generate workspace file
echo "📂 Generating VS Code workspace..."
python -m control.main project workspace

# Setup pre-commit hooks (optional)
if command -v git &> /dev/null && [ -d ".git" ]; then
    echo "🪝 Setting up pre-commit hooks..."
    pre-commit install || echo "⚠️ Pre-commit hook setup skipped"
fi

echo ""
echo "🎉 Setup complete!"
echo ""
echo "🎯 Next steps:"
echo "1. Activate environment: source .venv/bin/activate"
echo "2. Open workspace: code control.code-workspace"
echo "3. Run status check: control status"
echo "4. List available commands: control --help"
echo ""
echo "📖 For more information, see README.md"