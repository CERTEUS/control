#!/usr/bin/env bash
# +=====================================================================+
# |                          CERTEUS                                    |
# +=====================================================================+
# | FILE: tools/remote-bot/wait-pr-green.sh                            |
# | ROLE: Shell script for automation                                  |
# | PLIK: tools/remote-bot/wait-pr-green.sh                            |
# | ROLA: Skrypt shell do automatyzacji                                |
# +=====================================================================+

# PL: Moduł zapewniający funkcjonalność wait-pr-green
# EN: Module providing wait-pr-green functionality

set -Eeuo pipefail
trap 'echo "[ERR] $0 line:$LINENO status:$?" >&2' ERR

set -Eeuo pipefail
# Wrapper delegujący do wersji w submodule CERTEUS.
DIR="$(cd "$(dirname "$0")" && pwd)"
ROOT=""
for up in "" ".." "../.."; do
  CAND="$DIR/$up/certeus/tools/remote-bot/wait-pr-green.sh"
  if [ -f "$CAND" ]; then ROOT="$DIR/$up"; break; fi
done
if [ -z "$ROOT" ]; then
  echo "Nie znaleziono certeus/tools/remote-bot/wait-pr-green.sh względem $DIR" >&2
  exit 2
fi
exec "$ROOT/certeus/tools/remote-bot/wait-pr-green.sh" "$@"