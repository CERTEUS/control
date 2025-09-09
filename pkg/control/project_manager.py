# +=====================================================================+
# |                          CERTEUS                                    |
# +=====================================================================+
# | FILE: control/project_manager.py                                   |
# | ROLE: Manager module for business logic                            |
# | PLIK: control/project_manager.py                                   |
# | ROLA: Moduł menedżera logiki biznesowej                            |
# +=====================================================================+

"""
PL: Moduł zarządzania workspace control dla project_manager

EN: Control workspace management module for project_manager
"""

# === IMPORTY / IMPORTS ===

from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Any

from rich.console import Console
from rich.table import Table

console = Console()


class ProjectManager:
    """Manages multiple projects and their configurations."""

    def __init__(self, workspace_root: Path) -> None:
        self.workspace_root = workspace_root
        self.config_file = workspace_root / "internal" / "projects.json"
        self.config_file.parent.mkdir(exist_ok=True)
        self.projects = self._load_config()

    def _load_config(self) -> dict[str, Any]:
        """Load project configuration."""
        if self.config_file.exists():
            data: dict[str, Any] = json.loads(self.config_file.read_text())
            return data
        return {
            "version": "1.0",
            "projects": {
                "control": {
                    "type": "manager",
                    "path": ".",
                    "python_env": ".venv",
                    "description": "Control workspace manager",
                },
                "certeus": {
                    "type": "product",
                    "path": "workspaces/certeus",
                    "python_env": "workspaces/certeus/.venv",
                    "description": "CERTEUS main product",
                    "github": "CERTEUS/certeus",
                },
            },
        }

    def _save_config(self) -> None:
        """Save project configuration."""
        self.config_file.write_text(json.dumps(self.projects, indent=2))

    def list_projects(self) -> None:
        """List all managed projects."""
        table = Table(title="🎯 Managed Projects")
        table.add_column("Name", style="cyan")
        table.add_column("Type", style="yellow")
        table.add_column("Path", style="green")
        table.add_column("Python Env", style="blue")
        table.add_column("Description", style="white")

        for name, config in self.projects.get("projects", {}).items():
            table.add_row(
                name,
                config.get("type", "unknown"),
                config.get("path", ""),
                config.get("python_env", ""),
                config.get("description", ""),
            )

        console.print(table)

    def add_project(
        self, name: str, path: str, project_type: str = "other", description: str = ""
    ) -> None:
        """Add a new project to management."""
        project_path = Path(path)

        # Detect Python environment
        python_env = ""
        if (project_path / ".venv").exists():
            python_env = f"{path}/.venv"
        elif (project_path / "venv").exists():
            python_env = f"{path}/venv"

        self.projects.setdefault("projects", {})[name] = {
            "type": project_type,
            "path": path,
            "python_env": python_env,
            "description": description,
        }

        self._save_config()
        console.print(f"✅ Added project '{name}'", style="green")

    def remove_project(self, name: str) -> None:
        """Remove a project from management."""
        if name in self.projects.get("projects", {}):
            del self.projects["projects"][name]
            self._save_config()
            console.print(f"✅ Removed project '{name}'", style="green")
        else:
            console.print(f"❌ Project '{name}' not found", style="red")

    def open_project_vscode(self, name: str) -> None:
        """Open project in VS Code."""
        if name not in self.projects.get("projects", {}):
            console.print(f"❌ Project '{name}' not found", style="red")
            return

        project_path = self.workspace_root / self.projects["projects"][name]["path"]

        try:
            subprocess.run(  # noqa: S603  # VS Code is trusted application
                ["code", str(project_path)],
                check=True,  # noqa: S607
            )
            console.print(f"📂 Opened '{name}' in VS Code", style="green")
        except subprocess.CalledProcessError:
            console.print(f"❌ Failed to open '{name}' in VS Code", style="red")
        except FileNotFoundError:
            console.print("❌ VS Code 'code' command not found in PATH", style="red")

    def health_check_all(self) -> None:
        """Run health check on all projects."""
        console.print("🔍 Health Check - All Projects", style="bold blue")

        for name, config in self.projects.get("projects", {}).items():
            console.print(f"\n📋 {name}", style="bold cyan")
            project_path = self.workspace_root / config["path"]

            # Check path exists
            if project_path.exists():
                console.print("  ✅ Path exists", style="green")
            else:
                console.print("  ❌ Path missing", style="red")
                continue

            # Check Python environment
            python_env = config.get("python_env")
            if python_env:
                env_path = self.workspace_root / python_env
                if env_path.exists():
                    console.print("  ✅ Python environment", style="green")
                else:
                    console.print("  ❌ Python environment missing", style="red")
            else:
                console.print("  ⚠️ No Python environment configured", style="yellow")

            # Check Git repository
            if (project_path / ".git").exists():
                console.print("  ✅ Git repository", style="green")
            else:
                console.print("  ⚠️ Not a Git repository", style="yellow")

            # Check VS Code configuration
            if (project_path / ".vscode").exists():
                console.print("  ✅ VS Code configuration", style="green")
            else:
                console.print("  ⚠️ No VS Code configuration", style="yellow")

    def generate_workspace_file(self) -> None:
        """Generate VS Code multi-root workspace file."""
        workspace_config = {
            "folders": [
                {"name": name, "path": config["path"]}
                for name, config in self.projects.get("projects", {}).items()
            ],
            "settings": {"python.defaultInterpreterPath": "./control/.venv/Scripts/python.exe"},
            "extensions": {
                "recommendations": [
                    "ms-python.python",
                    "ms-python.vscode-pylance",
                    "charliermarsh.ruff",
                    "github.copilot",
                    "github.copilot-chat",
                ]
            },
        }

        workspace_file = self.workspace_root / "control.code-workspace"
        workspace_file.write_text(json.dumps(workspace_config, indent=2))
        console.print(f"✅ Generated workspace file: {workspace_file}", style="green")
