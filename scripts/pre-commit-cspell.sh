#!/usr/bin/env bash
# +=====================================================================+
# |                          CERTEUS                                    |
# +=====================================================================+
# | FILE: scripts/pre-commit-cspell.sh                                 |
# | ROLE: Shell script for automation                                  |
# | PLIK: scripts/pre-commit-cspell.sh                                 |
# | ROLA: Skrypt shell do automatyzacji                                |
# +=====================================================================+

# PL: Moduł zapewniający funkcjonalność pre-commit-cspell
# EN: Module providing pre-commit-cspell functionality

set -Eeuo pipefail
trap 'echo "[ERR] $0 line:$LINENO status:$?" >&2' ERR

# Wrapper delegujący do wersji w submodule CERTEUS.
DIR="$(cd "$(dirname "$0")" && pwd)"
ROOT=""
for up in "" ".." "../.." "../../.."; do
  CAND="$DIR/$up/workspaces/certeus/tools/pre-commit-cspell.sh"
  if [ -f "$CAND" ]; then ROOT="$DIR/$up"; break; fi
done
if [ -z "$ROOT" ]; then
  echo "Nie znaleziono workspaces/certeus/tools/pre-commit-cspell.sh względem $DIR" >&2
  exit 2
fi
exec "$ROOT/workspaces/certeus/tools/pre-commit-cspell.sh" "$@"
