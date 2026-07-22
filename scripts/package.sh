#!/usr/bin/env bash
#
# Build the single-file codeAnalyzer executable for the host platform (Linux/macOS).
# (Windows delivery uses scripts/package-windows.ps1, which must run on Windows.)
#
# Usage: scripts/package.sh [RID]   (default: linux-x64)
#
set -euo pipefail
RID="${1:-linux-x64}"
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PY="$ROOT/.venv/bin/python"

"$ROOT/scripts/build-analyzer.sh" "$RID"
"$ROOT/scripts/stage-analyzer.sh" "$RID"

PYTHONPATH= "$PY" -m PyInstaller --clean --noconfirm \
  --distpath "$ROOT/dist" --workpath "$ROOT/build" \
  "$ROOT/packaging/codeanalyzer.spec"

echo "Built -> $ROOT/dist/codeanalyzer/  (run dist/codeanalyzer/codeanalyzer)"
