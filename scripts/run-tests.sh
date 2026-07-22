#!/usr/bin/env bash
#
# Run the full test suite (Python + C#) in a clean environment.
# PYTHONPATH is cleared and pytest plugin autoload is disabled so that stray system
# packages (e.g. a ROS install) cannot leak into the run.
#
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

echo "== Python tests =="
PYTHONPATH= PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 "$ROOT/.venv/bin/python" -m pytest "$ROOT/tests/python" -q

echo
echo "== C# tests =="
export DOTNET_ROOT="${DOTNET_ROOT:-$HOME/.dotnet}"
export PATH="$DOTNET_ROOT:$PATH"
export DOTNET_CLI_TELEMETRY_OPTOUT=1
export DOTNET_NOLOGO=1
dotnet test "$ROOT/csharp-analyzer/TcfAnalyzer.sln" -v minimal --nologo
