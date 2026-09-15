# -*- mode: python ; coding: utf-8 -*-

import os

from PyInstaller.utils.hooks import collect_submodules


project_dir = SPECPATH


hiddenimports = []

for module in (
  "gui",
  "dotenv",
  "openpyxl",
  "matplotlib"
):

    hiddenimports += collect_submodules(module)


hiddenimports += ["pandas"]


a = Analysis(
    [os.path.join(project_dir, "main.py")],
    pathex=[project_dir],
    binaries=[],
    datas=[],
    hiddenimports=hiddenimports,
    hookspath=[],
    runtime_hooks=[
        os.path.join(
            project_dir,
            "diagnostic_hook.py"
        )
    ],
    excludes=[],
)


# PyInstaller 6 format: no a.zipped_data,
# a.zipfiles or cipher argument.

pyz = PYZ(
    a.pure
)


exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name="ManageMeStock-Diagnostic",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    icon=None,
)
