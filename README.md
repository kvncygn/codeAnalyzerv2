# codeAnalyzer

A **local-only** static code analyzer with a localhost web UI. It scans a folder of
source files and produces per-method and per-file reports for C# (TCF methods +
helpers) and file-level metrics for C/C++.

> **Local-only guarantee.** The application makes no internet requests and sends no
> source code or analysis data off the machine. No cloud, no AI APIs, no telemetry, no
> remote logging. The web UI binds to `127.0.0.1` only.

## What it analyzes

- **C# (`.cs`)** — methods whose names start with the configured **TCF prefix**
  (default `TCF`) get full metrics: line counts (total / code / comment /
  inline-comment / blank), comment ratio, cyclomatic complexity, and the **helper
  functions** they use. A *helper* is a project-defined, non-TCF method called by at
  least one TCF method, resolved **semantically** (see Limitations).
- **C/C++ (`.c .h .cpp .hpp .cc .cxx .hh`)** — file-level line metrics only
  (TCF and helper counts are always `0`).

## Architecture (hybrid)

Accuracy-critical C# analysis uses **Roslyn** (the real C# compiler API); the
application shell is **Python**.

- **Python** — Flask UI, folder scanning, line counting (exact rules, all languages),
  C/C++ metrics, reporting, orchestration, packaging.
- **.NET / Roslyn analyzer (bundled)** — per-`.cs` semantic analysis: methods, TCF
  classification, cyclomatic complexity, **helper-vs-library** call resolution, and
  comment spans. Invoked by Python as a subprocess (JSON). Shipped **self-contained**
  (no .NET required on the target machine).

See [`docs/architecture.md`](docs/architecture.md) for the data flow and analyzer JSON
contract.

## Requirements

- **Python 3.12+** (development uses a `uv`-managed virtual environment)
- **.NET 8 SDK** — to *build* the analyzer; **not** needed to *run* the packaged app

## Develop / run (Linux / macOS)

```bash
# Python environment
~/.local/bin/uv venv .venv --python 3.12
~/.local/bin/uv pip install -e ".[dev]" --python .venv/bin/python

# Build the C# analyzer (self-contained, for local dev)
scripts/build-analyzer.sh linux-x64

# Run the app  ->  http://127.0.0.1:5000
scripts/run-dev.sh            # (or: .venv/bin/python -m codeanalyzer)

# Run all tests (Python + C#)
scripts/run-tests.sh

# Build the packaged app for this OS  ->  dist/codeanalyzer/ (one-dir)
scripts/package.sh linux-x64
```

## Using the app

Starting the app prints a URL with a one-time **access token** and opens it in your
browser, e.g. `http://127.0.0.1:5000/?t=<token>`. The token (bound to a Strict-SameSite
session cookie) keeps other local users on a shared machine — and malicious web pages —
from driving the app; the Host header is also pinned to localhost. On a trusted
single-user box you can skip it with `CODEANALYZER_NO_AUTH=1`.

Enter a folder path (or click **Browse…** for a native folder picker), optionally change
the TCF prefix, and click **Analyze**. The last folder/prefix are remembered between
runs. Results include a project summary, a per-file table (sortable, filterable), a
collapsible source tree, paginated & searchable TCF-method and helper-usage views
(adjustable page size), **outlier highlighting** (high complexity / low comment ratio),
and **CSV / text / JSON export** — all generated locally in the browser. If port 5000 is
busy, the app automatically picks the next free port.

## Windows delivery (one-dir bundle)

The end-user app ships as a **PyInstaller one-dir bundle** (a folder, not a single
self-extracting `.exe`): it starts faster and trips antivirus heuristics far less than a
one-file build. The final build must run **on Windows** (PyInstaller does not
cross-compile). On a Windows machine with **.NET 8 SDK** and **Python 3.12**:

```powershell
py -3.12 -m venv .venv
.venv\Scripts\pip install -e ".[dev,package]"
powershell -ExecutionPolicy Bypass -File scripts\package-windows.ps1
# -> dist\codeanalyzer\codeanalyzer.exe   (run it; opens http://127.0.0.1:5000)
```

Deliver the **whole `dist\codeanalyzer\` folder** (e.g. zipped). The bundle needs neither
Python nor .NET installed.

> **Antivirus / SmartScreen:** unsigned executables may trigger Windows SmartScreen or AV
> heuristics on locked-down machines. For production delivery, **code-sign**
> `codeanalyzer.exe` (and ideally the bundled `analyzer.exe`) with the organization's
> certificate. The one-dir layout already reduces false positives versus one-file.

See [`docs/architecture.md`](docs/architecture.md) for details.

## Repo layout

```
csharp-analyzer/    .NET 8 Roslyn analyzer (+ tests)
src/codeanalyzer/   Python package (UI, scanning, metrics, reporting, orchestration)
tests/              Python tests + fixtures
scripts/            build / run / package scripts
docs/               architecture.md + developer-guide.md (contributor manual)
REQUIREMENTS.md           requirements spec
PLAN.md             implementation plan
```

## Limitations

Helper detection is best-effort static analysis (semantic, but compiler-context
dependent). See the **Limitations** section of
[`docs/architecture.md`](docs/architecture.md).


    
