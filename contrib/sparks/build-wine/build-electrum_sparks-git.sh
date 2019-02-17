#!/bin/bash

NAME_ROOT=Electrum-Sparks
PYTHON_VERSION=3.6.6

#VERSION='3.2.3.2_beta3'

# These settings probably don't need any change
export WINEPREFIX=/opt/wine64
export PYTHONDONTWRITEBYTECODE=1
export PYTHONHASHSEED=22

PYHOME=c:/python$PYTHON_VERSION
PYTHON="wine $PYHOME/python.exe -OO -B"

# download electrum-sparks from github https://github.com/sparkspay/electrum-sparks.git
if [ ! -d "$WINEPREFIX/drive_c/electrum-sparks" ] ; then
    git clone https://github.com/sparkspay/electrum-sparks.git $WINEPREFIX/drive_c/electrum-sparks
fi

cd $WINEPREFIX/drive_c/electrum-sparks
git pull --force

# Let's begin!
cd `dirname $0`
set -e

mkdir -p tmp
cd tmp

pushd $WINEPREFIX/drive_c/electrum-sparks

# Load electrum_sparks-icons and electrum_sparks-locale for this release
git submodule init
git submodule update




#VERSION=`git describe --tags --dirty --always`
VERSION=`git describe --tags --always`
echo "Last commit: $VERSION"

# create locales
./contrib/make_locale


find -exec touch -d '2000-11-11T11:11:11+00:00' {} +
popd

cp $WINEPREFIX/drive_c/electrum-sparks/LICENCE .
pyrcc5 $WINEPREFIX/drive_c/electrum-sparks/icons.qrc -o $WINEPREFIX/drive_c/electrum-sparks/electrum_sparks/gui/qt/icons_rc.py


# Install frozen dependencies

$PYTHON -m pip install -r $WINEPREFIX/drive_c/electrum-sparks/contrib/deterministic-build/requirements.txt
$PYTHON -m pip install -r $WINEPREFIX/drive_c/electrum-sparks/contrib/deterministic-build/requirements-hw.txt

pushd $WINEPREFIX/drive_c/electrum-sparks
$PYTHON setup.py install
popd

cd ..

rm -rf dist/

# build standalone and portable versions
wine "C:/python$PYTHON_VERSION/scripts/pyinstaller.exe" --noconfirm --ascii --clean --name $NAME_ROOT-$VERSION -w deterministic.spec

# set timestamps in dist, in order to make the installer reproducible
pushd dist
find -exec touch -d '2000-11-11T11:11:11+00:00' {} +
popd

# build NSIS installer
# $VERSION could be passed to the electrum_sparks.nsi script, but this would require some rewriting in the script itself.
wine "$WINEPREFIX/drive_c/Program Files (x86)/NSIS/makensis.exe" /DPRODUCT_VERSION=$VERSION electrum_sparks.nsi

cd dist
mv Electrum-Sparks-setup.exe $NAME_ROOT-$VERSION-setup.exe
pwd
cd ..

echo "Done."
md5sum dist/Electrum-Sparks*exe
