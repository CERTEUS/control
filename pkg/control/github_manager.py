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
import os
import subprocess
from pathlib import Path  # noqa: TC003  # Used at runtime in constructor

from rich.console import Console
from rich.table import Table

# === STAŁE / CONSTANTS ===

GH_CLI_NOT_AVAILABLE_MSG = "❌ GitHub CLI not available"

console = Console()


class GitHubManager:
    """Manages GitHub operations and integrations."""

    def __init__(self, workspace_root: Path) -> None:
        self.workspace_root = workspace_root
        self.gh_executable = self._find_gh_executable()
        self.gh_available = self._check_gh_cli()

    def _find_gh_executable(self) -> str:
        """Find the full path to the gh executable."""
        # Check common paths
        common_paths = [
            "gh.exe",  # In PATH
            "gh",  # In PATH (Unix)
            r"C:\Program Files\GitHub CLI\gh.exe",  # Windows default
            r"C:\Users\{username}\AppData\Local\GitHub CLI\gh.exe",  # Windows user
        ]

        # Check PATH first
        for path in common_paths[:2]:
            try:
                result = subprocess.run(  # noqa: S603  # Validated command arguments
                    ["where" if os.name == "nt" else "which", path],
                    capture_output=True,
                    text=True,
                    timeout=5,
                    check=False,
                )
                if result.returncode == 0:
                    return result.stdout.strip().split("\n")[0]
            except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
                continue

        # Fallback to just 'gh' if not found
        return "gh"

    def _validate_gh_args(self, args: list[str]) -> bool:
        """Validate GitHub CLI arguments to prevent injection."""
        # Basic validation for JSON fields and repo names
        return all(not any(char in arg for char in [";", "&", "|", "`", "$", "("]) for arg in args)

    def _run_gh_command(
        self, args: list[str], cwd: Path | None = None
    ) -> subprocess.CompletedProcess[str]:
        """Safely run GitHub CLI command with validation."""
        if not self._validate_gh_args(args):
            msg = f"Invalid or unsafe GitHub CLI arguments: {args}"
            raise ValueError(msg)

        full_args = [self.gh_executable, *args]
        return subprocess.run(  # noqa: S603  # Arguments validated by _validate_gh_args
            full_args,
            capture_output=True,
            text=True,
            timeout=30,  # Add timeout
            check=False,  # We handle return codes manually
            cwd=cwd,
        )

    def _check_gh_cli(self) -> bool:
        """Check if GitHub CLI is available."""
        try:
            result = self._run_gh_command(["--version"])
        except (
            subprocess.CalledProcessError,
            FileNotFoundError,
            subprocess.TimeoutExpired,
            ValueError,
        ):
            return False
        else:
            return result.returncode == 0

    def status_all_repos(self) -> None:
        """Show GitHub status for all repositories."""
        if not self.gh_available:
            console.print(
                f"{GH_CLI_NOT_AVAILABLE_MSG}. Install with: winget install GitHub.cli", style="red"
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
            result = self._run_gh_command(
                ["repo", "list", "--json", "name,visibility,defaultBranch,updatedAt"]
            )

            if result.returncode != 0:
                console.print(f"❌ GitHub API error: {result.stderr}", style="red")
                return

            repos = json.loads(result.stdout)

            for repo in repos:
                # Get PR count
                pr_result = self._run_gh_command(
                    ["pr", "list", "--repo", repo["name"], "--json", "number"]
                )

                pr_count = 0
                if pr_result.returncode == 0:
                    pr_count = len(json.loads(pr_result.stdout))

                table.add_row(
                    repo["name"],
                    repo["visibility"],
                    repo["defaultBranch"],
                    str(pr_count),
                    repo["updatedAt"][:10],  # Date only
                )

            console.print(table)

        except ValueError as e:
            console.print(f"❌ GitHub API error: {e}", style="red")

    def create_pr(self, repo_path: str, title: str, body: str = "") -> None:
        """Create a pull request for a repository."""
        if not self.gh_available:
            console.print(GH_CLI_NOT_AVAILABLE_MSG, style="red")
            return

        repo_full_path = self.workspace_root / repo_path

        try:
            result = self._run_gh_command(
                ["pr", "create", "--title", title, "--body", body], cwd=repo_full_path
            )

            if result.returncode == 0:
                console.print(f"✅ PR created: {result.stdout.strip()}", style="green")
            else:
                console.print(f"❌ Failed to create PR: {result.stderr}", style="red")

        except ValueError as e:
            console.print(f"❌ Failed to create PR: {e}", style="red")

    def sync_fork(self, repo_path: str) -> None:
        """Sync fork with upstream repository."""
        if not self.gh_available:
            console.print(GH_CLI_NOT_AVAILABLE_MSG, style="red")
            return

        repo_full_path = self.workspace_root / repo_path

        try:
            result = self._run_gh_command(["repo", "sync"], cwd=repo_full_path)

            if result.returncode == 0:
                console.print(f"✅ Synced fork: {repo_path}", style="green")
            else:
                console.print(f"❌ Failed to sync fork: {result.stderr}", style="red")

        except ValueError as e:
            console.print(f"❌ Failed to sync fork: {e}", style="red")

    def list_workflows(self, repo_path: str) -> None:
        """List GitHub Actions workflows for a repository."""
        if not self.gh_available:
            console.print(GH_CLI_NOT_AVAILABLE_MSG, style="red")
            return

        repo_full_path = self.workspace_root / repo_path

        try:
            result = self._run_gh_command(
                ["workflow", "list", "--json", "name,state,updatedAt"], cwd=repo_full_path
            )

            if result.returncode != 0:
                console.print(f"❌ Failed to list workflows: {result.stderr}", style="red")
                return

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
                result = self._run_gh_command(
                    ["api", "repos/:owner/:repo/vulnerability-alerts"], cwd=repo_full_path
                )

                if result.returncode == 0:
                    console.print("  ✅ Vulnerability alerts enabled", style="green")
                else:
                    console.print("  ⚠️ Vulnerability alerts status unknown", style="yellow")
            except ValueError:
                console.print("  ⚠️ Could not check vulnerability alerts", style="yellow")
