# -*- mode: python -*-

block_cipher = None

a = Analysis(['src/restatic/__main__.py'],
             pathex=['/Users/manu/Workspace/restatic/src'],
             binaries=[
                ('bin/macosx64/borg', 'bin'),
             ],
             datas=[
                ('src/restatic/assets/UI/*', 'assets/UI'),
                ('src/restatic/assets/icons/*', 'assets/icons'),
             ],
             hiddenimports=['restatic.views.collection_rc'],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='restatic',
          debug=False,
          bootloader_ignore_signals=True,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=True )

app = BUNDLE(exe,
             name='Restatic.app',
             icon='src/restatic/assets/icons/app-icon.icns',
             bundle_identifier='com.borgbase.client.macos',
             info_plist={
                     'NSHighResolutionCapable': 'True',
                     'LSUIElement': '1',
                     'CFBundleShortVersionString': '0.4.6',
                     'CFBundleVersion': '0.4.6',
                     'NSAppleEventsUsageDescription': 'Please allow',
                     'SUFeedURL': 'https://borgbase.github.io/restatic/appcast-pre.xml'
                     },
             )
if False:
    coll = COLLECT(exe,
                   a.binaries,
                   a.zipfiles,
                   a.datas,
                   strip=False,
                   name='restatic-dir')
