# +=====================================================================+
# |                    CONTROL - Simple Migration                      |
# +=====================================================================+
# | FILE: control/migration_manager.py                                |
# | ROLE: Simple duplication cleanup                                  |
# +=====================================================================+

"""Simple migration manager for control workspace."""

from __future__ import annotations

from pathlib import Path

from rich.console import Console
from rich.prompt import Confirm

console = Console()


class MigrationManager:
    """Simple migration manager for projects."""

    def __init__(self, workspace_root: Path) -> None:
        """Initialize migration manager."""
        self.workspace_root = workspace_root

    def run_consolidation_wizard(self) -> None:
        """Run simple consolidation wizard."""
        console.print("\n🧙 [bold magenta]Project Consolidation Wizard[/bold magenta]")

        # Check for certeus duplication
        base_certeus = Path("f:/projekty/certeus")
        workspace_certeus = self.workspace_root / "workspaces" / "certeus"

        if base_certeus.exists() and workspace_certeus.exists():
            console.print("\n📊 [bold yellow]Found certeus duplication[/bold yellow]")
            console.print(f"1. Original: {base_certeus}")
            console.print(f"2. Workspace: {workspace_certeus}")

            choice = Confirm.ask("Keep workspace version and remove original?", default=True)

            if choice:
                console.print("[green]✓ Using workspace version - no action needed[/green]")
                console.print(
                    "[yellow]⚠️  You can manually remove f:/projekty/certeus if needed[/yellow]"
                )
            else:
                console.print("[yellow]Keeping both versions for now[/yellow]")
        else:
            console.print("[green]✓ No duplicates found![/green]")

        console.print("\n🎉 [bold green]Consolidation completed![/bold green]")
