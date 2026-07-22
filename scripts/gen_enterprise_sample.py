#!/usr/bin/env python3
"""Generate a realistic, large-scale synthetic C#/C++ codebase for stress testing.

This is a TEST FIXTURE GENERATOR -- not part of the shipped analyzer. It mirrors a typical
enterprise layout where the two kinds of C# file are SEPARATE:

  * TCF files (Service*.cs)   -- contain ONLY methods whose name starts with the TCF
                                 prefix. They call helpers that live in other files and
                                 a few library methods (which must NOT count as helpers).
  * Helper files (Helpers*.cs) -- contain ONLY non-TCF methods. Some are called by TCF
                                 methods (=> helpers), some are never called (=> NOT
                                 helpers). No TCF method is defined here.

So every TCF file should report Helpers=0 and every helper file should report TCF=0,
while helper *usage* is resolved across files. The script prints the expected ground
truth so the analyzer's output can be checked against it -- not just eyeballed.

Usage:
    python scripts/gen_enterprise_sample.py OUTDIR [--tcf-files N] [--helper-files M] \
        [--min-lines L] [--max-lines L] [--cpp K] [--seed S]
"""
from __future__ import annotations

import argparse
import random
from pathlib import Path

PREFIX = "TCF"
NS = "Enterprise"  # one shared namespace so cross-file calls need no `using`


def gen_helper_file(rng: random.Random, idx: int, min_lines: int, max_lines: int
                    ) -> tuple[str, list[str]]:
    """A file of only non-TCF helper methods. Returns (text, [HelperClass.Method names])."""
    target = rng.randint(min_lines, max_lines)
    cls = f"Helpers{idx}"
    out = [
        "using System;",
        "",
        f"// Auto-generated helper file #{idx} (non-TCF methods only).",
        f"namespace {NS}",
        "{",
        f"    public static class {cls}",
        "    {",
    ]
    names: list[str] = []
    h = 0
    while len(out) < target:
        hname = f"H{idx}_{h}"
        out.append(f"        // helper candidate {hname}")
        if rng.random() < 0.3:
            out.append("        /* small")
            out.append("           helper */")
        out.append(f"        public static int {hname}(int x)")
        out.append("        {")
        out.append(f"            int r = x + {h};      // inline comment")
        if rng.random() < 0.4:
            out.append(f"            if (r < 0) {{ r = -r; }}  // +1 complexity")
        out.append("            return r;")
        out.append("        }")
        out.append("")
        names.append(f"{cls}.{hname}")
        h += 1
    out.append("    }")
    out.append("}")
    return "\n".join(out) + "\n", names


def gen_tcf_file(rng: random.Random, idx: int, min_lines: int, max_lines: int,
                 helper_pool: list[str], counters: dict) -> str:
    """A file of only TCF methods that call cross-file helpers + library + (some) TCF."""
    target = rng.randint(min_lines, max_lines)
    cls = f"Service{idx}"
    out = [
        "using System;",
        "using System.Collections.Generic;",
        "",
        f"// Auto-generated TCF file #{idx} (TCF methods only; helpers live elsewhere).",
        f"namespace {NS}",
        "{",
        f"    public class {cls}",
        "    {",
    ]
    midx = 0
    prev_tcf: str | None = None
    while len(out) < target:
        name = f"{PREFIX}_Svc{idx}_Op{midx}"
        caller_label = f"{cls}.{name}"
        out.append(f"        // TCF entry point #{midx}")
        if rng.random() < 0.35:
            out.append("        /* multi-line note")
            out.append("           describing the routine */")
        out.append(f"        public int {name}(int n)")
        out.append("        {")
        out.append("            var acc = new List<int>();")
        out.append("            acc.Add(n);                 // library List.Add -> NOT a helper")
        counters["library_calls"] += 1
        # branches -> complexity
        for b in range(rng.randint(0, 3)):
            if rng.random() < 0.5:
                out.append(f"            if (n > {b} || n < -{b})   // if + ||")
                out.append("            {")
                out.append(f"                acc.Add(n - {b});")
                out.append("            }")
            else:
                out.append(f"            for (int i = 0; i < {b + 1}; i++)")
                out.append("            {")
                out.append(f"                acc.Add(i * {b + 1}); // inline")
                out.append("            }")
        # cross-file helper calls
        if helper_pool:
            for _ in range(rng.randint(1, 3)):
                full = rng.choice(helper_pool)
                hcls, hmeth = full.split(".")
                out.append(f"            acc.Add({hcls}.{hmeth}(n));   // cross-file project helper")
                counters["helpers_called"].setdefault(full, set()).add(caller_label)
        # occasionally an TCF->TCF call (must be IGNORED as a helper edge)
        if prev_tcf is not None and rng.random() < 0.3:
            out.append(f"            acc.Add({prev_tcf}(n - 1));  // TCF->TCF, must be ignored")
            counters["tcf_to_tcf"] += 1
        out.append("            int total = 0;")
        out.append("            foreach (var v in acc) { total += v; }")
        out.append("            return total;")
        out.append("        }")
        out.append("")
        counters["tcf"] += 1
        prev_tcf = name
        midx += 1
    out.append("    }")
    out.append("}")
    return "\n".join(out) + "\n"


def gen_cpp_file(rng: random.Random, idx: int, min_lines: int, max_lines: int) -> str:
    target = rng.randint(min_lines, max_lines)
    out = ["// Auto-generated C++ stress file", "#include <vector>", "#include <string>", ""]
    fn = 0
    while len(out) < target:
        out.append(f"// function {fn}")
        out.append(f"int compute_{fn}(int a, int b) {{")
        out.append('    std::string s = R"(raw // not a comment /* nor this */)";')
        out.append("    int r = a + b; // inline comment")
        if rng.random() < 0.5:
            out.append("    /* block")
            out.append("       comment */")
        out.append("    return r;")
        out.append("}")
        out.append("")
        fn += 1
    return "\n".join(out) + "\n"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("outdir")
    ap.add_argument("--tcf-files", type=int, default=12)
    ap.add_argument("--helper-files", type=int, default=6)
    ap.add_argument("--min-lines", type=int, default=5000)
    ap.add_argument("--max-lines", type=int, default=10000)
    ap.add_argument("--cpp", type=int, default=2)
    ap.add_argument("--seed", type=int, default=42)
    args = ap.parse_args()

    rng = random.Random(args.seed)
    out = Path(args.outdir)
    out.mkdir(parents=True, exist_ok=True)

    counters = {"tcf": 0, "library_calls": 0, "tcf_to_tcf": 0, "helpers_called": {}}
    total_lines = 0

    # 1) Helper files first, so TCF files can call into them.
    helper_pool: list[str] = []
    defined_helpers = 0
    for i in range(args.helper_files):
        text, names = gen_helper_file(rng, i, args.min_lines, args.max_lines)
        helper_pool.extend(names)
        defined_helpers += len(names)
        path = out / f"Helpers{i}.cs"
        path.write_text(text, encoding="utf-8")
        n = text.count("\n"); total_lines += n
        print(f"  wrote {path.name:18} {n:>6} lines  ({len(names)} helper defs)")

    # 2) TCF files that call cross-file helpers.
    for i in range(args.tcf_files):
        text = gen_tcf_file(rng, i, args.min_lines, args.max_lines, helper_pool, counters)
        path = out / f"Service{i}.cs"
        path.write_text(text, encoding="utf-8")
        n = text.count("\n"); total_lines += n
        print(f"  wrote {path.name:18} {n:>6} lines")

    # 3) C/C++ files.
    for j in range(args.cpp):
        text = gen_cpp_file(rng, j, args.min_lines // 2, args.max_lines // 2)
        path = out / f"engine{j}.cpp"
        path.write_text(text, encoding="utf-8")
        n = text.count("\n"); total_lines += n
        print(f"  wrote {path.name:18} {n:>6} lines")

    used = {h for h, callers in counters["helpers_called"].items() if callers}
    print("\n=== GROUND TRUTH (from generator) ===")
    print(f"TCF files (TCF>0, Helpers=0)      : {args.tcf_files}")
    print(f"Helper files (TCF=0, Helpers>0)   : {args.helper_files}")
    print(f"C++ files                         : {args.cpp}")
    print(f"total lines (~)                   : {total_lines}")
    print(f"TCF methods                       : {counters['tcf']}")
    print(f"helper methods DEFINED            : {defined_helpers}")
    print(f"helper methods CALLED by TCF (=helpers): {len(used)}")
    print(f"helper defs NEVER called (NOT helpers) : {defined_helpers - len(used)}")
    print(f"library List.Add() sites (NOT helpers) : {counters['library_calls']}")
    print(f"TCF->TCF call sites (IGNORED)          : {counters['tcf_to_tcf']}")
    print(f"\nOutput folder: {out}")


if __name__ == "__main__":
    main()
