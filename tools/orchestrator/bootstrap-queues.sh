#!/usr/bin/env bash
set -Eeuo pipefail
# Wrapper delegujący do wersji w submodule CERTEUS.
DIR="$(cd "$(dirname "$0")" && pwd)"
ROOT=""
for up in "" ".." "../.."; do
  CAND="$DIR/$up/certeus/tools/orchestrator/bootstrap-queues.sh"
  if [ -f "$CAND" ]; then ROOT="$DIR/$up"; break; fi
done
if [ -z "$ROOT" ]; then
  echo "Nie znaleziono certeus/tools/orchestrator/bootstrap-queues.sh względem $DIR" >&2
  exit 2
fi
exec "$ROOT/certeus/tools/orchestrator/bootstrap-queues.sh" "$@"
