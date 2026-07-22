"""Exact line-counting rules (REQUIREMENTS.md), applied uniformly to all languages.

Counting is driven by *comment spans* (from the Roslyn analyzer for C#, from the C/C++
lexer for C/C++). Per physical line we decide ``has_code`` / ``has_comment`` and apply:

    blank            -> blank += 1
    code only        -> code += 1
    comment only     -> comment += 1
    code + comment   -> code += 1, comment += 1, inline_comment += 1

Coordinates are 0-based ``(line, column)`` where column is a character index into the
line. (Roslyn reports UTF-16 columns; these equal code-point columns for the Basic
Multilingual Plane, i.e. all realistic source — see docs/architecture.md.)
"""

from __future__ import annotations

import bisect
from collections.abc import Sequence
from dataclasses import dataclass

# Non-CR line breaks recognized for splitting (CR / CRLF are handled separately).
# Matches Roslyn's set: LF, NEL (U+0085), LS (U+2028), PS (U+2029).
_BREAKS = ("\n", chr(0x85), chr(0x2028), chr(0x2029))


@dataclass(frozen=True)
class CommentSpan:
    """A comment region in 0-based (line, column) coordinates; end column is exclusive."""

    start_line: int
    start_col: int
    end_line: int
    end_col: int


@dataclass(frozen=True)
class LineCounts:
    """Line tallies for a file or a method."""

    total: int = 0
    code: int = 0
    comment: int = 0
    inline_comment: int = 0
    blank: int = 0

    def __add__(self, other: LineCounts) -> LineCounts:
        return LineCounts(
            self.total + other.total,
            self.code + other.code,
            self.comment + other.comment,
            self.inline_comment + other.inline_comment,
            self.blank + other.blank,
        )

    @property
    def comment_ratio(self) -> float:
        return self.comment / self.total if self.total else 0.0


def scan_lines(text: str) -> tuple[list[str], list[int]]:
    """Split *text* into physical lines and their start offsets.

    A trailing line break does not create an extra empty line. The returned ``starts``
    list may contain a final phantom offset (== len(text)) used only for offset mapping.
    """
    lines: list[str] = []
    starts: list[int] = [0]
    i, n, seg = 0, len(text), 0
    while i < n:
        ch = text[i]
        if ch == "\r":
            lines.append(text[seg:i])
            i = i + 2 if (i + 1 < n and text[i + 1] == "\n") else i + 1
            seg = i
            starts.append(i)
        elif ch in _BREAKS:
            lines.append(text[seg:i])
            i += 1
            seg = i
            starts.append(i)
        else:
            i += 1
    if seg < n:
        lines.append(text[seg:n])
    return lines, starts


def split_lines(text: str) -> list[str]:
    return scan_lines(text)[0]


def offset_to_linecol(starts: Sequence[int], offset: int) -> tuple[int, int]:
    """Map an absolute character offset to 0-based (line, column)."""
    line = max(0, bisect.bisect_right(starts, offset) - 1)
    return line, offset - starts[line]


def _has_code(content: str, intervals: list[tuple[int, int]]) -> bool:
    """True if the line has any non-whitespace character outside the comment intervals."""
    if not intervals:
        return any(not ch.isspace() for ch in content)
    covered = bytearray(len(content))
    for start, end in intervals:
        for j in range(max(0, start), min(len(content), end)):
            covered[j] = 1
    return any(covered[j] == 0 and not ch.isspace() for j, ch in enumerate(content))


def line_flags(text: str, comments: Sequence[CommentSpan]) -> list[tuple[bool, bool]]:
    """Return ``(has_code, has_comment)`` for each physical line of *text*."""
    lines, _ = scan_lines(text)
    n = len(lines)
    intervals: list[list[tuple[int, int]]] = [[] for _ in range(n)]
    for c in comments:
        first = max(0, c.start_line)
        last = min(n - 1, c.end_line)
        for ln in range(first, last + 1):
            start = c.start_col if ln == c.start_line else 0
            end = c.end_col if ln == c.end_line else len(lines[ln])
            if end > start:
                intervals[ln].append((start, end))
    return [(_has_code(line, intervals[i]), bool(intervals[i])) for i, line in enumerate(lines)]


def counts_from_flags(
    flags: Sequence[tuple[bool, bool]], start: int = 0, end: int | None = None
) -> LineCounts:
    """Tally line counts over ``flags[start:end]`` (end exclusive; default = all)."""
    if end is None:
        end = len(flags)
    total = code = comment = inline = blank = 0
    for has_code, has_comment in flags[start:end]:
        total += 1
        if has_code and has_comment:
            code += 1
            comment += 1
            inline += 1
        elif has_code:
            code += 1
        elif has_comment:
            comment += 1
        else:
            blank += 1
    return LineCounts(total, code, comment, inline, blank)


def count(text: str, comments: Sequence[CommentSpan]) -> LineCounts:
    """Convenience: full-file line counts for *text* given its comment spans."""
    return counts_from_flags(line_flags(text, comments))
