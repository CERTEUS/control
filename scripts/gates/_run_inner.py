#!/usr/bin/env python3
from __future__ import annotations

import runpy
import sys
from pathlib import Path


def run_under_repo(target_rel: str) -> int:
    here = Path(__file__).resolve()
    repo = here.parents[2]
    target = repo / target_rel
    try:
        runpy.run_path(str(target), run_name="__main__")
    except SystemExit as e:  # propagate script's exit code
        try:
            return int(e.code) if e.code is not None else 0
        except Exception:
            return 1
    return 0


def main(argv: list[str]) -> int:  # thin wrapper if needed later
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

