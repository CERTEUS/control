#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import runpy

HERE = Path(__file__).resolve()
TARGET = HERE.parents[2] / "certeus" / "scripts" / "gates" / "gauge_gate.py"


def main() -> int:
    try:
        runpy.run_path(str(TARGET), run_name="__main__")
    except SystemExit as e:
        try:
            return int(e.code) if e.code is not None else 0
        except Exception:
            return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

