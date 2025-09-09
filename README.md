# CONTROL — AUTOREPO

To repozytorium pełni rolę autonomicznego „control plane”.

Dokumentacja operacyjna i szczegóły działania są wewnętrzne i niepubliczne.
Jeśli potrzebujesz dostępu, skontaktuj się z właścicielami organizacji.

Zakres publicznych informacji celowo ograniczono.

## Gałęzie i CI

- Robocza gałąź: `work/daily`; stabilna: `main`.
- CI: workflow `control-ci` checkoutuje submodule (recursive) i uruchamia testy w `certeus` (`cd certeus && pytest -q`).
- Cięższe bramki (`ci-gates`) biegną w `certeus` na PR/main.

## Struktura repo

- Produkt (kod, SDK, schematy, serwisy, klienci, dokumentacja): wyłącznie w submodule `certeus/`.
- Control (to repo): orkiestracja, narzędzia i automatyzacje (np. `tools/`, `devops/`, mirrory OpenAPI w `docs/api/`).
- Artefakty tymczasowe: ignorowane (patrz `.gitignore` — `exports/`, `out/`).

Uwaga: katalogi produktu z poziomu root (`clients/`, `services/`, `sdk/`, `schemas/`, `scripts/`, `security/`, `static/`, `packs/`, `tasks/`) zostały usunięte z `control` i przeniesione/uzupełnione w `certeus/` (jeśli brakowało). Dzięki temu `control` pozostaje czyste i pełni rolę nadrzędnego „control plane”.
