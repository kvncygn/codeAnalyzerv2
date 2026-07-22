# PLAN.md — Implementation Plan

> **Özet (TR):** REQUIREMENTS.md gereksinimlerini uygulayan, tamamen yerel, **hibrit** statik
> kod analizcisi: Python uygulama kabuğu + gömülü **.NET 8 / Roslyn** C# motoru. Windows'a
> tek **PyInstaller `.exe`** olarak teslim edilir. Mimari, veri akışı, JSON sözleşmesi,
> helper modeli ve limitations → `docs/architecture.md`. Bu dosya: algoritmalar, kararlar,
> test ve yol haritası. Çelişki olursa **REQUIREMENTS.md kazanır**.

The architecture overview, data flow, analyzer JSON contract, helper model, and
limitations live in **[`docs/architecture.md`](docs/architecture.md)**. This file is the
implementation plan: algorithms, locked decisions, testing, and roadmap. **REQUIREMENTS.md** is
the authoritative requirements spec; where this plan and REQUIREMENTS.md disagree, REQUIREMENTS.md
wins.

---

## 1. Guardrails

- **Local-only at runtime** for every component (Python app *and* the bundled .NET
  analyzer): no internet, no cloud/AI, no telemetry, no remote logging. Flask binds to
  `127.0.0.1` only.
- Supported extensions only: `.cs .c .h .cpp .hpp .cc .cxx .hh` (matched
  case-insensitively).
- **Never crash** on: invalid folder, empty folder, no supported files, encoding errors,
  syntax errors. One bad file must not stop the others.
- Dev-time installs (`uv`, .NET SDK, NuGet) are setup steps — not the application.

## 2. Tech Stack (final)

| Concern | Choice |
|---|---|
| App shell / UI | Python 3.12 (uv venv) + Flask, `127.0.0.1` only |
| C# analysis | .NET 8 + Roslyn (`Microsoft.CodeAnalysis.CSharp`), bundled self-contained exe |
| C/C++ comments | small pure-Python lexer (no native deps) |
| Tests | pytest (Python) + xUnit (C#) |
| Lint / format / types | ruff + black + mypy; `.editorconfig`; C# `Nullable` enabled |
| Packaging | self-contained analyzer per RID + PyInstaller → single Windows `.exe` |

> **tree-sitter is not used.** Roslyn supersedes it for C#; a small Python lexer covers
> C/C++ comment detection. This keeps the PyInstaller bundle free of native parser deps.

## 3. Repo Layout

```
csharp-analyzer/    .NET 8 Roslyn analyzer (+ xUnit tests)
src/codeanalyzer/   Python package: scanner, line_metrics, cpp_comments,
                    analyzer_bridge, orchestrator, report, web/
tests/python/       pytest + fixtures
scripts/            build-analyzer.sh, run-dev.sh, package-windows.ps1
docs/architecture.md
```

## 4. Line Counting (exact REQUIREMENTS.md rules) — `line_metrics`

**Single source of truth:** *all* line counting (C# and C/C++) is implemented once, in
Python. The Roslyn analyzer and the C/C++ lexer only supply **comment spans**; Python
applies the exact rules uniformly. (This avoids two divergent implementations of the
counting rules.)

Per physical line, decide `has_code` and `has_comment`, then:

| has_code | has_comment | effect |
|---|---|---|
| F | F | `blank += 1` |
| T | F | `code += 1` |
| F | T | `comment += 1` |
| T | T | `code += 1`, `comment += 1`, `inline_comment += 1` |

`total += 1` for every physical line.

**Algorithm (over the decoded text, character columns):**
1. Python is the single file reader: bytes are decoded once (encoding-fallback chain) and
   the resulting text is what both the analyzer and the line counter use.
2. Split the text into physical lines using Roslyn-compatible line breaks (LF, CRLF, CR,
   NEL/LS/PS). A trailing line break does not add an empty line; an empty file is 0 lines.
3. Obtain `comment` spans `(startLine, startCol, endLine, endCol)`, 0-based with character
   columns — from the analyzer JSON for `.cs`, from the Python lexer for C/C++.
4. Project spans onto per-line character intervals (single/first/middle/last line).
5. Per line: `has_comment` = the line has any comment interval; `has_code` = any
   non-whitespace character **not** inside a comment interval. Strings are code
   automatically (never inside a comment).

Columns are character indices (code points). Roslyn reports UTF-16 columns, which equal
code points for the Basic Multilingual Plane (all realistic source); non-BMP characters
are a documented, negligible caveat.

This is correct for inline comments, comment-only lines, multi-line `/* */` (code before
`/*` / after `*/`), and `"http://x"` / `"// x"` (stay code).

**Per-method metrics** reuse the file's per-row classification, sliced to the method's
`[startLine, endLine]` (from the analyzer). `total = end - start + 1`;
`comment_ratio = comment / total` (0.0 if total is 0). Leading `///` doc comments precede
the method node and are not counted in the method.

## 5. C/C++ Comment Lexer — `cpp_comments`

A small, well-tested byte/char state machine emitting comment spans. Must handle:
`//` line comments, `/* */` block comments, `"..."` strings and `'...'` chars (with
`\` escapes), **backslash-newline line continuation** (can extend a `//` comment / splice
lines), and **C++ raw strings** `R"delim( ... )delim"` (no escapes inside). Comment
markers inside strings/chars are not comments, and string markers inside comments are not
strings.

## 6. C# Analyzer (Roslyn) — `csharp-analyzer/`

A self-contained .NET 8 console tool. Input: the scanned `.cs` file paths + the TCF
prefix. It builds **one ad-hoc `CSharpCompilation`** from those files + BCL references
(`TRUSTED_PLATFORM_ASSEMBLIES`), then emits JSON per file (contract in
`docs/architecture.md`). Because the compilation contains exactly the folder's `.cs`
files, "defined in source" ≡ "defined under the analyzed folder".

- **Methods:** `MethodDeclarationSyntax` only (constructors, properties/indexers, local
  functions excluded). `isTcf = name.StartsWith(prefix)`. `startLine/endLine` from the
  declaration span.
- **Cyclomatic complexity** = `1 +` count, within the method body, of these
  `SyntaxKind`s: `IfStatement`, `ForStatement`, `ForEachStatement`,
  `ForEachVariableStatement`, `WhileStatement`, `DoStatement`, `CaseSwitchLabel`,
  `CasePatternSwitchLabel`, `SwitchExpressionArm`, `CatchClause`, `ConditionalExpression`,
  and the binary `LogicalAndExpression`, `LogicalOrExpression`, `CoalesceExpression`.
  `DefaultSwitchLabel` is excluded.
- **Helper resolution (semantic):** for each `InvocationExpressionSyntax` in an TCF
  method, resolve the symbol (`GetSymbolInfo`); take `OriginalDefinition`. If it is in
  source and non-TCF → **helper** (emit `{name, file}`); in source and TCF → ignore
  (TCF-to-TCF); metadata/unresolved → **library** (ignore). *(Proven in the Roslyn smoke
  test: project `Add()` ⇒ helper, `list.Add()` ⇒ library.)*
- **Comment spans:** emit comment trivia spans (byte columns) for Python line counting.
- **Resilience:** parsing/semantic errors never throw; report `diagnostics.hasErrors` and
  continue. A file Python can't even hand off is skipped with a warning.

## 7. Helper Model

Helper = a C# method, defined under the analyzed folder, non-TCF, called by ≥1 TCF method,
resolved **semantically**. TCF-centric (no helper is ever "unused"). Full definition and
**limitations** in `docs/architecture.md`. No external/library report, no TCF-to-TCF
report, no manual helper-file selection.

## 8. Reports & Output Order

Exact REQUIREMENTS.md order: **1)** Project Summary · **2)** File Summary · **3)** Source Tree
(files + their TCF methods, example format) · **4)** TCF Method Details · **5)** Helper
Usage Summary. Plus a **Warnings/Errors** panel (skipped files, encoding issues,
analyzer diagnostics).

## 9. UI Flow (simplified — no helper selection)

- `GET /` — form: **folder path**, **TCF prefix** (default `TCF`).
- `POST /analyze` — validate folder; scan; run analysis; render the 5 ordered sections +
  warnings; optional local JSON download.
- Bind `127.0.0.1`. Folder is typed (browsers can't expose real paths).

## 10. Error Handling

- Invalid/empty folder, no supported files → friendly inline message, never a stack
  trace.
- Per file, both sides wrap work in try/except; encoding via byte read + fallback chain
  (`utf-8` → `utf-8-sig` → `utf-16` → `cp1252` → `errors=replace`) with a warning.
- Analyzer `diagnostics.hasErrors` → warning "possible syntax errors; partial results".

## 11. Testing

- **Python (pytest):** line-counting edge cases (inline / comment-only / blank; strings
  containing `//` and `/* */`; multi-line comments; BOM; CRLF; C++ raw strings; verbatim/
  interpolated C# strings via the analyzer path), scanner/encoding, report ordering &
  tree formatting, error paths (bad/empty folder, broken-encoding, syntax-error file).
- **C# (xUnit):** method enumeration, TCF classification, complexity on known branches,
  and **the name-collision trap** (project `Add` vs `list.Add`), cross-file helper,
  TCF-to-TCF ignored, syntax-error resilience.
- **End-to-end:** a small mixed sample tree with hand-computed expected numbers.

## 12. Packaging & Delivery

Details in `docs/architecture.md`. In short: publish the analyzer **self-contained,
single-file** — `linux-x64` for local dev/test here, `win-x64` for delivery — into
`src/codeanalyzer/_bundled/`; then **PyInstaller on Windows** bundles the Python app +
`analyzer.exe` into one executable. The analyzer path resolver handles both dev and frozen
(PyInstaller) layouts. Verify no telemetry/network at runtime.

## 13. Conservative Decisions (locked)

1. "C# method" = `MethodDeclarationSyntax` only (no ctors/properties/local functions).
2. `comment_ratio = comment_lines / total_line_count`.
3. Switch complexity: each case label (`Case*SwitchLabel`) = +1; `default` excluded.
4. Helper iff call resolves to a **source-defined non-TCF** method; metadata/unresolved
   (incl. third-party NuGet) ⇒ library ⇒ ignored.
5. `.h` labeled `C/C++ Header`; C/C++ comments via the Python lexer.
6. Line metrics over the decoded text with **character columns** and Roslyn-compatible
   line splitting (single reader: Python decodes once; the analyzer reuses that text).
7. Method metric span = the declaration node span; leading doc comments excluded.

## 14. Roadmap (tasks #1–#9)

1. ✅ Scaffold clean repo + tooling.
2. ▶ Rewrite REQUIREMENTS.md + PLAN.md for hybrid architecture (this).
3. C# Roslyn analyzer: JSON contract, complexity, semantic helper resolution, comment
   spans, resilience, xUnit tests, self-contained publish (linux-x64 + win-x64).
4. Python: cross-platform scanner + encoding-robust reader + file-type classification.
5. Python: `line_metrics` (exact rules) + `cpp_comments` lexer + tests.
6. Python: orchestration (subprocess + JSON merge) + data models + error collection.
7. Python: report builder (5 ordered sections + source tree) + tests.
8. Flask UI (`127.0.0.1`) + error handling.
9. Packaging & delivery: PyInstaller spec + scripts + Windows build/run docs.
