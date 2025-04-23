# -*- mode: python ; coding: utf-8 -*-

from PyInstaller.utils.hooks import collect_data_files, collect_submodules


# 收集 rasterio 和 fiona 的隐藏导入
hiddenimports = collect_submodules('rasterio') + collect_submodules('fiona') +collect_submodules('osgeo')

# 收集 rasterio 和 fiona 的数据文件
datas = collect_data_files('rasterio') + collect_data_files('fiona') +collect_data_files('osgeo', includes=['*.dll', '*.pyd'])
def get_gdal_bin_path():
    try:
        import osgeo
        # 这是一个近似方法，可能需要根据您的安装调整
        if os.name == 'nt':  # Windows
            import winreg
            reg_path = r"SOFTWARE\GDAL"
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, reg_path) as key:
                gdal_path = winreg.QueryValueEx(key, "GDAL_HOME")[0]
                return os.path.join(gdal_path, 'bin')
        else:
            # Linux/Mac 可能需要其他方法
            return None
    except:
        return None

gdal_bin_path = get_gdal_bin_path()
if gdal_bin_path and os.path.exists(gdal_bin_path):
    for dll in os.listdir(gdal_bin_path):
        if dll.lower().endswith('.dll'):
            datas.append((os.path.join(gdal_bin_path, dll), 'gdal\\bin'))
a = Analysis(
    ['rstool.py'],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports+ ['_gdal_array'],  # 显式添加
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
    a.binaries,
    a.datas,
    [],
    name='rstool',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['G:\\code\\rstool\\resources\\images\\icon.ico'],
)
