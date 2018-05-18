# -*- mode: python -*-

block_cipher = None

added_files = [
               ('Data.db', '.'),
               ('Pics/*.png', 'Pics'),
               ('Pics/*.icns', 'Pics')
              ]

a = Analysis(['main.py'],
             pathex=['/Users/username/Librarian'],
             binaries=[],
             datas=added_files,
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='main',
          debug=False,
          strip=False,
          upx=True,
          console=False )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='Librarian')
app = BUNDLE(coll,
             name='Librarian.app',
             icon='Pics/icon.icns',
             bundle_identifier='com.LTR.Librarian')
