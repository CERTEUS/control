# +=====================================================================+
# |                          CERTEUS                                    |
# +=====================================================================+
# | FILE: conftest.py                                                  |
# | ROLE: Application module                                           |
# | PLIK: conftest.py                                                  |
# | ROLA: Moduł aplikacji                                              |
# +=====================================================================+

"""
PL: Moduł zapewniający funkcjonalność conftest

EN: Module providing conftest functionality
"""

# === IMPORTY / IMPORTS ===

from __future__ import annotations

import pytest


@pytest.fixture
def control_version():
    """Provide control package version."""
    from control import __version__

    return __version__


@pytest.fixture
def temp_repo_dir(tmp_path):
    """Provide temporary directory for repository testing."""
    repo_dir = tmp_path / "test_repo"
    repo_dir.mkdir()
    return repo_dir
