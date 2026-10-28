#!/bin/bash
# ./build.sh <slug|dir>  →  <dir>/out/<PREFIX>-Book-{full,share}.pdf (+ panel labels) + photo/manual web package (+ zip)
# <slug> resolves to examples/<slug>/ (or ./<slug>/); any directory holding a data.py works.
set -euo pipefail
B="$(cd "$(dirname "$0")" && pwd)"; E="$B/engine"
ARG="${1:?usage: build.sh <slug|dir>}"
for c in "$ARG" "$B/examples/$ARG" "$B/$ARG"; do [ -f "$c/data.py" ] && { P="$(cd "$c" && pwd)"; break; }; done
[ -n "${P:-}" ] || { echo "no data.py for '$ARG' (tried ./$ARG, examples/$ARG)"; exit 1; }
for t in python3 xelatex latexmk magick pdfinfo; do command -v $t >/dev/null || { echo "missing: $t"; exit 1; }; done
export PROP="$P"
cd "$P"
meta() { python3 -c "import runpy; print(runpy.run_path('data.py')['META'].get('$1',''))"; }
PREFIX=$(meta prefix); COVER=$(meta cover)
python3 "$E/photos.py"
if [ -n "$COVER" ] && [ -f "photos/orig/$COVER" ]; then
  magick "photos/orig/$COVER" -auto-orient -resize '2550x1920^' -gravity center -extent 2550x1920 -strip -quality 85 photos/print/cover.jpg
fi
mkdir -p out tex
rm -rf tex/gen
HASPANELS=$(python3 -c "import runpy; print(1 if runpy.run_path('data.py').get('PANELS') else 0)")
if [ "$HASPANELS" = 1 ]; then
  EDITION=full python3 "$E/gen.py" >/dev/null
  (cd tex && latexmk -g -xelatex -interaction=nonstopmode -halt-on-error panel-labels.tex >/dev/null) || { echo "LaTeX failed (panel labels): see $P/tex/panel-labels.log"; exit 1; }
  cp tex/panel-labels.pdf "out/$PREFIX-Panel-Labels.pdf"
fi
for ed in full share; do
  rm -rf tex/gen
  EDITION=$ed python3 "$E/gen.py" >/dev/null
  (cd tex && latexmk -g -xelatex -interaction=nonstopmode -halt-on-error -jobname="book-$ed" main.tex >/dev/null) \
    || { echo "LaTeX failed ($ed): see $P/tex/book-$ed.log"; exit 1; }
  cp "tex/book-$ed.pdf" "out/$PREFIX-Book-$ed.pdf"
done
rm -rf tex/gen; EDITION=full python3 "$E/gen.py" >/dev/null
python3 "$E/gallery.py"
rm -f "out/$PREFIX-photos.zip" && (cd photos && zip -qr "../out/$PREFIX-photos.zip" publish -x '*.DS_Store')
for f in out/*.pdf; do printf '%-48s %4s pp\n' "$f" "$(pdfinfo "$f" | awk '/^Pages/{print $2}')"; done
