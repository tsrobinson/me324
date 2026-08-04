#!/usr/bin/env bash
# Regenerate the PDF exports of the released lecture decks with decktape.
#
# Run AFTER `quarto render`, from the repo root:
#   bash tools/make-slide-pdfs.sh            # all decks in docs/lectures/
#   bash tools/make-slide-pdfs.sh lecture-02 # only decks matching a prefix
#
# PDFs land in lectures/pdf/, which _quarto.yml declares as a site resource,
# so the next render copies them into docs/. This script also copies them
# straight into docs/lectures/pdf/ so no extra render is needed.
set -euo pipefail
cd "$(dirname "$0")/.."

PORT=8642
FILTER="${1:-}"

mkdir -p lectures/pdf docs/lectures/pdf
python3 -m http.server "$PORT" -d docs >/dev/null 2>&1 &
SERVER=$!
trap 'kill "$SERVER"' EXIT
sleep 1

for f in docs/lectures/*.html; do
  name=$(basename "$f" .html)
  if [[ -n "$FILTER" && "$name" != "$FILTER"* ]]; then continue; fi
  echo "==> $name"
  decktape reveal -s 1280x760 \
    "http://localhost:$PORT/lectures/$name.html" \
    "lectures/pdf/$name.pdf"
  cp "lectures/pdf/$name.pdf" "docs/lectures/pdf/$name.pdf"
done
