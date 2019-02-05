#!/bin/bash
# Lucky number
export PYTHONHASHSEED=22

here=$(dirname "$0")
test -n "$here" -a -d "$here" || exit

echo "Clearing $here/build and $here/dist..."
rm "$here"/build/* -rf
rm "$here"/dist/* -rf

rm "$here"/../../../build/wine/* -rf
rm "$here"/../../../dist/wine/* -rf


mkdir -p /tmp/electrum_sparks-build
mkdir -p /tmp/electrum_sparks-build/pip-cache
export PIP_CACHE_DIR="/tmp/electrum_sparks-build/pip-cache"

$here/build-secp256k1.sh || exit 1
$here/build-neoscrypt.sh || exit 1

$here/prepare-wine.sh || exit 1

echo "Resetting modification time in C:\Python..."
# (Because of some bugs in pyinstaller)
pushd /opt/wine64/drive_c/python*
find -exec touch -d '2000-11-11T11:11:11+00:00' {} +
popd
ls -l /opt/wine64/drive_c/python*

$here/build-electrum_sparks-git.sh && \
echo "Done."
