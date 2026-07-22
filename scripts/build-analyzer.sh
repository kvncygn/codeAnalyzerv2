#!/usr/bin/env bash
#
# Publish the C# analyzer as a self-contained, single-file executable for one RID.
# The target machine then needs no .NET runtime installed.
#
# Usage:
#   scripts/build-analyzer.sh [RID]
# Examples:
#   scripts/build-analyzer.sh linux-x64   # local dev/test (default)
#   scripts/build-analyzer.sh win-x64     # Windows delivery
#
set -euo pipefail

RID="${1:-linux-x64}"
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PROJECT="$ROOT/csharp-analyzer/src/TcfAnalyzer/TcfAnalyzer.csproj"
OUT="$ROOT/artifacts/analyzer/$RID"

export DOTNET_ROOT="${DOTNET_ROOT:-$HOME/.dotnet}"
export PATH="$DOTNET_ROOT:$PATH"
export DOTNET_CLI_TELEMETRY_OPTOUT=1
export DOTNET_NOLOGO=1

echo "Publishing analyzer for $RID ..."
dotnet publish "$PROJECT" \
  -c Release \
  -r "$RID" \
  --self-contained true \
  -p:PublishSingleFile=true \
  -p:IncludeNativeLibrariesForSelfExtract=true \
  -o "$OUT"

echo "Done -> $OUT"
