# Architecture

> For a hands-on contributor manual — design rationale, a file-by-file code map, and
> "where do I change X" recipes — see [`developer-guide.md`](developer-guide.md).

## Overview

codeAnalyzer is a **hybrid local-only** application: a Python application shell plus a
bundled **.NET / Roslyn** analyzer for accurate C# semantic analysis. Everything runs
locally — no network, cloud, AI, or telemetry at runtime. The web UI binds to
`127.0.0.1` only.

The split exists for one reason: **accuracy**. Distinguishing a project helper call
from a library call (e.g. a project `Add()` vs `List<T>.Add()`) requires real semantic
binding, which Roslyn provides and a syntax-only parser cannot.

## Components

### Python (`src/codeanalyzer/`)
- `scanner` — walk the target folder, classify file types (case-insensitive
  extensions), read bytes with an encoding-fallback chain.
- `line_metrics` — the exact REQUIREMENTS.md line-counting rules (bytes-based), driven by
  comment spans.
- `cpp_comments` — a small, well-tested C/C++ comment & string lexer that produces
  comment spans for C/C++ files.
- `analyzer_bridge` — locate and invoke the bundled .NET analyzer via subprocess.
- `orchestrator` — merge analyzer JSON + line metrics into typed result objects.
- `report` — build the five ordered report sections + the source tree.
- `web` — the Flask application.

### .NET / Roslyn (`csharp-analyzer/`)
A self-contained console tool. For the set of scanned `.cs` files it builds an **ad-hoc
`CSharpCompilation`** (the files + BCL references) and emits JSON.

## Data flow

1. User enters a folder path + TCF prefix in the UI (`127.0.0.1`).
2. Python scans the folder for supported files.
3. Python invokes `analyzer(.exe)` with the C# file set and prefix; receives JSON.
4. Python computes line metrics — C# comment spans come from the analyzer JSON; C/C++
   comment spans come from the Python lexer — and merges them with the analyzer's
   semantic facts.
5. Python assembles the report and renders it (and can offer a local JSON download).

## Analyzer JSON contract (per C# file) — *draft, finalized with implementation*

```jsonc
{
  "path": "....cs",
  "diagnostics": { "hasErrors": false, "errorCount": 0 },
  "comments": [ { "startLine": 1, "startCol": 0, "endLine": 1, "endCol": 12 } ],
  "methods": [
    {
      "name": "TCF_Process",
      "isTcf": true,
      "startLine": 10, "endLine": 42,
      "cyclomaticComplexity": 5,
      "usedHelpers": [ { "name": "Add", "file": "Service.cs" } ]
    }
  ]
}
```
Library / unresolved / TCF-to-TCF callees are intentionally **not** emitted.
Columns are 0-based **character** offsets (Roslyn's UTF-16 columns, which equal code
points for the BMP); Python decodes each file once and reuses that text for counting.

## Helper model

A **helper** is a method that is:
1. a C# method (`method_declaration`),
2. defined in a file **under the analyzed folder**,
3. **non-TCF** (name does not start with the prefix), and
4. called by **≥ 1 TCF method**.

Call → definition resolution is **semantic** (Roslyn), against an ad-hoc compilation of
the scanned files + BCL references, so `Add()` (project) is correctly distinguished from
`list.Add()` (BCL). Reports: per-TCF `usedHelpers`, a Helper Usage Summary
(helper → TCF callers), and helper counts. There is **no** external/library report, no
TCF-to-TCF report, and no manual helper-file selection.

### Limitations
- **Unresolved third-party calls** (NuGet/refs not present) resolve to no source symbol
  → treated as library → ignored. Correct for helper-vs-library, but such calls are not
  otherwise analyzed.
- **Indirect calls** — delegates / `Func<>` / events / reflection — are not attributed
  (no static tool can fully resolve these).
- Semantics rely on BCL references + the scanned sources (no `.csproj`/restore). For
  very reference-heavy code, pointing the analyzer at a real project/solution could
  improve fidelity — a possible future enhancement, out of current scope.
- Helpers are **regular methods only** — not constructors, properties/indexers, or
  local functions.

## Cross-platform & packaging

- Code is cross-platform: `pathlib` paths, case-insensitive extensions, CRLF/BOM-safe
  line handling, robust encoding fallback (`utf-8` → `utf-8-sig` → `utf-16` → `cp1252`
  → replacement).
- The .NET analyzer is published **self-contained, single-file** per RID: `linux-x64`
  for local development, `win-x64` for delivery. The runtime is bundled, so the target
  machine needs no .NET install.
- The Windows distributable is built with **PyInstaller on Windows** (PyInstaller does
  not cross-compile), bundling the Python app + `analyzer.exe` into one executable.
- **Telemetry:** .NET CLI telemetry is opted out at build time
  (`DOTNET_CLI_TELEMETRY_OPTOUT=1`); a shipped self-contained runtime sends no
  telemetry. The Python app sends nothing.
