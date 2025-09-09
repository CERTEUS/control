# PR Policy — Control

## Zasady

- Gałęzie: praca na `work/daily`; PR kierowany na `main` po zielonych przebiegach `Tests`.
- CI: `control-ci` uruchamia testy w submodule `certeus` (kanoniczny zestaw).
- Dokumentacja musi być aktualna (AGENT.md, WORKLOG, CHANGELOG) dla zmian procesowych.
- Skany/secrets: brak wrażliwych danych w diffs.

## Checklist PR

- [ ] Lint/format: `ruff check . --fix` / `ruff format .` (jeśli dotyczy)
- [ ] `cd certeus && pytest -q` lokalnie zielone
- [ ] Dokumentacja zaktualizowana (AGENT.md/WORKLOG/CHANGELOG)
- [ ] OpenAPI sync/verify (jeśli dotyczy): `tools/openapi-sync.sh verify`
- [ ] Zielone statusy `control-ci` (i `Tests` w Certeus)

