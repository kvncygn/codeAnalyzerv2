# PyInstaller spec for codeAnalyzer (one-DIR).
#
# One-dir (a folder, not a single self-extracting .exe) is deliberate: it starts faster
# (no per-launch temp extraction) and trips antivirus heuristics far less often than a
# one-file build -- both matter on locked-down enterprise Windows machines.
#
# Bundles: the Python app, its Flask templates/static, and the self-contained C# analyzer
# binary staged into src/codeanalyzer/_bundled/ (analyzer on Linux/macOS, analyzer.exe on
# Windows). Build with:  pyinstaller packaging/codeanalyzer.spec
#
# Output: dist/codeanalyzer/  (run dist/codeanalyzer/codeanalyzer[.exe])
#
# ruff: noqa
from pathlib import Path

spec_dir = Path(SPECPATH)
repo = spec_dir.parent
src = repo / "src"
pkg = src / "codeanalyzer"
bundled = pkg / "_bundled"

datas = [
    (str(pkg / "web" / "templates"), "codeanalyzer/web/templates"),
    (str(pkg / "web" / "static"), "codeanalyzer/web/static"),
]
for analyzer in sorted(bundled.glob("analyzer*")):
    datas.append((str(analyzer), "_bundled"))

a = Analysis(
    [str(spec_dir / "entry.py")],
    pathex=[str(src)],
    binaries=[],
    datas=datas,
    hiddenimports=[
        "codeanalyzer",
        "codeanalyzer.__main__",
        "codeanalyzer.web",
        "codeanalyzer.web.server",
    ],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="codeanalyzer",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=True,
    disable_windowed_traceback=False,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=False,
    name="codeanalyzer",
)
