# Ensure local venv Scripts is on PATH so subprocess can find `python3`
import os
from pathlib import Path

try:
    repo = Path(__file__).resolve().parent
    scripts = repo / ".venv" / "Scripts"
    if scripts.exists():
        p = os.environ.get("PATH", "")
        sp = str(scripts)
        if sp not in p.split(os.pathsep):
            os.environ["PATH"] = sp + os.pathsep + p
except Exception:
    pass
