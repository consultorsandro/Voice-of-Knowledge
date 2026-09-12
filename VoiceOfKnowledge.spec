# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_data_files

datas = [('.venv/Lib/site-packages/espeakng_loader/espeak-ng-data', 'espeakng_loader/espeak-ng-data')]
datas += collect_data_files('language_tags')


a = Analysis(
    ['src/voice_of_knowledge/gui/main_window.py'],
    pathex=['src'],
    binaries=[('.venv/Lib/site-packages/espeakng_loader/espeak-ng.dll', 'espeakng_loader')],
    datas=datas,
    hiddenimports=[],
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
    name='VoiceOfKnowledge',
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
    name='VoiceOfKnowledge',
)
