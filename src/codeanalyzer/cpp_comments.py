"""A small, robust C/C++ comment lexer.

For C/C++ files we only need comment spans to drive line counting (no semantic analysis).
This scanner finds ``//`` and ``/* */`` comments while correctly skipping string and
character literals, C++11 raw strings, digit separators, and backslash-newline line
continuation (which can extend a ``//`` comment onto the next line).
"""

from __future__ import annotations

from .line_metrics import CommentSpan, offset_to_linecol, scan_lines

_RAW_PREFIXES = frozenset({"R", "LR", "uR", "UR", "u8R"})


def find_comment_spans(text: str) -> list[CommentSpan]:
    """Return the comment regions in *text* as 0-based (line, column) spans."""
    _, starts = scan_lines(text)
    spans: list[CommentSpan] = []
    for begin, end in _find_comment_offsets(text):
        sl, sc = offset_to_linecol(starts, begin)
        el, ec = offset_to_linecol(starts, end)
        spans.append(CommentSpan(sl, sc, el, ec))
    return spans


def _find_comment_offsets(text: str) -> list[tuple[int, int]]:
    offsets: list[tuple[int, int]] = []
    i, n = 0, len(text)
    while i < n:
        ch = text[i]
        if ch == '"':
            if i > 0 and text[i - 1] == "R" and _is_raw_prefix(text, i - 1):
                i = _skip_raw_string(text, i)
            else:
                i = _skip_quoted(text, i, '"')
        elif ch == "'":
            # A single quote between alphanumerics is a C++ digit separator (e.g. 1'000),
            # not a character literal.
            if i > 0 and (text[i - 1].isalnum() or text[i - 1] == "_"):
                i += 1
            else:
                i = _skip_quoted(text, i, "'")
        elif ch == "/" and i + 1 < n and text[i + 1] == "/":
            end = _skip_line_comment(text, i)
            offsets.append((i, end))
            i = end
        elif ch == "/" and i + 1 < n and text[i + 1] == "*":
            end = _skip_block_comment(text, i)
            offsets.append((i, end))
            i = end
        else:
            i += 1
    return offsets


def _skip_quoted(text: str, i: int, quote: str) -> int:
    """Skip a string/char literal starting at the opening *quote*; return the index after it."""
    n = len(text)
    i += 1
    while i < n:
        ch = text[i]
        if ch == "\\":
            i += 2  # escaped char (also handles backslash-newline continuation)
            continue
        if ch == quote:
            return i + 1
        i += 1
    return n


def _skip_line_comment(text: str, i: int) -> int:
    """Skip a ``//`` comment; return the offset of the terminating newline (exclusive)."""
    n = len(text)
    i += 2
    while i < n:
        ch = text[i]
        if ch == "\\":
            # Backslash-newline splices the line: the comment continues onto the next.
            if i + 1 < n and text[i + 1] == "\n":
                i += 2
            elif i + 1 < n and text[i + 1] == "\r":
                i += 3 if (i + 2 < n and text[i + 2] == "\n") else 2
            else:
                i += 1
            continue
        if ch in ("\n", "\r", chr(0x85), chr(0x2028), chr(0x2029)):
            return i
        i += 1
    return n


def _skip_block_comment(text: str, i: int) -> int:
    """Skip a ``/* */`` comment; return the offset just after ``*/`` (or end of text)."""
    end = text.find("*/", i + 2)
    return len(text) if end == -1 else end + 2


def _is_raw_prefix(text: str, r_index: int) -> bool:
    start = r_index
    while start - 1 >= 0 and (text[start - 1].isalnum() or text[start - 1] == "_"):
        start -= 1
    return text[start : r_index + 1] in _RAW_PREFIXES


def _skip_raw_string(text: str, i: int) -> int:
    """Skip a C++11 raw string ``R"delim( ... )delim"`` starting at the opening quote."""
    n = len(text)
    k = i + 1
    delim_start = k
    while k < n and text[k] != "(" and (k - delim_start) < 16 and text[k] not in ' \t\r\n\\")':
        k += 1
    if k >= n or text[k] != "(":
        return _skip_quoted(text, i, '"')  # malformed; treat as a normal string
    delimiter = text[delim_start:k]
    closing = ")" + delimiter + '"'
    end = text.find(closing, k + 1)
    return n if end == -1 else end + len(closing)
