#!/usr/bin/env bash
set -euo pipefail

# Instaluje lokalne zabezpieczenia Git:
# - pre-commit blokujący commit pliku AGENT.md
# - wpis w .git/info/exclude ignorujący AGENT.md
# Skrypt jest idempotentny i bezpieczny przy wielokrotnym uruchomieniu.

ROOT_DIR="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
HOOKS_DIR="${ROOT_DIR}/.git/hooks"
EXCLUDE_FILE="${ROOT_DIR}/.git/info/exclude"

mkdir -p "${HOOKS_DIR}" "${ROOT_DIR}/.git/info"

# Zawartość hooka pre-commit
read -r -d '' HOOK_CONTENT <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
# Block committing AGENT.md under any circumstance
if git diff --cached --name-only | grep -qx "AGENT.md"; then
  echo "ERROR: AGENT.md is internal and must never be committed." >&2
  echo "Remove it from the index: git reset AGENT.md" >&2
  exit 1
fi
EOF

HOOK_PATH="${HOOKS_DIR}/pre-commit"

# Zapisz hook tylko jeśli różni się od obecnego
if [[ -f "${HOOK_PATH}" ]]; then
  CURRENT_SHA="$(sha256sum "${HOOK_PATH}" | awk '{print $1}')"
  NEW_SHA="$(printf '%s' "${HOOK_CONTENT}" | sha256sum | awk '{print $1}')"
  if [[ "${CURRENT_SHA}" != "${NEW_SHA}" ]]; then
    printf '%s' "${HOOK_CONTENT}" >"${HOOK_PATH}"
    chmod +x "${HOOK_PATH}"
    echo "Zaktualizowano .git/hooks/pre-commit"
  fi
else
  printf '%s' "${HOOK_CONTENT}" >"${HOOK_PATH}"
  chmod +x "${HOOK_PATH}"
  echo "Zainstalowano .git/hooks/pre-commit"
fi

# Dopisz AGENT.md do lokalnego exclude, jeśli brak
if ! grep -qxF 'AGENT.md' "${EXCLUDE_FILE}" 2>/dev/null; then
  echo 'AGENT.md' >> "${EXCLUDE_FILE}"
  echo "Dodano AGENT.md do .git/info/exclude"
fi

echo "Hook setup OK."

