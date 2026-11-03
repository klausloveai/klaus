#!/bin/bash
# Creates (once) a venv with PyMuPDF + Pillow and prints its python path.
VENV="$HOME/.cache/pi-mkt-venv"
if [ ! -x "$VENV/bin/python" ]; then
  python3 -m venv "$VENV" >/dev/null && "$VENV/bin/pip" install -q pymupdf pillow >/dev/null 2>&1
fi
echo "$VENV/bin/python"
