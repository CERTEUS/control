#!/usr/bin/env python3
"""
Complete System Verification Script
Checks all components for full Control system functionality
"""

import subprocess
import sys
from pathlib import Path
import importlib.util


def run_command(cmd: list[str], description: str) -> bool:
    """Run command and return success status"""
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            print(f"✅ {description}")
            return True
        else:
            print(f"❌ {description} - FAILED: {result.stderr.strip()}")
            return False
    except subprocess.TimeoutExpired:
        print(f"⏱️ {description} - TIMEOUT")
        return False
    except Exception as e:
        print(f"❌ {description} - ERROR: {e}")
        return False


def check_file_exists(path: str, description: str) -> bool:
    """Check if file exists"""
    if Path(path).exists():
        print(f"✅ {description}")
        return True
    else:
        print(f"❌ {description} - FILE MISSING: {path}")
        return False


def check_python_import(module: str, description: str) -> bool:
    """Check if Python module can be imported"""
    try:
        importlib.import_module(module)
        print(f"✅ {description}")
        return True
    except ImportError:
        print(f"❌ {description} - IMPORT FAILED: {module}")
        return False


def main():
    """Run complete system verification"""
    print("🔍 Control System Verification")
    print("=" * 50)
    
    checks = []
    
    # Python environment
    print("\n📦 Python Environment:")
    checks.append(run_command([sys.executable, "--version"], "Python executable"))
    checks.append(check_python_import("pkg.control.main", "Control CLI module"))
    checks.append(check_python_import("docker", "Docker Python client"))
    checks.append(check_python_import("pytest", "Pytest testing framework"))
    checks.append(check_python_import("ruff", "Ruff linting/formatting"))
    
    # Core files
    print("\n📁 Configuration Files:")
    checks.append(check_file_exists("pyproject.toml", "Python project configuration"))
    checks.append(check_file_exists("pytest.ini", "Pytest configuration"))
    checks.append(check_file_exists(".vscode/settings.json", "VS Code settings"))
    checks.append(check_file_exists("control.code-workspace", "VS Code workspace"))
    checks.append(check_file_exists(".github/workflows/ci.yml", "GitHub Actions CI"))
    
    # Control CLI
    print("\n🎛️ Control CLI:")
    checks.append(run_command([sys.executable, "-m", "pkg.control.main", "health"], "Health check"))
    checks.append(run_command([sys.executable, "-m", "pkg.control.main", "status"], "Status check"))
    
    # Docker
    print("\n🐳 Docker Environment:")
    checks.append(run_command(["docker", "--version"], "Docker installation"))
    checks.append(run_command(["docker", "info"], "Docker daemon"))
    checks.append(run_command(["docker-compose", "--version"], "Docker Compose"))
    
    # Git
    print("\n📝 Git Environment:")
    checks.append(run_command(["git", "--version"], "Git installation"))
    checks.append(run_command(["git", "status"], "Git repository status"))
    checks.append(run_command(["git", "config", "user.name"], "Git user configuration"))
    
    # Testing
    print("\n🧪 Testing Infrastructure:")
    checks.append(run_command([sys.executable, "-m", "pytest", "test/", "--collect-only", "-q"], "Test collection"))
    
    # Documentation
    print("\n📖 Documentation:")
    checks.append(check_file_exists("README.md", "Main README"))
    checks.append(check_file_exists("docs/COMPLETE_SETUP_GUIDE.md", "Setup guide"))
    checks.append(check_file_exists("docs/ENTERPRISE_STANDARDS.md", "Enterprise standards"))
    checks.append(check_file_exists("AGENT.md", "Agent documentation"))
    
    # Summary
    print("\n" + "=" * 50)
    passed = sum(checks)
    total = len(checks)
    success_rate = (passed / total) * 100
    
    print(f"📊 Verification Results: {passed}/{total} checks passed ({success_rate:.1f}%)")
    
    if success_rate >= 95:
        print("🎉 System is READY for production use!")
        return 0
    elif success_rate >= 80:
        print("⚠️ System is mostly ready but has some issues")
        return 1
    else:
        print("❌ System needs significant setup work")
        return 2


if __name__ == "__main__":
    sys.exit(main())
