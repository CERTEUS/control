# +=====================================================================+
# |                          CERTEUS                                    |
# +=====================================================================+
# | FILE: control/docker_manager.py                                   |
# | ROLE: Docker container management for all projects                |
# | PLIK: control/docker_manager.py                                   |
# | ROLA: Zarządzanie kontenerami Docker dla wszystkich projektów     |
# +=====================================================================+

"""
PL: Menedżer Docker dla workspace control

EN: Docker manager for control workspace
"""

# === IMPORTY / IMPORTS ===
from __future__ import annotations

import subprocess
import sys
from pathlib import Path
from typing import Any, Optional

import docker
import yaml
from rich.console import Console
from rich.table import Table

console = Console()

# === KLASY / CLASSES ===


class DockerManager:
    """
    PL: Menedżer kontenerów Docker dla wszystkich projektów.
    EN: Docker container manager for all projects.
    """

    def __init__(self, workspace_root: Path) -> None:
        """
        PL: Inicjalizuje menedżer Docker.
        EN: Initialize Docker manager.
        """
        self.workspace_root = workspace_root
        self.client = docker.from_env()
        self.config = self._load_config()

    def _load_config(self) -> dict[str, Any]:
        """
        PL: Ładuje konfigurację agentów.
        EN: Load agent configuration.
        """
        config_path = self.workspace_root / ".agentconfig.yml"
        if config_path.exists():
            with config_path.open(encoding="utf-8") as f:
                return yaml.safe_load(f)
        return {}

    def status(self) -> None:
        """
        PL: Pokazuje status wszystkich kontenerów.
        EN: Show status of all containers.
        """
        console.print("\n🐳 [bold blue]Docker Container Status[/bold blue]")

        table = Table()
        table.add_column("Container", style="cyan", no_wrap=True)
        table.add_column("Image", style="white")
        table.add_column("Status", style="green")
        table.add_column("Ports", style="yellow")
        table.add_column("Health", style="magenta")

        try:
            containers = self.client.containers.list(all=True)
            for container in containers:
                # Status color
                status_color = "green" if container.status == "running" else "red"
                status = f"[{status_color}]{container.status}[/{status_color}]"

                # Health check
                health = "N/A"
                if hasattr(container.attrs, "State") and "Health" in container.attrs.get(
                    "State", {}
                ):
                    health_status = container.attrs["State"]["Health"]["Status"]
                    health_color = "green" if health_status == "healthy" else "red"
                    health = f"[{health_color}]{health_status}[/{health_color}]"

                # Ports
                ports = []
                if container.ports:
                    for port, bindings in container.ports.items():
                        if bindings:
                            for binding in bindings:
                                ports.append(f"{binding['HostPort']}:{port}")
                ports_str = ", ".join(ports) if ports else "None"

                table.add_row(
                    container.name,
                    container.image.tags[0] if container.image.tags else "unknown",
                    status,
                    ports_str,
                    health,
                )

            console.print(table)
        except Exception as e:
            console.print(f"[red]Error fetching container status: {e}[/red]")

    def start_stack(self) -> None:
        """
        PL: Uruchamia cały stos kontenerów.
        EN: Start the entire container stack.
        """
        console.print("\n🚀 [bold green]Starting Control Stack[/bold green]")

        compose_file = self.workspace_root / "docker-compose.yml"
        if not compose_file.exists():
            console.print("[red]docker-compose.yml not found![/red]")
            return

        try:
            cmd = ["docker-compose", "-f", str(compose_file), "up", "-d"]
            result = subprocess.run(cmd, capture_output=True, text=True, cwd=self.workspace_root)

            if result.returncode == 0:
                console.print("[green]✓ Stack started successfully[/green]")
                console.print(result.stdout)
            else:
                console.print(f"[red]✗ Error starting stack: {result.stderr}[/red]")

        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")

    def stop_stack(self) -> None:
        """
        PL: Zatrzymuje cały stos kontenerów.
        EN: Stop the entire container stack.
        """
        console.print("\n🛑 [bold red]Stopping Control Stack[/bold red]")

        compose_file = self.workspace_root / "docker-compose.yml"
        if not compose_file.exists():
            console.print("[red]docker-compose.yml not found![/red]")
            return

        try:
            cmd = ["docker-compose", "-f", str(compose_file), "down"]
            result = subprocess.run(cmd, capture_output=True, text=True, cwd=self.workspace_root)

            if result.returncode == 0:
                console.print("[green]✓ Stack stopped successfully[/green]")
            else:
                console.print(f"[red]✗ Error stopping stack: {result.stderr}[/red]")

        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")

    def restart_service(self, service_name: str) -> None:
        """
        PL: Restartuje konkretny serwis.
        EN: Restart specific service.
        """
        console.print(f"\n🔄 [bold yellow]Restarting {service_name}[/bold yellow]")

        try:
            container = self.client.containers.get(f"control-{service_name}")
            container.restart()
            console.print(f"[green]✓ {service_name} restarted successfully[/green]")
        except docker.errors.NotFound:
            console.print(f"[red]✗ Container control-{service_name} not found[/red]")
        except Exception as e:
            console.print(f"[red]Error restarting {service_name}: {e}[/red]")

    def logs(self, service_name: str, lines: int = 50) -> None:
        """
        PL: Pokazuje logi kontenera.
        EN: Show container logs.
        """
        console.print(f"\n📋 [bold blue]Logs for {service_name} (last {lines} lines)[/bold blue]")

        try:
            container = self.client.containers.get(f"control-{service_name}")
            logs = container.logs(tail=lines, timestamps=True).decode("utf-8")
            console.print(logs)
        except docker.errors.NotFound:
            console.print(f"[red]✗ Container control-{service_name} not found[/red]")
        except Exception as e:
            console.print(f"[red]Error fetching logs: {e}[/red]")

    def health_check(self) -> dict[str, bool]:
        """
        PL: Sprawdza health wszystkich serwisów.
        EN: Check health of all services.
        """
        health_status = {}

        # Service name mappings (logical name -> actual container name)
        service_containers = {
            "postgres": ["control-postgres", "infra-postgres-1"],
            "redis": ["control-redis", "infra-redis-1"],
            "minio": ["control-minio"],
            "ollama": ["control-ollama", "ollama"],
            "codex": ["control-codex", "codex"],
        }

        for service, container_names in service_containers.items():
            health_status[service] = False
            for container_name in container_names:
                try:
                    container = self.client.containers.get(container_name)
                    if container.status == "running":
                        # Check if container has health check configured
                        health_data = container.attrs.get("State", {}).get("Health")
                        if health_data:
                            health_status[service] = health_data.get("Status") == "healthy"
                        else:
                            # No health check configured, consider running as healthy
                            health_status[service] = True
                        break
                except Exception:
                    continue

        return health_status

    def start_testing_stack(self) -> None:
        """
        PL: Uruchamia kompletny stack testowy z wszystkimi narzędziami CI.
        EN: Start complete testing stack with all CI tools.
        """
        console.print("\n🧪 [bold blue]Starting Testing Stack[/bold blue]")

        compose_file = self.workspace_root / "docker-compose.testing.yml"
        if not compose_file.exists():
            console.print("[red]docker-compose.testing.yml not found![/red]")
            return

        try:
            cmd = ["docker-compose", "-f", str(compose_file), "up", "-d", "--build"]
            result = subprocess.run(cmd, capture_output=True, text=True, cwd=self.workspace_root)

            if result.returncode == 0:
                console.print("[green]✓ Testing stack started successfully[/green]")
                console.print("[cyan]Available services:[/cyan]")
                console.print("  • PostgreSQL:    localhost:5432")
                console.print("  • Redis:         localhost:6379")
                console.print("  • MinIO:         localhost:9000 (API), localhost:9001 (Console)")
                console.print("  • Ollama:        localhost:11434")
                console.print("  • Certeus API:   localhost:8000")
                console.print("  • ProofGate:     localhost:8081")
                console.print("  • Prometheus:    localhost:9090")
                console.print("  • Grafana:       localhost:3000 (admin:admin)")
                console.print("  • SonarQube:     localhost:9001")
                console.print(result.stdout)
            else:
                console.print(f"[red]✗ Error starting testing stack: {result.stderr}[/red]")

        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")

    def stop_testing_stack(self) -> None:
        """
        PL: Zatrzymuje kompletny stack testowy.
        EN: Stop complete testing stack.
        """
        console.print("\n🛑 [bold red]Stopping Testing Stack[/bold red]")

        compose_file = self.workspace_root / "docker-compose.testing.yml"
        if not compose_file.exists():
            console.print("[red]docker-compose.testing.yml not found![/red]")
            return

        try:
            cmd = ["docker-compose", "-f", str(compose_file), "down", "-v"]
            result = subprocess.run(cmd, capture_output=True, text=True, cwd=self.workspace_root)

            if result.returncode == 0:
                console.print("[green]✓ Testing stack stopped successfully[/green]")
                console.print(result.stdout)
            else:
                console.print(f"[red]✗ Error stopping testing stack: {result.stderr}[/red]")

        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")

    def run_ci_tests(self) -> None:
        """
        PL: Uruchamia pełny zestaw testów CI w kontenerze.
        EN: Run complete CI test suite in container.
        """
        console.print("\n🧪 [bold cyan]Running CI Tests[/bold cyan]")

        try:
            # Check if testing container is running
            container_name = "control-certeus-testing"
            container = self.client.containers.get(container_name)

            if container.status != "running":
                console.print(
                    f"[red]Container {container_name} is not running. Start testing stack first.[/red]"
                )
                return

            # Run pytest with all CI options
            cmd = [
                "python",
                "-m",
                "pytest",
                "--cov=.",
                "--cov-report=term",
                "--cov-report=xml:out/coverage.xml",
                "--cov-report=html:out/htmlcov",
                "--cov-fail-under=0",
                "-v",
            ]

            console.print(f"[cyan]Running: {' '.join(cmd)}[/cyan]")
            result = container.exec_run(cmd, workdir="/workspace")

            console.print(result.output.decode())

            if result.exit_code == 0:
                console.print("[green]✓ All tests passed[/green]")
            else:
                console.print(f"[red]✗ Tests failed with exit code {result.exit_code}[/red]")

        except Exception as e:
            console.print(f"[red]Error running tests: {e}[/red]")

    def run_ci_gates(self) -> None:
        """
        PL: Uruchamia CI gates (lint, security, quality checks).
        EN: Run CI gates (lint, security, quality checks).
        """
        console.print("\n🚪 [bold magenta]Running CI Gates[/bold magenta]")

        try:
            container_name = "control-certeus-testing"
            container = self.client.containers.get(container_name)

            if container.status != "running":
                console.print(
                    f"[red]Container {container_name} is not running. Start testing stack first.[/red]"
                )
                return

            gates = [
                ("Linting", ["python", "-m", "ruff", "check", "."]),
                (
                    "Type checking",
                    [
                        "python",
                        "-m",
                        "mypy",
                        "--config-file",
                        "mypy.ini",
                        "certeus",
                    ],
                ),
                (
                    "Security scan",
                    ["python", "-m", "bandit", "-r", ".", "-f", "json"],
                ),
                (
                    "Safety check",
                    ["python", "-m", "safety", "check", "--continue-on-error"],
                ),
                (
                    "Codespell",
                    ["codespell"],
                ),
            ]

            for gate_name, cmd in gates:
                console.print(f"[cyan]Running {gate_name}...[/cyan]")
                result = container.exec_run(cmd, workdir="/workspace")

                if result.exit_code == 0:
                    console.print(f"[green]✓ {gate_name} passed[/green]")
                else:
                    console.print(f"[yellow]⚠ {gate_name} issues found[/yellow]")
                    console.print(result.output.decode()[:500])

        except Exception as e:
            console.print(f"[red]Error running CI gates: {e}[/red]")

    def cleanup(self) -> None:
        """
        PL: Czyści niepotrzebne kontenery i obrazy.
        EN: Clean up unused containers and images.
        """
        console.print("\n🧹 [bold magenta]Cleaning up Docker resources[/bold magenta]")

        try:
            # Remove stopped containers
            self.client.containers.prune()
            console.print("[green]✓ Stopped containers removed[/green]")

            # Remove unused images
            self.client.images.prune(filters={"dangling": False})
            console.print("[green]✓ Unused images removed[/green]")

            # Remove unused volumes
            self.client.volumes.prune()
            console.print("[green]✓ Unused volumes removed[/green]")

        except Exception as e:
            console.print(f"[red]Error during cleanup: {e}[/red]")

    def exec_command(self, service_name: str, command: str) -> None:
        """
        PL: Wykonuje komendę w kontenerze.
        EN: Execute command in container.
        """
        console.print(f"\n⚡ [bold cyan]Executing in {service_name}: {command}[/bold cyan]")

        try:
            container = self.client.containers.get(f"control-{service_name}")
            result = container.exec_run(command, stdout=True, stderr=True)
            console.print(result.output.decode("utf-8"))
        except docker.errors.NotFound:
            console.print(f"[red]✗ Container control-{service_name} not found[/red]")
        except Exception as e:
            console.print(f"[red]Error executing command: {e}[/red]")
