#!/usr/bin/env bash
# +=====================================================================+
# |                          CERTEUS                                    |
# +=====================================================================+
# | FILE: tools/remote-bot/close-issues.sh                             |
# | ROLE: Shell script for automation                                  |
# | PLIK: tools/remote-bot/close-issues.sh                             |
# | ROLA: Skrypt shell do automatyzacji                                |
# +=====================================================================+

# PL: Moduł zapewniający funkcjonalność close-issues
# EN: Module providing close-issues functionality

set -Eeuo pipefail
trap 'echo "[ERR] $0 line:$LINENO status:$?" >&2' ERR

set -Eeuo pipefail
trap 'echo "[ERR] ${0##*/} line:${LINENO} status:$?" >&2' ERR

OWNER=${1:-CERTEUS}
REPO=${2:-control}

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
TOKEN=$(python "$ROOT_DIR/remote-bot/get_installation_token.py" | tr -d '\r\n')

api() {
  local method="$1"; shift
  local path="$1"; shift
  curl -fsS -X "$method" -H 'Accept: application/vnd.github+json' \
    -H "Authorization: token $TOKEN" \
    "https://api.github.com/repos/$OWNER/$REPO$path" "$@"
}

echo "Closing all open issues in $OWNER/$REPO…"
ids=$(api GET "/issues?state=open&per_page=100" | jq -r '.[].number') || ids=""
if [ -z "$ids" ]; then echo "No open issues"; exit 0; fi
for n in $ids; do
  echo "- closing #$n"
  api PATCH "/issues/$n" -d '{"state":"closed"}' >/dev/null || true
done
echo "Done."