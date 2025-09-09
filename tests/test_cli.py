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

from control.main import cli


def test_cli_help():
    """Test CLI help command."""
    runner = CliRunner()
    result = runner.invoke(cli, ["--help"])
    assert result.exit_code == 0
    assert "Control workspace manager" in result.output


def test_status_command():
    """Test status command."""
    runner = CliRunner()
    result = runner.invoke(cli, ["status"])
    assert result.exit_code == 0
    assert "Control Status" in result.output


def test_health_command():
    """Test health command."""
    runner = CliRunner()
    result = runner.invoke(cli, ["health"])
    assert result.exit_code == 0
    assert "Environment Health Check" in result.output
