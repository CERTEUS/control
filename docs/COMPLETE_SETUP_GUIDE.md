# Complete Setup Guide - Control System & VS Code

## 📋 Overview

This document provides a complete checklist for setting up the Control system locally in VS Code and ensuring GitHub integration works flawlessly.

## 🎯 Current Status (Successfully Implemented)

### ✅ Core Components
- **Control CLI System** - Full workspace management
- **Enterprise CI/CD Pipeline** - GitHub Actions with quality gates
- **Docker Orchestration** - Multi-service testing environment
- **Security Scanning** - Bandit, Safety, Trivy, CodeSpell
- **Quality Assurance** - MyPy, Ruff, pytest with coverage
- **Monitoring Stack** - Prometheus, Grafana, SonarQube integration

### ✅ VS Code Integration
- **Python environment** - Properly configured with .venv
- **Language servers** - Pylance, MyPy integration
- **Debugging** - Python debugger configuration
- **Tasks** - Automated build, test, lint tasks
- **Extensions** - Polish spell checker, Code Spell Checker

### ✅ Testing Infrastructure
- **461 tests passing** - Comprehensive test coverage
- **2 legitimately skipped** (platform-specific Linux FUSE, UV solver on Windows)
- **No warnings** - All Pydantic and other warnings resolved
- **Property-based testing** - Hypothesis integration

## 🔧 Missing Components Analysis

### 1. **VS Code Extensions Setup**

Check if these extensions are installed:

```bash
# Required extensions for full functionality
code --list-extensions | grep -E "(ms-python|charliermarsh|ms-vscode|streetsidesoftware)"
```

**Should have:**
- `ms-python.python` - Python support
- `ms-python.debugpy` - Python debugger
- `ms-python.pylint` - Python linting
- `charliermarsh.ruff` - Ruff formatter/linter
- `ms-vscode.vscode-json` - JSON support
- `streetsidesoftware.code-spell-checker` - Spell checking
- `streetsidesoftware.code-spell-checker-polish` - Polish language support

### 2. **GitHub Integration Components**

#### **Personal Access Token (PAT)**
```bash
# Check if GitHub CLI is configured
gh auth status

# If not configured:
gh auth login --hostname github.com --protocol https --web
```

#### **SSH Key Setup**
```bash
# Check existing SSH keys
ls -la ~/.ssh/

# Generate if missing
ssh-keygen -t ed25519 -C "your-email@example.com"

# Add to SSH agent
ssh-add ~/.ssh/id_ed25519

# Add to GitHub (copy public key)
cat ~/.ssh/id_ed25519.pub
```

### 3. **Environment Variables**

Create/verify `.env` file in project root:

```bash
# GitHub integration
GITHUB_TOKEN=your_personal_access_token_here
GITHUB_USER=your_github_username

# Docker configuration  
DOCKER_BUILDKIT=1
COMPOSE_DOCKER_CLI_BUILD=1

# Python/Testing
PYTHONPATH=.
PYTEST_TIMEOUT=300

# Development flags
DEBUG=1
ENVIRONMENT=development
```

### 4. **Docker Desktop Configuration**

Verify Docker Desktop settings:
- **Enable BuildKit** - For faster builds
- **WSL Integration** - If using WSL
- **Resource allocation** - At least 4GB RAM, 2 CPUs
- **File sharing** - Project directory accessible

```bash
# Test Docker functionality
docker run hello-world
docker-compose version
```

### 5. **Pre-commit Hooks** (Optional but Recommended)

```bash
# Install pre-commit
pip install pre-commit

# Install hooks
pre-commit install

# Run on all files
pre-commit run --all-files
```

### 6. **Global Git Configuration**

```bash
# Configure Git properly
git config --global user.name "Your Name"  
git config --global user.email "your-email@example.com"
git config --global init.defaultBranch main
git config --global pull.rebase false
git config --global core.autocrlf false  # Important on Windows
```

## 🚀 Quick Setup Commands

### **1. Environment Setup**
```bash
cd f:/projekty/control

# Activate Python environment
.venv/Scripts/activate  # Windows
source .venv/bin/activate  # Linux/Mac

# Install/update dependencies
pip install -e .
pip install --upgrade pip setuptools wheel
```

### **2. Verify Installation**
```bash
# Test Control CLI
python -m pkg.control.main health
python -m pkg.control.main status

# Run tests
python -m pytest test/ -v

# Test Certeus
cd workspaces/certeus
python -m pytest tests/ -q
```

### **3. Docker Stack Test**
```bash
# Start testing infrastructure
python -m pkg.control.docker start-testing-stack

# Run CI gates
python -m pkg.control.docker run-ci-gates

# Stop stack
python -m pkg.control.docker stop-testing-stack
```

### **4. VS Code Workspace**
```bash
# Generate/update workspace file
python -m pkg.control.main project workspace

# Open in VS Code
code control.code-workspace
```

## 🔍 Troubleshooting Common Issues

### **Python Path Issues**
```bash
# Fix Python path in VS Code
# Ctrl+Shift+P > Python: Select Interpreter
# Choose: F:/projekty/control/.venv/Scripts/python.exe
```

### **Docker Issues**
```bash
# Reset Docker if having issues
docker system prune -af
docker volume prune -f
```

### **Git Issues**
```bash
# Fix line endings on Windows
git config core.autocrlf false
git rm --cached -r .
git reset --hard
```

### **Testing Issues**
```bash
# Clear pytest cache
rm -rf .pytest_cache
rm -rf workspaces/certeus/.pytest_cache

# Rebuild Python cache
find . -name "__pycache__" -type d -exec rm -rf {} +
```

## 📊 Verification Checklist

### ✅ **Local Development**
- [ ] Python 3.11+ installed and working
- [ ] Virtual environment activated
- [ ] All dependencies installed (`pip list`)
- [ ] Control CLI commands working (`health`, `status`)
- [ ] Tests passing (461 passed, 2 skipped)
- [ ] Docker stack starts successfully
- [ ] VS Code opens workspace correctly

### ✅ **GitHub Integration**  
- [ ] Git configured with proper credentials
- [ ] SSH key added to GitHub account
- [ ] Can push/pull from repositories
- [ ] GitHub Actions running successfully
- [ ] Pre-commit hooks working (if installed)

### ✅ **VS Code Features**
- [ ] Python interpreter detected correctly
- [ ] Code completion working (Pylance)
- [ ] Linting working (Ruff, MyPy)
- [ ] Debugging configuration working
- [ ] Spell checker working (EN+PL)
- [ ] Tasks running (`Ctrl+Shift+P` > Tasks: Run Task)

### ✅ **Docker & Testing**
- [ ] Docker Desktop running
- [ ] Testing stack starts (`docker-compose up`)
- [ ] All services healthy
- [ ] CI gates pass locally
- [ ] SonarQube, Prometheus accessible

## 🎯 Advanced Features

### **Remote Development**
- **GitHub Codespaces** - Cloud development environment
- **Dev Containers** - Consistent development environment
- **Remote SSH** - Develop on remote servers

### **Monitoring & Observability**
- **Prometheus** - Metrics collection (localhost:9090)
- **Grafana** - Metrics visualization (localhost:3000) 
- **SonarQube** - Code quality (localhost:9000)

### **Security Features**
- **Secret scanning** - GitHub Actions
- **Dependency scanning** - Safety, Bandit
- **Container scanning** - Trivy
- **License compliance** - Automated checks

## 📝 Next Steps

1. **Run full verification** - Use checklist above
2. **Install missing components** - Based on gaps identified
3. **Test integration** - Push changes, verify CI/CD
4. **Document custom setup** - Add any environment-specific notes
5. **Automate setup** - Consider setup scripts for new machines

## 🆘 Getting Help

If you encounter issues:

1. **Check logs**: `python -m pkg.control.main health --verbose`
2. **Verify environment**: All items in verification checklist
3. **Reset if needed**: Clean Docker, Python cache, Git state
4. **Documentation**: Check `docs/` directory for specific guides

---

**Last Updated**: 11 września 2025
**Status**: Enterprise-ready system with comprehensive testing and CI/CD
