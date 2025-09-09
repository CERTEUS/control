# +=====================================================================+
# |                          CERTEUS                                    |
# +=====================================================================+
# | FILE: control/github_manager.py                                    |
# | ROLE: Manager module for business logic                            |
# | PLIK: control/github_manager.py                                    |
# | ROLA: Moduł menedżera logiki biznesowej                            |
# +=====================================================================+

"""
PL: Moduł zarządzania workspace control dla github_manager

EN: Control workspace management module for github_manager
"""

# === IMPORTY / IMPORTS ===

from __future__ import annotations

import json
import subprocess
from pathlib import Path

from rich.console import Console
from rich.table import Table

console = Console()


class GitHubManager:
    """Manages GitHub operations and integrations."""

    def __init__(self, workspace_root: Path):
        self.workspace_root = workspace_root
        self.gh_available = self._check_gh_cli()

    def _check_gh_cli(self) -> bool:
        """Check if GitHub CLI is available."""
        try:
            subprocess.run(["gh", "--version"], capture_output=True, check=True, text=True)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False

    def status_all_repos(self) -> None:
        """Show GitHub status for all repositories."""
        if not self.gh_available:
            console.print(
                "❌ GitHub CLI not available. Install with: winget install GitHub.cli", style="red"
            )
            return

        table = Table(title="🐙 GitHub Repository Status")
        table.add_column("Repository", style="cyan")
        table.add_column("Visibility", style="yellow")
        table.add_column("Default Branch", style="green")
        table.add_column("Open PRs", style="blue")
        table.add_column("Last Updated", style="white")

        # Get all repositories in organization or user
        try:
            result = subprocess.run(
                ["gh", "repo", "list", "--json", "name,visibility,defaultBranch,updatedAt"],
                capture_output=True,
                check=True,
                text=True,
            )
            repos = json.loads(result.stdout)

            for repo in repos:
                # Get PR count
                pr_result = subprocess.run(
                    ["gh", "pr", "list", "--repo", repo["name"], "--json", "number"],
                    check=False,
                    capture_output=True,
                    text=True,
                )
                pr_count = len(json.loads(pr_result.stdout)) if pr_result.returncode == 0 else 0

                table.add_row(
                    repo["name"],
                    repo["visibility"],
                    repo["defaultBranch"],
                    str(pr_count),
                    repo["updatedAt"][:10],  # Date only
                )

            console.print(table)

        except subprocess.CalledProcessError as e:
            console.print(f"❌ GitHub API error: {e}", style="red")

    def create_pr(self, repo_path: str, title: str, body: str = "") -> None:
        """Create a pull request for a repository."""
        if not self.gh_available:
            console.print("❌ GitHub CLI not available", style="red")
            return

        repo_full_path = self.workspace_root / repo_path

        try:
            result = subprocess.run(
                ["gh", "pr", "create", "--title", title, "--body", body],
                cwd=repo_full_path,
                capture_output=True,
                check=True,
                text=True,
            )
            console.print(f"✅ PR created: {result.stdout.strip()}", style="green")

        except subprocess.CalledProcessError as e:
            console.print(f"❌ Failed to create PR: {e.stderr}", style="red")

    def sync_fork(self, repo_path: str) -> None:
        """Sync fork with upstream repository."""
        if not self.gh_available:
            console.print("❌ GitHub CLI not available", style="red")
            return

        repo_full_path = self.workspace_root / repo_path

        try:
            subprocess.run(["gh", "repo", "sync"], cwd=repo_full_path, check=True)
            console.print(f"✅ Synced fork: {repo_path}", style="green")

        except subprocess.CalledProcessError as e:
            console.print(f"❌ Failed to sync fork: {e}", style="red")

    def list_workflows(self, repo_path: str) -> None:
        """List GitHub Actions workflows for a repository."""
        if not self.gh_available:
            console.print("❌ GitHub CLI not available", style="red")
            return

        repo_full_path = self.workspace_root / repo_path

        try:
            result = subprocess.run(
                ["gh", "workflow", "list", "--json", "name,state,updatedAt"],
                cwd=repo_full_path,
                capture_output=True,
                check=True,
                text=True,
            )
            workflows = json.loads(result.stdout)

            if not workflows:
                console.print(f"No workflows found in {repo_path}", style="yellow")
                return

            table = Table(title=f"🔄 GitHub Actions - {repo_path}")
            table.add_column("Workflow", style="cyan")
            table.add_column("State", style="green")
            table.add_column("Last Updated", style="white")

            for workflow in workflows:
                table.add_row(workflow["name"], workflow["state"], workflow["updatedAt"][:10])

            console.print(table)

        except subprocess.CalledProcessError as e:
            console.print(f"❌ Failed to list workflows: {e.stderr}", style="red")

    def check_security_alerts(self, repo_path: str) -> None:
        """Check for security vulnerabilities in repository."""
        repo_full_path = self.workspace_root / repo_path

        # Check for known security files
        security_files = [
            ".github/SECURITY.md",
            "SECURITY.md",
            ".github/dependabot.yml",
            ".github/workflows/codeql-analysis.yml",
        ]

        console.print(f"🔒 Security Check - {repo_path}", style="bold blue")

        for sec_file in security_files:
            file_path = repo_full_path / sec_file
            if file_path.exists():
                console.print(f"  ✅ {sec_file}", style="green")
            else:
                console.print(f"  ❌ {sec_file}", style="red")

        # Check for vulnerability scanning with GitHub CLI
        if self.gh_available:
            try:
                result = subprocess.run(
                    ["gh", "api", "repos/:owner/:repo/vulnerability-alerts"],
                    check=False,
                    cwd=repo_full_path,
                    capture_output=True,
                    text=True,
                )
                if result.returncode == 0:
                    console.print("  ✅ Vulnerability alerts enabled", style="green")
                else:
                    console.print("  ⚠️ Vulnerability alerts status unknown", style="yellow")
            except subprocess.CalledProcessError:
                console.print("  ⚠️ Could not check vulnerability alerts", style="yellow")
