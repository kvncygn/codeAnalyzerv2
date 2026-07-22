# Example source folders (for manual testing)

Ready-to-analyze folders you can point the analyzer at. In the app, type the
**full path** to one of these folders (e.g. `C:\...\codeAnalyzer\examples\enterprise`)
and click **Analyze**. Everything stays local — these are just sample source files.

## `edge-cases/` — correctness traps (tiny, hand-written)

Five files that exercise the tricky rules from `REQUIREMENTS.md`. Use this to confirm the
analyzer is *correct*, not just that it runs.

| File | What it proves |
|------|----------------|
| `Orders.cs` | `items.Add()` (library `List<T>.Add`) is **not** a helper, but project `CalcTotal()`/`ApplyRush()`/`Log()` **are**. `Unused()` is never called by an TCF method → **not** a helper. `TCF_Bootstrap()` only calls another TCF method → that edge is **ignored**. Doc/`/* */` comment spans counted correctly. |
| `Broken.cs` | Deliberate **syntax error** (missing brace). Analysis must not crash; other files still analyze. |
| `util.c`, `engine.cpp`, `types.hpp` | C/C++ → **file-level metrics only**, `TCF = 0`, `Helpers = 0`. |

Expected highlights: `CalcTotal` is a helper called by **two** TCF methods
(`TCF_ProcessOrder`, `TCF_Validate`); a warning is shown for `Broken.cs`.

## `enterprise/` — realistic cross-file layout (generated)

Mirrors a realistic enterprise layout: **TCF methods and helpers live in separate files.**
`Service*.cs` contain only `TCF_*` methods; `Helpers*.cs` contain only non-TCF helper
methods that the TCF methods call **across files** (semantic resolution).

Ground truth (seed 7):

```
TCF files (TCF>0, Helpers=0)             : 4   (Service0-3.cs)
Helper files (TCF=0, Helpers>0)          : 3   (Helpers0-2.cs)
C++ files                                : 2   (engine0-1.cpp)
TCF methods                              : 75
helper methods DEFINED                   : 136
helper methods CALLED by TCF (= helpers) : 90
helper defs NEVER called (NOT helpers)   : 46
library List.Add() sites (NOT helpers)   : 75
TCF->TCF call sites (IGNORED)            : 29
```

So a correct run reports **75 TCF methods** and **90 helpers** (not 136), every
`Service*.cs` shows `Helpers=0`, every `Helpers*.cs` shows `TCF=0`, and every
helper-usage entry points into a `Helpers*.cs` file.

## Generating a true enterprise-scale set (5k–10k line files)

This repo keeps the samples small. To stress-test with a realistic large-codebase size
(15–20 files of 5,000–10,000 lines each), run the generator into a folder **outside**
the repo:

```powershell
py -3.12 scripts\gen_enterprise_sample.py C:\temp\big-sample ^
  --tcf-files 14 --helper-files 6 --cpp 2 --min-lines 5000 --max-lines 10000
```

It prints the exact ground truth so you can verify the report. (`--seed` makes it
reproducible; defaults already target 12 TCF + 6 helper files at 5k–10k lines.)
