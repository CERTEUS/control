## AGENT.md (INTERNAL — OPERATIONAL GUIDE)

UWAGA: komunikacja tylko w języku polskim. Standard kodowania w `.control/diary/coding_standard.md`.

Cel: pełna dokumentacja operacyjna i ściąga dla agentów. Ten plik jest ignorowany przez Git i nie trafia do repozytorium publicznego.

### Standard kodowania (skrót dla agentów)

- Podstawowy dokument: `.control/diary/coding_standard.md` (obowiązujący, v2.x).  
- Shell: `#!/usr/bin/env bash`, `set -Eeuo pipefail`, globalny `trap 'echo "[ERR] $0 line:$LINENO status:$?'\" >&2' ERR`.
- Markdown: pusta linia przed/po nagłówkach i listach (patrz sekcja niżej).  
- Konwencje repo: czytelność > spryt, deterministyczność, testowalność, bezpieczeństwo domyślne, logi/metryki/trace.  
- Przegląd narzędzi i reguł: patrz „Kontrakt dla Agentów” w `.control/diary/coding_standard.md`.

### Zasady Markdown

- Zawsze wstaw 1 pustą linię przed i po każdym nagłówku (`#`, `##`, …).
- Zawsze wstaw 1 pustą linię przed i po listach (`-`, `*`, `1.`).

### Lokalizacja dokumentów (zawsze ukryte)

- Katalog dokumentów wewnętrznych: `.control/` (wyłączony z Git).  
- Struktura:  
  - `.control/diary/` — dziennik decyzji i artefaktów (np. `coding_standard.md`, `WORKLOG.md`).  
  - `.control/plans/` — plany, roadmapy, backlogi (prywatne).  
  - `.control/keys/` — klucze i sekrety (szyfrowane lub lokalne).  
- Zasada: nowe dokumenty projektowe (specyfikacje, ADR, checklisty) umieszczaj w `.control/` — nie w katalogach publicznych.  
- Ten `AGENT.md` to wejście i skrót — szczegóły zawsze w `.control/*`.

### Konfiguracja cSpell / lint

- VS Code: zainstaluj „Polish - Code Spell Checker” oraz „Code Spell Checker”.
- Globalnie: `tools/windows/setup-vscode-cspell.ps1` (Windows/PowerShell) — ustawia `cSpell.language = "en,pl"`, `cSpell.enabledLanguageIds = [markdown, plaintext, git-commit]`, `cSpell.diagnosticLevel = Information`.
- W repo: `.vscode/settings.json` (lokalne) i `.markdownlint.json` (wymuszające odstępy wokół nagłówków i list).

### Dostęp i sekrety

- Katalog sekretów i czarna skrzynka: `.control/` (ignorowany przez Git).
- Zmienne: `GH_APP_ID`, `GH_APP_INSTALLATION_ID`, oraz JEDNA z: `GH_APP_PRIVATE_KEY_B64` / `GH_APP_PRIVATE_KEY` / `GH_APP_PRIVATE_KEY_PATH`.
- `.env` lokalny jest dozwolony (ignorowany przez Git). Nie commituj sekretów.

### Czarna skrzynka `.control/`

- `plans/` — prywatne backlogi i strategie (niepublikowane).
- `keys/` — zaszyfrowane kopie tokenów/kluczy (np. GPG lub age). Domyślny klucz PEM: `.control/keys/github-app-private-key.pem`.
- `diary/` — osobisty dziennik decyzji (co i dlaczego). Plik: `.control/diary/WORKLOG.md`.

### Kontrakt Agenta (operacyjny skrót)

- Stosuj reguły z `.control/diary/coding_standard.md` (ForgeHeader v2, testy, obsługa błędów, logi).  
- W skryptach bash: `set -Eeuo pipefail` + `trap` oraz bezpieczne cytowanie (`"$var"`).  
- Utrzymuj minimalne, czytelne zmiany; nie commituj plików z `.control/`, `.env*`, `AGENT.md`.  
- Dokumenty wewnętrzne dodawaj tylko w `.control/` (np. ADR: `.control/diary/ADR-YYYYMMDD-<slug>.md`).
- Po zakończeniu prac dopisz wpis do dziennika `.control/diary/WORKLOG.md` (PL/EN, krótko: co i dlaczego).

### Gałęzie i CI (polityka)

- Jedna gałąź robocza: `work/daily` (Control i Certeus).
- `main` = stan referencyjny; sync z `work/daily` po zielonych przebiegach.
- CI:
  - Certeus: `Tests` (pip + python) na `work/daily` i `main`; cięższe `ci-gates` na PR/main.
  - Control: `control-ci` checkoutuje submodule (recursive) i uruchamia testy Certeus (`cd certeus && pytest -q`).

### Zdalne sterowanie (Agents Orchestrator)

- Start jednorazowy (A0..A9): `tools/agents/run_all.sh`  
- Pętla (z watchdogiem PR): `tools/agents/auto_agents.sh`  
- Instalacja zależności (Node, Codex CLI): `tools/agents/install.sh`  
- Zatrzymanie wszystkich: `tools/agents/stop_all.sh`  
- Komendy w Issue umieszczaj w bloku kodu `bash`; są filtrowane przez allowlist.  
- Logi z wykonań: `.control/diary/agent_runs/`.
- Tokeny: użyj `tools/remote-bot/get_installation_token.py` (GitHub App) lub `.control/secrets/GITHUB_TOKEN.txt`.  

### Tokeny i GitHub API

- Generowanie tokenu App:
  - `TOKEN=$(python tools/remote-bot/get_installation_token.py)`
  - użycie z git: `git push https://x-access-token:${TOKEN}@github.com/ORG/REPO.git HEAD`
  - użycie z API: `curl -H "Authorization: token $TOKEN" …`

### OpenAPI i synchronizacja kontraktu

- Weryfikacja: `tools/openapi-sync.sh verify`
- Synchronizacja (źródło: Certeus): `tools/openapi-sync.sh sync --from certeus`

### Praca dzienna (workflow)

1) Implementacja w `certeus` (kod), wrappery/CI w `control` (jeśli potrzebne).
2) `cd certeus && pytest -q` lokalnie → zielono.
3) Push na `work/daily` (odpowiednie repo).
4) Monitor zielonego stanu: `tools/remote-bot/wait-branch-green.sh CERTEUS <repo> work/daily`.
5) Promocja na `main` po zielonych przebiegach.

### Wrappery i artefakty (Control)

- Wrappery gate’ów: `scripts/gates/*` → delegują do `certeus/scripts/gates/*`.
- Artefakty testowe: `schemas/*`, `packs/jurisdictions/PL/rules/*`, `clients/web/public/index.html`, `sdk/*`, shimy: `services/lexlog_parser/*`, `security/ra.py`.

### Szybki start (przeniesione z README)

1) Konfiguracja sekretów:

- Skopiuj `cp .env.example .env` i uzupełnij `GH_APP_ID`, `GH_APP_INSTALLATION_ID` i klucz jedną z metod (PEM/BASE64/ścieżka)
- Alternatywnie: `tools/remote-bot/setup.sh --write-key` zapisze PEM do `.control/keys/github-app-private-key.pem`
- Jednowierszowy sekret: `.control/remote-bot.secret` (generator: `tools/remote-bot/pack-secret.sh --write`)

2) Walidacja: `tools/remote-bot/gh_app_token.sh --check` (oczekiwane: OK)

3) Pierwsze użycie:

- Token: `tools/remote-bot/gh_app_token.sh`
- Lista repo: `tools/remote-bot/list-repos.sh`
- Klonowanie: `tools/remote-bot/clone-repo.sh owner/repo [dir]`

### Login + Kontener Codex (Windows Git Bash)

Punkt odniesienia do pracy agentów (Codex CLI + kontener):

1) Login Codex NA HOŚCIE (Git Bash):

- Ustaw sesję: `mkdir -p /f/projekty/codex_home && export CODEX_HOME=F:/projekty/codex_home`
- Zaloguj: `codex login` → w przeglądarce dokończ i sprawdź `/status` (TUI).

2) Kontener dev (obraz: `codex-ubuntu`):

- Start: `docker run -d --name codex -p 1455:1455 -v /f/projekty/control:/workspace/control -v /f/projekty/codex_home:/root/.codex codex-ubuntu bash -lc "sleep infinity"`
- Git trust:  
  `docker exec codex git config --global --add safe.directory /workspace/control`  
  `docker exec codex git config --global --add safe.directory /workspace/control/certeus`
- Status logowania w kontenerze: `docker exec codex codex login status`

3) Weryfikacja submodule/remote (w kontenerze):

```
docker exec codex bash -c "cd /workspace/control && git submodule status"
docker exec codex bash -c "cd /workspace/control/certeus && git remote -v"
```

Uwaga: w Git Bash używaj `bash -c "…"` przy `docker exec`, by uniknąć błędów ścieżek.

### Typowe przepływy

- Z tokenem w env: `tools/remote-bot/with-gh.sh <polecenie>`
- Integracja z GitHub CLI: `make login` lub `tools/remote-bot/with-gh.sh gh auth status`

Przykładowy push z tokenem:

```
eval "$(tools/remote-bot/gh_app_token.sh --export)" && git push "https://x-access-token:${GITHUB_TOKEN}@github.com/<owner>/<repo>.git" HEAD:main
```

### Jak to działa (skrót)

- `tools/remote-bot/gh_app_token.sh` tworzy JWT (RS256) → pobiera `access_token` instalacji → zwraca lub eksportuje `GITHUB_TOKEN`/`GH_TOKEN`.
- Pozostałe skrypty konsumują ten token do akcji API/Git.

### Sekret jednowierszowy

- Plik `.control/remote-bot.secret` (ignorowany przez Git)
- Format: `APP_ID:INSTALLATION_ID:BASE64_PEM` lub `json:{...}` lub `b64:<...>` albo linia kluczy `GH_APP_ID=... GH_APP_INSTALLATION_ID=... GH_APP_PRIVATE_KEY_B64=...`
- Generator: `tools/remote-bot/pack-secret.sh`

### Bezpieczeństwo

- Nie commituj `.control/`, `.env`, `.env.example`, `AGENT.md`.
- Lokalne hooki blokują dodanie `AGENT.md` do commitu (`tools/hook-setup.sh`).
- Tokeny instalacji są krótkotrwałe i generowane on‑demand.

### Referencje narzędzi i skróty

- Token: `tools/remote-bot/gh_app_token.sh` (`--check`, `--json`, `--export`, `--jwt`)
- Lista: `tools/remote-bot/list-repos.sh`
- Klon: `tools/remote-bot/clone-repo.sh owner/repo [dir]`
- Wrapper: `tools/remote-bot/with-gh.sh <cmd>`
- Setup: `tools/remote-bot/setup.sh`
- Makefile: `make setup | token | token-json | login | list | clone owner=<o> repo=<r> [dir=<katalog>] | secret-pack | secret-write`

### Rozwiązywanie problemów

- Brak `jq`/`python3` → zainstaluj przynajmniej jedno.
- „Nie znaleziono klucza prywatnego” → uzupełnij `.env` lub `.control/keys/github-app-private-key.pem`.
- Błędy API → zweryfikuj `GH_APP_ID`, `GH_APP_INSTALLATION_ID`, ważność PEM.

—
# CERTEUS • AGENT OPERATIONS MANUAL (A0–A9) – “Loop Until Green”

**Cel:** Agenci A0–A9 pracują autonomicznie nad repo `CERTEUS/certeus` wg planu 36 tygodni. Każdy agent:
1) czyta własną listę `control/tasks/Ax.md`,  
2) **implementuje** w `certeus`,  
3) po **każdej** zmianie uruchamia testy i linty lokalnie,  
4) gdy wszystko **zielone** → **branch, commit, push, PR**,  
5) czeka na **zielone PR‑checks**; jeśli czerwone → wraca do poprawek.  

## Repos & Ścieżki
- **control (orchestracja):** `F:\projekty\control` (w kontenerze: `/workspace/control`).  
- **certeus (kod):** `F:\projekty\certeus` (w kontenerze: `/workspace/certeus`).  
- **Plany / Mapa:** `control\AGENT.md` (ten plik), `control\tasks\A0..A9.md`.  
- **Standardy jakości:** `control\.control\diary\coding_standard.md` (ForgeHeader v2, kontrakt agentów):contentReference[oaicite:2]{index=2}.  
- **Mapa programu (role, fazy, bramki, tygodnie):** `certeus\docs\read_mapa.md`:contentReference[oaicite:3]{index=3}.

## Role (stałe)
- **A0 – PM/Architekt**: roadmapa, bramki jakości, ryzyka, release sign‑off.  
- **A1 – PCO & Verifier**: schema PCO, walidator LFSC/DRAT/SMT, CLI `pco`.  
- **A2 – Formal Methods**: generacja/normalizacja dowodów, Z3↔CVC5, certyfikaty.  
- **A3 – Provenance/Ledger**: Merkle DAG, kotwice, membership proofs, API ledger.  
- **A4 – SLO/Observability**: metryki (ECE, Brier, p95), dashboardy, SLO‑Gate.  
- **A5 – Security/Supply Chain**: SBOM, Grype, cosign, SLSA‑3, sekrety.  
- **A6 – API/Gateway/Policies**: FastAPI/OpenAPI, proof‑only enforcement, OPA/rego.  
- **A7 – Cockpit/UI**: PCO Viewer, MerkleGraph, AuditPack, timeline.  
- **A8 – Bench/Research**: zbiory zadań, metodyka, wyniki publiczne.  
- **A9 – QA/Test & Release**: property/metamorphic/fuzz, wydania, checklists.  
> Źródło i rozwinięcia zadań per tydzień: **read_mapa**:contentReference[oaicite:4]{index=4}.

## „Loop Until Green” (algorytm pracy agenta)
1. **Wejście**: własny `tasks/Ax.md`.  
2. **Przełącz repo**: praca wyłącznie w `/workspace/certeus`.  
3. **Implementuj** wg taska (twórz/edytuj wskazane ścieżki).  
4. **Uruchom testy/linty:**  
   - Python: `pytest -q` (lub `make test` jeśli jest),  
   - Lint: `ruff check`, `mypy` (jeśli konfig istnieje).  
5. **Jeśli FAIL** → bez pytania analizuj log, popraw kod i **wróć do p.4**.  
6. **Jeśli PASS lokalnie:**  
   - `git switch -c feature/Ax-Ty`, `git add -A`, `git commit -m "feat(Ax): …"`,  
   - `git push origin HEAD`.  
7. **Utwórz PR** via GitHub API (`GITHUB_TOKEN`): `POST /repos/CERTEUS/certeus/pulls`.  
8. **Czekaj na zielone PR‑checks** (poll API co 10 s do timeout); jeśli czerwone → **wróć do p.3**.  
9. **Done**: dopisz do `CHANGELOG`, zamknij task.

## Definition of Done (DoD)
- Kod + testy + dokument (README/doc w odpowiednim folderze) + wpis do `docs/` (jeśli dotyczy) + **zielone CI** + podpis/cosign (jeśli dotyczy release) + ujęcie w **CHANGELOG**.  
- **ForgeHeader v2** w każdym pliku źródłowym (PL/EN, metadane, sekcje, Invariants, Errors) – patrz **coding_standard.md**:contentReference[oaicite:5]{index=5}.  
- **Proof‑Native**: PCO, Merkle, SLO‑Gate zgodnie z mapą:contentReference[oaicite:6]{index=6}.

## Jakość & standardy (obowiązkowe)
- **ForgeHeader v2** we wszystkich plikach (nagłówek normatywny).  
- PEP8+typing, TS strict/Dart null‑safety, brak „magii”, testowalność, obsługa błędów, logi i metryki – patrz **CERTEUS — CODING STANDARD**:contentReference[oaicite:7]{index=7}.  
- Każdy PR musi przejść **bramki** (linty, testy, SLO‑Gate jeżeli aktywny) – warunek **merge**:contentReference[oaicite:8]{index=8}.

## Tokeny i przełączanie repo
- Agent używa `GITHUB_TOKEN` (export z `control/.control/secrets/*`), aby: `git push`, tworzyć PR, czytać statusy.  
- **Repo źródłowe** do edycji: `certeus`. **Repo planu**: `control`.  
- Agenci **mogą przełączać się** między repo przez `-C` (cwd) lub jawne ścieżki.

## Fazy & Bramki (gilotyny)
- **G1 (T6)**: ≥90% ścieżek wymaga PCO; `pco verify --strict ≤ 200 ms`; Merkle proofs lokalnie** PASS**:contentReference[oaicite:9]{index=9}.  
- **G2 (T12)**: kotwica dzienna publiczna; SLO‑Gate **realnie blokuje** releasy; wyniki Bench v0.1 opublikowane:contentReference[oaicite:10]{index=10}.  
- Kolejne G3…GA zgodnie z **read_mapa**:contentReference[oaicite:11]{index=11}.

## Kontrakt dla agentów
- Nie wolno omijać testów/bramek. Nie wolno „zieleniać” przez wyłączanie asercji.  
- Każda zmiana kodu → odpowiadające testy.  
- Zmiany architektoniczne → **ADR** w `docs/adr/`.  
- Szanuj **Security by Design** (SBOM, skany, secrets) – patrz standard:contentReference[oaicite:12]{index=12}.

---

Notatka: jeśli potrzebujesz dodatkowych uprawnień lub rozszerzeń automatyzacji, zgłoś wymagania – środowisko wspiera pełny dostęp w ramach konfiguracji GitHub App.
