#!/usr/bin/env python3
from __future__ import annotations

import os
import sys
from pathlib import Path


def main(argv: list[str]) -> int:
    here = Path(__file__).resolve()
    dir_ = here.parent
    target = None
    for up in (dir_, dir_.parent, dir_.parent.parent, dir_.parent.parent.parent):
        cand = up / "certeus" / "tools" / "agents" / "watch_all_green.py"
        if cand.exists():
            target = cand
            break
    if target is None:
        print(f"Cannot locate certeus/tools/agents/watch_all_green.py from {dir_}", file=sys.stderr)
        return 2
    os.execv(sys.executable, [sys.executable, str(target), *argv])
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
