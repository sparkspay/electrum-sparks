#!/bin/bash
set -ev

if [[ -z $TRAVIS_TAG ]]; then
  echo TRAVIS_TAG unset, exiting
  exit 1
fi

BUILD_REPO_URL=https://github.com/sparkspay/electrum-sparks.git

cd build

git clone --branch $TRAVIS_TAG $BUILD_REPO_URL electrum-sparks

mkdir -p electrum-sparks/dist
wget -O electrum-sparks/dist/tor-proxy-setup.exe \
    https://github.com/zebra-lucky/tor-proxy/releases/download/0.3.3.9/tor-proxy-0.3.3.9-setup.exe

docker run --rm \
    -v $(pwd):/opt \
    -w /opt/electrum-sparks \
    -t zebralucky/electrum-sparks-winebuild:Linux /opt/build_linux.sh

sudo find . -name '*.po' -delete
sudo find . -name '*.pot' -delete

export WINEARCH=win32
export WINEPREFIX=/root/.wine-32
export PYHOME=$WINEPREFIX/drive_c/Python36

wget https://github.com/zebra-lucky/zbarw/releases/download/20180620/zbarw-zbarcam-0.10-win32.zip
unzip zbarw-zbarcam-0.10-win32.zip && rm zbarw-zbarcam-0.10-win32.zip

wget https://github.com/zebra-lucky/x11_hash/releases/download/1.4.1/x11_hash-1.4.1-win32.zip
unzip x11_hash-1.4.1-win32.zip && rm x11_hash-1.4.1-win32.zip

wget https://github.com/zebra-lucky/secp256k1/releases/download/0.1/libsecp256k1-0.1-win32.zip
unzip libsecp256k1-0.1-win32.zip && rm libsecp256k1-0.1-win32.zip

docker run --rm \
    -e WINEARCH=$WINEARCH \
    -e WINEPREFIX=$WINEPREFIX \
    -e PYHOME=$PYHOME \
    -v $(pwd):/opt \
    -v $(pwd)/electrum-sparks/:$WINEPREFIX/drive_c/electrum-sparks \
    -w /opt/electrum-sparks \
    -t zebralucky/electrum-sparks-winebuild:WinePy36 /opt/build_wine.sh

export WINEARCH=win64
export WINEPREFIX=/root/.wine-64
export PYHOME=$WINEPREFIX/drive_c/Python36

wget https://github.com/zebra-lucky/zbarw/releases/download/20180620/zbarw-zbarcam-0.10-win64.zip
unzip zbarw-zbarcam-0.10-win64.zip && rm zbarw-zbarcam-0.10-win64.zip

wget https://github.com/zebra-lucky/x11_hash/releases/download/1.4.1/x11_hash-1.4.1-win64.zip
unzip x11_hash-1.4.1-win64.zip && rm x11_hash-1.4.1-win64.zip

wget https://github.com/zebra-lucky/secp256k1/releases/download/0.1/libsecp256k1-0.1-win64.zip
unzip libsecp256k1-0.1-win64.zip && rm libsecp256k1-0.1-win64.zip

docker run --rm \
    -e WINEARCH=$WINEARCH \
    -e WINEPREFIX=$WINEPREFIX \
    -e PYHOME=$PYHOME \
    -v $(pwd):/opt \
    -v $(pwd)/electrum-sparks/:$WINEPREFIX/drive_c/electrum-sparks \
    -w /opt/electrum-sparks \
    -t zebralucky/electrum-sparks-winebuild:WinePy36 /opt/build_wine.sh
