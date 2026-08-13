# -*- mode: python ; coding: utf-8 -*-
from pathlib import Path

spec_dir = Path(SPECPATH)
src_dir = spec_dir / 'src' / 'codeanalyzer'

datas = [
    (str(src_dir / 'web' / 'templates'), 'codeanalyzer/web/templates'),
    (str(src_dir / 'web' / 'static'), 'codeanalyzer/web/static'),
    (str(src_dir / '_bundled'), '_bundled')
]

a = Analysis(
    ['start_app.py'],
    pathex=[str(spec_dir)],
    binaries=[],
    datas=datas,
    hiddenimports=[
        "codeanalyzer",
        "codeanalyzer.__main__",
        "codeanalyzer.web",
        "codeanalyzer.web.server",
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='CodeAnalyzer',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='CodeAnalyzer',
)
