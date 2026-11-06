#!/usr/bin/env bash
# Copy the bibliography from the literature submodule into the paper root (for Overleaf).
#   scripts/sync_bib.sh           write references.bib and bib_short.def from literature/bib/
#   scripts/sync_bib.sh --check   only report whether the root copies match the submodule (exit 1 if not)
# Never edit the root copies by hand; edit in phd-literature (see LITERATURE.md).
set -euo pipefail
cd "$(dirname "$0")/.."
src=literature/bib
[ -f "$src/references.bib" ] || { echo "literature/ is empty: run 'git submodule update --init'"; exit 1; }
status=0
for f in references.bib bib_short.def; do
  header="% GENERATED from $src/$f by scripts/sync_bib.sh -- do not edit; edit in phd-literature."
  expected=$(printf '%s\n\n' "$header"; sed '1s/^\xEF\xBB\xBF//' "$src/$f")
  if [ "${1:-}" = "--check" ]; then
    if [ "$expected" != "$(cat "$f" 2>/dev/null)" ]; then echo "OUT OF SYNC: $f"; status=1; else echo "in sync: $f"; fi
  else
    printf '%s\n' "$expected" > "$f"; echo "wrote $f"
  fi
done
exit $status
