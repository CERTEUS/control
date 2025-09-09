# +=====================================================================+
# |                          CERTEUS                                    |
# +=====================================================================+
# | FILE: control/main.py                                              |
# | ROLE: Main application entry point                                 |
# | PLIK: control/main.py                                              |
# | ROLA: Główny punkt wejścia aplikacji                               |
# +=====================================================================+

"""
PL: Moduł zarządzania workspace control dla main

EN: Control workspace management module for main
"""

# === IMPORTY / IMPORTS ===

# === IMPORTY / IMPORTS ===
from __future__ import annotations

import sys
from pathlib import Path

import click
from rich.console import Console

from .git_manager import GitManager
from .github_manager import GitHubManager
from .project_manager import ProjectManager

# === KONFIGURACJA / CONFIGURATION ===

console = Console()

# === MODELE / MODELS ===

# === LOGIKA / LOGIC ===

# === I/O / ENDPOINTS ===


@click.group()
@click.version_option()
def cli() -> None:
    """
    PL: Menedżer workspace control dla wielu repozytoriów.
    EN: Control workspace manager for multiple repositories.
    """


@cli.command()
def status() -> None:
    """
    PL: Pokazuje status wszystkich zarządzanych repozytoriów.
    EN: Show status of all managed repositories.
    """
    console.print("🎯 Control Status", style="bold green")
    workspace_root = Path.cwd()

    # Project overview
    pm = ProjectManager(workspace_root)
    pm.list_projects()

    # Git status
    gm = GitManager(workspace_root)
    gm.status_all()
    gm.status_all()


@cli.command()
def health() -> None:
    """Check health of development environment."""
    console.print("🔍 Environment Health Check", style="bold blue")
    workspace_root = Path.cwd()

    # Check Python version
    console.print(f"✅ Python: {sys.version}")

    # Check virtual environment
    venv_path = Path(".venv")
    if venv_path.exists():
        console.print(f"✅ Virtual environment: {venv_path.absolute()}")
    else:
        console.print("❌ Virtual environment not found", style="red")

    # Check pyproject.toml
    pyproject_path = Path("pyproject.toml")
    if pyproject_path.exists():
        console.print("✅ Project configuration: pyproject.toml")
    else:
        console.print("❌ Project configuration missing", style="red")

    # Project health check
    pm = ProjectManager(workspace_root)
    pm.health_check_all()


@cli.group()
def git() -> None:
    """Git operations for all repositories."""


@git.command()
def pull() -> None:
    """Pull latest changes for all repositories."""
    gm = GitManager(Path.cwd())
    gm.pull_all()


@git.command()
def fetch() -> None:
    """Fetch all repositories without merging."""
    gm = GitManager(Path.cwd())
    gm.fetch_all()


@git.command()
@click.argument("branch_name")
@click.option("--repo", help="Target specific repository")
def switch(branch_name: str, repo: str | None) -> None:
    """Switch branch in specified repo or all repos."""
    gm = GitManager(Path.cwd())
    gm.switch_branch(branch_name, repo)


@cli.group()
def project() -> None:
    """Project management commands."""


@project.command("list")
def project_list() -> None:
    """List all managed projects."""
    pm = ProjectManager(Path.cwd())
    pm.list_projects()


@project.command()
@click.argument("name")
@click.argument("path")
@click.option("--type", "project_type", default="other", help="Project type")
@click.option("--description", default="", help="Project description")
def add(name: str, path: str, project_type: str, description: str) -> None:
    """Add a new project to management."""
    pm = ProjectManager(Path.cwd())
    pm.add_project(name, path, project_type, description)


@project.command()
@click.argument("name")
def remove(name: str) -> None:
    """Remove a project from management."""
    pm = ProjectManager(Path.cwd())
    pm.remove_project(name)


@project.command("open")
@click.argument("name")
def open_project(name: str) -> None:
    """Open project in VS Code."""
    pm = ProjectManager(Path.cwd())
    pm.open_project_vscode(name)


@project.command()
def workspace() -> None:
    """Generate VS Code multi-root workspace file."""
    pm = ProjectManager(Path.cwd())
    pm.generate_workspace_file()


@cli.group()
def github() -> None:
    """GitHub operations and management."""


@github.command("repos")
def github_repos() -> None:
    """List all GitHub repositories."""
    ghm = GitHubManager(Path.cwd())
    ghm.status_all_repos()


@github.command()
@click.argument("repo_path")
@click.argument("title")
@click.option("--body", default="", help="PR description")
def pr(repo_path: str, title: str, body: str) -> None:
    """Create a pull request."""
    ghm = GitHubManager(Path.cwd())
    ghm.create_pr(repo_path, title, body)


@github.command()
@click.argument("repo_path")
def workflows(repo_path: str) -> None:
    """List GitHub Actions workflows."""
    ghm = GitHubManager(Path.cwd())
    ghm.list_workflows(repo_path)


@github.command()
@click.argument("repo_path")
def security(repo_path: str) -> None:
    """Check security configuration."""
    ghm = GitHubManager(Path.cwd())
    ghm.check_security_alerts(repo_path)


if __name__ == "__main__":
    cli()
