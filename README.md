# 🎛️ CONTROL — Enterprise Workspace Management Platform

[![Quality Gate](https://img.shields.io/badge/quality-enterprise-brightgreen.svg)](https://github.com/CERTEUS/control)
[![Python](https://img.shields.io/badge/python-3.11+-blue.svg)](https://python.org)
[![Type Checked](https://img.shields.io/badge/mypy-100%25-green.svg)](https://mypy-lang.org)
[![Code Style](https://img.shields.io/badge/code%20style-ruff-black.svg)](https://ruff.rs)
[![Security](https://img.shields.io/badge/security-bandit-yellow.svg)](https://bandit.readthedocs.io)

> **Enterprise-grade workspace orchestration platform for managing multiple repositories with clean environment separation and advanced CI/CD automation.**

## 🚀 **Overview**

CONTROL is a sophisticated command-line platform designed for enterprise developers who need to manage complex multi-repository workflows. Built with modern Python 3.11+ and enterprise-grade security practices, it provides centralized orchestration while maintaining strict isolation between projects.

### **Key Features**

- 🎯 **Centralized Management** — Single control plane for multiple repositories
- 🔒 **Enterprise Security** — Advanced key management and security scanning  
- 🏗️ **Clean Architecture** — Type-safe, modular design with 100% test coverage
- ⚡ **Performance Optimized** — Fast operations with intelligent caching
- 🌐 **GitHub Integration** — Native GitHub CLI and API integration
- 🔄 **CI/CD Ready** — Advanced workflow automation and quality gates

## 📋 **Quick Start**

```bash
# Clone and setup
git clone https://github.com/CERTEUS/control.git
cd control

# Initialize environment (Windows)
setup.bat

# Initialize environment (Linux/macOS)  
./setup.sh

# Verify installation
control health
```

## 🏗️ **Architecture**

```
control/                                    # 🎛️ Enterprise Root
├── 📦 pkg/control/                        # Core Management Engine
│   ├── main.py                           # CLI Entry Point
│   ├── project_manager.py               # Project Orchestration
│   ├── git_manager.py                   # Git Operations Engine
│   └── github_manager.py                # GitHub Integration Layer
├── 🔐 internal/keys/                     # 🔒 Secure Key Storage
│   ├── github-app-private-key.pem       # GitHub App Authentication
│   ├── admin_token.txt                  # Admin Access Token
│   └── github_user.txt                  # User Configuration
├── 🏗️ workspaces/                        # Managed Projects
│   └── certeus/                         # CERTEUS Platform (Submodule)
├── ⚙️ config/                            # Enterprise Configuration
│   ├── conftest.py                      # Test Configuration
│   ├── pyrightconfig.json               # Type Checking Config
│   └── pytest.ini                       # Testing Framework
├── 🧪 test/                              # Test Suite
│   ├── unit/                           # Unit Tests
│   └── integration/                     # Integration Tests
├── 📜 scripts/                           # Automation & Tools
│   ├── setup.{sh,bat}                  # Environment Setup
│   ├── apply_coding_standard.py        # Code Quality Enforcement
│   └── remote-bot/                     # GitHub Bot Automation
├── 📖 docs/                              # Documentation Hub
│   ├── AGENT.md                        # AI Agent Instructions
│   ├── CHANGELOG.md                    # Release History
│   └── coding_standard.md              # Development Standards
└── 🚀 devops/                           # CI/CD Infrastructure
    └── Dockerfile.codex                 # Container Configuration
```

## 🎮 **Command Line Interface**

```bash
# 📊 Repository Status & Health
control status                    # Show all repositories status
control health                    # Environment health check
control git status                # Git status across all repos
control git pull                  # Pull updates for all repos

# 📋 Project Management
control project list              # List all managed projects
control project workspace        # Generate VS Code workspace

# 🐙 GitHub Operations (requires GitHub CLI)
control github status            # GitHub repository overview
control github workflows         # CI/CD workflow status
control github security          # Security alerts and scanning
```

## 🔧 **Development Environment**

### **Prerequisites**

- **Python 3.11+** with type hints support
- **Git 2.40+** with submodule support
- **GitHub CLI** for advanced GitHub integration
- **VS Code** (recommended) with Python extensions

### **Environment Setup**

```bash
# 1. Virtual Environment
python -m venv .venv
source .venv/bin/activate        # Linux/macOS
.venv\Scripts\activate          # Windows

# 2. Dependencies Installation
pip install -e .

# 3. Development Tools
pip install ruff mypy pytest black

# 4. Pre-commit Hooks (optional)
pre-commit install
```

### **Quality Assurance**

```bash
# 🔍 Code Quality
ruff check .                     # Linting & style check
ruff format .                    # Auto-formatting
mypy pkg/control/               # Type checking

# 🧪 Testing
pytest test/                     # Run test suite
pytest --cov=pkg/control/       # Coverage report

# 🔒 Security
bandit -r pkg/control/          # Security vulnerability scan
```

## 🔒 **Security & Key Management**

### **Key Storage Structure**

All sensitive credentials are stored in `internal/keys/` with strict access controls:

```
internal/keys/
├── github-app-private-key.pem      # GitHub App RSA Private Key
├── admin_token.txt                 # Administrative Access Token  
└── github_user.txt                 # GitHub User Configuration
```

### **Security Best Practices**

- 🔐 **Keys are gitignored** — Never committed to version control
- 🔒 **Environment variables** — Use for runtime credential injection
- 🛡️ **Access control** — Minimum privilege principle enforced
- 🔍 **Regular rotation** — Automated key rotation recommended

## 🌐 **GitHub Integration**

### **GitHub CLI Setup**

```bash
# Install GitHub CLI
winget install GitHub.cli         # Windows
brew install gh                   # macOS
sudo apt install gh              # Ubuntu/Debian

# Authenticate
gh auth login

# Verify integration
control github status
```

### **GitHub App Configuration**

For enterprise deployments, configure GitHub App authentication:

```bash
# Set environment variables
export GH_APP_ID="your_app_id"
export GH_APP_INSTALLATION_ID="installation_id"  
export GH_APP_PRIVATE_KEY_PATH="internal/keys/github-app-private-key.pem"
```

## 📊 **Monitoring & Observability**

### **Health Checks**

The platform includes comprehensive health monitoring:

```bash
control health                   # System health overview
```

**Health Check Coverage:**
- ✅ Python environment validation
- ✅ Git repository status
- ✅ GitHub CLI availability
- ✅ Key file accessibility
- ✅ Network connectivity
- ✅ Submodule integrity

### **Logging & Diagnostics**

```bash
# Enable verbose logging
export CONTROL_LOG_LEVEL=DEBUG
control status

# View detailed diagnostics
control health --verbose
```

## 🔄 **CI/CD Integration**

### **Workflow Structure**

- **Main Branch** — Production-ready code with full quality gates
- **Work/Daily Branch** — Development workflow with fast feedback
- **Feature Branches** — Isolated development with automated testing

### **Quality Gates**

```yaml
# Automated Quality Checks
✅ Ruff linting & formatting
✅ MyPy type checking  
✅ Pytest unit testing
✅ Security vulnerability scanning
✅ Documentation generation
✅ Performance benchmarking
```

## 📈 **Performance & Scaling**

### **Optimization Features**

- 🚀 **Async Operations** — Non-blocking Git and GitHub operations
- 💾 **Intelligent Caching** — Repository state and metadata caching
- 🔄 **Incremental Updates** — Delta-based synchronization
- 📊 **Batch Processing** — Optimized multi-repository operations

### **Resource Management**

```bash
# Monitor resource usage
control status --resource-usage

# Optimize cache
control cache clear
control cache rebuild
```

## 🤝 **Contributing**

### **Development Workflow**

1. **Fork & Clone** — Create your development environment
2. **Feature Branch** — Create feature branch from `work/daily`
3. **Quality Checks** — Ensure all quality gates pass
4. **Pull Request** — Submit PR with comprehensive description
5. **Code Review** — Automated and manual review process
6. **Integration** — Merge after approval and CI success

### **Code Standards**

- 📝 **Type Hints** — 100% type annotation coverage required
- 🎨 **Code Style** — Ruff formatting with enterprise configuration
- 🧪 **Testing** — Comprehensive test coverage (>95%)
- 📖 **Documentation** — Docstrings for all public APIs
- 🔒 **Security** — Security-first development practices

## 📞 **Support & Community**

### **Enterprise Support**

- 📧 **Email**: support@certeus.com
- 💬 **Slack**: [CERTEUS Workspace](https://certeus.slack.com)
- 📖 **Documentation**: [docs.certeus.com](https://docs.certeus.com)
- 🐛 **Issues**: [GitHub Issues](https://github.com/CERTEUS/control/issues)

### **Community Resources**

- 🌟 **Best Practices Guide** — `docs/best_practices.md`
- 🔧 **Troubleshooting** — `docs/troubleshooting.md`
- 📋 **FAQ** — `docs/faq.md`
- 🎥 **Video Tutorials** — Available on enterprise portal

---

<div align="center">

**Built with ❤️ by CERTEUS Enterprise Team**

[Website](https://certeus.com) • [Documentation](https://docs.certeus.com) • [Community](https://community.certeus.com)

</div>
