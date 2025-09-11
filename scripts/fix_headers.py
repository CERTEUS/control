#!/usr/bin/env python3
# +-------------------------------------------------------------+
# | CERTEUS Control System | ForgeHeader v3 - Enterprise     |
# | FILE: scripts/fix_headers.py                              |
# | ROLE: Automated ForgeHeader v3 compliance fixer          |
# +-------------------------------------------------------------+

"""
Automated ForgeHeader v3 compliance fixer.

This script automatically adds ForgeHeader v3 to files that are missing it.
Supports Python, shell scripts, YAML files, and TypeScript files.
"""

import sys
from pathlib import Path

# Templates for different file types
TEMPLATES = {
    ".py": """# +-------------------------------------------------------------+
# | CERTEUS Control System | ForgeHeader v3 - Enterprise     |
# | FILE: {relative_path}                                      |
# | ROLE: {description}                                        |
# +-------------------------------------------------------------+

""",
    ".sh": """#!/bin/bash
# +-------------------------------------------------------------+
# | CERTEUS Control System | ForgeHeader v3 - Enterprise     |
# | FILE: {relative_path}                                      |
# | ROLE: {description}                                        |
# +-------------------------------------------------------------+

""",
    ".yml": """# +-------------------------------------------------------------+
# | CERTEUS Control System | ForgeHeader v3 - Enterprise     |
# | FILE: {relative_path}                                      |
# | ROLE: {description}                                        |
# +-------------------------------------------------------------+

""",
    ".yaml": """# +-------------------------------------------------------------+
# | CERTEUS Control System | ForgeHeader v3 - Enterprise     |
# | FILE: {relative_path}                                      |
# | ROLE: {description}                                        |
# +-------------------------------------------------------------+

""",
    ".ts": """/**
 * +-------------------------------------------------------------+
 * | CERTEUS Control System | ForgeHeader v3 - Enterprise     |
 * | FILE: {relative_path}                                      |
 * | ROLE: {description}                                        |
 * +-------------------------------------------------------------+
 */

""",
}

# Description patterns
DESCRIPTIONS = {
    "main.py": "Main application entry point",
    "test_": "Unit tests for system verification",
    "verify": "System verification utilities",
    "migration": "Database migration utilities",
    "manager": "Management utilities",
    "adapter": "Adapter implementation for external systems",
    "client": "Client library implementation",
    "plugin": "Plugin implementation",
    "service": "Service implementation",
    "gateway": "API gateway implementation",
    "parser": "Data parsing utilities",
    "mapping": "Data mapping utilities",
    "evaluator": "Evaluation engine implementation",
    "deploy": "Deployment automation scripts",
    "setup": "Environment setup scripts",
    "agent": "Agent automation scripts",
    "docker-compose": "Docker compose configuration",
    "plugin.yaml": "Plugin configuration file",
    "bandit.yml": "Security scanning configuration",
    "mkdocs.yml": "Documentation configuration",
    ".pre-commit": "Pre-commit hooks configuration",
}


def get_description(file_path: str) -> str:
    """Generate appropriate description for file."""
    name = Path(file_path).name.lower()

    for pattern, desc in DESCRIPTIONS.items():
        if pattern in name:
            return desc

    # Fallback descriptions by directory
    if "tests/" in file_path.lower():
        return "Test implementation"
    if "scripts/" in file_path.lower():
        return "Automation script"
    if "services/" in file_path.lower():
        return "Service implementation"
    if "tools/" in file_path.lower():
        return "Development tool"
    if "plugins/" in file_path.lower():
        return "Plugin implementation"
    if ".github/" in file_path:
        return "GitHub workflow configuration"
    if "infra/" in file_path:
        return "Infrastructure configuration"
    return "Implementation file"


def fix_file(file_path: Path, root_path: Path) -> bool:
    """Add ForgeHeader v3 to a file if missing."""
    try:
        with open(file_path, encoding="utf-8") as f:
            content = f.read()

        # Skip if already has CERTEUS header
        if "CERTEUS Control System" in content[:500]:
            return False

        suffix = file_path.suffix.lower()
        if suffix not in TEMPLATES:
            return False

        relative_path = str(file_path.relative_to(root_path)).replace("\\", "/")
        description = get_description(relative_path)

        template = TEMPLATES[suffix]
        header = template.format(relative_path=relative_path, description=description)

        # Handle shebang for Python files
        if suffix == ".py" and content.startswith("#!/"):
            lines = content.split("\n", 1)
            shebang = lines[0] + "\n"
            rest = lines[1] if len(lines) > 1 else ""
            new_content = shebang + header + rest
        else:
            new_content = header + content

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(new_content)

        print(f"✅ Added ForgeHeader v3 to {relative_path}")
        return True

    except Exception as e:
        print(f"❌ Failed to fix {file_path}: {e}")
        return False


def main():
    """Fix ForgeHeader v3 for all files."""
    if len(sys.argv) > 1:
        files_to_fix = sys.argv[1:]
    else:
        # Get files from check_headers.py output
        files_to_fix = [
            "pkg/control/migration_manager.py",
            "scripts/verify_system.py",
            "workspaces/certeus/security/ra.py",
            "workspaces/certeus/services/api_gateway/idempotency.py",
            "workspaces/certeus/services/lexlog_parser/evaluator.py",
            "workspaces/certeus/services/lexlog_parser/mapping.py",
            "workspaces/certeus/services/lexlog_parser/parser.py",
            "docker-compose.testing.yml",
            "docker-compose.yml",
            "workspaces/certeus/bandit.yml",
            "workspaces/certeus/mkdocs.yml",
            ".pre-commit-config.yaml",
        ]

    root_path = Path.cwd()
    fixed_count = 0

    print(f"🔧 Fixing ForgeHeader v3 for {len(files_to_fix)} files...")

    for file_str in files_to_fix:
        file_path = root_path / file_str.replace("\\", "/")
        if file_path.exists():
            if fix_file(file_path, root_path):
                fixed_count += 1
        else:
            print(f"⚠️ File not found: {file_str}")

    print(f"✅ Fixed {fixed_count} files")
    return 0 if fixed_count > 0 else 1


if __name__ == "__main__":
    sys.exit(main())
