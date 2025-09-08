#!/usr/bin/env bash
set -Eeuo pipefail
# Wrapper delegujący do wersji w submodule CERTEUS.
DIR="$(cd "$(dirname "$0")" && pwd)"
ROOT=""
for up in "" ".." "../.." "../../.."; do
  CAND="$DIR/$up/certeus/tools/agents/run_all.sh"
  if [ -f "$CAND" ]; then ROOT="$DIR/$up"; break; fi
done
if [ -z "$ROOT" ]; then
  echo "Nie znaleziono certeus/tools/agents/run_all.sh względem $DIR" >&2
  exit 2
fi
exec "$ROOT/certeus/tools/agents/run_all.sh" "$@"
