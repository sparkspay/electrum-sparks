#!/bin/bash
set -ev

if [[ -z $TRAVIS_TAG ]]; then
  echo TRAVIS_TAG unset, exiting
  exit 1
fi

BUILD_REPO_URL=https://github.com/SparksReborn/electrum-sparks.git

cd build

git clone --branch $TRAVIS_TAG $BUILD_REPO_URL electrum-sparks

cd electrum-sparks

export PY36BINDIR=/Library/Frameworks/Python.framework/Versions/3.6/bin/
export PATH=$PATH:$PY36BINDIR
source ./contrib/sparks/travis/electrum_sparks_version_env.sh;
echo wine build version is $SPARKS_ELECTRUM_VERSION

sudo pip3 install --upgrade pip
sudo pip3 install -r contrib/deterministic-build/requirements.txt
sudo pip3 install \
    x11_hash>=1.4 \
    pycryptodomex==3.6.1 \
    btchip-python==0.1.27 \
    keepkey==4.0.2 \
    safet==0.1.3 \
    trezor==0.10.2

pyrcc5 icons.qrc -o electrum_sparks/gui/qt/icons_rc.py

export PATH="/usr/local/opt/gettext/bin:$PATH"
./contrib/make_locale
find . -name '*.po' -delete
find . -name '*.pot' -delete

cp contrib/sparks/osx.spec .
cp contrib/sparks/pyi_runtimehook.py .
cp contrib/sparks/pyi_tctl_runtimehook.py .

pyinstaller \
    -y \
    --name electrum-sparks-$SPARKS_ELECTRUM_VERSION.bin \
    osx.spec

info "Adding Sparks URI types to Info.plist"
plutil -insert 'CFBundleURLTypes' \
   -xml '<array><dict> <key>CFBundleURLName</key> <string>sparks</string> <key>CFBundleURLSchemes</key> <array><string>sparks</string></array> </dict></array>' \
   -- dist/Electrum-Sparks.app/Contents/Info.plist \
   || fail "Could not add keys to Info.plist. Make sure the program 'plutil' exists and is installed."

sudo hdiutil create -fs HFS+ -volname "Electrum-Sparks" \
    -srcfolder dist/Electrum-Sparks.app \
    dist/Electrum-Sparks-$SPARKS_ELECTRUM_VERSION-macosx.dmg
