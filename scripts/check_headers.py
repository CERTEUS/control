#!/usr/bin/env python3
# +=====================================================================+
# |                          CERTEUS                                    |
# +=====================================================================+
# | FILE: scripts/check_headers.py                                     |
# | ROLE: ForgeHeader v3 compliance checker                           |
# | PLIK: scripts/check_headers.py                                     |
# | ROLA: Sprawdzanie zgodności z ForgeHeader v3                      |
# +=====================================================================+

"""
PL: Skrypt sprawdzający zgodność nagłówków ForgeHeader v3 w plikach projektu
EN: Script for checking ForgeHeader v3 compliance in project files
"""

import os
import sys
from pathlib import Path


def check_forgeheader(file_path: Path) -> bool:
    """Check if file has valid ForgeHeader v3."""
    try:
        with file_path.open(encoding="utf-8") as f:
            content = f.read(1500)  # Read first 1500 chars for header check
        
        # Check for CERTEUS header and required FILE:/ROLE: lines
        return "CERTEUS" in content and "FILE:" in content and "ROLE:" in content
        
    except (UnicodeDecodeError, OSError):
        # Skip binary files or files with encoding issues
        return True


def get_files_to_check(root_path: Path) -> list[Path]:
    """Get list of files that should be checked for ForgeHeader."""
    file_patterns = ["*.py", "*.sh", "*.yml", "*.yaml", "*.js", "*.ts"]
    skip_patterns = [
        ".venv", "__pycache__", ".git", "build", "dist",
        "node_modules", ".mypy_cache", ".pytest_cache", ".ruff_cache",
        "workspaces/certeus"  # Skip submodule - it has its own checks
    ]
    
    files_to_check = []
    
    for pattern in file_patterns:
        for file_path in root_path.rglob(pattern):
            # Skip if file is in any skip pattern
            if any(skip in str(file_path) for skip in skip_patterns):
                continue
            files_to_check.append(file_path)
    
    return files_to_check


def main() -> int:
    """Main function."""
    root_path = Path(".")
    files_to_check = get_files_to_check(root_path)
    failed_files = []
    
    print(f"🔍 Checking ForgeHeader v3 compliance for {len(files_to_check)} files...")
    
    for file_path in files_to_check:
        if not check_forgeheader(file_path):
            failed_files.append(str(file_path))
    
    if failed_files:
        print("❌ Files missing ForgeHeader v3:")
        for f in failed_files:
            print(f"  - {f}")
        print(f"\n💡 Total: {len(failed_files)} files need ForgeHeader v3")
        return 1
    
    print("✅ All files have ForgeHeader v3")
    return 0


if __name__ == "__main__":
    sys.exit(main())
