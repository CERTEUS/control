# CHANGELOG — Control

## 2025-09-09 — Konsolidacja gałęzi i stabilizacja CI

- Polityka gałęzi: pozostaje `main` + jedna robocza `work/daily`; usunięto gałęzie poboczne, by uniknąć dryfu.
- CI: workflow `control-ci` checkoutuje submodule (recursive), instaluje zależności pipem i uruchamia testy w `certeus` (`cd certeus && pytest -q`).
- Dokumenty: zaktualizowano `AGENT.md`, `worklog.md` oraz sekcje o polityce gałęzi i CI.
- Narzędzia: `tools/remote-bot/get_installation_token.py`, `wait-branch-green.sh`, `openapi-sync.sh` (verify/sync), orchestrator `tools/agents/*`.

