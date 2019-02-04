#!/bin/bash
# heavily based on https://github.com/ofek/coincurve/blob/417e726f553460f88d7edfa5dc67bfda397c4e4a/.travis/build_windows_wheels.sh

set -e


build_dll() {
    #sudo apt-get install -y mingw-w64
    DEFINES="-DNEOSCRYPT_ASM -DNEOSCRYPT_OPT -DNEOSCRYPT_MINER_4WAY -DNEOSCRYPT_SHA256"
    CFLAGS="-Wall -O2 -fomit-frame-pointer -fno-stack-protector"
    LD="$1-gcc"
    CC="$1-gcc"
    LDFLAGS="-shared -W -static-libgcc -static-libstdc++ "

    echo "$CC $CFLAGS $DEFINES -c neoscrypt.c"
    `$CC $CFLAGS $DEFINES -c neoscrypt.c`

    echo "$CC $CFLAGS $DEFINES -c neoscrypt_test.c"
    `$CC $CFLAGS $DEFINES -c neoscrypt_test.c`

    echo "$CC $DEFINES -c neoscrypt_asm.S"
    `$CC $DEFINES -c neoscrypt_asm.S`

    echo "$LD $LDFLAGS -o neoscrypt neoscrypt.o neoscrypt_test.o neoscrypt_asm.o"
    `$LD $LDFLAGS -o neoscrypt-0.dll neoscrypt.o neoscrypt_test.o neoscrypt_asm.o`


    ${1}-strip neoscrypt-0.dll
}


cd /tmp/electrum_sparks-build

if [ ! -d neoscrypt_module ]; then
    git clone https://github.com/SparksReborn/neoscrypt_module.git
    cd neoscrypt_module;
else
    cd neoscrypt_module
    git pull
fi

#git reset --hard 452d8e4d2a2f9f1b5be6b02e18f1ba102e5ca0b4
git clean -f -x -q

build_dll i686-w64-mingw32  # 64-bit would be: x86_64-w64-mingw32
mv neoscrypt-0.dll neoscrypt.dll

find -exec touch -d '2000-11-11T11:11:11+00:00' {} +

echo "building neoscrypt finished"
