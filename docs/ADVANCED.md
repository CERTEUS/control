# Control - Advanced Features

## 🎯 Multi-Repository Management

Control workspace teraz oferuje zaawansowane funkcje zarządzania wieloma projektami z jednego miejsca.

### 📊 Project Management

```bash
# Lista wszystkich projektów
control project list

# Dodanie nowego projektu
control project add my-project ./path/to/project --type="library" --description="My awesome library"

# Otwarcie projektu w VS Code
control project open certeus

# Usunięcie projektu
control project remove old-project

# Generowanie workspace VS Code
control project workspace
```

### 🔄 Git Operations

```bash
# Status wszystkich repozytoriów
control git status  # lub control status (pokazuje też Git)

# Pull dla wszystkich repo
control git pull

# Fetch bez merge
control git fetch

# Przełączanie brancha we wszystkich repo
control git switch main

# Przełączanie brancha w konkretnym repo
control git switch feature-branch --repo certeus
```

### 🐙 GitHub Integration

```bash
# Lista repozytoriów GitHub
control github repos

# Tworzenie Pull Request
control github pr certeus "Fix critical bug" --body="Detailed description"

# Lista GitHub Actions workflows
control github workflows certeus

# Sprawdzenie konfiguracji bezpieczeństwa
control github security certeus
```

## 🛠️ VS Code Integration

### Multi-Root Workspace

Generuj plik `.code-workspace` dla wszystkich projektów:

```bash
control project workspace
code control.code-workspace
```

Workspace zawiera:
- Wszystkie projekty jako foldery
- Właściwe ścieżki Python interpretera
- Zalecane rozszerzenia
- Ustawienia VS Code

### Tasks Integration

Dostępne zadania w VS Code (Ctrl+Shift+P → "Tasks: Run Task"):

- **Control: Health Check** - Sprawdzenie środowiska
- **Control: Run Tests** - Uruchomienie testów
- **Control: Git Status All** - Status Git wszystkich repo
- **Control: Git Pull All** - Pull wszystkich repo
- **Control: List Projects** - Lista projektów
- **Control: Generate Workspace** - Generowanie workspace

## 🚀 Automation & CI/CD

### GitHub Actions

Automatyczny CI/CD pipeline:

```yaml
# .github/workflows/ci.yml
- Control tests (Python 3.11, 3.12)
- Certeus smoke tests  
- Integration tests
- Code quality checks
```

### Pre-commit Hooks

```bash
# Instalacja
pre-commit install

# Manualne uruchomienie
pre-commit run --all-files
```

## 📦 Setup & Installation

### Automatyczny Setup

**Linux/macOS:**
```bash
./setup.sh
```

**Windows:**
```batch
setup.bat
```

### Ręczny Setup

```bash
# 1. Środowisko wirtualne
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
.venv\Scripts\activate.bat  # Windows

# 2. Instalacja
pip install -e .

# 3. Narzędzia deweloperskie
pip install ruff pytest pre-commit mypy

# 4. Sprawdzenie
control health
```

## 🎯 Workflow Examples

### Praca z wieloma projektami

```bash
# Poranne sprawdzenie
control status
control git fetch

# Synchronizacja z GitHub
control github repos
control git pull

# Praca nad feature
control git switch feature-branch --repo certeus
control project open certeus

# Po zakończeniu pracy
control github pr certeus "Add new feature" --body="Description"
```

### Dodanie nowego projektu

```bash
# Dodanie do zarządzania
control project add new-api ./apis/new-api --type="api" --description="New REST API"

# Regeneracja workspace
control project workspace

# Otwarcie w VS Code
code control.code-workspace
```

### Bezpieczeństwo i jakość

```bash
# Sprawdzenie bezpieczeństwa
control github security certeus
control github security control

# Sprawdzenie CI/CD
control github workflows certeus

# Lokalne testy
control health
pytest tests/
ruff check .
```

## 🔧 Configuration

### Project Configuration

Projekty zarządzane w `.control/projects.json`:

```json
{
  "version": "1.0",
  "projects": {
    "control": {
      "type": "manager",
      "path": ".",
      "python_env": ".venv",
      "description": "Control workspace manager"
    },
    "certeus": {
      "type": "product", 
      "path": "certeus",
      "python_env": "certeus/.venv",
      "description": "CERTEUS main product",
      "github": "CERTEUS/certeus"
    }
  }
}
```

### VS Code Settings

Automatyczna konfiguracja dla:
- ✅ Izolacja środowisk Python
- ✅ Wykluczenie zagnieżdżonych `.venv` z analizy
- ✅ Optymalizacja wydajności Pylance
- ✅ Formatting i linting z Ruff
- ✅ Git i GitHub integration

## 📈 Benefits

### Przed Control
- ❌ Ręczne przełączanie między projektami
- ❌ Mieszanie środowisk Python
- ❌ Powtarzalne zadania Git/GitHub
- ❌ Fragmentacja narzędzi

### Po Control
- ✅ Centralne zarządzanie projektami
- ✅ Izolowane środowiska
- ✅ Automatyzacja Git/GitHub
- ✅ Ujednolicone workflow
- ✅ Integracja z VS Code
- ✅ CI/CD automation
