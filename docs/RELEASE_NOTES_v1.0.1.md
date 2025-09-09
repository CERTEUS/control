# RELEASE NOTES v1.0.1 — Konsolidacja gałęzi i stabilizacja CI (Control)

Data: 2025-09-09

- Polityka gałęzi: `main` + `work/daily` (jedna robocza); usunięto gałęzie poboczne.
- CI: `control-ci` — checkout submodule (recursive), pip install, testy w `certeus` (`cd certeus && pytest -q`).
- Dokumentacja: zaktualizowano `AGENT.md`, `worklog.md`, dodano `CHANGELOG.md`, `docs/PR_POLICY.md`.
- Narzędzia: `tools/remote-bot/get_installation_token.py`, `wait-branch-green.sh`, `openapi-sync.sh`, orchestrator `tools/agents/*`.

