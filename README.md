# CONTROL — AUTOREPO

Repozytorium sterujące dla zarządzania wieloma projektami z zachowaniem czystej separacji środowisk.

## Cel

To repozytorium pełni rolę autonomicznego „control plane" - centralne miejsce zarządzania różnymi projektami i repozytoriami, utrzymując zawsze jedno okno dostępu do działania w różnych projektach.

## Struktura środowisk

- **Control** (to repo): Własne środowisko wirtualne `.venv/` z narzędziami zarządzania
- **Certeus** (zagnieżdżone): Izolowane środowisko `certeus/.venv/` z zależnościami projektu

## Konfiguracja VS Code

Projekt skonfigurowany dla unikania konfliktów:

- Każde repo ma własny interpreter Python
- Wykluczenie zagnieżdżonych `.venv` z analizy Pylance
- Izolacja konfiguracji między projektami
- Optymalizacja wydajności dla dużych codebases

## Użycie

```bash
# Aktywacja środowiska control
source .venv/bin/activate  # Linux/macOS
.venv\Scripts\activate.bat  # Windows

# Status repozytoriów
control status

# Sprawdzenie środowiska
control health
```

## Gałęzie i CI

- Robocza gałąź: `work/daily`; stabilna: `main`
- CI: workflow `control-ci` checkoutuje submodule (recursive) i uruchamia testy w `certeus`
- Cięższe bramki (`ci-gates`) biegną w `certeus` na PR/main

## Struktura repo

- **Produkt** (kod, SDK, schematy, serwisy): wyłącznie w submodule `certeus/`
- **Control** (to repo): orkiestracja, narzędzia i automatyzacje
- **Artefakty tymczasowe**: ignorowane (patrz `.gitignore`)

## Utrzymanie

1. Aktualizuj zależności: `pip install --upgrade -e .`
2. Sprawdzaj formatowanie: `ruff check .`
3. Uruchamiaj testy: `pytest`
4. Kontroluj status: `control status`
