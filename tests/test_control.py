# +=====================================================================+
# |                          CERTEUS                                    |
# +=====================================================================+
# | FILE: tests/test_control.py                                        |
# | ROLE: Test module for automated testing                            |
# | PLIK: tests/test_control.py                                        |
# | ROLA: Moduł testowy do automatycznych testów                       |
# +=====================================================================+

"""
PL: Moduł zarządzania workspace control dla test_control

EN: Control workspace management module for test_control
"""

# === IMPORTY / IMPORTS ===

from __future__ import annotations


def test_control_package_imports():
    """Test that control package can be imported."""
    import control

    assert control.__version__
    assert control.__author__
    assert control.__description__


def test_control_version_format(control_version):
    """Test that version follows semantic versioning."""
    import re

    # Basic semantic versioning pattern
    pattern = r"^\d+\.\d+\.\d+(?:-[a-zA-Z0-9.-]+)?(?:\+[a-zA-Z0-9.-]+)?$"
    assert re.match(pattern, control_version)
