@echo off
REM Control Workspace Setup Script for Windows
REM Automatically sets up the control workspace environment

echo 🚀 Control Workspace Setup
echo ==========================

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found. Please install Python 3.11+ first.
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo ✅ Python %PYTHON_VERSION% found

REM Create virtual environment
if not exist ".venv" (
    echo 📦 Creating virtual environment...
    python -m venv .venv
    echo ✅ Virtual environment created
) else (
    echo ✅ Virtual environment already exists
)

REM Activate virtual environment
echo 🔧 Activating virtual environment...
call .venv\Scripts\activate.bat

REM Upgrade pip
echo ⬆️ Upgrading pip...
python -m pip install --upgrade pip wheel setuptools

REM Install control package
echo 📋 Installing control package...
pip install -e .

REM Install development tools
echo 🛠️ Installing development tools...
pip install ruff pytest pre-commit mypy

REM Run health check
echo 🔍 Running health check...
python -m pkg.control.main health

REM Generate workspace file
echo 📂 Generating VS Code workspace...
python -m pkg.control.main project workspace

REM Setup pre-commit hooks (optional)
git --version >nul 2>&1
if not errorlevel 1 (
    if exist ".git" (
        echo 🪝 Setting up pre-commit hooks...
        pre-commit install || echo ⚠️ Pre-commit hook setup skipped
    )
)

echo.
echo 🎉 Setup complete!
echo.
echo 🎯 Next steps:
echo 1. Activate environment: .venv\Scripts\activate.bat
echo 2. Open workspace: code control.code-workspace
echo 3. Run status check: control status
echo 4. List available commands: control --help
echo.
echo 📖 For more information, see README.md

pause
