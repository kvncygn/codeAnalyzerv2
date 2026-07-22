"""End-to-end test of the real Python <-> Roslyn seam.

Unlike the orchestrator unit tests (which feed synthetic analyzer JSON), this runs the
actual bundled analyzer over the committed ``examples/edge-cases`` folder and checks the
ground truth documented in ``examples/README.md``. Skipped when the analyzer binary has
not been built (e.g. a fresh clone without ``scripts/build-analyzer.sh``).
"""

from __future__ import annotations

from pathlib import Path

import pytest

from codeanalyzer.analyzer_bridge import find_analyzer
from codeanalyzer.orchestrator import analyze

EXAMPLES = Path(__file__).resolve().parents[2] / "examples" / "edge-cases"

pytestmark = pytest.mark.skipif(
    find_analyzer() is None or not EXAMPLES.is_dir(),
    reason="analyzer executable not built, or examples/edge-cases missing",
)


@pytest.fixture(scope="module")
def result():  # type: ignore[no-untyped-def]
    return analyze(EXAMPLES, "TCF")


def test_helpers_resolved_semantically(result) -> None:  # type: ignore[no-untyped-def]
    callers = {u.helper.name: set(u.callers) for u in result.helper_usage}

    # Project method called by two TCF methods -> a helper with both callers.
    assert callers.get("CalcTotal") == {"TCF_ProcessOrder", "TCF_Validate"}
    assert "ApplyRush" in callers
    assert "Log" in callers


def test_non_helpers_are_excluded(result) -> None:  # type: ignore[no-untyped-def]
    names = {u.helper.name for u in result.helper_usage}
    assert "Unused" not in names          # never called by an TCF method
    assert "Add" not in names             # library List<T>.Add, not a project helper
    assert "WriteLine" not in names       # Console.WriteLine, library
    assert "TCF_ProcessOrder" not in names  # TCF->TCF call is ignored, not a helper


def test_cpp_files_have_zero_method_counts(result) -> None:  # type: ignore[no-untyped-def]
    cpp = [f for f in result.files if f.language.name != "CSHARP"]
    assert cpp, "expected the C/C++ sample files to be present"
    for f in cpp:
        assert f.tcf_method_count == 0
        assert f.helper_method_count == 0


def test_syntax_error_warns_but_does_not_crash(result) -> None:  # type: ignore[no-untyped-def]
    # Broken.cs has a deliberate syntax error; analysis still completes for the rest.
    assert any("Broken.cs" in w for w in result.warnings)
    assert result.summary.tcf_method_count >= 2  # Orders.cs methods still analyzed
