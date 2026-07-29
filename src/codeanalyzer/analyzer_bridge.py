"""Locate and invoke the bundled C# (Roslyn) analyzer executable.

The Python side communicates with the analyzer over a simple stdin/stdout JSON contract,
so the .NET engine stays a self-contained black box that ships next to the app.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any

from .scanner import SourceFile

_TIMEOUT_SECONDS = 600


class AnalyzerError(RuntimeError):
    """Raised when the C# analyzer cannot be found, run, or produces invalid output."""


def _exe_name() -> str:
    return "analyzer.exe" if os.name == "nt" else "analyzer"


def _host_rid() -> str:
    if sys.platform.startswith("win"):
        return "win-x64"
    if sys.platform == "darwin":
        return "osx-x64"
    return "linux-x64"


def _find_repo_root(start: Path) -> Path | None:
    for parent in (start, *start.parents):
        if (parent / "pyproject.toml").is_file():
            return parent
    return None


def find_analyzer(explicit: Path | None = None) -> Path | None:
    """Return the path to the analyzer executable, or ``None`` if it cannot be found.

    Search order: explicit argument, ``CODEANALYZER_ANALYZER`` env var, the PyInstaller
    bundle, the installed package's ``_bundled`` dir, then the dev ``artifacts`` tree.
    """
    name = _exe_name()
    candidates: list[Path] = []
    if explicit is not None:
        candidates.append(explicit)
    env = os.environ.get("CODEANALYZER_ANALYZER")
    if env:
        candidates.append(Path(env))
    meipass = getattr(sys, "_MEIPASS", None)
    if meipass:
        candidates.append(Path(meipass) / "_bundled" / name)
    candidates.append(Path(__file__).resolve().parent / "_bundled" / name)
    repo = _find_repo_root(Path(__file__).resolve())
    if repo is not None:
        candidates.append(repo / "artifacts" / "analyzer" / _host_rid() / name)
    return next((c for c in candidates if c.is_file()), None)


def run_analyzer(
    cs_files: list[SourceFile], analyzer_path: Path | None = None
) -> dict[str, Any]:
    """Run the analyzer over the given C# files and return the parsed JSON response."""
    exe = find_analyzer(analyzer_path)
    if exe is None:
        raise AnalyzerError(
            "C# analyzer executable not found. Build it with scripts/build-analyzer.sh "
            "or set the CODEANALYZER_ANALYZER environment variable."
        )

    request = {
        "tcfPrefix": "TCF",
        "files": [{"path": str(f.path), "text": f.text} for f in cs_files],
    }
    try:
        proc = subprocess.run(
            [str(exe)],
            input=json.dumps(request),
            capture_output=True,
            text=True,
            encoding="utf-8",
            timeout=_TIMEOUT_SECONDS,
        )
    except (OSError, subprocess.SubprocessError) as err:
        raise AnalyzerError(f"Failed to run the C# analyzer: {err}") from err

    if proc.returncode != 0:
        detail = (proc.stderr or "").strip()[:500]
        raise AnalyzerError(f"C# analyzer exited with code {proc.returncode}: {detail}")

    try:
        result: dict[str, Any] = json.loads(proc.stdout)
    except json.JSONDecodeError as err:
        raise AnalyzerError(f"C# analyzer produced invalid JSON: {err}") from err
    return result
