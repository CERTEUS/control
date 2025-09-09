#!/usr/bin/env bash
# +=====================================================================+
# |                          CERTEUS                                    |
# +=====================================================================+
# | FILE: scripts/verify-markdown.sh                                   |
# | ROLE: Shell script for automation                                  |
# | PLIK: scripts/verify-markdown.sh                                   |
# | ROLA: Skrypt shell do automatyzacji                                |
# +=====================================================================+

# PL: Moduł zapewniający funkcjonalność verify-markdown
# EN: Module providing verify-markdown functionality

set -Eeuo pipefail
trap 'echo "[ERR] $0 line:$LINENO status:$?" >&2' ERR

# Wrapper delegujący do wersji w submodule CERTEUS.
DIR="$(cd "$(dirname "$0")" && pwd)"
ROOT=""
for up in "" ".." "../.." "../../.."; do
  CAND="$DIR/$up/workspaces/certeus/tools/verify-markdown.sh"
  if [ -f "$CAND" ]; then ROOT="$DIR/$up"; break; fi
done
if [ -z "$ROOT" ]; then
  echo "Nie znaleziono workspaces/certeus/tools/verify-markdown.sh względem $DIR" >&2
  exit 2
fi
exec "$ROOT/workspaces/certeus/tools/verify-markdown.sh" "$@"
