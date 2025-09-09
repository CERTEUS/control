# +=====================================================================+
# |                          CERTEUS                                    |
# +=====================================================================+
# | FILE: tests/test_cli.py                                            |
# | ROLE: Test module for automated testing                            |
# | PLIK: tests/test_cli.py                                            |
# | ROLA: Moduł testowy do automatycznych testów                       |
# +=====================================================================+

"""
PL: Moduł zapewniający funkcjonalność test_cli

EN: Module providing test_cli functionality
"""

# === IMPORTY / IMPORTS ===

from __future__ import annotations

from click.testing import CliRunner

from pkg.control.main import cli


def test_cli_help() -> None:
    """Test CLI help command."""
    runner = CliRunner()
    result = runner.invoke(cli, ["--help"])
    assert result.exit_code == 0  # noqa: S101  # Test assertion
    assert "Control workspace" in result.output  # noqa: S101  # Test assertion


def test_status_command() -> None:
    """Test status command."""
    runner = CliRunner()
    result = runner.invoke(cli, ["status"])
    assert result.exit_code == 0  # noqa: S101  # Test assertion
    assert "Control Status" in result.output  # noqa: S101  # Test assertion


def test_health_command() -> None:
    """Test health command."""
    runner = CliRunner()
    result = runner.invoke(cli, ["health"])
    assert result.exit_code == 0  # noqa: S101  # Test assertion
    assert "Environment Health Check" in result.output  # noqa: S101  # Test assertion
