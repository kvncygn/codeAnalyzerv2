"""Render an :class:`AnalysisResult` as a plain-text report in the required order:

1. Project Summary   2. File Summary   3. Source Tree   4. TCF Method Details
5. Helper Usage Summary   (+ a Warnings panel when there is anything to report)
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .models import AnalysisResult, FileReport


def render_text(result: AnalysisResult) -> str:
    """Render the full analysis as a plain-text report (sections in the exact order)."""
    out: list[str] = []
    _project_summary(result, out)
    out.append("")
    _file_summary(result, out)
    out.append("")
    out.append("=== Source Tree ===")
    out.extend(build_source_tree(result.files))
    out.append("")
    _tcf_details(result, out)
    out.append("")
    _helper_usage(result, out)
    out.append("")
    _unused_methods(result, out)
    if result.warnings:
        out.append("")
        out.append("=== Warnings ===")
        out.extend(f"- {w}" for w in result.warnings)
    return "\n".join(out) + "\n"


def render_json(result: AnalysisResult) -> dict[str, Any]:
    """Render the full analysis as a JSON-serializable dict (for the whole-result export).

    Mirrors the on-screen report so downstream tooling can consume it without scraping.
    """
    s = result.summary
    c = s.counts

    def counts(lc: Any) -> dict[str, Any]:
        return {
            "total": lc.total,
            "code": lc.code,
            "comment": lc.comment,
            "inline_comment": lc.inline_comment,
            "blank": lc.blank,
            "comment_ratio": round(lc.comment_ratio, 4),
        }

    return {
        "folder": result.folder,
        "tcf_prefix": result.tcf_prefix,
        "summary": {
            "file_count": s.file_count,
            **counts(c),
            "csharp_file_count": s.csharp_file_count,
            "csharp_method_count": s.csharp_method_count,
            "tcf_method_count": s.tcf_method_count,
            "helper_method_count": s.helper_method_count,
            "unused_method_count": s.unused_method_count,
        },
        "files": [
            {
                "rel_path": f.rel_path,
                "file_type": f.file_type,
                "counts": counts(f.counts),
                "tcf_method_count": f.tcf_method_count,
                "helper_method_count": f.helper_method_count,
                "tcf_method_names": list(f.tcf_method_names),
            }
            for f in result.files
        ],
        "tcf_methods": [
            {
                "name": m.name,
                "file": m.file,
                "start_line": m.start_line,
                "end_line": m.end_line,
                "counts": counts(m.counts),
                "cyclomatic_complexity": m.cyclomatic_complexity,
                "used_helpers": [h.name for h in m.used_helpers],
            }
            for m in sorted(result.tcf_methods, key=lambda hm: (hm.file, hm.start_line))
        ],
        "helper_usage": [
            {"name": u.helper.name, "file": u.helper.file, "callers": list(u.callers)}
            for u in result.helper_usage
        ],
        "unused_methods": [
            {
                "name": m.name,
                "file": m.file,
                "start_line": m.start_line,
                "end_line": m.end_line,
                "cyclomatic_complexity": m.cyclomatic_complexity,
            }
            for m in result.unused_methods
        ],
        "warnings": list(result.warnings),
    }


def _project_summary(result: AnalysisResult, out: list[str]) -> None:
    s = result.summary
    c = s.counts
    out.append("=== Project Summary ===")
    out.append(f"{'Folder':<18}: {result.folder}")
    out.append(f"{'TCF prefix':<18}: {result.tcf_prefix}")
    rows = (
        ("Source files", s.file_count),
        ("Total lines", c.total),
        ("Code lines", c.code),
        ("Comment lines", c.comment),
        ("Inline comments", c.inline_comment),
        ("Blank lines", c.blank),
        ("C# files", s.csharp_file_count),
        ("C# methods", s.csharp_method_count),
        ("TCF methods", s.tcf_method_count),
        ("Helper methods", s.helper_method_count),
        ("Unused methods", s.unused_method_count),
    )
    for label, value in rows:
        out.append(f"{label:<18}: {value}")


def _file_summary(result: AnalysisResult, out: list[str]) -> None:
    out.append("=== File Summary ===")
    if not result.files:
        out.append("(no supported source files found)")
        return
    out.append(
        f"{'Type':<14}{'Total':>7}{'Code':>7}{'Cmt':>7}{'Inl':>7}{'Blank':>7}"
        f"{'TCF':>5}{'Help':>6}  File"
    )
    for f in result.files:
        c = f.counts
        out.append(
            f"{f.file_type:<14}{c.total:>7}{c.code:>7}{c.comment:>7}{c.inline_comment:>7}"
            f"{c.blank:>7}{f.tcf_method_count:>5}{f.helper_method_count:>6}  {f.rel_path}"
        )


def build_source_tree(files: tuple[FileReport, ...]) -> list[str]:
    """Build the source tree lines: each file with its line/TCF/helper counts and, for
    C# files, the TCF methods nested underneath."""
    out = ["[ROOT]"]
    tree: dict[str, Any] = {}
    for fr in files:
        parts = Path(fr.rel_path).parts
        node = tree
        for part in parts[:-1]:
            node = node.setdefault(part, {})
        node[parts[-1]] = fr
    _render_tree(tree, 0, out)
    return out


def build_tree_data(files: tuple[FileReport, ...]) -> list[dict[str, Any]]:
    """Build a nested tree structure for HTML rendering.

    Each node is either a directory ``{"kind": "dir", "name", "children"}`` or a file
    ``{"kind": "file", "file": FileReport}``. Directories come first, then files, each
    group sorted alphabetically -- matching the plain-text tree ordering.
    """
    tree: dict[str, Any] = {}
    for fr in files:
        parts = Path(fr.rel_path).parts
        node = tree
        for part in parts[:-1]:
            node = node.setdefault(part, {})
        node[parts[-1]] = fr
    return _tree_nodes(tree)


def _tree_nodes(node: dict[str, Any]) -> list[dict[str, Any]]:
    nodes: list[dict[str, Any]] = []
    for name in sorted(node, key=lambda k: (not isinstance(node[k], dict), k)):
        value = node[name]
        if isinstance(value, dict):
            nodes.append({"kind": "dir", "name": name, "children": _tree_nodes(value)})
        else:
            nodes.append({"kind": "file", "file": value})
    return nodes


def _render_tree(node: dict[str, Any], depth: int, out: list[str]) -> None:
    indent = "    " * depth
    # Directories first, then files; alphabetical within each group.
    for name in sorted(node, key=lambda k: (not isinstance(node[k], dict), k)):
        value = node[name]
        if isinstance(value, dict):
            out.append(f"{indent}+-- {name}/")
            _render_tree(value, depth + 1, out)
        else:
            out.append(
                f"{indent}+-- {name} ({value.counts.total} lines, "
                f"TCF={value.tcf_method_count}, Helpers={value.helper_method_count})"
            )
            for method_name in value.tcf_method_names:
                out.append(f"{indent}    +-- {method_name}")


def _tcf_details(result: AnalysisResult, out: list[str]) -> None:
    out.append("=== TCF Method Details ===")
    if not result.tcf_methods:
        out.append("(no TCF methods found)")
        return
    for m in sorted(result.tcf_methods, key=lambda hm: (hm.file, hm.start_line)):
        c = m.counts
        out.append(f"{m.name}  ({m.file}:{m.start_line}-{m.end_line})")
        out.append(
            f"    total={c.total} code={c.code} comment={c.comment} "
            f"inline={c.inline_comment} blank={c.blank} "
            f"comment_ratio={c.comment_ratio:.2f} complexity={m.cyclomatic_complexity}"
        )
        helpers = ", ".join(h.name for h in m.used_helpers) or "(none)"
        out.append(f"    helpers: {helpers}")


def _helper_usage(result: AnalysisResult, out: list[str]) -> None:
    out.append("=== Helper Usage Summary ===")
    if not result.helper_usage:
        out.append("(no helpers used by TCF methods)")
        return
    for usage in result.helper_usage:
        out.append(f"{usage.helper.name}  ({usage.helper.file})  <- {', '.join(usage.callers)}")


def _unused_methods(result: AnalysisResult, out: list[str]) -> None:
    out.append("=== Unused Methods ===")
    if not result.unused_methods:
        out.append("(no unused methods found)")
        return
    for m in result.unused_methods:
        out.append(f"{m.name}  ({m.file}:{m.start_line}-{m.end_line})  complexity={m.cyclomatic_complexity}")
