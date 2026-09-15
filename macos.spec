# -*- mode: python ; coding: utf-8 -*-

import os

from PyInstaller.utils.hooks import collect_submodules


print(
    f"Current working directory: "
    f"{os.getcwd()}"
)


hiddenimports = []


try:

    hiddenimports.extend(
        collect_submodules("dotenv")
    )

    print("Added dotenv modules")

except Exception as e:

    print(
        f"Warning: Could not collect dotenv modules: {e}"
    )


try:

    hiddenimports.extend(
        collect_submodules("openpyxl")
    )

    print("Added openpyxl modules")

except Exception as e:

    print(
        f"Warning: Could not collect openpyxl modules: {e}"
    )


for module in [
    "gui"
]:

    try:

        hiddenimports.extend(
            collect_submodules(module)
        )

        print(
            f"Added {module} modules"
        )

    except Exception as e:

        print(
            f"Note: Module {module} not added: {e}"
        )


datas = []


assets_dir = os.path.join(
    os.getcwd(),
    "assets"
)

if (
    os.path.exists(assets_dir)
    and os.path.isdir(assets_dir)
):

    datas.append(
        (
            assets_dir,
            "assets"
        )
    )

    print(
        f"Adding assets directory: "
        f"{assets_dir}"
    )

else:

    print(
        f"Warning: assets directory not found at "
        f"{assets_dir}"
    )


templates_dir = os.path.join(
    os.getcwd(),
    "templates"
)

if (
    os.path.exists(templates_dir)
    and os.path.isdir(templates_dir)
):

    datas.append(
        (
            templates_dir,
            "templates"
        )
    )

    print(
        f"Adding templates directory: "
        f"{templates_dir}"
    )

else:

    print(
        f"Warning: templates directory not found at "
        f"{templates_dir}"
    )


a = Analysis(
    ["main.py"],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=None,
    noarchive=False,
)


pyz = PYZ(
    a.pure,
    a.zipped_data,
    cipher=None
)


exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="ManageMeStock",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=True,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)


coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name="ManageMeStock",
)


app = BUNDLE(
    coll,
    name="ManageMeStock.app",
    icon=None,
    bundle_identifier="com.managemestock.app",
    info_plist={
        "CFBundleShortVersionString": "1.0.0",
        "CFBundleVersion": "1.0.0",
        "NSHighResolutionCapable": "True",
    },
)
