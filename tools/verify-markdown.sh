#!/usr/bin/env bash
set -euo pipefail

err=0
check_file() {
  local f="$1"
  awk -v file="$f" '
  function report(n,msg){ printf("%s:%d: %s\n", file, n, msg) }
  BEGIN{ prev=""; in_list=0; prev_was_heading=0 }
  {
    line=$0
    is_blank = (match(line, /^\s*$/) > 0)
    is_heading = (match(line, /^#{1,6}[[:space:]]/) > 0)
    is_list = (match(line, /^\s*([-*]|[0-9]+\.)[[:space:]]/) > 0)

    if (prev_was_heading && !is_blank) { report(NR-1, "Brak pustej linii po nagłówku") }
    prev_was_heading=0

    if (is_heading && NR>1 && prev !~ /^\s*$/) { report(NR, "Brak pustej linii przed nagłówkiem") }
    if (is_heading) { prev_was_heading=1 }

    if (is_list) {
      if (!in_list) {
        if (NR>1 && prev !~ /^\s*$/) { report(NR, "Brak pustej linii przed listą") }
        in_list=1
      }
    } else {
      if (in_list) {
        if (!is_blank) { report(NR-1, "Brak pustej linii po liście") }
        in_list=0
      }
    }

    prev=line
  }
  ' "$f" || true
}

shopt -s nullglob
files=(""*.md)
for f in "${files[@]}"; do
  out=$(check_file "$f") || true
  if [[ -n "$out" ]]; then printf '%s\n' "$out"; err=1; fi
done

exit $err
