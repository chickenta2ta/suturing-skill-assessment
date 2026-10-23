#!/bin/sh
# Compose Fig. 1 (overview.pdf) from its two parts, as overview.tex says. Run after either part is regenerated.
set -e
cd "$(dirname "$0")"
export PATH=/opt/homebrew/bin:$PATH
tmp=$(mktemp -d)
pdflatex -interaction=nonstopmode -halt-on-error -output-directory="$tmp" overview.tex > "$tmp/pdflatex.log" 2>&1 \
    || { tail -20 "$tmp/pdflatex.log"; exit 1; }
cp "$tmp/overview.pdf" overview.pdf
rm -rf "$tmp"
ls -l overview.pdf
