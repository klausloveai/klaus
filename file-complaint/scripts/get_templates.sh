#!/bin/bash
# Download the firm's Litigation-Forms templates from Drive into $1 (a scratch dir).
# Requires the gws CLI (Klaus's Google Workspace CLI, connected to Drive).
# Usage: bash get_templates.sh /path/to/scratch
set -e
DEST="${1:?usage: get_templates.sh <dest_dir>}"
mkdir -p "$DEST"
cd "$DEST"   # gws only writes to the current directory, so run from there

get() { # id  outfile
  gws drive files get --params "{\"fileId\":\"$1\",\"alt\":\"media\",\"supportsAllDrives\":true}" -o "$2" >/dev/null
  # JC forms ship encrypted (empty password); decrypt so pypdf can read them
  # without the optional 'cryptography' dependency. qpdf exits 3 on warnings
  # (still writes output), so key off the output file existing, not the exit code.
  qpdf --decrypt "$2" "dec_$2" 2>/dev/null || true
  [ -f "dec_$2" ] && mv "dec_$2" "$2"
  echo "  downloaded $2"
}

echo "Downloading templates to $DEST"
get 1eCAnesHkpmn2sVXleIgLVgaCIr4XPyi5 sum100.pdf   # sum100(Hernan).pdf
get 1bcU_7BhFx-XPgzASI_-RQcOp2hNrVrzj cm010.pdf    # cm010(Hernan).pdf
get 19U8ASWcSwDXOXwGo-wGmdOo6ICwESOyT civ109.pdf   # LASC CIV 109.pdf
echo "done"
