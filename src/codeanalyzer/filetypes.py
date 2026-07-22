"""Supported source-file extensions and their classification."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from pathlib import Path


class Language(str, Enum):
    """The analysis category a file belongs to."""

    CSHARP = "csharp"
    C_CPP = "c_cpp"


@dataclass(frozen=True)
class FileKind:
    """A supported file type: a human-readable label and its analysis language."""

    label: str
    language: Language


# Extension -> FileKind. Extensions are matched case-insensitively.
_EXTENSION_MAP: dict[str, FileKind] = {
    ".cs": FileKind("C#", Language.CSHARP),
    ".c": FileKind("C", Language.C_CPP),
    ".cpp": FileKind("C++", Language.C_CPP),
    ".cc": FileKind("C++", Language.C_CPP),
    ".cxx": FileKind("C++", Language.C_CPP),
    ".h": FileKind("C/C++ Header", Language.C_CPP),
    ".hpp": FileKind("C++ Header", Language.C_CPP),
    ".hh": FileKind("C++ Header", Language.C_CPP),
}

SUPPORTED_EXTENSIONS: frozenset[str] = frozenset(_EXTENSION_MAP)


def classify(path: Path) -> FileKind | None:
    """Return the :class:`FileKind` for a path by extension, or ``None`` if unsupported."""
    return _EXTENSION_MAP.get(path.suffix.lower())
