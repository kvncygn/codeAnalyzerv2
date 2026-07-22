#!/usr/bin/env bash
#
# Copy a published analyzer binary into the Python package so PyInstaller can bundle it.
# Usage: scripts/stage-analyzer.sh [RID]   (default: linux-x64)
#
set -euo pipefail
RID="${1:-linux-x64}"
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

name="analyzer"
[ "$RID" = "win-x64" ] && name="analyzer.exe"

SRC="$ROOT/artifacts/analyzer/$RID/$name"
DEST="$ROOT/src/codeanalyzer/_bundled"

if [ ! -f "$SRC" ]; then
  echo "Analyzer not found: $SRC" >&2
  echo "Build it first: scripts/build-analyzer.sh $RID" >&2
  exit 1
fi

rm -rf "$DEST"
mkdir -p "$DEST"
cp "$SRC" "$DEST/$name"
echo "Staged $name -> $DEST"
