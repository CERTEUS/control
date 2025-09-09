#!/usr/bin/env bash
# +=====================================================================+
# |                          CERTEUS                                    |
# +=====================================================================+
# | FILE: tools/openapi-sync.sh                                        |
# | ROLE: API endpoint and routing module                              |
# | PLIK: tools/openapi-sync.sh                                        |
# | ROLA: Moduł endpoint API i routingu                                |
# +=====================================================================+

# PL: Moduł zapewniający funkcjonalność openapi-sync
# EN: Module providing openapi-sync functionality

set -Eeuo pipefail
trap 'echo "[ERR] $0 line:$LINENO status:$?" >&2' ERR

set -Eeuo pipefail
# Wrapper delegujący do wersji w submodule CERTEUS.
DIR="$(cd "$(dirname "$0")" && pwd)"
ROOT=""
for up in "" ".." "../.."; do
  CAND="$DIR/$up/certeus/tools/openapi-sync.sh"
  if [ -f "$CAND" ]; then ROOT="$DIR/$up"; break; fi
done
if [ -z "$ROOT" ]; then
  echo "Nie znaleziono certeus/tools/openapi-sync.sh względem $DIR" >&2
  exit 2
fi
exec "$ROOT/certeus/tools/openapi-sync.sh" "$@"