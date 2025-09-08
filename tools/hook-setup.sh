#!/usr/bin/env bash
set -Eeuo pipefail
# Wrapper delegujący do wersji w submodule CERTEUS, aby uniknąć duplikacji.
DIR="$(cd "$(dirname "$0")" && pwd)"
ROOT=""
for up in "" ".." "../.." "../../.."; do
  CAND="$DIR/$up/certeus/tools/hook-setup.sh"
  if [ -f "$CAND" ]; then ROOT="$DIR/$up"; break; fi
done
if [ -z "$ROOT" ]; then
  echo "Nie znaleziono certeus/tools/hook-setup.sh względem $DIR" >&2
  exit 2
fi
exec "$ROOT/certeus/tools/hook-setup.sh" "$@"
