#!/bin/sh
# Build the paper into build/ and list LaTeX problems (undefined references, overfull boxes, ...).
set -e
cd "$(dirname "$0")"
export PATH=/opt/homebrew/bin:$PATH
mkdir -p build
latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=build Template_ISBI_latex.tex > build/latexmk.log 2>&1 \
    || { tail -30 build/latexmk.log; exit 1; }
grep -nE '^!|undefined|Overfull|multiply defined|Citation' build/Template_ISBI_latex.log || echo "no LaTeX problems"
