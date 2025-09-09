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

from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from pathlib import Path

# Import at module level for fixture
from pkg.control import __version__


@pytest.fixture
def control_version() -> str:
    """Provide control package version."""
    return __version__


@pytest.fixture
def temp_repo_dir(tmp_path: Path) -> Path:
    """Provide temporary directory for repository testing."""
    repo_dir = tmp_path / "test_repo"
    repo_dir.mkdir()
    return repo_dir
