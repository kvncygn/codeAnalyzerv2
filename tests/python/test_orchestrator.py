from __future__ import annotations

from pathlib import Path
from typing import Any

import pytest

from codeanalyzer.analyzer_bridge import find_analyzer
from codeanalyzer.orchestrator import analyze, build_result
from codeanalyzer.scanner import scan

S_CS = (
    "// header\n"
    "class S {\n"
    "  int Add(int a, int b) { return a + b; }\n"
    "  int TCF_M(int n) { return Add(n, 1); }\n"
    "}\n"
)
U_C = "// c\nint main(){}\n"


def _write_sample(tmp_path: Path) -> None:
    (tmp_path / "S.cs").write_text(S_CS, encoding="utf-8")
    (tmp_path / "u.c").write_text(U_C, encoding="utf-8")


def _fake_response(tmp_path: Path) -> dict[str, Any]:
    return {
        "files": [
            {
                "path": str(tmp_path / "S.cs"),
                "ok": True,
                "diagnostics": {"hasErrors": False, "errorCount": 0},
                "comments": [{"startLine": 0, "startCol": 0, "endLine": 0, "endCol": 9}],
                "methods": [
                    {
                        "name": "Add",
                        "isTcf": False,
                        "startLine": 2,
                        "endLine": 2,
                        "cyclomaticComplexity": 1,
                        "usedHelpers": [],
                    },
                    {
                        "name": "TCF_M",
                        "isTcf": True,
                        "startLine": 3,
                        "endLine": 3,
                        "cyclomaticComplexity": 1,
                        "usedHelpers": [{"name": "Add", "file": str(tmp_path / "S.cs")}],
                    },
                ],
            }
        ]
    }


def test_build_result_merges_metrics_and_helpers(tmp_path: Path) -> None:
    _write_sample(tmp_path)
    result = build_result(tmp_path, "TCF", scan(tmp_path), _fake_response(tmp_path))

    s = result.summary
    assert s.file_count == 2
    assert s.csharp_file_count == 1
    assert s.csharp_method_count == 2
    assert s.tcf_method_count == 1
    assert s.helper_method_count == 1

    cs = next(f for f in result.files if f.rel_path == "S.cs")
    assert cs.tcf_method_count == 1
    assert cs.helper_method_count == 1
    assert cs.tcf_method_names == ("TCF_M",)

    c_file = next(f for f in result.files if f.rel_path == "u.c")
    assert c_file.file_type == "C"
    assert c_file.tcf_method_count == 0 and c_file.helper_method_count == 0
    assert c_file.counts.total == 2 and c_file.counts.code == 1 and c_file.counts.comment == 1

    method = result.tcf_methods[0]
    assert method.name == "TCF_M"
    assert (method.start_line, method.end_line) == (4, 4)  # 1-based
    assert [h.name for h in method.used_helpers] == ["Add"]

    assert len(result.helper_usage) == 1
    usage = result.helper_usage[0]
    assert usage.helper.name == "Add"
    assert usage.helper.file == "S.cs"
    assert usage.callers == ("TCF_M",)


@pytest.mark.skipif(find_analyzer() is None, reason="analyzer executable not built")
def test_analyze_end_to_end_with_real_analyzer(tmp_path: Path) -> None:
    _write_sample(tmp_path)
    result = analyze(tmp_path, "TCF")

    assert result.summary.tcf_method_count == 1
    assert result.summary.helper_method_count == 1
    assert result.summary.csharp_method_count == 2
    assert result.helper_usage[0].helper.name == "Add"
    assert result.helper_usage[0].callers == ("TCF_M",)
