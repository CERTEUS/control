# CONTROL — autonomiczny punkt dowodzenia CERTEUS

CONTROL to repozytorium „control plane” dla całego konta CERTEUS. Działa jako autonomiczny punkt dowodzenia: zarządza dostępem, automatyzuje operacje na repozytoriach i udostępnia jednolite narzędzia dla agentów/botów oraz ludzi. Fundamentem jest GitHub App z pełnymi uprawnieniami (Twoja odpowiedzialność), która generuje krótkotrwałe tokeny instalacji do wykonywania zadań operacyjnych bez trzymania stałych sekretów w kodzie.

## Misja
- Ujednolicone, bezpieczne wejście do wszystkich repozytoriów CERTEUS.
- Minimalizacja ekspozycji sekretów: krótkotrwałe tokeny, sekrety wyłącznie lokalnie.
- Niska bariera użycia: jedno repo, proste skrypty, powtarzalne przepływy.

## Funkcje
- Generowanie tokenów instalacji GitHub App (JWT → access_token) on‑demand.
- Operacje krzyżo‑repozytoryjne (listowanie, klonowanie, wywołania CLI/API) z automatycznym wstrzyknięciem `GITHUB_TOKEN`/`GH_TOKEN`.
- Tryb „jednowierszowego” sekretu dla szybkiej konfiguracji środowiska.
- Zgodność z `gh` (GitHub CLI) oraz surowym `curl`/`git`.

## Struktura repozytorium
- `.control/` — lokalny katalog na sekrety (ignorowany przez git).
- `tools/remote-bot/` — skrypty operacyjne (GitHub App, tokeny, klonowanie, wrappery).
- `.env.example` — szablon zmiennych środowiskowych.
- `Makefile` — skróty do najczęstszych zadań operacyjnych.

## Wymagania
- Wymagane: `curl`, `openssl`, `git`.
- JSON: `jq` lub `python3` (wystarczy jedno).
- Opcjonalnie: `gh` (GitHub CLI) dla wygody (status/logowanie), nie jest konieczny.

## Szybki start
1) Skonfiguruj sekrety (jedna z dróg):
- Skopiuj: `cp .env.example .env`, uzupełnij `GH_APP_ID`, `GH_APP_INSTALLATION_ID` oraz klucz jedną z metod:
  - `GH_APP_PRIVATE_KEY` (PEM; może zawierać dosłowne `\n`),
  - `GH_APP_PRIVATE_KEY_B64` (cały PEM w base64),
  - `GH_APP_PRIVATE_KEY_PATH` (np. `.control/github-app-private-key.pem`).
- Lub: `make setup` i wklej PEM do `.control/github-app-private-key.pem`.
- Alternatywnie: jednowierszowy pakiet w `.control/remote-bot.secret` (patrz Sekcja „Sekret jednowierszowy”).

2) Walidacja środowiska:
- `tools/remote-bot/gh_app_token.sh --check` → oczekiwane `OK`.

3) Pierwsze użycie:
- Token testowy: `make token` (wypisze krótkotrwały `GITHUB_TOKEN`).
- Lista repo: `make list` lub `tools/remote-bot/list-repos.sh`.
- Klonowanie: `make clone owner=<owner> repo=<repo>` lub `tools/remote-bot/clone-repo.sh owner/repo [dir]`.

## Typowe przepływy
- Uruchom dowolne polecenie z tokenem w env: `tools/remote-bot/with-gh.sh <polecenie>`
  - Przykład: `tools/remote-bot/with-gh.sh gh repo list`
- Integracja z `gh`: `make login` (pokazuje status autoryzacji CLI przy użyciu generowanego tokenu).

## Jak to działa (w skrócie)
- `tools/remote-bot/gh_app_token.sh`:
  - Ładuje `.env` i/lub `.control/remote-bot.secret` (jeśli istnieje).
  - Buduje JWT (RS256) podpisany kluczem GitHub App, następnie pobiera `access_token` instalacji przez GitHub API.
  - Zwraca token na stdout lub eksportuje `GITHUB_TOKEN`/`GH_TOKEN` (`--export`).
- Pozostałe skrypty używają tego tokenu do bezpiecznych operacji na repozytoriach.

## Sekret jednowierszowy
- Plik: `.control/remote-bot.secret` (ignorowany przez git).
- Format podstawowy: `APP_ID:INSTALLATION_ID:BASE64_PEM`.
- Obsługiwane także warianty: `json:{...}` lub `b64:<base64_JSON>` albo linia kluczy `GH_APP_ID=... GH_APP_INSTALLATION_ID=... GH_APP_PRIVATE_KEY_B64=...`.
- Generator: `tools/remote-bot/pack-secret.sh` (opcja `--write` zapisze plik).

## Bezpieczeństwo
- Sekrety tylko lokalnie: `.control/` i `.env` są ignorowane przez git.
- Tokeny instalacji są krótkotrwałe i generowane on‑demand.
- Skala uprawnień zależy od konfiguracji GitHub App — używaj zgodnie z zasadą najmniejszych uprawnień.

## Referencje do narzędzi
- Token: `tools/remote-bot/gh_app_token.sh` (opcje: `--check`, `--json`, `--export`, `--jwt`).
- Lista repo: `tools/remote-bot/list-repos.sh`.
- Klonowanie: `tools/remote-bot/clone-repo.sh owner/repo [dir]`.
- Wrapper z tokenem: `tools/remote-bot/with-gh.sh <cmd>`.
- Setup katalogów i uprawnień: `tools/remote-bot/setup.sh`.

## Skróty `Makefile`
- `make setup` — przygotuj `.control/` i uprawnienia.
- `make token` / `make token-json` — pobierz token / pełny JSON odpowiedzi API.
- `make login` — status `gh auth` z użyciem wygenerowanego tokenu.
- `make list` — wypisz dostępne repozytoria dla instalacji.
- `make clone owner=<o> repo=<r> [dir=<katalog>]` — sklonuj repo przez token instalacji.
- `make secret-pack` / `make secret-write` — wyemituj lub zapisz jednowierszowy sekret.

## Rozwiązywanie problemów (TL;DR)
- Brak `jq` i `python3`: zainstaluj przynajmniej jedno z nich.
- Błąd „Nie znaleziono klucza prywatnego”: uzupełnij `.env` lub `.control/github-app-private-key.pem`.
- API zwraca komunikat o błędzie: sprawdź poprawność `GH_APP_ID`, `GH_APP_INSTALLATION_ID` i ważność klucza PEM.

## Status projektu
Repo stanowi „command center” dla konta CERTEUS. Zmiany skupiają się na bezpieczeństwie, ergonomii i niezawodności operacji między repozytoriami. Pull requesty mile widziane (lint commitów i CI w przygotowaniu).
