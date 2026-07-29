"""Drive a full analysis: scan, invoke the C# analyzer, and merge into a typed result."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .analyzer_bridge import run_analyzer
from .cpp_comments import find_comment_spans
from .filetypes import Language
from .line_metrics import CommentSpan, LineCounts, count, counts_from_flags, line_flags
from .models import (
    AnalysisResult,
    FileReport,
    HelperRef,
    HelperUsage,
    ProjectSummary,
    TcfMethod,
    UnusedDefinition,
    UnusedMethod,
)
from .scanner import ScanResult, SourceFile, scan, validate_target


class InvalidFolderError(ValueError):
    """Raised when the target folder is missing or not a directory."""


def analyze(folder: Path, analyzer_path: Path | None = None) -> AnalysisResult:
    """Scan *folder*, run the C# analyzer, and build the merged analysis result."""
    error = validate_target(folder)
    if error is not None:
        raise InvalidFolderError(error)

    scan_result = scan(folder)
    cs_files = [f for f in scan_result.files if f.kind.language is Language.CSHARP]
    response: dict[str, Any] = (
        run_analyzer(cs_files, analyzer_path) if cs_files else {"files": []}
    )
    return build_result(folder, scan_result, response)


def build_result(
    folder: Path, scan_result: ScanResult, analyzer_response: dict[str, Any]
) -> AnalysisResult:
    """Merge scan output, analyzer JSON, and line metrics into an :class:`AnalysisResult`.

    Pure (no I/O) so it can be unit-tested with synthetic analyzer responses.
    """
    warnings = list(scan_result.warnings)
    by_path = {fr.get("path"): fr for fr in analyzer_response.get("files", [])}

    def to_rel(path_str: str) -> str:
        path = Path(path_str)
        try:
            return str(path.relative_to(folder))
        except ValueError:
            return path_str

    # Pass 1: per-file counts/TCF names, plus global TCF methods and helper bookkeeping.
    per_file: list[tuple[SourceFile, LineCounts, list[str]]] = []
    tcf_methods: list[TcfMethod] = []
    helper_callers: dict[HelperRef, set[str]] = {}
    helpers_by_file: dict[str, set[HelperRef]] = {}
    all_non_tcf_methods: list[UnusedMethod] = []
    all_unused_definitions: list[UnusedDefinition] = []
    csharp_file_count = 0
    csharp_method_count = 0

    for sf in scan_result.files:
        if sf.kind.language is Language.CSHARP:
            csharp_file_count += 1
            counts, names, n_methods, non_tcf, unused_defs = _analyze_csharp(
                sf, by_path.get(str(sf.path)), warnings, tcf_methods,
                helper_callers, helpers_by_file, to_rel,
            )
            csharp_method_count += n_methods
            all_non_tcf_methods.extend(non_tcf)
            all_unused_definitions.extend(unused_defs)
            per_file.append((sf, counts, names))
        else:
            counts = count(sf.text, find_comment_spans(sf.text))
            per_file.append((sf, counts, []))

    # Pass 2: build file reports (helper_method_count now known per defining file).
    files = tuple(
        FileReport(
            rel_path=str(sf.rel_path),
            file_type=sf.kind.label,
            language=sf.kind.language,
            counts=counts,
            tcf_method_count=len(names),
            helper_method_count=len(helpers_by_file.get(str(sf.rel_path), ())),
            tcf_method_names=tuple(names),
        )
        for sf, counts, names in per_file
    )

    total_counts = LineCounts()
    for file_report in files:
        total_counts = total_counts + file_report.counts

    summary = ProjectSummary(
        file_count=len(files),
        counts=total_counts,
        csharp_file_count=csharp_file_count,
        csharp_method_count=csharp_method_count,
        tcf_method_count=len(tcf_methods),
        helper_method_count=len(helper_callers),
        unused_method_count=0, # Will be set below
        unused_definition_count=0, # Will be set below
    )

    helper_usage = tuple(
        HelperUsage(helper, tuple(sorted(callers)))
        for helper, callers in sorted(
            helper_callers.items(), key=lambda kv: (kv[0].name, kv[0].file)
        )
    )

    used_helper_set = set(helper_callers.keys())
    unused_methods = tuple(
        sorted(
            (m for m in all_non_tcf_methods if HelperRef(m.name, m.file) not in used_helper_set),
            key=lambda m: (m.name, m.file)
        )
    )

    summary = ProjectSummary(
        file_count=summary.file_count,
        counts=summary.counts,
        csharp_file_count=summary.csharp_file_count,
        csharp_method_count=summary.csharp_method_count,
        tcf_method_count=summary.tcf_method_count,
        helper_method_count=summary.helper_method_count,
        unused_method_count=len(unused_methods),
        unused_definition_count=len(all_unused_definitions),
    )

    return AnalysisResult(
        folder=str(folder),
        summary=summary,
        files=files,
        tcf_methods=tuple(tcf_methods),
        helper_usage=helper_usage,
        unused_methods=unused_methods,
        unused_definitions=tuple(all_unused_definitions),
        warnings=tuple(warnings),
    )


def _analyze_csharp(
    sf: SourceFile,
    file_result: dict[str, Any] | None,
    warnings: list[str],
    tcf_methods: list[TcfMethod],
    helper_callers: dict[HelperRef, set[str]],
    helpers_by_file: dict[str, set[HelperRef]],
    to_rel: Any,
) -> tuple[LineCounts, list[str], int, list[UnusedMethod], list[UnusedDefinition]]:
    """Process one C# file's analyzer result; returns (counts, tcf_names, method_count, non_tcf_methods, unused_defs)."""
    if file_result is None:
        warnings.append(f"{sf.rel_path}: not analyzed by the C# engine")
        return LineCounts(), [], 0, [], []

    if file_result.get("diagnostics", {}).get("hasErrors"):
        warnings.append(f"{sf.rel_path}: possible syntax errors; results may be partial")

    comments = [
        CommentSpan(c["startLine"], c["startCol"], c["endLine"], c["endCol"])
        for c in file_result.get("comments", [])
    ]
    flags = line_flags(sf.text, comments)
    file_counts = counts_from_flags(flags)

    methods = file_result.get("methods", [])
    tcf_names: list[str] = []
    non_tcf_methods: list[UnusedMethod] = []
    for method in methods:
        start, end = method["startLine"], method["endLine"]
        if not method.get("isTcf"):
            non_tcf_methods.append(
                UnusedMethod(
                    name=method["name"],
                    file=str(sf.rel_path),
                    start_line=start + 1,
                    end_line=end + 1,
                    cyclomatic_complexity=method.get("cyclomaticComplexity", 1),
                )
            )
            continue
        start, end = method["startLine"], method["endLine"]
        used = tuple(
            HelperRef(h["name"], to_rel(h["file"])) for h in method.get("usedHelpers", [])
        )
        tcf_names.append(method["name"])
        tcf_methods.append(
            TcfMethod(
                name=method["name"],
                file=str(sf.rel_path),
                start_line=start + 1,
                end_line=end + 1,
                counts=counts_from_flags(flags, start, end + 1),
                cyclomatic_complexity=method.get("cyclomaticComplexity", 1),
                used_helpers=used,
            )
        )
        for href in used:
            helper_callers.setdefault(href, set()).add(method["name"])
            helpers_by_file.setdefault(href.file, set()).add(href)

    unused_defs: list[UnusedDefinition] = []
    for ud in file_result.get("unusedDefinitions", []):
        unused_defs.append(
            UnusedDefinition(
                name=ud["name"],
                type=ud["type"],
                line=ud["line"],
                file=str(sf.rel_path),
            )
        )

    return file_counts, tcf_names, len(methods), non_tcf_methods, unused_defs
