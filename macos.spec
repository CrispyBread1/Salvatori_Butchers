# -*- mode: python ; coding: utf-8 -*-
import os
from PyInstaller.utils.hooks import collect_submodules

# Print working directory to debug
print(f"Current working directory: {os.getcwd()}")

# Collect necessary modules
hiddenimports = []
try:
    hiddenimports.extend(collect_submodules("psycopg2"))
    print("Added psycopg2 modules")
except Exception as e:
    print(f"Warning: Could not collect psycopg2 modules: {e}")

try:
    hiddenimports.extend(collect_submodules("dotenv"))
    print("Added dotenv modules")
except Exception as e:
    print(f"Warning: Could not collect dotenv modules: {e}")

try:
    hiddenimports.extend(collect_submodules("openpyxl"))
    print("Added openpyxl modules")
except Exception as e:
    print(f"Warning: Could not collect openpyxl modules: {e}")

# Optional modules - only include if they exist
for module in ["gui", "database", "resources"]:
    try:
        hiddenimports.extend(collect_submodules(module))
        print(f"Added {module} modules")
    except Exception as e:
        print(f"Note: Module {module} not added: {e}")

# Data files with explicit existence checks
datas = []

# Add .env file if it exists
env_file = os.path.join(os.getcwd(), '.env')
if os.path.exists(env_file):
    datas.append((env_file, '.'))
    print(f"Adding .env file: {env_file}")
else:
    print(f"Warning: .env file not found at {env_file}")

# MODIFIED: Better handling for assets directory
assets_dir = os.path.join(os.getcwd(), 'assets')
if os.path.exists(assets_dir) and os.path.isdir(assets_dir):
    datas.append((assets_dir, 'assets'))
    print(f"Adding assets directory: {assets_dir}")
else:
    print(f"Warning: assets directory not found at {assets_dir}")
    # Optionally create empty directory if needed
    # os.makedirs(assets_dir, exist_ok=True)
    # datas.append((assets_dir, 'assets'))
    # print(f"Created empty assets directory")

# Handle templates directory similarly
templates_dir = os.path.join(os.getcwd(), 'templates')
if os.path.exists(templates_dir) and os.path.isdir(templates_dir):
    datas.append((templates_dir, 'templates'))
    print(f"Adding templates directory: {templates_dir}")
else:
    print(f"Warning: templates directory not found at {templates_dir}")

a = Analysis(
    ['main.py'],
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

pyz = PYZ(a.pure, a.zipped_data, cipher=None)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='ManageMeStock',
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
    name='ManageMeStock',
)

app = BUNDLE(
    coll,
    name='ManageMeStock.app',
    icon=None,
    bundle_identifier='com.managemestock.app',
    info_plist={
        'CFBundleShortVersionString': '1.0.0',
        'CFBundleVersion': '1.0.0',
        'NSHighResolutionCapable': 'True',
    },
)
