from PyInstaller.utils.hooks import collect_submodules

env_file = os.path.join(os.getcwd(), '.env')
print(f"Packaging .env file from: {env_file}")
print(f"File exists: {os.path.exists(env_file)}")


hiddenimports = collect_submodules("psycopg2") + collect_submodules("gui") + collect_submodules("database") + collect_submodules("resources") + collect_submodules("dotenv") + collect_submodules("openpyxl")

a = Analysis(
    ["main.py"],
    pathex=[],
    binaries=[],
    datas=[(env_file, ".")], 
    hiddenimports=hiddenimports,
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=None)
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name="ManageMeStock",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    icon=None,
)
