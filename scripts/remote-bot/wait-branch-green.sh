#!/usr/bin/env bash
# +=====================================================================+
# |                          CERTEUS                                    |
# +=====================================================================+
# | FILE: tools/remote-bot/wait-branch-green.sh                        |
# | ROLE: Shell script for automation                                  |
# | PLIK: tools/remote-bot/wait-branch-green.sh                        |
# | ROLA: Skrypt shell do automatyzacji                                |
# +=====================================================================+

# PL: Moduł zapewniający funkcjonalność wait-branch-green
# EN: Module providing wait-branch-green functionality

set -Eeuo pipefail
trap 'echo "[ERR] $0 line:$LINENO status:$?" >&2' ERR

set -Eeuo pipefail
trap 'echo "[ERR] ${0##*/} line:${LINENO} status:$?" >&2' ERR

OWNER=${1:-CERTEUS}
REPO=${2:-control}
BRANCH=${3:-work/daily}
TIMEOUT=${TIMEOUT:-1200}
SLEEP=${SLEEP:-10}

get_token() {
  python "$(dirname "$0")/get_installation_token.py"
}

api() {
  local path="$1"
  curl -fsS -H 'Accept: application/vnd.github+json' -H "Authorization: token $(get_token | tr -d '\r\n')" "https://api.github.com/repos/${OWNER}/${REPO}${path}"
}

echo "Waiting for ${OWNER}/${REPO}@${BRANCH} latest run to be green…"
start=$(date +%s)
while :; do
  run=$(api "/actions/runs?branch=${BRANCH}&per_page=1" | jq -r '.workflow_runs[0] | {id, name, status, conclusion} | @json')
  id=$(jq -r '.id' <<<"$run")
  name=$(jq -r '.name' <<<"$run")
  status=$(jq -r '.status' <<<"$run")
  concl=$(jq -r '.conclusion' <<<"$run")
  echo "- id=$id name=$name status=$status conclusion=$concl"
  if [[ "$status" == "completed" ]]; then
    if [[ "$concl" == "success" ]]; then
      echo "GREEN: ${OWNER}/${REPO}@${BRANCH}"
      exit 0
    else
      echo "FAILED: ${OWNER}/${REPO}@${BRANCH} (conclusion=$concl)" >&2
      exit 3
    fi
  fi
  now=$(date +%s)
  if (( now - start >= TIMEOUT )); then
    echo "TIMEOUT waiting for green" >&2
    exit 2
  fi
  sleep "$SLEEP"
done