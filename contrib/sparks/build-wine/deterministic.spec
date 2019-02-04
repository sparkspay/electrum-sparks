# -*- mode: python -*-

from PyInstaller.utils.hooks import collect_data_files, collect_submodules, collect_dynamic_libs

import sys
for i, x in enumerate(sys.argv):
    if x == '--name':
        cmdline_name = sys.argv[i+1]
        break
else:
    raise Exception('no name')

PYTHON_VERSION = '3.6.6'
PYHOME = 'c:/python' + PYTHON_VERSION

home = 'C:\\electrum-sparks\\'

# see https://github.com/pyinstaller/pyinstaller/issues/2005
hiddenimports = []
hiddenimports += collect_submodules('trezorlib')
hiddenimports += collect_submodules('safetlib')
hiddenimports += collect_submodules('btchip')
hiddenimports += collect_submodules('keepkeylib')
hiddenimports += collect_submodules('websocket')
#hiddenimports += collect_submodules('ckcc')

# Add libusb binary
binaries = [(PYHOME+"/libusb-1.0.dll", ".")]

# Workaround for "Retro Look":
binaries += [b for b in collect_dynamic_libs('PyQt5') if 'qwindowsvista' in b[0]]

binaries += [('C:/tmp/libsecp256k1.dll', '.')]
binaries += [('C:/tmp/neoscrypt.dll', '.')]

datas = [
    (home+'electrum_sparks/*.json', 'electrum_sparks'),
    (home+'electrum_sparks/wordlist/english.txt', 'electrum_sparks/wordlist'),
    (home+'electrum_sparks/locale', 'electrum_sparks/locale'),
    (home+'electrum_sparks/plugins', 'electrum_sparks/plugins'),
    ('C:\\Program Files (x86)\\ZBar\\bin\\', '.'),
]
datas += collect_data_files('trezorlib')
datas += collect_data_files('safetlib')
datas += collect_data_files('btchip')
datas += collect_data_files('keepkeylib')
#datas += collect_data_files('ckcc')

# We don't put these files in to actually include them in the script but to make the Analysis method scan them for imports
a = Analysis([home+'electrum-sparks',
              home+'electrum_sparks/gui/qt/main_window.py',
              home+'electrum_sparks/gui/text.py',
              home+'electrum_sparks/util.py',
              home+'electrum_sparks/wallet.py',
              home+'electrum_sparks/simple_config.py',
              home+'electrum_sparks/bitcoin.py',
              home+'electrum_sparks/dnssec.py',
              home+'electrum_sparks/commands.py',
              home+'electrum_sparks/plugins/cosigner_pool/qt.py',
              home+'electrum_sparks/plugins/email_requests/qt.py',
              home+'electrum_sparks/plugins/trezor/client.py',
              home+'electrum_sparks/plugins/trezor/qt.py',
              home+'electrum_sparks/plugins/safe_t/client.py',
              home+'electrum_sparks/plugins/safe_t/qt.py',
              home+'electrum_sparks/plugins/keepkey/qt.py',
              home+'electrum_sparks/plugins/ledger/qt.py',
              #home+'electrum_sparks/plugins/coldcard/qt.py',
              #home+'packages/requests/utils.py'
              ],
             binaries=binaries,
             datas=datas,
             #pathex=[home+'lib', home+'gui', home+'plugins'],
             hiddenimports=hiddenimports,
             hookspath=[])


# http://stackoverflow.com/questions/19055089/pyinstaller-onefile-warning-pyconfig-h-when-importing-scipy-or-scipy-signal
for d in a.datas:
    if 'pyconfig' in d[0]:
        a.datas.remove(d)
        break

# hotfix for #3171 (pre-Win10 binaries)
a.binaries = [x for x in a.binaries if not x[1].lower().startswith(r'c:\windows')]

pyz = PYZ(a.pure)


#####
# "standalone" exe with all dependencies packed into it

exe_standalone = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    name=os.path.join('build\\pyi.win32\\electrum_sparks', cmdline_name + ".exe"),
    debug=False,
    strip=None,
    upx=False,
    icon=home+'icons\\electrum-sparks.ico',
    console=False)
    # console=True makes an annoying black box pop up, but it does make Electrum output command line commands, with this turned off no output will be given but commands can still be used

exe_portable = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas + [ ('is_portable', 'README.md', 'DATA' ) ],
    name=os.path.join('build\\pyi.win32\\electrum_sparks', cmdline_name + "-portable.exe"),
    debug=False,
    strip=None,
    upx=False,
    icon=home+'icons\\electrum-sparks.ico',
    console=False)

#####
# exe and separate files that NSIS uses to build installer "setup" exe

exe_dependent = EXE(
    pyz,
    a.scripts,
    exclude_binaries=True,
    name=os.path.join('build\\pyi.win32\\electrum_sparks', cmdline_name),
    debug=False,
    strip=None,
    upx=False,
    icon=home+'icons/electrum-sparks.ico',
    console=False)

coll = COLLECT(
    exe_dependent,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=None,
    upx=True,
    debug=False,
    icon=home+'icons\\electrum-sparks.ico',
    console=False,
    name=os.path.join('dist', 'electrum_sparks'))
