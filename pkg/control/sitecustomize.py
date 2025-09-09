# +=====================================================================+
# |                          CERTEUS                                    |
# +=====================================================================+
# | FILE: sitecustomize.py                                             |
# | ROLE: Application module                                           |
# | PLIK: sitecustomize.py                                             |
# | ROLA: Moduł aplikacji                                              |
# +=====================================================================+

"""
PL: Moduł zapewniający funkcjonalność sitecustomize

EN: Module providing sitecustomize functionality
"""

# === IMPORTY / IMPORTS ===

from __future__ import annotations

# +=====================================================================+
# |                          CONTROL                                    |
# +=====================================================================+
# | MODULE:  F:/projekty/control/sitecustomize.py                       |
# | DATE:    2025-09-09                                                  |
# | PURPOSE: Clean environment separation for multi-repo workspace      |
# +=====================================================================+
import os
import sys
from pathlib import Path


def setup_control_environment() -> None:
    """Set up clean Python environment for control workspace."""
    try:
        # Get control repo root
        repo_root = Path(__file__).resolve().parent

        # Ensure control's .venv Scripts is on PATH for subprocess execution
        control_scripts = repo_root / ".venv" / "Scripts"
        if control_scripts.exists():
            current_path = os.environ.get("PATH", "")
            scripts_str = str(control_scripts)

            # Only add if not already present
            if scripts_str not in current_path.split(os.pathsep):
                os.environ["PATH"] = scripts_str + os.pathsep + current_path

        # Set PYTHONPATH to include control package root
        control_python_path = str(repo_root)
        current_pythonpath = os.environ.get("PYTHONPATH", "")

        if current_pythonpath:
            if control_python_path not in current_pythonpath.split(os.pathsep):
                os.environ["PYTHONPATH"] = control_python_path + os.pathsep + current_pythonpath
        else:
            os.environ["PYTHONPATH"] = control_python_path

        # Ensure control package can be imported
        if str(repo_root) not in sys.path:
            sys.path.insert(0, str(repo_root))

    except Exception:  # noqa: S110  # Silent fail is intended for environment setup
        # Fail silently to avoid breaking environment
        pass


# Execute setup when module is imported
setup_control_environment()
