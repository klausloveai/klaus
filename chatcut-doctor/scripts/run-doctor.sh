#!/bin/sh
set -eu
doctor_root=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
doctor_runtime=${CHATCUT_DOCTOR_RUNTIME:-}
if [ -z "$doctor_runtime" ]; then doctor_runtime=$(command -v node || true); fi
if [ -z "$doctor_runtime" ] || [ ! -f "$doctor_root/cli/bin/chatcut.mjs" ]; then
  printf '%s\n' 'Use the prepared local Doctor candidate and select an existing Node 22+ or ChatCut Electron runtime with CHATCUT_DOCTOR_RUNTIME. Nothing was installed.' >&2
  exit 3
fi
exec env ELECTRON_RUN_AS_NODE=1 "$doctor_runtime" "$doctor_root/cli/bin/chatcut.mjs" doctor "$@"
