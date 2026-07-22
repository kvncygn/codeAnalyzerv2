from __future__ import annotations

from codeanalyzer.cpp_comments import find_comment_spans
from codeanalyzer.line_metrics import CommentSpan, LineCounts, count, split_lines


def lc(text: str) -> LineCounts:
    """Count lines using comment spans found by the C/C++ lexer."""
    return count(text, find_comment_spans(text))


def test_code_only_line() -> None:
    assert lc("int x = 5;") == LineCounts(total=1, code=1, comment=0, inline_comment=0, blank=0)


def test_comment_only_line() -> None:
    assert lc("// hello") == LineCounts(1, 0, 1, 0, 0)


def test_blank_line() -> None:
    assert lc("   \t ") == LineCounts(1, 0, 0, 0, 1)


def test_inline_comment_line() -> None:
    # The canonical REQUIREMENTS.md example: counts as both code and comment (+inline).
    assert lc("int x = 5; // comment") == LineCounts(1, 1, 1, 1, 0)


def test_string_with_comment_markers_stays_code() -> None:
    assert lc('s = "http://x /* y */ // z";') == LineCounts(1, 1, 0, 0, 0)


def test_multiline_block_comment() -> None:
    text = "a();\n/* one\n   two */ b();\n"
    # line0 code; line1 comment-only; line2 comment + trailing code -> inline
    assert lc(text) == LineCounts(total=3, code=2, comment=2, inline_comment=1, blank=0)


def test_trailing_newline_does_not_add_blank_line() -> None:
    assert lc("a;\nb;\n").total == 2
    assert split_lines("a;\nb;\n") == ["a;", "b;"]


def test_crlf_is_one_line() -> None:
    assert lc("a; // c\r\nb;\r\n") == LineCounts(2, 2, 1, 1, 0)


def test_empty_file_has_zero_lines() -> None:
    assert lc("") == LineCounts(0, 0, 0, 0, 0)


def test_counts_with_explicit_spans() -> None:
    # "x // y" -> code 'x' + comment '// y' on one line.
    assert count("x // y\nz\n", [CommentSpan(0, 2, 0, 6)]) == LineCounts(2, 2, 1, 1, 0)


def test_comment_ratio() -> None:
    counts = lc("// a\ncode;\n// b\n")
    assert counts.total == 3
    assert counts.comment_ratio == 2 / 3
