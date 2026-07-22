from __future__ import annotations

from pathlib import Path

from codeanalyzer.filetypes import Language, classify
from codeanalyzer.scanner import decode_bytes, scan, validate_target


def test_classify_by_extension_is_case_insensitive() -> None:
    cs = classify(Path("A.CS"))
    assert cs is not None and cs.label == "C#" and cs.language is Language.CSHARP
    cpp = classify(Path("u.CPP"))
    assert cpp is not None and cpp.label == "C++"
    h = classify(Path("h.h"))
    assert h is not None and h.language is Language.C_CPP
    assert classify(Path("readme.txt")) is None


def test_validate_target(tmp_path: Path) -> None:
    assert validate_target(tmp_path) is None
    assert validate_target(tmp_path / "missing") is not None
    a_file = tmp_path / "x.cs"
    a_file.write_text("//", encoding="utf-8")
    assert validate_target(a_file) is not None  # a file is not a folder


def test_decode_utf8_and_bom() -> None:
    assert decode_bytes("café // x".encode()) == ("café // x", None)
    text, note = decode_bytes(b"\xef\xbb\xbfint x;")
    assert text == "int x;"
    assert note is None


def test_decode_cp1252_fallback_warns() -> None:
    # 0xE9 is 'é' in cp1252 but an invalid standalone UTF-8 byte.
    text, note = decode_bytes(b"int x; // caf\xe9")
    assert "café" in text
    assert note is not None and "cp1252" in note


def test_scan_finds_supported_and_skips_others(tmp_path: Path) -> None:
    (tmp_path / "a.cs").write_text("class A {}", encoding="utf-8")
    (tmp_path / "sub").mkdir()
    (tmp_path / "sub" / "b.cpp").write_text("int main(){}", encoding="utf-8")
    (tmp_path / "notes.txt").write_text("ignore me", encoding="utf-8")

    result = scan(tmp_path)

    assert sorted(f.kind.label for f in result.files) == ["C#", "C++"]
    assert sorted(str(f.rel_path) for f in result.files) == ["a.cs", str(Path("sub") / "b.cpp")]
    assert result.warnings == []


def test_scan_empty_folder_is_clean(tmp_path: Path) -> None:
    result = scan(tmp_path)
    assert result.files == []
    assert result.warnings == []
