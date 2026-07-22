# Build the Windows executable as a one-DIR bundle (dist\codeanalyzer\codeanalyzer.exe).
#
# One-dir (a folder, not a single self-extracting .exe) starts faster and trips antivirus
# heuristics far less than a one-file build -- both matter on enterprise machines. Deliver
# the whole dist\codeanalyzer\ folder (e.g. zipped).
#
# Run on Windows (PyInstaller does not cross-compile). Prerequisites:
#   - .NET 8 SDK
#   - Python 3.12 with the project installed:  pip install -e ".[dev,package]"
#
# Usage (from the repo root):  powershell -ExecutionPolicy Bypass -File scripts\package-windows.ps1

$ErrorActionPreference = "Stop"
$root = Split-Path -Parent $PSScriptRoot
$env:DOTNET_CLI_TELEMETRY_OPTOUT = "1"
$env:DOTNET_NOLOGO = "1"

Write-Host "== Publishing self-contained analyzer (win-x64) =="
dotnet publish "$root\csharp-analyzer\src\TcfAnalyzer\TcfAnalyzer.csproj" `
  -c Release -r win-x64 --self-contained true `
  -p:PublishSingleFile=true -p:IncludeNativeLibrariesForSelfExtract=true `
  -o "$root\artifacts\analyzer\win-x64"

Write-Host "== Staging analyzer.exe into the package =="
$dest = "$root\src\codeanalyzer\_bundled"
Remove-Item -Recurse -Force $dest -ErrorAction SilentlyContinue
New-Item -ItemType Directory -Force -Path $dest | Out-Null
Copy-Item "$root\artifacts\analyzer\win-x64\analyzer.exe" "$dest\analyzer.exe"

Write-Host "== Bundling with PyInstaller =="
# Prefer the project venv so PyInstaller is found regardless of system PATH
$python = if (Test-Path "$root\.venv\Scripts\python.exe") { "$root\.venv\Scripts\python.exe" } else { "python" }
& $python -m PyInstaller --clean --noconfirm `
  --distpath "$root\dist" --workpath "$root\build" `
  "$root\packaging\codeanalyzer.spec"

Write-Host "Built -> $root\dist\codeanalyzer\codeanalyzer.exe  (deliver the whole folder)"
