import os
import sys
import pytest
from pathlib import Path

# Thwart any import errors by dynamically adding src to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "src"))

from codeanalyzer.orchestrator import analyze, analyze_dev
from codeanalyzer.html_analyzer import analyze_html_reports

@pytest.fixture
def chaos_folder(tmp_path):
    """
    Creates an extremely hostile environment for the analyzers.
    Includes malicious files, deeply nested directories, corrupted data, and permission issues.
    """
    
    # 1. Extreme Directory Nesting (15 levels to push path traversal but stay within Win32 limits)
    deep_path = tmp_path
    for i in range(15):
        deep_path = deep_path / f"nested_{i}"
    deep_path.mkdir(parents=True)
    
    # Deep nested valid file
    deep_html = deep_path / "TC_SCN_TCF_Deep_RC1.html"
    deep_html.write_text("<html><th>Number of Total Steps</th><td><b>10</b></td></html>")
    
    # 2. Poisoned Binary HTML (Completely corrupt encoding)
    poisoned_html = tmp_path / "TC_SCN_TCF_Poison_RC1.html"
    poisoned_html.write_bytes(b"<html><td>FAILED (INCOMPLETE)</td>\xff\x00\xfa" * 1000)
    
    # 3. Giant HTML with regex killer (100,000 matches)
    giant_html = tmp_path / "TC_SCN_TCF_Giant_RC1.html"
    giant_content = "<th>Number of Total Steps</th><td>100</td>\n"
    giant_content += "<td>FAILED (INCOMPLETE)</td>\n" * 100000
    giant_html.write_text(giant_content)
    
    # 4. Broken C Code (Missing braces, crazy tokens)
    broken_c = tmp_path / "broken.c"
    broken_c.write_text("void broken() { \n int x = 5;\n if(1) { \n !!!@@@### \n")
    
    # 5. Giant C File (10,000 unclosed braces)
    giant_c = tmp_path / "giant.c"
    giant_c.write_text("void giant() {\n" + "{\n" * 10000)
    
    # 6. Locked File (Remove read permissions)
    locked_c = tmp_path / "locked.c"
    locked_c.write_text("void secret() {}")
    os.chmod(locked_c, 0o000)
    
    # 7. Weird UTF-8 Emoji/Unicode Path
    weird_html = tmp_path / "TC_SCN_TCF_🔥Emoji_Test_🚀_RC1.html"
    weird_html.write_text("<html><th>Number of Failed Steps</th><td>0</td></html>", encoding="utf-8")
    
    # 8. Malformed Extension Tricks
    fake_cs = tmp_path / "fake.cs"
    fake_cs.write_text("This is not C# code, it is just a text file. class Program {}")

    # 9. No-Extension file
    no_ext = tmp_path / "TC_SCN_TCF_NoExt_RC1"
    no_ext.write_text("<html></html>")
    
    # 10. Massive 0-byte (Empty) Files
    empty_html = tmp_path / "TC_SCN_TCF_Empty_RC1.html"
    empty_html.touch()
    
    empty_cs = tmp_path / "empty.cs"
    empty_cs.touch()

    return tmp_path

def test_html_analyzer_chaos(chaos_folder):
    """Ensure HTML Analyzer does not crash under extreme conditions."""
    try:
        result = analyze_html_reports(chaos_folder)
        # Should successfully return a result object even if it ignored most garbage
        assert result is not None
        assert isinstance(result.virtual_folders, list)
    except Exception as e:
        pytest.fail(f"HTML Analyzer CRASHED during Chaos Test: {e}")

def test_dev_analyzer_chaos(chaos_folder):
    """Ensure Developer Analyzer (C/C++) does not crash under extreme conditions."""
    try:
        result = analyze_dev(chaos_folder)
        assert result is not None
        assert hasattr(result, "methods")
    except Exception as e:
        pytest.fail(f"Dev Analyzer CRASHED during Chaos Test: {e}")

def test_test_analyzer_chaos(chaos_folder):
    """Ensure C# Test Analyzer does not crash under extreme conditions."""
    try:
        result = analyze(chaos_folder)
        assert result is not None
        assert hasattr(result, "files")
    except Exception as e:
        pytest.fail(f"C# Test Analyzer CRASHED during Chaos Test: {e}")
