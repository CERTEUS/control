#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path
import runpy

HERE = Path(__file__).resolve()
TARGET = HERE.parents[2] / "certeus" / "scripts" / "gates" / "boundary_rebuild_gate.py"

if __name__ == "__main__":
    try:
        runpy.run_path(str(TARGET), run_name="__main__")
    except SystemExit as e:
        try:
            sys.exit(int(e.code) if e.code is not None else 0)
        except Exception:
            sys.exit(1)

