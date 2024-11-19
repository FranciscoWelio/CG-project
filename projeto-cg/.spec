# -*- mode: python ; coding: utf-8 -*-

import os
from PyInstaller.utils.hooks import collect_all

block_cipher = None

# Collect all necessary data for the modules
pages_datas, pages_binaries, pages_hiddenimports = collect_all('pages')
transformations_datas, transformations_binaries, transformations_hiddenimports = collect_all('transformations')

a = Analysis(
    ['main.py'],
    pathex=['.'],  # Add current directory to Python path
    binaries=[],
    datas=[
        *pages_datas,
        *transformations_datas,
        ('pages', 'pages'),  # Include the entire pages directory
        ('transformations', 'transformations')  # Include transformations directory as well
    ],
    hiddenimports=[
        *pages_hiddenimports,
        *transformations_hiddenimports,
        'pages',
        'opengl_frame',
        'viewport',
        'transformations',
        'numpy',
        'pygame',
        'OpenGL',
        'PIL',
        'tkinter'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,        # Adiciona binários ao EXE
    a.zipfiles,        # Adiciona arquivos zip ao EXE
    a.datas,          # Adiciona dados ao EXE
    [],
    name='main',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,  # Armazena arquivos temporários em memória
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)