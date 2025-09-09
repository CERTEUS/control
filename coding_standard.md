# CERTEUS & CONTROL — ENTERPRISE CODING STANDARD

> **Jeden niepowtarzalny standard kodowania dla wszystkich projektów CERTEUS**  
> Wersja: 3.0 (Enterprise Big Tech)  
> Data: 2025-09-09  
> Status: OBOWIĄZUJĄCY dla wszystkich agentów (człowiek + AI)

## 🎯 Cel i filozofia

Kod ma być **czytelny**, **przewidywalny**, **testowalny**, **proof-native** i **enterprise-ready**.  
Zasada: **czytelność > spryt**, **deterministyczność**, **bezpieczeństwo domyślne**.

CERTEUS to **Big Tech** — utrzymujemy standardy na poziomie Google/Microsoft/Meta.

---

## 📋 SPIS TREŚCI

1. [Nagłówki plików (ForgeHeader v3)](#forgeheader)
2. [Struktura kodu (sekcje)](#struktura)
3. [Nazewnictwo i konwencje](#nazewnictwo)
4. [Języki programowania](#jezyki)
5. [Konfiguracja narzędzi](#narzedzia)
6. [Bezpieczeństwo i błędy](#bezpieczenstwo)
7. [Testy i jakość](#testy)
8. [Git i CI/CD](#git)
9. [Dokumentacja](#dokumentacja)
10. [Checklist dla PR](#checklist)

---

## 🏗️ Nagłówki plików (ForgeHeader v3) {#forgeheader}

**KAŻDY plik musi zawierać standardowy nagłówek CERTEUS.**

### Python (.py)

```python
# +=====================================================================+
# |                          CERTEUS                                    |
# +=====================================================================+
# | FILE: services/api_gateway/main.py                                  |
# | ROLE: FastAPI main application entry point                          |
# | PLIK: services/api_gateway/main.py                                  |
# | ROLA: Główny punkt wejścia aplikacji FastAPI                        |
# +=====================================================================+

"""
PL: Główna aplikacja FastAPI z routerami i middleware.
    Obsługuje autentyfikację, CORS i telemetrię OpenTelemetry.

EN: Main FastAPI application with routers and middleware.
    Handles authentication, CORS and OpenTelemetry telemetry.
"""

# === IMPORTY / IMPORTS ===

from __future__ import annotations

import logging
from fastapi import FastAPI
# ... pozostałe importy

# === KONFIGURACJA / CONFIGURATION ===

logger = logging.getLogger(__name__)

# === MODELE / MODELS ===

# Modele danych, typy, struktury

# === LOGIKA / LOGIC ===

# Logika biznesowa, funkcje pomocnicze

# === I/O / ENDPOINTS ===

# API endpoints, HTTP handlers

# === TESTY / TESTS ===

# Funkcje testowe (tylko w plikach test_*)
```

### Shell (.sh, .bash)

```bash
#!/usr/bin/env bash
# +=====================================================================+
# |                          CERTEUS                                    |
# +=====================================================================+
# | FILE: scripts/deploy.sh                                             |
# | ROLE: Production deployment script                                  |
# | PLIK: scripts/deploy.sh                                             |
# | ROLA: Skrypt wdrażania produkcyjnego                                |
# +=====================================================================+

# PL: Skrypt automatyzujący wdrożenie na środowisko produkcyjne.
# EN: Script automating deployment to production environment.

set -Eeuo pipefail
trap 'echo "[ERR] $0 line:$LINENO status:$?" >&2' ERR

# === KONFIGURACJA / CONFIGURATION ===

readonly SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
readonly PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

# === FUNKCJE / FUNCTIONS ===

deploy_app() {
    echo "Deploying application..."
    # implementacja
}

# === MAIN ===

main() {
    deploy_app
}

if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi
```

### TypeScript/JavaScript (.ts, .js)

```typescript
/*
 * +=====================================================================+
 * |                          CERTEUS                                    |
 * +=====================================================================+
 * | FILE: clients/web/src/components/Dashboard.tsx                      |
 * | ROLE: Main dashboard component                                      |
 * | PLIK: clients/web/src/components/Dashboard.tsx                      |
 * | ROLA: Główny komponent dashboardu                                   |
 * +=====================================================================+
 */

/**
 * PL: Główny komponent dashboardu z metrykami i statusem systemu.
 * EN: Main dashboard component with metrics and system status.
 */

// === IMPORTS / IMPORTY ===

import React from 'react';
import { useState, useEffect } from 'react';
import type { DashboardData } from '../types';

// === TYPES / TYPY ===

interface DashboardProps {
  refreshInterval?: number;
}

// === LOGIC / LOGIKA ===

// === COMPONENTS / KOMPONENTY ===

export const Dashboard: React.FC<DashboardProps> = ({ refreshInterval = 5000 }) => {
  // implementacja
};
```

### HTML (.html)

```html
<!--
+=====================================================================+
|                          CERTEUS                                    |
+=====================================================================+
| FILE: clients/web/public/index.html                                 |
| ROLE: Main web client page                                          |
| PLIK: clients/web/public/index.html                                 |
| ROLA: Główna strona klienta web                                     |
+=====================================================================+
-->

<!DOCTYPE html>
<html lang="pl" data-theme="dark">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>CERTEUS • Dashboard</title>
</head>
<body>
    <!-- PL: Główny kontener aplikacji -->
    <!-- EN: Main application container -->
    <div id="app"></div>
</body>
</html>
```

### YAML (.yml, .yaml)

```yaml
# +=====================================================================+
# |                          CERTEUS                                    |
# +=====================================================================+
# | FILE: .github/workflows/ci.yml                                      |
# | ROLE: Continuous Integration pipeline                               |
# | PLIK: .github/workflows/ci.yml                                      |
# | ROLA: Pipeline ciągłej integracji                                   |
# +=====================================================================+

# PL: Workflow CI z testami, lintingiem i bramkami jakości
# EN: CI workflow with tests, linting and quality gates

name: CI Pipeline
on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
```

---

## 🏗️ Struktura kodu (sekcje) {#struktura}

**Wszystkie pliki muszą mieć uporządkowane sekcje.**

### Python - obowiązkowe sekcje:

```python
# === IMPORTY / IMPORTS ===
# Standard library imports
# Third-party imports  
# Local imports

# === KONFIGURACJA / CONFIGURATION ===
# Constants, config, logger setup

# === MODELE / MODELS ===
# Data models, types, classes

# === LOGIKA / LOGIC ===
# Business logic, helper functions

# === I/O / ENDPOINTS ===
# API endpoints, CLI commands

# === TESTY / TESTS ===
# Test functions (tylko w test_*.py)
```

### TypeScript/JavaScript - obowiązkowe sekcje:

```typescript
// === IMPORTS / IMPORTY ===
// === TYPES / TYPY ===
// === CONSTANTS / STAŁE ===
// === LOGIC / LOGIKA ===
// === COMPONENTS / KOMPONENTY ===
// === EXPORTS / EKSPORTY ===
```

---

## 📝 Nazewnictwo i konwencje {#nazewnictwo}

### Ogólne zasady:

- **Pliki/zmienne/funkcje**: `snake_case`
- **Klasy/Typy**: `PascalCase`
- **Stałe**: `UPPER_CASE`
- **Prywatne**: `_leading_underscore`
- **Katalogi**: `kebab-case` lub `snake_case`

### Struktura projektów:

```
project/
├── src/                    # Kod źródłowy
├── tests/                  # Testy
├── docs/                   # Dokumentacja
├── scripts/                # Skrypty automatyzacji
├── tools/                  # Narzędzia deweloperskie
├── configs/                # Konfiguracje
└── .github/                # CI/CD workflows
```

### Nazwy plików:

- **Python**: `snake_case.py`
- **Tests**: `test_*.py` lub `*_test.py`
- **Scripts**: `kebab-case.sh`
- **Configs**: `snake_case.yml`

---

## 💻 Języki programowania {#jezyki}

### Python (≥3.11)

```python
# Obowiązkowe
from __future__ import annotations

# Type hints wszędzie
def process_data(items: list[dict[str, Any]]) -> ProcessResult:
    """
    PL: Przetwarza dane wejściowe i zwraca wynik.
    EN: Processes input data and returns result.
    
    Args:
        items: Lista słowników z danymi
        
    Returns:
        Przetworzony wynik
        
    Raises:
        ValueError: Gdy dane są nieprawidłowe
    """
    if not items:
        raise ValueError("empty_input")
    
    # implementacja
    return ProcessResult(...)

# Obsługa błędów
try:
    result = process_data(data)
except ValueError as e:
    logger.error("Processing failed: %s", e)
    raise
```

### TypeScript (strict mode)

```typescript
// Zawsze strict mode
export interface ApiResponse<T> {
  readonly data: T;
  readonly status: 'success' | 'error';
  readonly message?: string;
}

// Async/await + proper error handling
export async function fetchData<T>(url: string): Promise<ApiResponse<T>> {
  try {
    const response = await fetch(url);
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }
    
    const data = await response.json();
    return { data, status: 'success' };
  } catch (error) {
    console.error('Fetch failed:', error);
    return { 
      data: null as unknown as T, 
      status: 'error', 
      message: error instanceof Error ? error.message : 'Unknown error' 
    };
  }
}
```

### Bash (strict mode)

```bash
#!/usr/bin/env bash
set -Eeuo pipefail
trap 'echo "[ERR] $0 line:$LINENO status:$?" >&2' ERR

# Sprawdzanie argumentów
if [[ $# -lt 1 ]]; then
    echo "Usage: $0 <command>" >&2
    exit 1
fi

# Bezpieczne cytowanie
readonly COMMAND="${1}"
readonly OUTPUT_DIR="${OUTPUT_DIR:-./output}"

# Funkcje z error handling
deploy() {
    local env="${1:?Environment required}"
    
    if [[ ! -d "$env" ]]; then
        echo "Error: Environment '$env' not found" >&2
        return 1
    fi
    
    echo "Deploying to $env..."
    # implementacja
}
```

---

## 🔧 Konfiguracja narzędzi {#narzedzia}

### Ruff (Python) - pyproject.toml

```toml
[tool.ruff]
line-length = 100
target-version = "py311"
exclude = [
    ".venv",
    "__pycache__",
    ".git",
    "node_modules",
]

[tool.ruff.lint]
select = [
    "E", "F", "W",      # pycodestyle, pyflakes
    "I",                # isort
    "N",                # pep8-naming
    "UP",               # pyupgrade
    "ANN",              # flake8-annotations
    "S",                # bandit
    "B",                # flake8-bugbear
    "A",                # flake8-builtins
    "COM",              # flake8-commas
    "C4",               # flake8-comprehensions
    "DTZ",              # flake8-datetimez
    "T10",              # flake8-debugger
    "EM",               # flake8-errmsg
    "G",                # flake8-logging-format
    "PIE",              # flake8-pie
    "T20",              # flake8-print
    "PT",               # flake8-pytest-style
    "Q",                # flake8-quotes
    "RSE",              # flake8-raise
    "RET",              # flake8-return
    "SLF",              # flake8-self
    "SIM",              # flake8-simplify
    "TID",              # flake8-tidy-imports
    "ARG",              # flake8-unused-arguments
    "PTH",              # flake8-use-pathlib
    "ERA",              # eradicate
    "PL",               # pylint
    "TRY",              # tryceratops
    "RUF",              # ruff-specific
]

ignore = [
    "ANN101",           # self type annotation
    "ANN102",           # cls type annotation
    "COM812",           # trailing comma
    "ISC001",           # implicit string concatenation
]

[tool.ruff.format]
quote-style = "double"
indent-style = "space"
skip-magic-trailing-comma = false
line-ending = "auto"

[tool.ruff.lint.per-file-ignores]
"tests/**/*.py" = ["S101", "PLR2004"]  # assert, magic values in tests
"scripts/**/*.py" = ["T201"]           # print allowed in scripts
```

### ESLint (TypeScript/JavaScript)

```json
{
  "extends": [
    "@typescript-eslint/recommended",
    "@typescript-eslint/recommended-requiring-type-checking"
  ],
  "rules": {
    "@typescript-eslint/no-unused-vars": "error",
    "@typescript-eslint/explicit-function-return-type": "warn",
    "@typescript-eslint/no-explicit-any": "warn",
    "prefer-const": "error",
    "no-var": "error"
  }
}
```

### Prettier

```json
{
  "printWidth": 100,
  "tabWidth": 2,
  "useTabs": false,
  "semi": true,
  "singleQuote": true,
  "quoteProps": "as-needed",
  "trailingComma": "es5",
  "bracketSpacing": true,
  "arrowParens": "avoid"
}
```

---

## 🛡️ Bezpieczeństwo i błędy {#bezpieczenstwo}

### Obsługa błędów (Python)

```python
import logging
from contextlib import contextmanager

logger = logging.getLogger(__name__)

# Zawsze loguj błędy
def risky_operation(data: str) -> Result:
    try:
        return process(data)
    except ValidationError as e:
        logger.warning("Validation failed: %s", e)
        raise
    except Exception as e:
        logger.error("Unexpected error in risky_operation: %s", e, exc_info=True)
        raise ProcessingError(f"Operation failed: {e}") from e

# Context managers dla zasobów
@contextmanager
def managed_resource():
    resource = acquire_resource()
    try:
        yield resource
    finally:
        release_resource(resource)
```

### Bezpieczeństwo

```python
# NIE loguj sekretów
logger.info("User %s authenticated", user_id)  # ✅
logger.info("Password: %s", password)         # ❌

# Walidacja wejścia
def validate_input(data: dict[str, Any]) -> None:
    required_fields = {"user_id", "timestamp"}
    missing = required_fields - data.keys()
    if missing:
        raise ValueError(f"Missing required fields: {missing}")
    
    # Walidacja typów
    if not isinstance(data["user_id"], str):
        raise TypeError("user_id must be string")

# Bezpieczne subprocess
import subprocess
import shlex

def run_command(cmd: str, *args: str) -> str:
    # Użyj listy argumentów zamiast string
    cmd_list = [cmd] + list(args)
    
    try:
        result = subprocess.run(
            cmd_list,
            capture_output=True,
            text=True,
            check=True,
            timeout=30,
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        logger.error("Command failed: %s", e)
        raise
```

---

## 🧪 Testy i jakość {#testy}

### Struktura testów

```python
# === IMPORTY / IMPORTS ===

import pytest
from unittest.mock import Mock, patch
from myapp.service import DataProcessor

# === TESTY / TESTS ===

class TestDataProcessor:
    """Test suite for DataProcessor."""
    
    def test_process_valid_data(self):
        """Should process valid data successfully."""
        # Arrange
        processor = DataProcessor()
        data = {"key": "value"}
        
        # Act
        result = processor.process(data)
        
        # Assert
        assert result.status == "success"
        assert result.data == data
    
    def test_process_invalid_data_raises_error(self):
        """Should raise ValueError for invalid data."""
        processor = DataProcessor()
        
        with pytest.raises(ValueError, match="invalid_data"):
            processor.process(None)
    
    @pytest.mark.parametrize("input_data,expected", [
        ({"a": 1}, 1),
        ({"a": 2}, 2),
        ({}, 0),
    ])
    def test_extract_value_parametrized(self, input_data, expected):
        """Should extract value correctly."""
        processor = DataProcessor()
        result = processor.extract_value(input_data)
        assert result == expected
```

### Coverage i metryki

```bash
# Uruchom testy z coverage
python -m pytest --cov=src --cov-report=html --cov-report=term-missing

# Minimalne wymagania coverage
# - Unit tests: 80%+
# - Integration tests: 60%+
# - End-to-end tests: podstawowe ścieżki
```

---

## 📚 Git i CI/CD {#git}

### Commit messages (Conventional Commits)

```
feat: add user authentication endpoint
fix: resolve memory leak in data processor
docs: update API documentation
test: add integration tests for payment flow
refactor: extract common validation logic
perf: optimize database queries
ci: update GitHub Actions workflow
style: format code with ruff
```

### Branching strategy

```
main                    # Stabilna wersja
├── develop            # Integracja features
├── feature/user-auth  # Nowe funkcjonalności
├── hotfix/security    # Pilne poprawki
└── release/v1.2.0     # Przygotowanie release
```

### CI/CD Pipeline (.github/workflows/ci.yml)

```yaml
name: CI Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.11", "3.12"]
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: ${{ matrix.python-version }}
      
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
          pip install -r requirements-dev.txt
      
      - name: Lint with ruff
        run: |
          ruff check .
          ruff format --check .
      
      - name: Type check with mypy
        run: mypy src/
      
      - name: Test with pytest
        run: |
          pytest --cov=src --cov-report=xml
      
      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          file: ./coverage.xml

  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run security scan
        run: |
          pip install bandit safety
          bandit -r src/
          safety check
```

---

## 📖 Dokumentacja {#dokumentacja}

### README.md struktura

```markdown
# Project Name

Brief description of what the project does.

## Features

- Feature 1
- Feature 2
- Feature 3

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```python
from myproject import MyClass

# Example usage
instance = MyClass()
result = instance.process()
```

## Development

```bash
# Setup
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows

# Install dev dependencies
pip install -r requirements-dev.txt

# Run tests
pytest

# Format code
ruff format .
ruff check . --fix
```

## Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'feat: add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## License

MIT License - see LICENSE file for details.
```

### Docstrings (Python)

```python
def calculate_metrics(
    data: list[dict[str, Any]], 
    window_size: int = 10
) -> MetricsResult:
    """
    PL: Oblicza metryki dla podanych danych w określonym oknie.
    EN: Calculates metrics for given data within specified window.
    
    Args:
        data: Lista słowników zawierających dane do analizy
        window_size: Rozmiar okna do obliczeń (domyślnie 10)
    
    Returns:
        MetricsResult zawierający obliczone metryki:
        - mean: Średnia wartość
        - std: Odchylenie standardowe  
        - count: Liczba próbek
    
    Raises:
        ValueError: Gdy data jest pusta lub window_size <= 0
        TypeError: Gdy data nie zawiera wymaganych pól
    
    Example:
        >>> data = [{"value": 1}, {"value": 2}, {"value": 3}]
        >>> result = calculate_metrics(data, window_size=2)
        >>> print(result.mean)
        2.0
    """
```

---

## ✅ Checklist dla PR {#checklist}

### Pre-commit (lokalnie)

- [ ] `ruff check . --fix` - bez błędów
- [ ] `ruff format .` - kod sformatowany  
- [ ] `mypy src/` - type checking OK (Python)
- [ ] `pytest` - wszystkie testy przechodzą
- [ ] `pytest --cov=src --cov-fail-under=80` - coverage ≥80%

### PR Requirements

- [ ] **ForgeHeader v3** we wszystkich nowych/zmienionych plikach
- [ ] **Sekcje kodu** uporządkowane zgodnie ze standardem
- [ ] **Type hints** we wszystkich publicznych funkcjach (Python)
- [ ] **Docstrings** PL/EN dla publicznych API
- [ ] **Testy** dla nowej funkcjonalności
- [ ] **Error handling** i logging
- [ ] **Security review** - brak sekretów w kodzie
- [ ] **Performance** - brak oczywistych problemów wydajnościowych
- [ ] **Documentation** zaktualizowana (jeśli potrzebne)
- [ ] **Conventional commits** format
- [ ] **CI/CD** pipeline zielony

### Code Review Guidelines

**Reviewer sprawdza:**

1. **Funkcjonalność** - czy kod robi to co powinien
2. **Czytelność** - czy kod jest zrozumiały
3. **Testowanie** - czy testy pokrywają logikę
4. **Bezpieczeństwo** - czy nie ma luk bezpieczeństwa
5. **Wydajność** - czy nie ma oczywistych problemów
6. **Standard** - czy kod zgodny z tym dokumentem

**Feedback format:**
```
// Nit: Możesz użyć f-stringa zamiast .format()
print(f"Processing {count} items")  # zamiast "Processing {} items".format(count)

// Issue: Missing error handling
try:
    result = risky_operation()
except SpecificError as e:
    logger.error("Operation failed: %s", e)
    raise

// Question: Czy ta logika nie powinna być w osobnej funkcji?
```

---

## 🚀 Automatyzacja i narzędzia

### Pre-commit hooks (.pre-commit-config.yaml)

```yaml
repos:
  - repo: https://github.com/charliermarsh/ruff-pre-commit
    rev: v0.1.6
    hooks:
      - id: ruff
        args: [--fix, --exit-non-zero-on-fix]
      - id: ruff-format

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.7.1
    hooks:
      - id: mypy
        additional_dependencies: [types-requests]

  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-json
      - id: check-merge-conflict
      - id: check-added-large-files
```

### Makefile dla częstych zadań

```makefile
.PHONY: install test lint format type-check clean docs

install:
	pip install -r requirements.txt
	pip install -r requirements-dev.txt

test:
	pytest --cov=src --cov-report=html --cov-report=term-missing

lint:
	ruff check .

format:
	ruff format .

type-check:
	mypy src/

clean:
	find . -type d -name "__pycache__" -delete
	find . -type f -name "*.pyc" -delete
	rm -rf .coverage htmlcov/ .pytest_cache/

docs:
	mkdocs serve

all: format lint type-check test

ci: all
	@echo "✅ All checks passed!"
```

---

## 🎓 Podsumowanie

Ten standard kodowania jest **obowiązujący** dla wszystkich projektów CERTEUS i CONTROL.

**Kluczowe zasady:**

1. **ForgeHeader v3** - każdy plik ma nagłówek
2. **Sekcje kodu** - uporządkowana struktura
3. **Type safety** - zawsze używaj type hints
4. **Error handling** - obsługuj błędy, loguj problemy
5. **Testing** - testuj wszystko, minimum 80% coverage
6. **Security** - nigdy nie commituj sekretów
7. **Documentation** - docstrings PL/EN, README, komentarze
8. **Automation** - CI/CD, pre-commit hooks, linting

**Dla agentów AI:**
- Zawsze stosuj ten standard
- Pytaj o wyjaśnienia jeśli coś niejasne
- Preferuj czytelność nad "mądre" rozwiązania
- Każda zmiana = testy + dokumentacja

**Big Tech Quality:**
- Kod jak w Google/Microsoft/Meta
- Zero kompromisów na jakość
- Automatyzacja wszystkiego
- Metryki i monitoring

---

**CERTEUS - Gdzie każda linia kodu ma znaczenie.** ⚡

*Document version: 3.0 | Last updated: 2025-09-09*
