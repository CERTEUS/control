#!/usr/bin/env bash
# +=====================================================================+
# |                          CERTEUS                                    |
# +=====================================================================+
# | FILE: tools/hook-setup.sh                                          |
# | ROLE: Shell script for automation                                  |
# | PLIK: tools/hook-setup.sh                                          |
# | ROLA: Skrypt shell do automatyzacji                                |
# +=====================================================================+

# PL: Moduł zapewniający funkcjonalność hook-setup
# EN: Module providing hook-setup functionality

set -Eeuo pipefail
trap 'echo "[ERR] $0 line:$LINENO status:$?" >&2' ERR

set -Eeuo pipefail
# Wrapper delegujący do wersji w submodule CERTEUS, aby uniknąć duplikacji.
DIR="$(cd "$(dirname "$0")" && pwd)"
ROOT=""
for up in "" ".." "../.." "../../.."; do
  CAND="$DIR/$up/workspaces/certeus/tools/hook-setup.sh"
  if [ -f "$CAND" ]; then ROOT="$DIR/$up"; break; fi
done
if [ -z "$ROOT" ]; then
  echo "Nie znaleziono workspaces/certeus/tools/hook-setup.sh względem $DIR" >&2
  exit 2
fi
exec "$ROOT/workspaces/certeus/tools/hook-setup.sh" "$@"
