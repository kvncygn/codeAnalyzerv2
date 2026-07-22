from __future__ import annotations

from codeanalyzer.filetypes import Language
from codeanalyzer.line_metrics import LineCounts
from codeanalyzer.models import (
    AnalysisResult,
    FileReport,
    HelperRef,
    HelperUsage,
    ProjectSummary,
    TcfMethod,
    UnusedDefinition,
    UnusedMethod,
)
from codeanalyzer.report import build_source_tree, render_text


def _sample() -> AnalysisResult:
    files = (
        FileReport("Program.cs", "C#", Language.CSHARP, LineCounts(10, 6, 3, 1, 1), 2, 0,
                   ("TCF_Init", "TCF_Run")),
        FileReport("util/Helpers.cs", "C#", Language.CSHARP, LineCounts(20, 15, 3, 0, 2), 0, 1, ()),
        FileReport("u.c", "C", Language.C_CPP, LineCounts(8, 5, 2, 0, 1), 0, 0, ()),
    )
    methods = (
        TcfMethod("TCF_Init", "Program.cs", 1, 4, LineCounts(4, 3, 1, 0, 0), 2,
                  (HelperRef("Load", "util/Helpers.cs"),)),
        TcfMethod("TCF_Run", "Program.cs", 5, 9, LineCounts(5, 3, 1, 1, 0), 3, ()),
    )
    usage = (HelperUsage(HelperRef("Load", "util/Helpers.cs"), ("TCF_Init",)),)
    unused = (UnusedMethod("Orphan", "util/Helpers.cs", 20, 25, 1),)
    unused_defs = (UnusedDefinition("MAX_SIZE", "int", 10, "util/Helpers.cs"),)
    summary = ProjectSummary(3, LineCounts(38, 26, 8, 1, 4), 2, 5, 2, 1, 1, 1)
    return AnalysisResult("/proj", "TCF", summary, files, methods, usage, unused, unused_defs, ("u.c: a warning",))


def test_sections_are_in_required_order() -> None:
    text = render_text(_sample())
    order = [
        "=== Project Summary ===",
        "=== File Summary ===",
        "=== Source Tree ===",
        "=== TCF Method Details ===",
        "=== Helper Usage Summary ===",
        "=== Unused Methods ===",
        "=== Unused Definitions ===",
    ]
    positions = [text.index(h) for h in order]
    assert positions == sorted(positions)


def test_source_tree_format() -> None:
    lines = build_source_tree(_sample().files)
    text = "\n".join(lines)
    assert lines[0] == "[ROOT]"
    assert "+-- util/" in text
    assert "+-- Program.cs (10 lines, TCF=2, Helpers=0)" in text
    assert "+-- TCF_Init" in text
    assert "+-- Helpers.cs (20 lines, TCF=0, Helpers=1)" in text


def test_helper_usage_and_warnings() -> None:
    text = render_text(_sample())
    assert "Load  (util/Helpers.cs)  <- TCF_Init" in text
    assert "=== Warnings ===" in text
    assert "- u.c: a warning" in text


def test_tcf_details_include_ratio_and_complexity() -> None:
    text = render_text(_sample())
    assert "TCF_Init  (Program.cs:1-4)" in text
    assert "comment_ratio=0.25 complexity=2" in text
    assert "helpers: Load" in text
