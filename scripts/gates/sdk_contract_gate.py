#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path
import runpy

HERE = Path(__file__).resolve()
TARGET = HERE.parents[2] / "certeus" / "scripts" / "gates" / "sdk_contract_gate.py"

def main() -> int:
    try:
        runpy.run_path(str(TARGET), run_name="__main__")
    except SystemExit as e:
        try:
            code = int(e.code) if e.code is not None else 0
        except Exception:
            code = 1
    else:
        code = 0
    # Align report location expected by tests: move certeus/out -> ./out
    try:
        repo_root = Path(__file__).resolve().parents[2]
        inner_out = repo_root / "certeus" / "out" / "sdk_contract_report.json"
        outer_dir = repo_root / "out"
        if inner_out.exists():
            outer_dir.mkdir(parents=True, exist_ok=True)
            (outer_dir / "sdk_contract_report.json").write_text(inner_out.read_text(encoding="utf-8"), encoding="utf-8")
    except Exception:
        pass
    return code

if __name__ == "__main__":
    raise SystemExit(main())
