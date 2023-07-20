# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(['Capture-Coordonnée.py'],
             pathex=['C:\\Users\\mayerd01\\Desktop\\coordoner'],
             binaries=[],
             datas=[('icone/icone.ico', 'icone')],  # ajoutez cette ligne ici
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='Capture-Coordonnée',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False )
