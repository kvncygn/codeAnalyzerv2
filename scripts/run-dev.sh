#!/usr/bin/env bash
#
# Run the app from source for local development (serves http://127.0.0.1:5000).
# Requires the analyzer to be built once: scripts/build-analyzer.sh linux-x64
#
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PYTHONPATH= "$ROOT/.venv/bin/python" -m codeanalyzer
