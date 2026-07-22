"""Recursively scan a folder for supported source files and decode them robustly.

The scanner is the single point that reads files from disk. It decodes bytes to text with
an encoding-fallback chain (so a single bad file never crashes the run) and records
understandable warnings. The decoded text is what the rest of the pipeline operates on.
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path

from .filetypes import FileKind, classify


@dataclass(frozen=True)
class SourceFile:
    """A decoded source file discovered under the analyzed folder."""

    path: Path
    rel_path: Path
    kind: FileKind
    text: str


@dataclass
class ScanResult:
    """The outcome of a scan: the decoded files plus any non-fatal warnings."""

    files: list[SourceFile] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)


def validate_target(folder: Path) -> str | None:
    """Return a human-readable error if *folder* cannot be analyzed, else ``None``."""
    if not folder.exists():
        return f"Folder does not exist: {folder}"
    if not folder.is_dir():
        return f"Path is not a folder: {folder}"
    return None


def decode_bytes(data: bytes) -> tuple[str, str | None]:
    """Decode source *data* with a robust fallback chain.

    Returns ``(text, warning)`` where ``warning`` is ``None`` on a clean decode and a
    short explanation when a lossy or non-UTF-8 fallback was used.
    """
    if data.startswith(b"\xef\xbb\xbf"):
        return data.decode("utf-8-sig"), None
    if data[:2] in (b"\xff\xfe", b"\xfe\xff"):
        try:
            return data.decode("utf-16"), None
        except UnicodeDecodeError:
            pass
    try:
        return data.decode("utf-8"), None
    except UnicodeDecodeError:
        pass
    try:
        return data.decode("cp1252"), "not valid UTF-8; decoded as cp1252"
    except UnicodeDecodeError:
        pass
    return (
        data.decode("utf-8", errors="replace"),
        "encoding errors; decoded with replacement characters",
    )


def scan(folder: Path) -> ScanResult:
    """Recursively find supported source files under *folder* and decode them.

    Traversal and per-file read errors are collected as warnings rather than raised, so
    the analysis can proceed on whatever files are readable.
    """
    result = ScanResult()

    def on_error(err: OSError) -> None:
        target = getattr(err, "filename", None) or folder
        result.warnings.append(f"{target}: cannot access ({err.strerror or err})")

    for dirpath, dirnames, filenames in os.walk(folder, onerror=on_error):
        dirnames.sort()
        for filename in sorted(filenames):
            path = Path(dirpath) / filename
            kind = classify(path)
            if kind is None:
                continue
            try:
                data = path.read_bytes()
            except OSError as err:
                result.warnings.append(f"{path}: could not read ({err.strerror or err})")
                continue
            text, note = decode_bytes(data)
            if note is not None:
                result.warnings.append(f"{path}: {note}")
            result.files.append(
                SourceFile(path=path, rel_path=path.relative_to(folder), kind=kind, text=text)
            )

    return result
