from __future__ import annotations

from codeanalyzer.cpp_comments import find_comment_spans


def spans(text: str) -> list[tuple[int, int, int, int]]:
    return [(s.start_line, s.start_col, s.end_line, s.end_col) for s in find_comment_spans(text)]


def test_finds_line_and_block_comments() -> None:
    result = find_comment_spans("int x; // c\n/* b */ y;")
    assert len(result) == 2


def test_no_comment_inside_string() -> None:
    assert find_comment_spans('const char* s = "// not /* a */ comment";') == []


def test_no_comment_inside_char_literal() -> None:
    assert find_comment_spans("char c = '/';") == []


def test_digit_separator_is_not_a_char_literal() -> None:
    # 1'000'000 uses ' as a C++14 digit separator; the // after it is still a comment.
    result = find_comment_spans("int big = 1'000'000; // a million")
    assert len(result) == 1
    assert result[0].start_line == 0


def test_backslash_newline_continues_line_comment() -> None:
    result = find_comment_spans("// a \\\nstill comment\ncode();")
    assert len(result) == 1
    assert result[0].start_line == 0
    assert result[0].end_line == 1


def test_raw_string_hides_comment_markers() -> None:
    assert find_comment_spans('auto s = R"(// not a comment /* x */)";') == []


def test_block_comment_spans_multiple_lines() -> None:
    result = find_comment_spans("a;\n/* x\n   y */\nb;")
    assert len(result) == 1
    assert result[0].start_line == 1
    assert result[0].end_line == 2


def test_unterminated_block_comment_runs_to_eof() -> None:
    result = find_comment_spans("code; /* never closed")
    assert len(result) == 1
    assert result[0].start_line == 0
