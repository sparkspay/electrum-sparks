# -*- coding: utf-8 -*-

import sys


try:
    from neoscrypt import getPoWHash
    import_success = True
    load_libneoscrypt = False
except ImportError:
    import_success = False
    load_libneoscrypt = True


if load_libneoscrypt:
    from ctypes import cdll, create_string_buffer, byref

    if sys.platform == 'darwin':
        name = 'neoscrypt.dylib'
    elif sys.platform in ('windows', 'win32'):
        name = 'neoscrypt.dll'
    else:
        name = 'neoscrypt.so'

    try:
        lneoscrypt = cdll.LoadLibrary(name)
        neoscrypt = lneoscrypt.neoscrypt
    except:
        load_libneoscrypt = False


if load_libneoscrypt:
    hash_out = create_string_buffer(32)

    def getPoWHash(header):
        neoscrypt(header, byref(hash_out))
        return hash_out.raw


if not import_success and not load_libneoscrypt:
    raise ImportError('Can not import neoscrypt')
