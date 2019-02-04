#!/usr/bin/env python3

# python setup.py sdist --format=zip,gztar

import os
import sys
import platform
import imp
import argparse
import subprocess

from setuptools import setup, find_packages
from setuptools.command.install import install
from setuptools.command.build_py import build_py

with open('contrib/requirements/requirements.txt') as f:
    requirements = f.read().splitlines()

with open('contrib/requirements/requirements-hw.txt') as f:
    requirements_hw = f.read().splitlines()

version = imp.load_source('version', 'electrum_sparks/version.py')

if sys.version_info[:3] < (3, 4, 0):
    sys.exit("Error: Sparks-Electrum requires Python version >= 3.4.0...")

data_files = []

if platform.system() in ['Linux', 'FreeBSD', 'DragonFly']:
    parser = argparse.ArgumentParser()
    parser.add_argument('--root=', dest='root_path', metavar='dir', default='/')
    opts, _ = parser.parse_known_args(sys.argv[1:])
    usr_share = os.path.join(sys.prefix, "share")
    icons_dirname = 'pixmaps'
    if not os.access(opts.root_path + usr_share, os.W_OK) and \
       not os.access(opts.root_path, os.W_OK):
        icons_dirname = 'icons'
        if 'XDG_DATA_HOME' in os.environ.keys():
            usr_share = os.environ['XDG_DATA_HOME']
        else:
            usr_share = os.path.expanduser('~/.local/share')
    data_files += [
        (os.path.join(usr_share, 'applications/'), ['electrum-sparks.desktop']),
        (os.path.join(usr_share, icons_dirname), ['icons/electrum-sparks.png'])
    ]

class BuildPyCommand(build_py):
    def run(self):
        build_py.run(self)
        try:
            from PyQt5 import pyrcc_main
            if not pyrcc_main.processResourceFile(['icons.qrc'],
                                                  'build/lib/electrum_sparks/gui/qt/icons_rc.py',
                                                  False):
                raise RuntimeError('Failed to generate icons_rc.py')
        except ImportError:
            import subprocess
            subprocess.run(['pyrcc5', 'icons.qrc', '-o', 'build/lib/electrum_sparks/gui/qt/icons_rc.py'])
        with open('build/lib/electrum_sparks/version.py', 'r+') as fp:
            verfile = fp.readlines()
            verfile[0] = "ELECTRUM_VERSION = '{}'\n".format(
                version.ELECTRUM_VERSION)
            fp.seek(0)
            fp.writelines(verfile)
            fp.truncate()

extras_require = {
    'hardware': requirements_hw,
    'fast': ['pycryptodomex'],
    'gui': ['pyqt5'],
}
extras_require['full'] = [pkg for sublist in list(extras_require.values()) for pkg in sublist]


class CustomInstallCommand(install):
    def run(self):
        install.run(self)
        # potentially build Qt icons file
        try:
            import PyQt5
        except ImportError:
            pass
        else:
            try:
                path = os.path.join(self.install_lib, "electrum_sparks/gui/qt/icons_rc.py")
                if not os.path.exists(path):
                    subprocess.call(["pyrcc5", "icons.qrc", "-o", path])
            except Exception as e:
                print('Warning: building icons file failed with {}'.format(e))


setup(
    name="Electrum-Sparks",
    version=version.ELECTRUM_VERSION,
    install_requires=requirements,
    extras_require=extras_require,
    packages=[
        'electrum_sparks',
        'electrum_sparks.gui',
        'electrum_sparks.gui.qt',
        'electrum_sparks.plugins',
    ] + [('electrum_sparks.plugins.'+pkg) for pkg in find_packages('electrum_sparks/plugins')],
    package_dir={
        'electrum_sparks': 'electrum_sparks',
    },
    package_data={
        '': ['*.txt', '*.json', '*.ttf', '*.otf'],
        'electrum_sparks': [
            'wordlist/*.txt',
            'locale/*/LC_MESSAGES/electrum.mo',
        ],
    },
    #scripts=['electrum-sparks/electrum-sparks'],
    scripts=['electrum-sparks'],
    data_files=data_files,
    description="Lightweight Sparkspay Wallet",
    maintainer="akhavr",
    maintainer_email="akhavr@khavr.com",
    license="MIT License",
    url="https://electrum.sparkscoin.io",
    long_description="""Lightweight Sparkspay Wallet""",
    cmdclass={
#        'install': CustomInstallCommand,
         'build_py': BuildPyCommand,
    },
)
