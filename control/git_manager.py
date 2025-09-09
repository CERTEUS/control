# +=====================================================================+
# |                          CERTEUS                                    |
# +=====================================================================+
# | FILE: control/git_manager.py                                       |
# | ROLE: Manager module for business logic                            |
# | PLIK: control/git_manager.py                                       |
# | ROLA: Moduł menedżera logiki biznesowej                            |
# +=====================================================================+

"""
PL: Moduł zarządzania workspace control dla git_manager

EN: Control workspace management module for git_manager
"""

# === IMPORTY / IMPORTS ===

# === IMPORTY / IMPORTS ===
from __future__ import annotations

from pathlib import Path

from git import Repo
from rich.console import Console
from rich.table import Table

# === KONFIGURACJA / CONFIGURATION ===

console = Console()

# === MODELE / MODELS ===


class GitManager:
    """
    PL: Zarządza operacjami Git na wielu repozytoriach.
    EN: Manages Git operations across multiple repositories.
    """

    def __init__(self, workspace_root: Path) -> None:
        """
        PL: Inicjalizuje menedżer Git dla podanego workspace.
        EN: Initialize Git manager for given workspace.

        Args:
            workspace_root: Ścieżka do głównego katalogu workspace
        """
        self.workspace_root = workspace_root
        self.repos = self._discover_repos()

    # === LOGIKA / LOGIC ===

    def _discover_repos(self) -> dict[str, Path]:
        """
        PL: Odkrywa repozytoria Git w workspace.
        EN: Discover Git repositories in workspace.

        Returns:
            Słownik z nazwami repozytoriów i ich ścieżkami
        """
        repos: dict[str, Path] = {}

        # Main control repo
        if (self.workspace_root / ".git").exists():
            repos["control"] = self.workspace_root

        # Nested repositories
        for path in self.workspace_root.iterdir():
            if path.is_dir() and (path / ".git").exists():
                repos[path.name] = path

        return repos

    def status_all(self) -> None:
        """Show Git status for all repositories."""
        table = Table(title="📊 Git Status Overview")
        table.add_column("Repository", style="cyan")
        table.add_column("Branch", style="yellow")
        table.add_column("Status", style="green")
        table.add_column("Changes", style="red")

        for name, path in self.repos.items():
            try:
                repo = Repo(path)
                branch = repo.active_branch.name

                # Check for uncommitted changes
                changes = []
                if repo.is_dirty():
                    changes.append("dirty")
                if repo.untracked_files:
                    changes.append(f"{len(repo.untracked_files)} untracked")

                status = "✅ Clean" if not changes else "⚠️ Modified"
                changes_str = ", ".join(changes) if changes else "None"

                table.add_row(name, branch, status, changes_str)

            except Exception as e:
                table.add_row(name, "Error", f"❌ {e!s}", "")

        console.print(table)

    def pull_all(self) -> None:
        """Pull latest changes for all repositories."""
        console.print("🔄 Pulling all repositories...", style="bold blue")

        for name, path in self.repos.items():
            try:
                repo = Repo(path)
                console.print(f"📥 {name}: ", end="")

                # Fetch first
                repo.remotes.origin.fetch()

                # Pull if no uncommitted changes
                if not repo.is_dirty():
                    repo.remotes.origin.pull()
                    console.print("✅ Updated", style="green")
                else:
                    console.print("⚠️ Skipped (dirty)", style="yellow")

            except Exception as e:
                console.print(f"❌ Failed: {e}", style="red")

    def fetch_all(self) -> None:
        """Fetch all repositories without merging."""
        console.print("📡 Fetching all repositories...", style="bold blue")

        for name, path in self.repos.items():
            try:
                repo = Repo(path)
                console.print(f"📡 {name}: ", end="")
                repo.remotes.origin.fetch()
                console.print("✅ Fetched", style="green")

            except Exception as e:
                console.print(f"❌ Failed: {e}", style="red")

    def switch_branch(self, branch_name: str, repo_name: Optional[str] = None) -> None:
        """Switch branch in specified repo or all repos."""
        targets = {repo_name: self.repos[repo_name]} if repo_name else self.repos

        for name, path in targets.items():
            try:
                repo = Repo(path)
                console.print(f"🔄 {name}: ", end="")

                # Check if branch exists
                if branch_name in [b.name for b in repo.branches]:
                    repo.git.checkout(branch_name)
                    console.print(f"✅ Switched to {branch_name}", style="green")
                else:
                    console.print(f"❌ Branch '{branch_name}' not found", style="red")

            except Exception as e:
                console.print(f"❌ Failed: {e}", style="red")
